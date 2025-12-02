<template>
  <el-card class="employee-kpi-card">
    <template #header>
      <div class="card-header">
        <div class="header-title">
          <el-icon class="title-icon"><TrophyBase /></el-icon>
          <h3>{{ $t('dashboard_title') }}</h3>
          <el-tag type="primary" size="small" effect="plain">{{ $t('top_10') }}</el-tag>
        </div>
      </div>
    </template>

    <!-- KPI Bar Chart -->
    <div v-loading="loading" class="chart-wrapper">
      <div class="chart-container">
        <canvas ref="chartRef"></canvas>
      </div>
      
      <!-- Legend Info -->
      <div class="legend-info">
        <div class="legend-item">
          <span class="legend-dot excellent"></span>
          <span class="legend-text">{{ $t('kpi_excellent') }}</span>
        </div>
        <div class="legend-item">
          <span class="legend-dot good"></span>
          <span class="legend-text">{{ $t('kpi_good') }}</span>
        </div>
        <div class="legend-item">
          <span class="legend-dot medium"></span>
          <span class="legend-text">{{ $t('kpi_medium') }}</span>
        </div>
        <div class="legend-item">
          <span class="legend-dot low"></span>
          <span class="legend-text">{{ $t('kpi_needs_improvement') }}</span>
        </div>
      </div>
    </div>

    <!-- Employee Detail Dialog -->
    <el-dialog
      v-model="dialogVisible"
      :title="selectedEmployee?.name"
      width="85%"
      top="5vh"
      :close-on-click-modal="false"
      class="employee-dialog"
    >
      <template #header>
        <div class="dialog-header">
          <div class="employee-info-header">
            <el-avatar :size="50" class="employee-avatar">
              {{ selectedEmployee?.name?.charAt(0) }}
            </el-avatar>
            <div>
              <h3>{{ selectedEmployee?.name }}</h3>
              <p class="employee-email">{{ selectedEmployee?.email || $t('no_email') }}</p>
            </div>
          </div>
        </div>
      </template>

      <div v-if="employeeDetail" class="employee-detail">
        <!-- Summary Statistics -->
        <el-row :gutter="20" class="summary-row">
          <el-col :xs="12" :sm="6">
            <div class="stat-card">
              <div class="stat-icon hours">
                <el-icon><Clock /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value">{{ employeeDetail.total_worked_hours }}h</div>
                <div class="stat-label">{{ $t('total_hours_worked') }}</div>
              </div>
            </div>
          </el-col>
          <el-col :xs="12" :sm="6">
            <div class="stat-card">
              <div class="stat-icon score">
                <el-icon><Medal /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value">{{ employeeDetail.work_hour_score }}</div>
                <div class="stat-label">{{ $t('work_hour_score') }}</div>
              </div>
            </div>
          </el-col>
          <el-col :xs="12" :sm="6">
            <div class="stat-card">
              <div class="stat-icon bonus">
                <el-icon><Trophy /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value">{{ employeeDetail.completed_orders_count }}</div>
                <div class="stat-label">{{ $t('orders_count') }}</div>
              </div>
            </div>
          </el-col>
          <el-col :xs="12" :sm="6">
            <div class="stat-card highlight">
              <div class="stat-icon kpi">
                <el-icon><TrendCharts /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value" :style="{ color: getKPIColor(employeeDetail.kpi_score) }">
                  {{ employeeDetail.kpi_score }}
                </div>
                <div class="stat-label">KPI Score</div>
              </div>
            </div>
          </el-col>
        </el-row>

        <!-- Orders Detail -->
        <!-- <div class="orders-section">
          <div class="section-header">
            <h4>
              <el-icon><Document /></el-icon>
              Danh sách đơn hàng đã hoàn thành
            </h4>
            <el-tag type="success" size="small">
              {{ employeeDetail.completed_orders_count }} đơn
            </el-tag>
          </div>

          <el-table
            :data="employeeDetail.orders_detail"
            stripe
            max-height="450"
            class="orders-table"
            :header-cell-style="{ background: '#f5f7fa', color: '#606266', fontWeight: '600' }"
          >
            <el-table-column label="Mã đơn" prop="code" width="110" fixed>
              <template #default="{ row }">
                <el-tag size="small" effect="plain">{{ row.code }}</el-tag>
              </template>
            </el-table-column>
            
            <el-table-column label="Dịch vụ" prop="service_type" width="140">
              <template #default="{ row }">
                <div class="service-cell">
                  <el-icon><Box /></el-icon>
                  <span>{{ row.service_type }}</span>
                </div>
              </template>
            </el-table-column>
            
            <el-table-column label="Thời gian" width="360">
              <template #default="{ row }">
                <div class="timeline-cell">
                  <div class="timeline-item">
                    <span class="timeline-label">Bắt đầu:</span>
                    <span class="timeline-value">{{ formatDateTime(row.start_time) }}</span>
                  </div>
                  <div class="timeline-arrow">→</div>
                  <div class="timeline-item">
                    <span class="timeline-label">KT dự kiến:</span>
                    <span class="timeline-value">{{ formatDateTime(row.end_time) }}</span>
                  </div>
                  <div class="timeline-arrow">✓</div>
                  <div class="timeline-item">
                    <span class="timeline-label">KT thực tế:</span>
                    <span class="timeline-value highlight">
                      {{ row.actual_end ? formatDateTime(row.actual_end) : 'N/A' }}
                    </span>
                  </div>
                </div>
              </template>
            </el-table-column>
            
            <el-table-column label="Giờ làm" width="100" align="center">
              <template #default="{ row }">
                <el-tag type="info" effect="plain" size="small">
                  <el-icon><Timer /></el-icon>
                  {{ row.worked_hours }}h
                </el-tag>
              </template>
            </el-table-column>
            
            <el-table-column label="Thưởng sớm" width="110" align="center">
              <template #default="{ row }">
                <el-tag 
                  :type="row.early_bonus > 0 ? 'success' : ''" 
                  size="small"
                  effect="dark"
                >
                  <el-icon v-if="row.early_bonus > 0"><CircleCheck /></el-icon>
                  +{{ row.early_bonus }}
                </el-tag>
              </template>
            </el-table-column>
            
            <el-table-column label="Chi phí" width="140" align="right">
              <template #default="{ row }">
                <span class="cost-value">{{ formatCurrency(row.cost) }}</span>
              </template>
            </el-table-column>
          </el-table>
        </div> -->
      </div>
      
      <div v-else v-loading="detailLoading" class="loading-container"></div>
    </el-dialog>
  </el-card>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import { 
  TrophyBase, TrendCharts, Clock, Medal, Trophy, Document, 
  Box, Timer, CircleCheck 
} from '@element-plus/icons-vue'
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

const handleRowClick = async (row) => {
  selectedEmployee.value = row
  dialogVisible.value = true
  employeeDetail.value = null
  detailLoading.value = true
  
  try {
    const response = await enhancedDashboardService.getEmployeeKPIDetail(row.employee_id)
    
    if (response.success) {
      employeeDetail.value = response.data
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
  const date = new Date(dateTime)
  return date.toLocaleString('vi-VN', { 
    day: '2-digit', 
    month: '2-digit', 
    hour: '2-digit', 
    minute: '2-digit' 
  })
}

// Chart
const updateChart = () => {
  if (!chartRef.value || employees.value.length === 0) return
  
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
        borderRadius: 8,
        barThickness: 24
      }]
    },
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
          ctx.strokeStyle = '#67c23a'
          ctx.setLineDash([8, 4])
          ctx.stroke()
          
          // Add label
          ctx.fillStyle = '#67c23a'
          ctx.font = 'bold 12px sans-serif'
          ctx.fillText('Mục tiêu: 60', x + 5, chart.chartArea.top + 20)
          ctx.restore()
        }
      }
    ],
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      onClick: (event, elements) => {
        if (elements.length > 0) {
          const index = elements[0].index
          handleRowClick(employees.value[index])
        }
      },
      plugins: {
        legend: { display: false },
        title: {
          display: false
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.85)',
          padding: 12,
          titleFont: { size: 14, weight: 'bold' },
          bodyFont: { size: 13 },
          callbacks: {
            label: function(context) {
              const idx = context.dataIndex
              const emp = employees.value[idx] || {}
              const hours = Number(emp.total_worked_hours || 0)
              const orders = Number(emp.completed_orders || 0)
              const pct = Math.min((hours / 48) * 100, 100)
              const points = hours + orders
              const kpiTarget = 60
              const need = Math.max(0, kpiTarget - points)

              return [
                `KPI Score: ${emp.kpi_score}`,
                `Giờ làm: ${hours}h (${pct.toFixed(1)}%)`,
                `Đơn hoàn thành: ${orders}`,
                need > 0 ? `⚠ Cần thêm ${need.toFixed(1)} điểm` : '✓ Đã đạt mục tiêu'
              ]
            }
          }
        }
      },
      scales: {
        x: {
          beginAtZero: true,
          max: 100,
          grid: {
            color: 'rgba(0, 0, 0, 0.05)'
          },
          title: { 
            display: true, 
            text: 'KPI Score',
            font: { size: 13, weight: '600' }
          }
        },
        y: {
          grid: {
            display: false
          },
          ticks: {
            font: { size: 12, weight: '500' }
          }
        }
      }
    }
  })
}

// Lifecycle
onMounted(() => {
  fetchEmployees()
})

watch(employees, () => {
  nextTick(() => {
    updateChart()
  })
}, { deep: true })

defineExpose({ fetchEmployees })
</script>

<style scoped>
.employee-kpi-card {
  height: 100%;
  border-radius: 14px;
  overflow: hidden;
}

/* =======================
   HEADER
======================= */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 4px;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.title-icon {
  font-size: 26px;
  color: #ffffff;
}

.header-title h3 {
  margin: 0;
  font-size: 19px;
  font-weight: 700;
  color: #ffffff;
}

/* =======================
   CHART
======================= */
.chart-wrapper {
  position: relative;
  min-height: 380px;
}

.chart-container {
  height: 360px;
  padding: 14px 0;
  cursor: pointer;
}

/* =======================
   LEGEND
======================= */
.legend-info {
  display: flex;
  justify-content: center;
  gap: 26px;
  padding: 16px 0 10px;
  flex-wrap: wrap;
  border-top: 1px solid #ebeef5;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.legend-dot {
  width: 14px;
  height: 14px;
  border-radius: 4px;
}

.legend-dot.excellent { background: #67c23a; }
.legend-dot.good { background: #409eff; }
.legend-dot.medium { background: #e6a23c; }
.legend-dot.low { background: #f56c6c; }

.legend-text {
  font-size: 13px;
  font-weight: 500;
  color: #606266;
}

/* =======================
   DIALOG
======================= */
.employee-dialog :deep(.el-dialog__header) {
  padding: 22px 24px;
  border-bottom: 1px solid #ebeef5;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.dialog-header {
  color: white;
  font-weight: 600;
}

.employee-info-header {
  display: flex;
  align-items: center;
  gap: 18px;
}

.employee-avatar {
  background: rgba(255, 255, 255, 0.35);
  color: white;
  font-size: 22px;
  font-weight: 700;
  border: 3px solid rgba(255, 255, 255, 0.5);
}

.employee-info-header h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
}

.employee-email {
  margin-top: 4px;
  font-size: 13px;
  opacity: 0.9;
}

.employee-detail {
  padding: 20px 0;
}

/* =======================
   SUMMARY CARDS
======================= */
.summary-row {
  margin-bottom: 28px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 18px;
  border-radius: 14px;
  background: linear-gradient(135deg, #f7f9fc 0%, #ffffff 100%);
  border: 1px solid #eaecef;
  transition: all 0.25s ease;
}

.stat-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 14px rgba(0,0,0,0.08);
}

.stat-card.highlight {
  background: linear-gradient(135deg, #667eea12 0%, #764ba212 100%);
  border-color: #667eea35;
}

.stat-icon {
  width: 52px;
  height: 52px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
}

.stat-icon.hours {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.stat-icon.score {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.stat-icon.bonus {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
}

.stat-icon.kpi {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
  color: white;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: #262626;
}

.stat-label {
  font-size: 13px;
  color: #909399;
  margin-top: 4px;
}

/* =======================
   ORDERS TABLE
======================= */
.orders-section {
  margin-top: 22px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 10px;
  margin-bottom: 16px;
  border-bottom: 2px solid #ebeef5;
}

.section-header h4 {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  font-size: 17px;
  font-weight: 700;
}

.orders-table {
  border-radius: 10px;
  overflow: hidden;
}

.service-cell {
  display: flex;
  align-items: center;
  gap: 6px;
}

.timeline-cell {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 12px;
}

.timeline-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.timeline-label {
  font-size: 11px;
  color: #909399;
}

.timeline-value {
  font-size: 12px;
  font-weight: 600;
  color: #606266;
}

.timeline-value.highlight {
  color: #67c23a;
}

.timeline-arrow {
  font-size: 14px;
  color: #c0c4cc;
}

.cost-value {
  font-weight: 700;
  color: #e6a23c;
}

.loading-container {
  height: 280px;
}

/* =======================
   RESPONSIVE
======================= */
@media (max-width: 768px) {
  .legend-info {
    gap: 14px;
  }

  .stat-card {
    padding: 16px;
  }

  .stat-icon {
    width: 44px;
    height: 44px;
    font-size: 18px;
  }

  .stat-value {
    font-size: 20px;
  }

  .timeline-cell {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }

  .timeline-arrow {
    transform: rotate(90deg);
  }
}

</style>