<template>
  <el-card class="priority-orders-card">
    <template #header>
      <div class="card-header">
        <h3>
          <el-icon><Clock /></el-icon>
          Đơn Hàng Ưu Tiên
        </h3>
        <el-tag :type="autoRefresh ? 'success' : 'info'" size="small">
          {{ autoRefresh ? 'Auto-refresh: 30s' : 'Paused' }}
        </el-tag>
      </div>
    </template>

    <el-table
      v-loading="loading"
      :data="orders"
      stripe
      style="width: 100%"
      :row-class-name="getRowClass"
    >
      <el-table-column label="Mã đơn" prop="code" width="120" />
      
      <el-table-column label="Khách hàng" prop="customer_name" width="150" />
      
      <el-table-column label="Dịch vụ" prop="service_type" width="150" />
      
      <el-table-column label="Giờ còn lại" width="120">
        <template #default="{ row }">
          <el-tag :type="getTimeBucketType(row.time_bucket)" size="small">
            {{ row.hours_left }}h ({{ row.time_bucket }})
          </el-tag>
        </template>
      </el-table-column>
      
      <el-table-column label="Giá trị" width="130">
        <template #default="{ row }">
          {{ formatCurrency(row.price) }}
        </template>
      </el-table-column>
      
      <el-table-column label="Điểm ưu tiên" width="140">
        <template #default="{ row }">
          <div class="priority-score">
            <el-progress
              :percentage="row.priority_score * 100"
              :color="getPriorityColor(row.priority_score)"
              :stroke-width="8"
            />
            <span class="score-text">{{ row.priority_score }}</span>
          </div>
        </template>
      </el-table-column>
      
      <el-table-column label="Hệ số" width="150">
        <template #default="{ row }">
          <div class="factors">
            <span class="factor">⏰ {{ row.time_factor }}</span>
            <span class="factor">💰 {{ row.price_factor }}</span>
          </div>
        </template>
      </el-table-column>
      
      <el-table-column label="Trạng thái" width="120">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)" size="small">
            {{ getStatusText(row.status) }}
          </el-tag>
        </template>
      </el-table-column>

      <el-table-column label="Thao tác" width="180">
        <template #default="{ row }">
            <el-button
            type="primary"
            size="small"
            @click="goToDetail(row.order_id)"
            >
            Xem chi tiết
            </el-button>
            <!-- <el-button
            type="success"
            size="small"
            @click="goToAssign(row.order_id)"
            style="margin-left: 8px"
            >
            Phân công
            </el-button> -->
        </template>
        </el-table-column>
    </el-table>

    <!-- Pagination -->
    <div class="pagination-container">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[5, 10]"
        :total="totalRecords"
        layout="total, sizes, prev, pager, next"
        @current-change="handlePageChange"
        @size-change="handleSizeChange"
      />
    </div>
  </el-card>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { Clock } from '@element-plus/icons-vue'
import enhancedDashboardService from '~/services/dss/enhancedDashboardService'
import { useRouter } from 'vue-router'

// Props
const props = defineProps({
  autoRefresh: {
    type: Boolean,
    default: true
  }
})

// Data
const loading = ref(false)
const orders = ref([])
const currentPage = ref(1)
const pageSize = ref(5)
const totalRecords = ref(0)
const totalPages = ref(0)
let refreshInterval = null
const router = useRouter()

const goToDetail = (orderId) => {
  router.push(`/dss/orders/${orderId}`)
}

// const goToAssign = (orderId) => {
//   router.push(`/dss/orders/${orderId}?tab=assignment`)
// }
// Methods
const fetchOrders = async () => {
  loading.value = true
  try {
    const response = await enhancedDashboardService.getPriorityOrders({
      page: currentPage.value,
      page_size: pageSize.value
    })
    
    if (response.success) {
      orders.value = response.data
      totalRecords.value = response.pagination.total
      totalPages.value = response.pagination.total_pages
      console.log('✅ Priority orders loaded:', orders.value.length)
    }
  } catch (error) {
    console.error('❌ Error loading priority orders:', error)
  } finally {
    loading.value = false
  }
}

const handlePageChange = (page) => {
  currentPage.value = page
  fetchOrders()
}

const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
  fetchOrders()
}

const getRowClass = ({ row }) => {
  if (row.time_bucket === '1-2h') return 'urgent-row'
  if (row.time_bucket === '2-3h') return 'high-row'
  return ''
}

const getTimeBucketType = (bucket) => {
  const types = {
    '1-2h': 'danger',
    '2-3h': 'warning',
    '3-4h': 'warning',
    '4-5h': 'info',
    '5-8h': 'info',
    '8-12h': '',
    '12-24h': '',
    '24h+': ''
  }
  return types[bucket] || ''
}

const getPriorityColor = (score) => {
  if (score >= 0.8) return '#f56c6c'
  if (score >= 0.6) return '#e6a23c'
  if (score >= 0.4) return '#409eff'
  return '#909399'
}

const getStatusType = (status) => {
  const types = {
    pending: 'warning',
    in_progress: 'primary',
    completed: 'success'
  }
  return types[status] || ''
}

const getStatusText = (status) => {
  const texts = {
    pending: 'Chờ xử lý',
    in_progress: 'Đang làm',
    completed: 'Hoàn thành'
  }
  return texts[status] || status
}

const formatCurrency = (value) => {
  return new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND'
  }).format(value)
}

// Auto-refresh
const startAutoRefresh = () => {
  if (props.autoRefresh) {
    refreshInterval = setInterval(() => {
      fetchOrders()
    }, 30000) // 30 seconds
  }
}

const stopAutoRefresh = () => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
    refreshInterval = null
  }
}

// Lifecycle
onMounted(() => {
  fetchOrders()
  startAutoRefresh()
})

onUnmounted(() => {
  stopAutoRefresh()
})
</script>

<style scoped>
.priority-orders-card {
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

.priority-score {
  display: flex;
  align-items: center;
  gap: 8px;
}

.score-text {
  font-weight: 600;
  font-size: 14px;
}

.factors {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.factor {
  font-size: 12px;
  font-weight: 500;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

:deep(.urgent-row) {
  background-color: #fef0f0 !important;
}

:deep(.high-row) {
  background-color: #fdf6ec !important;
}
</style>
