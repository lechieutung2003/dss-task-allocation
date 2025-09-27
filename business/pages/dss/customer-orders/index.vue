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
                <th>Hành động</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="order in orders" :key="order.id" class="order-row">
                <td>{{ order.service_details?.name }}</td>
                <td>{{ formatArea(order.area_m2) }}</td>
                <td>{{ formatDateTime(order.preferred_start_time) }}</td>
                <td>{{ formatDateTime(order.preferred_end_time) }}</td>
                <td>{{ order.cost_confirm ? formatPrice(order.cost_confirm) : 'Chưa xác định' }}</td>
                <td><span class="status-badge">{{ order.status }}</span></td>
                <td>{{ order.note || 'Không có' }}</td>
                <td>
                  <button @click="viewInvoice(order)" class="action-btn view-invoice" title="Xem hóa đơn">
                    🧾 Hóa đơn
                  </button>
                </td>
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

// Modal hóa đơn
const showInvoiceModal = ref(false)
const selectedInvoice = ref(null)

const formatDateTime = (datetime) => {
  return datetime ? new Date(datetime).toLocaleString() : ''
}

const formatPrice = (price) => {
  return new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND'
  }).format(price)
}

// Hàm format diện tích để hiển thị số nguyên khi không có phần thập phân
const formatArea = (area) => {
  if (!area && area !== 0) return ''
  const num = parseFloat(area)
  return num % 1 === 0 ? num.toString() : num.toString()
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

/* Action button styles */
.action-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.view-invoice {
  background: #2563eb;
  color: white;
}

.view-invoice:hover {
  background: #1d4ed8;
}

/* Modal styles - Chủ đạo đen trắng theo form design */
.modal-overlay {
  display: flex;
  justify-content: center;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  padding: 40px 20px;
  align-items: center;
}

.modal-content {
  width: 100%;
  max-width: 900px;
  background-color: #fff;
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
}

.invoice-modal {
  max-width: 900px;
}

.modal-header {
  text-align: center;
  margin-bottom: 30px;
  position: relative;
}

.modal-header h2 {
  font-size: 28px;
  font-weight: 700;
  color: #151717;
  margin-bottom: 5px;
}

.close-btn {
  position: absolute;
  top: -10px;
  right: -10px;
  background: #fff;
  border: 1.5px solid #ecedec;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  font-size: 20px;
  cursor: pointer;
  color: #6b7280;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease-in-out;
}

.close-btn:hover {
  border-color: #2d79f3;
  color: #151717;
  background: #f8f9fa;
}

.modal-body {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.invoice-header {
  text-align: center;
  background: #151717;
  color: white;
  border-radius: 20px;
  padding: 30px;
  margin-bottom: 20px;
}

.invoice-title {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 5px;
}

.invoice-number {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 400;
  margin-bottom: 10px;
}

.invoice-date {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
}

.invoice-section {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.invoice-section h4 {
  font-weight: 600;
  margin-bottom: 15px;
  font-size: 18px;
  color: #151717;
  text-align: center;
}

.service-details,
.pricing-details {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.info-row {
  border: 1.5px solid #ecedec;
  border-radius: 10px;
  height: 50px;
  display: flex;
  align-items: center;
  padding-left: 10px;
  transition: 0.2s ease-in-out;
  background: #fff;
}

.info-row:hover {
  border-color: #2d79f3;
}

.info-row span:first-child {
  font-weight: 600;
  margin-bottom: 2px;
  color: #6b7280;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  display: block;
}

.info-row span:last-child {
  color: #151717;
  font-weight: 500;
  font-size: 15px;
  display: block;
}

.info-row {
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
}

.total-amount {
  grid-column: 1 / -1;
  background-color: #151717;
  border: none;
  color: white;
  height: 60px;
  font-size: 16px;
  font-weight: 600;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  border-radius: 10px;
  margin-top: 10px;
}

.total-amount span:first-child {
  color: white !important;
  font-size: 16px;
  text-transform: none;
  letter-spacing: normal;
}

.total-price {
  color: white !important;
  font-size: 20px;
  font-weight: 700;
}

.modal-footer {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #ecedec;
}

.btn-download {
  background-color: #151717;
  border: none;
  color: white;
  font-size: 15px;
  font-weight: 500;
  border-radius: 10px;
  height: 50px;
  padding: 0 30px;
  cursor: pointer;
  transition: background 0.2s ease-in-out;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-download:hover {
  background-color: #252727;
}

.btn-close {
  background: #fff;
  border: 1.5px solid #ecedec;
  color: #6b7280;
  font-size: 15px;
  font-weight: 500;
  border-radius: 10px;
  height: 50px;
  padding: 0 30px;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}

.btn-close:hover {
  border-color: #2d79f3;
  color: #151717;
}

@media (max-width: 768px) {
  .service-details,
  .pricing-details {
    grid-template-columns: 1fr;
  }
  
  .modal-footer {
    flex-direction: column;
    gap: 10px;
  }
  
  .btn-download, .btn-close {
    width: 100%;
  }
  
  .close-btn {
    top: -5px;
    right: -5px;
    width: 35px;
    height: 35px;
    font-size: 18px;
  }
}
</style>