<template>
  <div class="enhanced-dashboard-page">
    <div class="page-header">
      <h1>
        <el-icon><DataBoard /></el-icon>
        Dashboard Nâng Cao
      </h1>
      <div class="header-actions">
        <el-button
          :type="autoRefresh ? 'success' : 'info'"
          :icon="autoRefresh ? Timer : VideoPause"
          @click="toggleAutoRefresh"
        >
          {{ autoRefresh ? 'Auto-refresh ON' : 'Auto-refresh OFF' }}
        </el-button>
        <el-button type="primary" :icon="Refresh" @click="refreshAll" :loading="refreshing">
          Làm mới
        </el-button>
      </div>
    </div>

    <!-- Module 1: Priority Orders -->
    <PriorityOrdersTable :auto-refresh="autoRefresh" ref="priorityOrdersRef" />

    <!-- Module 2: Employee KPI -->
    <EmployeeKPITable ref="employeeKPIRef" />

    <!-- Module 3: Revenue Cost Profit -->
    <RevenueCostProfitChart ref="revenueChartRef" />

    <!-- Module 4: Service Type Pie (new) -->
    <ServiceTypePieChart ref="serviceTypeRef" />

    <!-- Module 5: Service Status Pie -->
    <ServiceStatusPieChart ref="serviceStatusRef" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { DataBoard, Refresh, Timer, VideoPause } from '@element-plus/icons-vue'
import PriorityOrdersTable from '~/components/enhanced-dashboard/PriorityOrdersTable.vue'
import EmployeeKPITable from '~/components/enhanced-dashboard/EmployeeKPITable.vue'
import RevenueCostProfitChart from '~/components/enhanced-dashboard/RevenueCostProfitChart.vue'
import ServiceTypePieChart from '~/components/enhanced-dashboard/ServiceTypePieChart.vue'
import ServiceStatusPieChart from '~/components/enhanced-dashboard/ServiceStatusPieChart.vue'
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

// Set page meta
definePageMeta({
  layout: 'business',
  middleware: 'auth'
})
</script>

<style scoped>
.enhanced-dashboard-page {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.page-header h1 {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.header-actions {
  display: flex;
  gap: 10px;
}
</style>
