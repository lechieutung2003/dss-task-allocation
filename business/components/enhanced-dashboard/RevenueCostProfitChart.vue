<template>
  <el-card class="revenue-cost-profit-card">
    <template #header>
      <div class="card-header">
        <h3>
          <el-icon><TrendCharts /></el-icon>
          Doanh Thu - Chi Phí - Lợi Nhuận
        </h3>
        
        <!-- Period Selector and Navigation -->
        <div class="filters">
          <el-button-group size="small">
            <el-button @click="gotoPrev">
              <el-icon><ArrowLeft /></el-icon>
              Trước
            </el-button>
            <el-button @click="gotoToday">Hôm nay</el-button>
            <el-button @click="gotoNext">
              Sau
              <el-icon><ArrowRight /></el-icon>
            </el-button>
          </el-button-group>
          
          <el-select
            v-model="selectedPeriod"
            size="small"
            style="width: 160px; margin-left: 10px"
            @change="handlePeriodChange"
          >
            <el-option label="Theo tuần (7 cột)" value="week" />
            <el-option label="Theo tháng (4 cột)" value="month" />
            <el-option label="Theo năm (12 cột)" value="year" />
          </el-select>
          
          <span style="margin-left: 10px; color: #606266; font-size: 14px">
            {{ anchorLabel }}
          </span>
        </div>
      </div>
    </template>

    <!-- Chart -->
    <div class="chart-container">
      <canvas ref="chartRef"></canvas>
    </div>

    <!-- Summary Statistics -->
    <el-row :gutter="20" class="summary-stats">
      <el-col :span="8">
        <el-statistic
          title="Tổng Doanh Thu"
          :value="totalRevenue"
          :precision="0"
          suffix="đ"
        >
          <template #prefix>
            <el-icon style="color: #67c23a"><Money /></el-icon>
          </template>
        </el-statistic>
      </el-col>
      <el-col :span="8">
        <el-statistic
          title="Tổng Chi Phí"
          :value="totalCost"
          :precision="0"
          suffix="đ"
        >
          <template #prefix>
            <el-icon style="color: #e6a23c"><Coin /></el-icon>
          </template>
        </el-statistic>
      </el-col>
      <el-col :span="8">
        <el-statistic
          title="Tổng Lợi Nhuận"
          :value="totalProfit"
          :precision="0"
          suffix="đ"
        >
          <template #prefix>
            <el-icon :style="{ color: totalProfit >= 0 ? '#67c23a' : '#f56c6c' }">
              <TrendCharts />
            </el-icon>
          </template>
        </el-statistic>
      </el-col>
    </el-row>

    <!-- Data Table -->
    <el-table
      v-loading="loading"
      :data="tableData"
      stripe
      style="width: 100%; margin-top: 20px"
      max-height="400"
    >
      <el-table-column label="Ngày" prop="date" width="150">
        <template #default="{ row }">
          {{ formatDate(row.date) }}
        </template>
      </el-table-column>
      
      <el-table-column label="Doanh Thu" width="180">
        <template #default="{ row }">
          <span class="revenue-text">{{ formatCurrency(row.revenue) }}</span>
        </template>
      </el-table-column>
      
      <el-table-column label="Chi Phí" width="180">
        <template #default="{ row }">
          <span class="cost-text">{{ formatCurrency(row.cost) }}</span>
        </template>
      </el-table-column>
      
      <el-table-column label="Lợi Nhuận" width="180">
        <template #default="{ row }">
          <span :class="row.profit >= 0 ? 'profit-positive' : 'profit-negative'">
            {{ formatCurrency(row.profit) }}
          </span>
        </template>
      </el-table-column>
      
      <el-table-column label="Tỷ suất lợi nhuận" width="150">
        <template #default="{ row }">
          <el-tag
            :type="getProfitMarginType(row.revenue, row.profit)"
            size="small"
          >
            {{ calculateProfitMargin(row.revenue, row.profit) }}%
          </el-tag>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { TrendCharts, Money, Coin, ArrowLeft, ArrowRight } from '@element-plus/icons-vue'
import { Chart, registerables } from 'chart.js'
import enhancedDashboardService from '~/services/dss/enhancedDashboardService'

Chart.register(...registerables)

// Data
const loading = ref(false)
const selectedPeriod = ref('week') // default to week
const tableData = ref([])
const chartRef = ref(null)
let chartInstance = null

// Current anchor date (used for navigation)
const currentAnchor = ref(new Date())

// Computed
const totalRevenue = computed(() => {
  return tableData.value.reduce((sum, item) => sum + item.revenue, 0)
})

const totalCost = computed(() => {
  return tableData.value.reduce((sum, item) => sum + item.cost, 0)
})

const totalProfit = computed(() => {
  return tableData.value.reduce((sum, item) => sum + item.profit, 0)
})

// Computed label showing current period
const anchorLabel = computed(() => {
  const anchor = currentAnchor.value
  if (!anchor) return ''
  
  if (selectedPeriod.value === 'week') {
    const monday = new Date(anchor)
    monday.setDate(anchor.getDate() - ((anchor.getDay() + 6) % 7))
    const sunday = new Date(monday)
    sunday.setDate(monday.getDate() + 6)
    return `${monday.toLocaleDateString('vi-VN')} — ${sunday.toLocaleDateString('vi-VN')}`
  } else if (selectedPeriod.value === 'month') {
    return anchor.toLocaleString('vi-VN', { month: 'long', year: 'numeric' })
  } else if (selectedPeriod.value === 'year') {
    return String(anchor.getFullYear())
  }
  return ''
})

// Helper: compute date range for API based on anchor + period
const computeRange = (anchor, period) => {
  const start = new Date(anchor)
  let end = new Date(anchor)
  
  if (period === 'week') {
    // Get Monday of the week containing anchor
    const monday = new Date(anchor)
    monday.setDate(anchor.getDate() - ((anchor.getDay() + 6) % 7))
    start.setTime(monday.getTime())
    start.setHours(0, 0, 0, 0)
    
    // Get Sunday of the same week
    end = new Date(monday)
    end.setDate(monday.getDate() + 6)
    end.setHours(23, 59, 59, 999)
  } else if (period === 'month') {
    // First day of the month
    start.setDate(1)
    start.setHours(0, 0, 0, 0)
    
    // Last day of the month
    end = new Date(start.getFullYear(), start.getMonth() + 1, 0)
    end.setHours(23, 59, 59, 999)
  } else if (period === 'year') {
    // First day of the year
    start.setMonth(0, 1)
    start.setHours(0, 0, 0, 0)
    
    // Last day of the year
    end = new Date(start.getFullYear(), 11, 31)
    end.setHours(23, 59, 59, 999)
  }
  
  const toDateOnly = d => d.toISOString().slice(0, 10)
  return { start_date: toDateOnly(start), end_date: toDateOnly(end) }
}

// helper: normalize buckets client-side if backend returns incomplete data
const normalizeBuckets = (data, period) => {
  if (!data || data.length === 0) {
    const buckets = []
    const anchor = currentAnchor.value
    
    if (period === 'week') {
      const monday = new Date(anchor)
      monday.setDate(anchor.getDate() - ((anchor.getDay() + 6) % 7))
      for (let i = 0; i < 7; i++) {
        const d = new Date(monday)
        d.setDate(monday.getDate() + i)
        buckets.push({ date: d.toISOString().slice(0,10), label: d.toLocaleDateString('vi-VN'), revenue:0, cost:0, profit:0 })
      }
    } else if (period === 'month') {
      buckets.push({ date: 'w1', label: 'Tuần 1 (1-7)', revenue:0, cost:0, profit:0 })
      buckets.push({ date: 'w2', label: 'Tuần 2 (8-14)', revenue:0, cost:0, profit:0 })
      buckets.push({ date: 'w3', label: 'Tuần 3 (15-21)', revenue:0, cost:0, profit:0 })
      buckets.push({ date: 'w4', label: 'Tuần 4 (22-end)', revenue:0, cost:0, profit:0 })
    } else if (period === 'year') {
      const year = anchor.getFullYear()
      for (let m = 1; m <= 12; m++) {
        const label = new Date(year, m-1, 1).toLocaleString('vi-VN', { month: 'short', year: 'numeric' })
        buckets.push({ date: `${year}-${String(m).padStart(2,'0')}`, label, revenue:0, cost:0, profit:0 })
      }
    }
    return buckets
  }
  // If server returned buckets, return as-is (backend should provide correct buckets)
  return data
}

const fetchData = async () => {
  loading.value = true
  try {
    const range = computeRange(currentAnchor.value, selectedPeriod.value)
    const params = { 
      period: selectedPeriod.value,
      start_date: range.start_date,
      end_date: range.end_date
    }
    console.debug('🔁 fetchData params:', params)
    
    const response = await enhancedDashboardService.getRevenueCostProfit(params)
    console.debug('🔁 fetchData response:', response)
    
    if (response && response.success) {
      const normalized = normalizeBuckets(response.data, selectedPeriod.value)
      tableData.value = normalized
      nextTick(() => updateChart())
    } else {
      tableData.value = normalizeBuckets([], selectedPeriod.value)
      nextTick(() => updateChart())
    }
  } catch (error) {
    console.error('❌ Error loading revenue/cost/profit:', error)
    tableData.value = normalizeBuckets([], selectedPeriod.value)
    nextTick(() => updateChart())
  } finally {
    loading.value = false
  }
}

// Navigation functions
const gotoPrev = () => {
  const a = new Date(currentAnchor.value)
  if (selectedPeriod.value === 'week') {
    a.setDate(a.getDate() - 7)
  } else if (selectedPeriod.value === 'month') {
    a.setMonth(a.getMonth() - 1)
  } else if (selectedPeriod.value === 'year') {
    a.setFullYear(a.getFullYear() - 1)
  }
  currentAnchor.value = a
  fetchData()
}

const gotoNext = () => {
  const a = new Date(currentAnchor.value)
  if (selectedPeriod.value === 'week') {
    a.setDate(a.getDate() + 7)
  } else if (selectedPeriod.value === 'month') {
    a.setMonth(a.getMonth() + 1)
  } else if (selectedPeriod.value === 'year') {
    a.setFullYear(a.getFullYear() + 1)
  }
  currentAnchor.value = a
  fetchData()
}

const gotoToday = () => {
  currentAnchor.value = new Date()
  fetchData()
}

const handlePeriodChange = () => {
  currentAnchor.value = new Date()
  fetchData()
}

const formatCurrency = (value) => {
  return new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND'
  }).format(value)
}

const formatDate = (dateStr) => {
  // handle non-ISO placeholders too
  const date = new Date(dateStr)
  if (isNaN(date.getTime())) return dateStr
  return date.toLocaleDateString('vi-VN')
}

const calculateProfitMargin = (revenue, profit) => {
  if (revenue === 0) return 0
  return ((profit / revenue) * 100).toFixed(2)
}

const getProfitMarginType = (revenue, profit) => {
  if (revenue === 0) return ''
  const margin = (profit / revenue) * 100
  if (margin >= 30) return 'success'
  if (margin >= 15) return ''
  if (margin >= 0) return 'warning'
  return 'danger'
}

// Chart
const updateChart = () => {
  if (!chartRef.value || tableData.value.length === 0) return
  
  if (chartInstance) chartInstance.destroy()
  const ctx = chartRef.value.getContext('2d')
  
  chartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: tableData.value.map(item => formatDate(item.date)),
      datasets: [
        {
          label: 'Doanh Thu',
          data: tableData.value.map(item => item.revenue),
          borderColor: '#67c23a',
          backgroundColor: 'rgba(103, 194, 58, 0.1)',
          borderWidth: 2,
          fill: true,
          tension: 0.4
        },
        {
          label: 'Chi Phí',
          data: tableData.value.map(item => item.cost),
          borderColor: '#e6a23c',
          backgroundColor: 'rgba(230, 162, 60, 0.1)',
          borderWidth: 2,
          fill: true,
          tension: 0.4
        },
        {
          label: 'Lợi Nhuận',
          data: tableData.value.map(item => item.profit),
          borderColor: '#409eff',
          backgroundColor: 'rgba(64, 158, 255, 0.1)',
          borderWidth: 2,
          fill: true,
          tension: 0.4
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: 'index',
        intersect: false
      },
      plugins: {
        legend: { display: true, position: 'top' },
        title: {
          display: true,
          text: 'Biểu Đồ Doanh Thu - Chi Phí - Lợi Nhuận',
          font: { size: 16, weight: 'bold' }
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              let label = context.dataset.label || ''
              if (label) label += ': '
              label += new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(context.parsed.y)
              return label
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: function(value) {
              return new Intl.NumberFormat('vi-VN', { notation: 'compact', compactDisplay: 'short' }).format(value) + 'đ'
            }
          }
        }
      }
    }
  })
}

// Lifecycle
onMounted(() => {
  currentAnchor.value = new Date()
  fetchData()
})

// Watch for data changes
watch(tableData, () => {
  nextTick(() => updateChart())
}, { deep: true })
</script>

<style scoped>
.revenue-cost-profit-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.card-header h3 {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.filters {
  display: flex;
  align-items: center;
  gap: 10px;
}

.chart-container {
  height: 400px;
  padding: 20px 0;
}

.summary-stats {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #ebeef5;
}

.revenue-text {
  color: #67c23a;
  font-weight: 600;
}

.cost-text {
  color: #e6a23c;
  font-weight: 600;
}

.profit-positive {
  color: #67c23a;
  font-weight: 600;
}

.profit-negative {
  color: #f56c6c;
  font-weight: 600;
}
</style>