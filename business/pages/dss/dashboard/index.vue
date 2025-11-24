<script setup>
import { ref } from 'vue'
import { DataBoard, Refresh, Timer, VideoPause } from '@element-plus/icons-vue'
import PriorityOrdersTable from '~/components/enhanced-dashboard/PriorityOrdersTable.vue'
import EmployeeKPITable from '~/components/enhanced-dashboard/EmployeeKPITable.vue'
import RevenueCostProfitChart from '~/components/enhanced-dashboard/RevenueCostProfitChart.vue'
import ServiceTypePieChart from '~/components/enhanced-dashboard/ServiceTypePieChart.vue'
import ServiceStatusPieChart from '~/components/enhanced-dashboard/ServiceStatusPieChart.vue'

definePageMeta({ layout: "dss", middleware: ["auth", "role-based"] });

// Refs to child components
const priorityOrdersRef = ref(null)
const employeeKPIRef = ref(null)
const revenueChartRef = ref(null)
const serviceTypeRef = ref(null)
const serviceStatusRef = ref(null)

// Data
const autoRefresh = ref(true)
const refreshing = ref(false)

// Methods
const toggleAutoRefresh = () => {
  autoRefresh.value = !autoRefresh.value
}

const refreshAll = async () => {
  refreshing.value = true
  try {
    const promises = []
    if (priorityOrdersRef.value && priorityOrdersRef.value.fetchOrders) promises.push(priorityOrdersRef.value.fetchOrders())
    if (employeeKPIRef.value && employeeKPIRef.value.fetchEmployees) promises.push(employeeKPIRef.value.fetchEmployees())
    if (revenueChartRef.value && revenueChartRef.value.fetchData) promises.push(revenueChartRef.value.fetchData())
    if (serviceTypeRef.value && serviceTypeRef.value.fetchData) promises.push(serviceTypeRef.value.fetchData())
    if (serviceStatusRef.value && serviceStatusRef.value.fetchData) promises.push(serviceStatusRef.value.fetchData())
    await Promise.all(promises)
  } finally {
    refreshing.value = false
  }
}
</script>

<template>
  <div class="dashboard-container">
    <!-- Header -->
    <div class="dashboard-header">
      <div class="header-left">
        <el-icon class="header-icon"><DataBoard /></el-icon>
        <h1 class="header-title">Dashboard Nâng Cao</h1>
      </div>
      <div class="header-actions">
        <el-button
          :type="autoRefresh ? 'success' : 'default'"
          :icon="autoRefresh ? Timer : VideoPause"
          @click="toggleAutoRefresh"
          size="default"
        >
          {{ autoRefresh ? 'Auto' : 'Manual' }}
        </el-button>
        <el-button 
          type="primary" 
          :icon="Refresh" 
          @click="refreshAll" 
          :loading="refreshing"
          size="default"
        >
          Làm mới
        </el-button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="dashboard-content">
      <!-- Priority Orders -->
      <div class="dashboard-card">
        <PriorityOrdersTable :auto-refresh="autoRefresh" ref="priorityOrdersRef" />
      </div>

      <!-- Employee KPI -->
      <div class="dashboard-card">
        <EmployeeKPITable ref="employeeKPIRef" />
      </div>

      <!-- Charts Grid -->
      <div class="charts-grid">
        <!-- Revenue Chart - Full Width -->
        <div class="dashboard-card chart-full">
          <RevenueCostProfitChart ref="revenueChartRef" />
        </div>

        <!-- Pie Charts - Side by Side -->
        <div class="dashboard-card chart-half">
          <ServiceTypePieChart ref="serviceTypeRef" />
        </div>
        <div class="dashboard-card chart-half">
          <ServiceStatusPieChart ref="serviceStatusRef" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard-container {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  margin-bottom: 20px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-icon {
  font-size: 28px;
  color: #409eff;
}

.header-title {
  margin: 0;
  font-size: 22px;
  font-weight: 600;
  color: #303133;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.dashboard-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.dashboard-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  transition: all 0.3s ease;
}

.dashboard-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.12);
}

.charts-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.chart-full {
  grid-column: 1 / -1;
}

.chart-half {
  min-height: 400px;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
  
  .chart-half {
    min-height: 350px;
  }
}

@media (max-width: 768px) {
  .dashboard-container {
    padding: 12px;
  }

  .dashboard-header {
    flex-direction: column;
    gap: 12px;
    padding: 16px;
  }

  .header-left {
    width: 100%;
  }

  .header-actions {
    width: 100%;
    justify-content: flex-end;
  }

  .header-title {
    font-size: 18px;
  }

  .dashboard-card {
    padding: 16px;
  }

  .chart-half {
    min-height: 300px;
  }
}

@media (max-width: 480px) {
  .header-actions {
    flex-wrap: wrap;
  }
  
  .header-actions :deep(.el-button span) {
    display: none;
  }
  
  .header-actions :deep(.el-button) {
    padding: 8px 12px;
  }
}

/* Global styles for sidebar */
:global(.layout-wrapper) {
  min-height: 150vh !important;
}

:global(.sidebar-container) {
  min-height: 150vh !important;
}

:global(.dss-layout .sidebar) {
  min-height: 150vh !important;
}
</style>