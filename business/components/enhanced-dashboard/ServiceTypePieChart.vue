<template>
  <el-card class="service-type-pie-card">
    <template #header>
      <div style="display:flex; align-items:center; justify-content:space-between">
        <div class="card-header-left">
          <el-icon><TrendCharts /></el-icon>
          <strong>{{ $t('service_by_booking_ratio') }}</strong>
        </div>
        <div class="card-header-sub">{{ $t('popular_service_comparison') }}</div>
      </div>
    </template>

    <div class="type-chart-wrapper">
      <div class="pie-container">
        <canvas ref="chartRef"></canvas>
        <div v-if="loading" class="chart-overlay-loading">
          <el-spinner />
        </div>
      </div>

      <div class="summary-list">
        <el-list
          v-if="!loading && summaryItems.length"
          bordered
        >
          <el-list-item
            v-for="item in summaryItems"
            :key="item.name"
          >
            <div class="summary-row">
              <div class="summary-left">
                <span
                  class="summary-color"
                  :style="{ background: item.color }"
                ></span>

                <div>
                  <div class="summary-name">{{ item.name }}</div>
                  <div class="summary-count">{{ $t('count_label') }}: {{ item.count }}</div>
                </div>
              </div>

              <div>
                <div class="summary-percent">{{ item.percent }}%</div>
                <div class="summary-ratio-text">{{ item.ratioText }}</div>
              </div>
            </div>
          </el-list-item>
        </el-list>

        <div v-else-if="!loading" class="no-data-text">
          {{ $t('no_service_data') }}
        </div>
      </div>
    </div>
  </el-card>
</template>


<script setup>
import { ref, onMounted, computed, nextTick } from 'vue'
import { TrendCharts } from '@element-plus/icons-vue'
import { Chart, registerables } from 'chart.js'
import enhancedDashboardService from '~/services/dss/enhancedDashboardService'
import { useI18n } from 'vue-i18n'

Chart.register(...registerables)

const chartRef = ref(null)
let chartInstance = null
const loading = ref(false)
const rawItems = ref([]) // expected: [{ service_type_id, name, count }]

const fetchData = async () => {
  loading.value = true
  try {
    const resp = await enhancedDashboardService.getServiceTypeCounts?.() ?? await enhancedDashboardService.getServiceTypePie?.() // try both names
    if (resp && resp.success && Array.isArray(resp.data)) {
      rawItems.value = resp.data.map(it => ({
        name: it.name || String(it.service_type_id),
        count: Number(it.count) || 0
      }))
    } else {
      rawItems.value = []
    }
    nextTick(() => updateChart())
  } catch (e) {
    rawItems.value = []
    console.error('ServiceTypePieChart fetch error', e)
  } finally {
    loading.value = false
  }
}

// prepare top-2 + other aggregation
const prepared = computed(() => {
  const list = [...rawItems.value].sort((a,b) => b.count - a.count)
  if (list.length <= 2) return list
  const top = list.slice(0,2)
  const otherCount = list.slice(2).reduce((s,it)=>s+it.count,0)
  const { t } = useI18n()
  top.push({ name: t('other'), count: otherCount })
  return top
})

const total = computed(() => prepared.value.reduce((s,it)=>s+it.count,0))

const summaryItems = computed(() => {
  const palette = ['#409eff','#67c23a','#e6a23c','#f56c6c']
  return prepared.value.map((it, idx) => {
    const pct = total.value === 0 ? 0 : Math.round((it.count / total.value) * 10000) / 100
    return {
      name: it.name,
      count: it.count,
      percent: pct,
      color: palette[idx % palette.length],
      ratioText: `${pct}%`
    }
  })
})

const updateChart = () => {
  if (!chartRef.value) return
  const ctx = chartRef.value.getContext('2d')
  const labels = prepared.value.map(i => i.name)
  const data = prepared.value.map(i => i.count)
  const colors = summaryItems.value.map(i => i.color)

  if (chartInstance) chartInstance.destroy()
  chartInstance = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels,
      datasets: [{
        data,
        backgroundColor: colors,
        borderWidth: 1,
        borderColor: '#fff'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'bottom' },
        tooltip: {
          callbacks: {
            label(ctx) {
              const val = ctx.parsed
              const pct = total.value === 0 ? 0 : ((val / total.value) * 100).toFixed(2)
              return `${ctx.label}: ${val} (${pct}%)`
            }
          }
        }
      }
    }
  })
}

onMounted(() => {
  fetchData()
})
</script>
<style scoped>
.service-type-pie-card {
  width: 100%;
  border-radius: 12px;
}

/* Header */
.card-header-left {
  display: flex;
  align-items: center;
  gap: 8px;
  color:#ffffff
}

.card-header-sub {
  color: #ffffff;
  font-size: 13px;
}

/* Layout tổng */
.type-chart-wrapper {
  display: flex;
  gap: 24px;
  align-items: center;
  padding: 20px 0;
}

/* Pie chart */
.pie-container {
  width: 260px;
  height: 260px;
  position: relative;
}

.chart-overlay-loading {
  position: absolute;
  inset: 0;
  background: rgba(255,255,255,0.55);
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Summary list */
.summary-list {
  flex: 1;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

.summary-left {
  display: flex;
  gap: 12px;
  align-items: center;
}

.summary-color {
  width: 12px;
  height: 12px;
  border-radius: 3px;
}

.summary-name {
  font-weight: 600;
}

.summary-count {
  font-size: 12px;
  color: #909399;
}

.summary-percent {
  font-weight: 700;
  text-align: right;
}

.summary-ratio-text {
  font-size: 12px;
  color: #909399;
  text-align: right;
}

.no-data-text {
  color: #909399;
  font-style: italic;
  padding-left: 6px;
}
</style>
