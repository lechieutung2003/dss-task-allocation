<template>
  <el-card class="employee-kpi-card">
    <template #header>
      <div class="card-header">
        <h3>
          <el-icon><TrophyBase /></el-icon>
          KPI Nhân Viên (Top 10)
        </h3>
      </div>
    </template>

    <!-- KPI Bar Chart -->
    <div class="chart-container">
      <canvas ref="chartRef"></canvas>
    </div>

    <!-- Employee Detail Dialog -->
    <el-dialog
      v-model="dialogVisible"
      :title="`Chi tiết KPI - ${selectedEmployee?.name}`"
      width="80%"
      :close-on-click-modal="false"
    >
      <div v-if="employeeDetail" class="employee-detail">
        <!-- Summary -->
        <el-row :gutter="20" class="summary-row">
          <el-col :span="6">
            <el-statistic title="Tổng giờ làm" :value="employeeDetail.total_worked_hours" suffix="h" />
          </el-col>
          <el-col :span="6">
            <el-statistic title="Điểm giờ làm" :value="employeeDetail.work_hour_score" />
          </el-col>
          <el-col :span="6">
            <el-statistic title="Thưởng sớm" :value="employeeDetail.early_bonus_total" />
          </el-col>
          <el-col :span="6">
            <el-statistic title="KPI Score" :value="employeeDetail.kpi_score">
              <template #suffix>
                <el-icon :color="getKPIColor(employeeDetail.kpi_score)">
                  <TrendCharts />
                </el-icon>
              </template>
            </el-statistic>
          </el-col>
        </el-row>

        <!-- Orders Detail -->
        <h4 style="margin-top: 20px">Danh sách đơn hàng đã hoàn thành ({{ employeeDetail.completed_orders_count }})</h4>
        <el-table
          :data="employeeDetail.orders_detail"
          stripe
          max-height="400"
        >
          <el-table-column label="Mã đơn" prop="code" width="120" />
          <el-table-column label="Dịch vụ" prop="service_type" width="150" />
          <el-table-column label="Giờ bắt đầu" width="180">
            <template #default="{ row }">
              {{ formatDateTime(row.start_time) }}
            </template>
          </el-table-column>
          <el-table-column label="Giờ kết thúc dự kiến" width="180">
            <template #default="{ row }">
              {{ formatDateTime(row.end_time) }}
            </template>
          </el-table-column>
          <el-table-column label="Giờ hoàn thành thực tế" width="180">
            <template #default="{ row }">
              {{ row.actual_end ? formatDateTime(row.actual_end) : 'N/A' }}
            </template>
          </el-table-column>
          <el-table-column label="Giờ làm" width="100">
            <template #default="{ row }">
              {{ row.worked_hours }}h
            </template>
          </el-table-column>
          <el-table-column label="Thưởng sớm" width="100">
            <template #default="{ row }">
              <el-tag :type="row.early_bonus > 0 ? 'success' : ''" size="small">
                +{{ row.early_bonus }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="Chi phí" width="130">
            <template #default="{ row }">
              {{ formatCurrency(row.cost) }}
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div v-else v-loading="detailLoading" style="height: 200px"></div>
    </el-dialog>
  </el-card>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import { TrophyBase, TrendCharts } from '@element-plus/icons-vue'
import { Chart, registerables } from 'chart.js'
import enhancedDashboardService from '~/services/dss/enhancedDashboardService'

Chart.register(...registerables)

// Data
const loading = ref(false)
const detailLoading = ref(false)
const employees = ref([])
const currentPage = ref(1)
const pageSize = ref(5)
const totalRecords = ref(0)
const chartRef = ref(null)
let chartInstance = null

// Dialog
const dialogVisible = ref(false)
const selectedEmployee = ref(null)
const employeeDetail = ref(null)

// Methods
const fetchEmployees = async () => {
  loading.value = true
  try {
    const response = await enhancedDashboardService.getEmployeeKPI({
      page: currentPage.value,
      page_size: pageSize.value
    })
    
    if (response.success) {
      employees.value = response.data
      totalRecords.value = response.pagination.total
      console.log('✅ Employee KPI loaded:', employees.value.length)
      
      // Update chart after data loaded
      nextTick(() => {
        updateChart()
      })
    }
  } catch (error) {
    console.error('❌ Error loading employee KPI:', error)
  } finally {
    loading.value = false
  }
}

const handlePageChange = (page) => {
  currentPage.value = page
  fetchEmployees()
}

const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
  fetchEmployees()
}

const handleRowClick = async (row) => {
  selectedEmployee.value = row
  dialogVisible.value = true
  employeeDetail.value = null
  detailLoading.value = true
  
  try {
    console.log('🔍 Fetching detail for employee:', row.employee_id)
    const response = await enhancedDashboardService.getEmployeeKPIDetail(row.employee_id)
    console.log('📦 Response:', response)
    console.log('✅ Response.success:', response.success)
    console.log('📊 Response.data:', response.data)
    
    if (response.success) {
      employeeDetail.value = response.data
      console.log('✅ Employee detail set:', employeeDetail.value)
    } else {
      console.error('❌ Response success is false')
    }
  } catch (error) {
    console.error('❌ Error loading employee detail:', error)
  } finally {
    detailLoading.value = false
  }
}

const getKPIColor = (score) => {
  if (score < 20) return '#f56c6c'
  if (score < 40) return '#e6a23c'
  if (score < 60) return '#409eff'
  return '#67c23a'
}

const formatCurrency = (value) => {
  return new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND'
  }).format(value)
}

const formatDateTime = (dateTime) => {
  if (!dateTime) return 'N/A'
  return new Date(dateTime).toLocaleString('vi-VN')
}

// Chart
const updateChart = () => {
  if (!chartRef.value || employees.value.length === 0) return
  
  // Destroy existing chart
  if (chartInstance) {
    chartInstance.destroy()
  }
  
  const ctx = chartRef.value.getContext('2d')

  chartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: employees.value.map(emp => emp.name),
      datasets: [{
        label: 'KPI Score',
        data: employees.value.map(emp => emp.kpi_score),
        backgroundColor: employees.value.map(emp => getKPIColor(emp.kpi_score)),
        borderRadius: 5
      }]
    },
    // thêm plugin tùy chỉnh để vẽ đường mốc và set x axis max = 100
    plugins: [
      {
        id: 'thresholdLine',
        beforeDraw(chart) {
          const threshold = 60
          const xScale = chart.scales.x
          if (!xScale) return
          const x = xScale.getPixelForValue(threshold)
          const ctx = chart.ctx
          ctx.save()
          ctx.beginPath()
          ctx.moveTo(x, chart.chartArea.top)
          ctx.lineTo(x, chart.chartArea.bottom)
          ctx.lineWidth = 2
          ctx.strokeStyle = 'rgba(0,0,0,0.6)' // màu gạch
          ctx.setLineDash([6, 4])
          ctx.stroke()
          ctx.restore()
        }
      }
    ],
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        title: {
          display: true,
          text: 'KPI Score - Top 10 Nhân Viên',
          font: { size: 16, weight: 'bold' }
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              const idx = context.dataIndex
              const emp = employees.value[idx] || {}
              const hours = Number(emp.total_worked_hours || 0)
              const orders = Number(emp.completed_orders || 0)
              const pct = Math.min((hours / 48) * 100, 100)
              const points = hours + orders
              const kpiTarget_h = 50
              const need = Math.max(0, kpiTarget_h - points)

              return [
                `Đã làm ${pct.toFixed(1)}% số giờ yêu cầu`,
                `Đơn hoàn thành: ${orders}`,
                `KPI hiện tại: ${points.toFixed(1)} điểm`,
                need > 0 ? `Cần thêm: ${need.toFixed(1)}h để đạt ${kpiTarget_h} điểm` : 'Đã đạt KPI'
              ]
            }
          }
        }
      },
      scales: {
        x: {
          beginAtZero: true,
          max: 100, // trục ngang kéo dài tới 100
          title: { display: true, text: 'KPI Score' }
        }
      }
    }
  })

}

// Lifecycle
onMounted(() => {
  fetchEmployees()
})

// Watch for data changes to update chart
watch(employees, () => {
  nextTick(() => {
    updateChart()
  })
}, { deep: true })
</script>

<style scoped>
.employee-kpi-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.chart-container {
  height: 400px;
  padding: 20px 0;
}

.employee-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.email {
  font-size: 12px;
  color: #909399;
}

.kpi-score {
  display: flex;
  align-items: center;
  gap: 8px;
}

.score-value {
  font-size: 16px;
  color: #303133;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.employee-detail {
  padding: 10px 0;
}

.summary-row {
  margin-bottom: 20px;
}
</style>
