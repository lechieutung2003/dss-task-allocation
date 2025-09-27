<template>
  <div class="orders-container">
    <div class="content-wrapper">
      <div class="content-header">
        <h2 class="form-title">Đơn hàng của bạn</h2>
        <p class="form-subtitle">Xem và quản lý các đơn hàng đã đặt</p>
      </div>

      <div v-if="loading" class="loading-state">
        <div class="loading-text">Đang tải...</div>
      </div>
      
      <div v-else class="content-body">
        <div v-if="error" class="error-message">{{ error }}</div>
        
        <div v-if="orders.length" class="orders-table-wrapper">
          <table class="orders-table">
            <thead>
              <tr>
                <th>Dịch vụ</th>
                <th>Diện tích (m2)</th>
                <th>Thời gian bắt đầu</th>
                <th>Thời gian kết thúc</th>
                <th>Giá ước tính</th>
                <th>Trạng thái</th>
                <th>Ghi chú</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="order in orders" :key="order.id" class="order-row">
                <td>{{ order.service_details?.name }}</td>
                <td>{{ order.area_m2 }}</td>
                <td>{{ formatDateTime(order.preferred_start_time) }}</td>
                <td>{{ formatDateTime(order.preferred_end_time) }}</td>
                <td>{{ order.cost_confirm ? formatPrice(order.cost_confirm) : 'Chưa xác định' }}</td>
                <td><span class="status-badge">{{ order.status }}</span></td>
                <td>{{ order.note || 'Không có' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div v-else class="empty-state">
          <p>Không có đơn hàng nào.</p>
          <RouterLink to="/dss/orders/create" class="button-submit">Đặt dịch vụ ngay</RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import CustomerOrderService from '@/services/dss/customerOrderService'

const orders = ref([])
const loading = ref(false)
const error = ref('')

const formatDateTime = (datetime) => {
  return datetime ? new Date(datetime).toLocaleString() : ''
}

const formatPrice = (price) => {
  return new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND'
  }).format(price)
}

const fetchOrders = async () => {
  loading.value = true
  error.value = ''
  try {
    const res = await CustomerOrderService.getOrders()
    console.log('API Response:', res)
    orders.value = Array.isArray(res) ? res : (res.results || [])
  } catch (e) {
    console.error('Error:', e)
    error.value = 'Không thể tải danh sách đơn hàng'
  } finally {
    loading.value = false
  }
}

onMounted(fetchOrders)
</script>

<style scoped>
.orders-container {
  display: flex;
  justify-content: center;
  padding: 40px 20px;
}

.content-wrapper {
  width: 100%;
  max-width: 1200px;
  background-color: #fff;
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}

.content-header {
  text-align: center;
  margin-bottom: 30px;
}

.form-title {
  font-size: 28px;
  font-weight: 700;
  color: #151717;
  margin-bottom: 5px;
}

.form-subtitle {
  font-size: 16px;
  color: #6b7280;
  font-weight: 400;
  margin: 0;
}

.loading-state {
  display: flex;
  justify-content: center;
  padding: 40px;
}

.loading-text {
  color: #6b7280;
  font-size: 16px;
}

.error-message {
  color: #ef4444;
  text-align: center;
  padding: 15px;
  margin-bottom: 20px;
  background-color: #fef2f2;
  border-radius: 10px;
}

.orders-table-wrapper {
  overflow-x: auto;
}

.orders-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  margin-top: 16px;
}

.orders-table th {
  background-color: #f9fafb;
  font-weight: 600;
  padding: 15px;
  text-align: left;
  border-bottom: 2px solid #ecedec;
}

.orders-table td {
  padding: 15px;
  border-bottom: 1px solid #ecedec;
}

.order-row {
  transition: background-color 0.2s;
}

.order-row:hover {
  background-color: #f9fafb;
}

.status-badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
  background-color: #e5e7eb;
  color: #374151;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
}

.empty-state p {
  color: #6b7280;
  margin-bottom: 20px;
}

.button-submit {
  background-color: #151717;
  border: none;
  color: white;
  font-size: 15px;
  font-weight: 500;
  border-radius: 10px;
  padding: 12px 24px;
  cursor: pointer;
  transition: background 0.2s ease-in-out;
  text-decoration: none;
  display: inline-block;
}

.button-submit:hover {
  background-color: #252727;
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 20px;
  }
  
  .orders-table th,
  .orders-table td {
    padding: 10px;
  }
  
  .form-title {
    font-size: 24px;
  }
}
</style>