<template>
  <el-card class="revenue-cost-profit-card">
    <template #header>
      <div class="card-header">
        <h3>
          <el-icon><TrendCharts /></el-icon>
          Doanh Thu - Chi Phí - Lợi Nhuận
        </h3>
        
        <!-- Filters -->
        <div class="filters">
          <el-radio-group v-model="selectedFilter" size="small" @change="handleFilterChange">
            <el-radio-button label="7days">7 ngày</el-radio-button>
            <el-radio-button label="30days">30 ngày</el-radio-button>
            <el-radio-button label="quarter">Quý</el-radio-button>
            <el-radio-button label="custom">Tùy chỉnh</el-radio-button>
          </el-radio-group>
          
          <el-select
            v-model="selectedPeriod"
            size="small"
            style="width: 120px; margin-left: 10px"
            @change="handlePeriodChange"
          >
            <el-option label="Theo ngày" value="day" />
            <el-option label="Theo tuần" value="week" />
            <el-option label="Theo tháng" value="month" />
          </el-select>
        </div>
      </div>
    </template>

    <!-- Custom Date Range Picker -->
    <div v-if="selectedFilter === 'custom'" class="custom-date-picker">
      <el-date-picker
        v-model="dateRange"
        type="daterange"
        range-separator="đến"
        start-placeholder="Ngày bắt đầu"
        end-placeholder="Ngày kết thúc"
        format="DD/MM/YYYY"
        value-format="YYYY-MM-DD"
        @change="handleDateRangeChange"
      />
    </div>

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
import { TrendCharts, Money, Coin } from '@element-plus/icons-vue'
import { Chart, registerables } from 'chart.js'
import enhancedDashboardService from '~/services/dss/enhancedDashboardService'

Chart.register(...registerables)

// Data
const loading = ref(false)
const selectedFilter = ref('30days')
const selectedPeriod = ref('day')
const dateRange = ref([])
const tableData = ref([])
const chartRef = ref(null)
let chartInstance = null

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

// Methods
const fetchData = async () => {
  loading.value = true
  try {
    const params = {
      filter: selectedFilter.value,
      period: selectedPeriod.value
    }
    
    // Add custom date range if selected
    if (selectedFilter.value === 'custom' && dateRange.value.length === 2) {
      params.start_date = dateRange.value[0]
      params.end_date = dateRange.value[1]
    }
    
    const response = await enhancedDashboardService.getRevenueCostProfit(params)
    
    if (response.success) {
      tableData.value = response.data
      console.log('✅ Revenue/Cost/Profit data loaded:', tableData.value.length)
      
      // Update chart
      nextTick(() => {
        updateChart()
      })
    }
  } catch (error) {
    console.error('❌ Error loading revenue/cost/profit:', error)
  } finally {
    loading.value = false
  }
}

const handleFilterChange = () => {
  if (selectedFilter.value !== 'custom') {
    fetchData()
  }
}

const handlePeriodChange = () => {
  fetchData()
}

const handleDateRangeChange = () => {
  if (dateRange.value && dateRange.value.length === 2) {
    fetchData()
  }
}

const formatCurrency = (value) => {
  return new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND'
  }).format(value)
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('vi-VN')
}

const calculateProfitMargin = (revenue, profit) => {
  if (revenue === 0) return 0
  return ((profit / revenue) * 100).toFixed(2)
}

const getProfitMarginType = (revenue, profit) => {
  const margin = (profit / revenue) * 100
  if (margin >= 30) return 'success'
  if (margin >= 15) return ''
  if (margin >= 0) return 'warning'
  return 'danger'
}

// Chart
const updateChart = () => {
  if (!chartRef.value || tableData.value.length === 0) return
  
  // Destroy existing chart
  if (chartInstance) {
    chartInstance.destroy()
  }
  
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
        legend: {
          display: true,
          position: 'top'
        },
        title: {
          display: true,
          text: 'Biểu Đồ Doanh Thu - Chi Phí - Lợi Nhuận',
          font: {
            size: 16,
            weight: 'bold'
          }
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              let label = context.dataset.label || ''
              if (label) {
                label += ': '
              }
              label += new Intl.NumberFormat('vi-VN', {
                style: 'currency',
                currency: 'VND'
              }).format(context.parsed.y)
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
              return new Intl.NumberFormat('vi-VN', {
                notation: 'compact',
                compactDisplay: 'short'
              }).format(value) + 'đ'
            }
          }
        }
      }
    }
  })
}

// Lifecycle
onMounted(() => {
  fetchData()
})

// Watch for data changes
watch(tableData, () => {
  nextTick(() => {
    updateChart()
  })
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

.custom-date-picker {
  margin-bottom: 20px;
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
