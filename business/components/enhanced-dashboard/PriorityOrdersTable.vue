<template>
  <el-card class="priority-orders-card">
    <template #header>
      <div class="card-header">
        <div class="header-left">
          <el-icon class="header-icon"><Clock /></el-icon>
          <span class="header-title">Đơn Hàng Ưu Tiên</span>
        </div>

        <el-tag :type="autoRefresh ? 'success' : 'info'" effect="dark" size="small">
          {{ autoRefresh ? 'Auto-refresh: 30s' : 'Tạm dừng' }}
        </el-tag>
      </div>
    </template>

    <el-table
      v-loading="loading"
      :data="orders"
      stripe
      class="custom-table"
      :row-class-name="getRowClass"
    >
      <el-table-column label="Mã đơn" prop="code" width="120" />

      <el-table-column label="Khách hàng" prop="customer_name" min-width="150" />

      <el-table-column label="Dịch vụ" prop="service_type" min-width="150" />

      <el-table-column label="Giờ còn lại" width="150">
        <template #default="{ row }">
          <el-tag class="time-badge" :type="getTimeBucketType(row.time_bucket)" effect="dark">
            {{ row.hours_left }}h • {{ row.time_bucket }}
          </el-tag>
        </template>
      </el-table-column>

      <el-table-column label="Giá trị" width="150">
        <template #default="{ row }">
          <span class="price">{{ formatCurrency(row.price) }}</span>
        </template>
      </el-table-column>

      <el-table-column label="Điểm ưu tiên" width="180">
        <template #default="{ row }">
          <div class="priority-score">
            <el-progress
              :percentage="row.priority_score * 100"
              :stroke-width="10"
              :color="getPriorityColor(row.priority_score)"
              class="progress-bar"
            />
            <span class="score-text">{{ row.priority_score }}</span>
          </div>
        </template>
      </el-table-column>

      <el-table-column label="Hệ số" width="150">
        <template #default="{ row }">
          <div class="factors">
            <span class="factor-item">⏰ {{ row.time_factor }}</span>
            <span class="factor-item">💰 {{ row.price_factor }}</span>
          </div>
        </template>
      </el-table-column>

      <el-table-column label="Trạng thái" width="130">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)" effect="dark" size="small">
            {{ getStatusText(row.status) }}
          </el-tag>
        </template>
      </el-table-column>

      <el-table-column label="Thao tác" width="160">
        <template #default="{ row }">
          <el-button
            type="primary"
            size="small"
            round
            plain
            @click="goToDetail(row.order_id)"
          >
            Xem chi tiết
          </el-button>
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
  margin-bottom: 22px;
  border-radius: 14px;
  overflow: hidden;
}

/* --- CARD HEADER --- */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 4px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-icon {
  font-size: 20px;
  color: #ffffff;
}

.header-title {
  font-size: 19px;
  font-weight: 700;
  color: #ffffff;
}

/* --- TABLE --- */
.custom-table {
  border-radius: 10px;
}

.price {
  font-weight: 600;
  color: #333;
}

.time-badge {
  font-weight: 600;
}

/* --- PRIORITY SCORE --- */
.priority-score {
  display: flex;
  align-items: center;
  gap: 10px;
}

.score-text {
  font-weight: 700;
  font-size: 14px;
  color: #444;
}

.progress-bar {
  width: 110px;
}

/* --- FACTORS --- */
.factors {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.factor-item {
  font-size: 12.5px;
  font-weight: 500;
  background: #f4f6f9;
  padding: 3px 6px;
  border-radius: 6px;
}

/* --- ROW COLORS --- */
:deep(.urgent-row) {
  background: #fff1f0 !important;
}

:deep(.high-row) {
  background: #fff7e6 !important;
}

/* --- PAGINATION --- */
.pagination-container {
  margin-top: 18px;
  display: flex;
  justify-content: center;
}

</style>
