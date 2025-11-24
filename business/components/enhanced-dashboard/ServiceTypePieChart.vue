<template>
  <el-card class="service-type-pie-card">
    <template #header>
      <div style="display:flex; align-items:center; justify-content:space-between">
        <div style="display:flex; align-items:center; gap:8px">
          <el-icon><TrendCharts /></el-icon>
          <strong>Dịch vụ theo tỷ lệ đặt</strong>
        </div>
        <div style="color:#606266; font-size:13px">
          So sánh 2 dịch vụ phổ biến nhất
        </div>
      </div>
    </template>

    <div style="display:flex; gap:20px; align-items:center; padding:16px 0">
      <div style="width:260px; height:260px; position:relative">
        <canvas ref="chartRef"></canvas>
        <div v-if="loading" style="position:absolute; inset:0; display:flex; align-items:center; justify-content:center; background:rgba(255,255,255,0.6)">
          <el-spinner />
        </div>
      </div>

      <div style="flex:1">
        <el-list v-if="!loading && summaryItems.length" bordered>
          <el-list-item v-for="item in summaryItems" :key="item.name">
            <div style="display:flex; justify-content:space-between; width:100%">
              <div style="display:flex; gap:12px; align-items:center">
                <span :style="{ width:12, height:12, display:'inline-block', background: item.color, borderRadius: 3 }"></span>
                <div>
                  <div style="font-weight:600">{{ item.name }}</div>
                  <div style="font-size:12px; color:#909399">Số lượt: {{ item.count }}</div>
                </div>
              </div>
              <div style="text-align:right">
                <div style="font-weight:700">{{ item.percent }}%</div>
                <div style="font-size:12px; color:#909399">{{ item.ratioText }}</div>
              </div>
            </div>
          </el-list-item>
        </el-list>

        <div v-else-if="!loading" style="color:#909399">Không có dữ liệu dịch vụ</div>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { ref, onMounted, computed, nextTick } from 'vue'
import { TrendCharts } from '@element-plus/icons-vue'
import { Chart, registerables } from 'chart.js'
import enhancedDashboardService from '~/services/dss/enhancedDashboardService'

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
  top.push({ name: 'Khác', count: otherCount })
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
.service-type-pie-card { width:100% }
</style>