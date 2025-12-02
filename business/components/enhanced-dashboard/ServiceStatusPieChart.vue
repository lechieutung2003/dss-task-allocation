<template>
  <el-card class="service-status-pie-card">
    <template #header>
      <div style="display:flex; align-items:center; justify-content:space-between;">
        <div class="card-header-left">
          <el-icon><TrendCharts /></el-icon>
          <strong>{{ $t('success_fail_ratio') }}</strong>
        </div>
        <div class="card-header-sub">{{ $t('success_fail_comparison') }}</div>
      </div>
    </template>

    <div class="chart-wrapper">
      <div class="pie-container">
        <canvas ref="chartRef"></canvas>
        <div v-if="loading" class="chart-overlay-loading">
          <el-spinner />
        </div>
      </div>

      <div class="summary-list">
        <template v-if="!loading">
          <el-list v-if="summaryItems.length" bordered>
            <el-list-item
              v-for="item in summaryItems"
              :key="item.name"
            >
              <div class="summary-item-row">
                <div class="summary-item-left">
                  <span
                    class="summary-color-box"
                    :style="{ background: item.color }"
                  ></span>

                  <div>
                    <div class="summary-name">{{ item.name }}</div>
                    <div class="summary-count">{{ $t('count_label') }}: {{ item.count }}</div>
                  </div>
                </div>

                <div style="text-align:right">
                  <div class="summary-percent">{{ item.percent }}%</div>
                  <div class="summary-ratio-text">{{ item.ratioText }}</div>
                </div>
              </div>
            </el-list-item>
          </el-list>

          <div v-else class="no-data-text">
            {{ $t('no_status_data') }}
          </div>
        </template>
      </div>
    </div>
  </el-card>
</template>


<script setup>
import { ref, onMounted, computed, nextTick, defineExpose } from 'vue'
import { TrendCharts } from '@element-plus/icons-vue'
import { Chart, registerables } from 'chart.js'
import enhancedDashboardService from '~/services/dss/enhancedDashboardService'

Chart.register(...registerables)

const chartRef = ref(null)
let chartInstance = null
const loading = ref(false)
const rawItems = ref([]) // expected: [{ status, name, count }]

const fetchData = async (params = {}) => {
  loading.value = true
  try {
    const resp = await enhancedDashboardService.getServiceStatusCounts(params)
    if (resp && resp.success && Array.isArray(resp.data)) {
      rawItems.value = resp.data.map(it => ({
        name: (it.name || (it.status || 'other')).toString(),
        count: Number(it.count) || 0
      }))
    } else {
      rawItems.value = []
    }
    nextTick(() => updateChart())
  } catch (e) {
    rawItems.value = []
    console.error('ServiceStatusPieChart fetch error', e)
  } finally {
    loading.value = false
  }
}

defineExpose({ fetchData })

// Only keep Completed and Rejected; ignore Others
const prepared = computed(() => {
  const map = { completed: 0, rejected: 0 }
  for (const it of rawItems.value) {
    const key = (it.name || '').toString().toLowerCase()
    if (key.includes('completed')) map.completed += it.count
    else if (key.includes('rejected') || key.includes('reject')) map.rejected += it.count
  }
  return [
    { name: 'Completed', count: map.completed },
    { name: 'Rejected', count: map.rejected }
  ].filter(i => i.count > 0) // remove zero entries so chart only shows present statuses
})

const total = computed(() => prepared.value.reduce((s, it) => s + it.count, 0))

const summaryItems = computed(() => {
  const palette = ['#67c23a','#f56c6c']
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
  // if no data, destroy and do nothing
  if (!data || data.length === 0) {
    chartInstance = null
    return
  }

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
.service-status-pie-card {
  width: 100%;
  border-radius: 12px;
}

.card-header-left {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #ffffff;
}

.card-header-sub {
  color: #f5f5f5;
  font-size: 13px;
}

.chart-wrapper {
  display: flex;
  gap: 24px;
  align-items: center;
  padding: 20px 0;
}

.pie-container {
  width: 230px;
  height: 230px;
  position: relative;
}

.chart-overlay-loading {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.55);
  border-radius: 50%;
}

.summary-list {
  flex: 1;
}

.summary-item-row {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

.summary-item-left {
  display: flex;
  gap: 12px;
  align-items: center;
}

.summary-color-box {
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
}

.summary-ratio-text {
  font-size: 12px;
  color: #909399;
}

.no-data-text {
  color: #909399;
  font-style: italic;
  padding-left: 6px;
}
</style>
