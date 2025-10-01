<template>
  <div class="about-page">
    <section class="stripe white">
      <div class="container">
        <div class="content-header">
          <h2 class="section-title">Đơn hàng của bạn</h2>
          <p class="section-subtitle">Xem và quản lý các đơn hàng đã đặt</p>
        </div>

        <!-- Tabs -->
        <div class="tabs-container">
          <div class="tabs">
            <button 
              v-for="tab in tabs" 
              :key="tab.status" 
              @click="activeTab = tab.status"
              :class="['tab-button', { active: activeTab === tab.status }]"
            >
              {{ tab.name }}
              <span v-if="getOrderCountByStatus(tab.status) > 0" class="tab-badge">
                {{ getOrderCountByStatus(tab.status) }}
              </span>
            </button>
          </div>
        </div>

              <div v-if="loading" class="loading-state">
          <div class="loading-text">Đang tải...</div>
        </div>
        
        <div v-else class="content-body">
          <div v-if="error" class="error-message">{{ error }}</div>
          
          <div v-if="filteredOrders.length" class="orders-table-wrapper">
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
                <tr v-for="order in filteredOrders" :key="order.id" class="order-row">
                  <td>{{ order.service_details?.name }}</td>
                  <td>{{ formatArea(order.area_m2) }}</td>
                  <td>{{ formatDateTime(order.preferred_start_time) }}</td>
                  <td>{{ formatDateTime(order.preferred_end_time) }}</td>
                  <td>{{ order.cost_confirm ? formatPrice(order.cost_confirm) : 'Chưa xác định' }}</td>
                  <td><span :class="['status-badge', getStatusClass(order.status)]">{{ getStatusText(order.status) }}</span></td>
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
          
          <!-- Phần Feedback/Admin Log dưới bảng -->
          <div v-if="(activeTab === 'completed' || activeTab === 'reject') && filteredOrders.length > 0" class="feedback-admin-section">
            <h3 class="section-title">
              {{ activeTab === 'completed' ? '💬 Phản hồi từ khách hàng' : '❌ Lý do từ chối' }}
            </h3>
            
            <div class="orders-feedback-list">
              <div v-for="order in filteredOrders" :key="order.id" class="order-feedback-item">
                <div class="order-summary">
                  <span class="order-service">{{ order.service_details?.name }}</span>
                  <span class="order-date">{{ formatDateTime(order.preferred_start_time) }}</span>
                </div>
                
                <!-- Customer Feedback cho completed -->
                <div v-if="activeTab === 'completed'" class="feedback-content">
                  <div v-if="order.customer_feedback" class="existing-feedback">
                    <div class="feedback-label">Phản hồi của bạn:</div>
                    <div class="feedback-text">{{ order.customer_feedback }}</div>
                  </div>
                  <div v-else class="feedback-input-section">
                    <div class="feedback-label">Để lại phản hồi về dịch vụ:</div>
                    <textarea 
                      v-model="feedbackInputs[order.id]" 
                      placeholder="Chia sẻ trải nghiệm của bạn về dịch vụ này..."
                      class="feedback-textarea"
                      rows="3"
                    ></textarea>
                    <button 
                      @click="submitFeedback(order.id)" 
                      class="submit-feedback-btn"
                      :disabled="!feedbackInputs[order.id]?.trim()"
                    >
                      📝 Gửi phản hồi
                    </button>
                  </div>
                </div>
                
                <!-- Admin Log cho reject -->
                <div v-else-if="activeTab === 'reject'" class="admin-log-content">
                  <div v-if="order.admin_log" class="admin-log">
                    <div class="admin-log-label">Lý do từ chối:</div>
                    <div class="admin-log-text">{{ order.admin_log }}</div>
                  </div>
                  <div v-else class="no-admin-log">
                    <em>Chưa có lý do từ chối được cung cấp</em>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div v-else class="empty-state">
            <p>{{ getEmptyMessage() }}</p>
            <RouterLink to="/dss/orders/create" class="featured-cta">Đặt dịch vụ ngay</RouterLink>
          </div>
        </div>
      </div>
    </section>

    <!-- Modal Hóa đơn -->
    <div v-if="showInvoiceModal && selectedInvoice" class="modal-overlay" @click="closeInvoiceModal">
      <div class="modal-content invoice-modal" @click.stop>
        <div class="modal-header">
          <h2>🧾 Hóa đơn dịch vụ</h2>
          <button class="close-btn" @click="closeInvoiceModal">×</button>
        </div>
        
        <div class="modal-body">
          <div class="invoice-header">
            <div class="invoice-title">HÓA ĐƠN DỊCH VỤ</div>
            <div class="invoice-number">Số: {{ selectedInvoice.invoiceNumber }}</div>
            <div class="invoice-date">
              <div>Ngày xuất: {{ selectedInvoice.issueDate }}</div>
              <div>Hạn thanh toán: {{ selectedInvoice.dueDate }}</div>
            </div>
          </div>

          <div class="invoice-section">
            <h4>Chi tiết dịch vụ</h4>
            <div class="service-details">
              <div class="info-row">
                <span>Dịch vụ:</span>
                <span>{{ selectedInvoice.orderInfo.serviceName }}</span>
              </div>
              <div class="info-row">
                <span>Diện tích:</span>
                <span>{{ selectedInvoice.orderInfo.area }} m²</span>
              </div>
              <div class="info-row">
                <span>Thời gian bắt đầu:</span>
                <span>{{ formatDateTime(selectedInvoice.orderInfo.startTime) }}</span>
              </div>
              <div class="info-row">
                <span>Thời gian kết thúc:</span>
                <span>{{ formatDateTime(selectedInvoice.orderInfo.endTime) }}</span>
              </div>
              <div class="info-row">
                <span>Phương thức thanh toán:</span>
                <span>{{ selectedInvoice.orderInfo.paymentMethod }}</span>
              </div>
              <div v-if="selectedInvoice.orderInfo.note !== 'Không có'" class="info-row">
                <span>Ghi chú:</span>
                <span>{{ selectedInvoice.orderInfo.note }}</span>
              </div>
            </div>
          </div>

          <div class="invoice-section">
            <h4>Thanh toán</h4>
            <div class="pricing-details">
              <div class="info-row">
                <span>Tạm tính:</span>
                <span>{{ selectedInvoice.pricing.subtotal.toLocaleString('vi-VN') }} VNĐ</span>
              </div>
              <div class="info-row">
                <span>VAT (10%):</span>
                <span>{{ selectedInvoice.pricing.tax.toLocaleString('vi-VN') }} VNĐ</span>
              </div>
              <div class="total-amount">
                <span><strong>Tổng cộng:</strong></span>
                <span class="total-price"><strong>{{ selectedInvoice.pricing.total.toLocaleString('vi-VN') }} VNĐ</strong></span>
              </div>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn-download" @click="downloadInvoice">📄 Tải xuống PDF</button>
          <button class="btn-close" @click="closeInvoiceModal">Đóng</button>
        </div>
      </div>
    </div>
    
    <!-- Toast Notification -->
    <div v-if="showToast" :class="['toast-notification', toastType]">
      {{ toastMessage }}
    </div>
    
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import CustomerOrderService from '@/services/dss/users/customer'
import '@/assets/css/customer.css'

const orders = ref([])
const loading = ref(false)
const error = ref('')
const activeTab = ref('pending')

// Modal hóa đơn
const showInvoiceModal = ref(false)
const selectedInvoice = ref(null)

// Feedback inputs cho completed orders
const feedbackInputs = ref({})

// Toast notification
const showToast = ref(false)
const toastMessage = ref('')
const toastType = ref('success') // 'success' hoặc 'error'

// Tabs configuration
const tabs = [
  { status: 'pending', name: 'Chờ xác nhận' },
  { status: 'confirm', name: 'Đã xác nhận' },
  { status: 'process', name: 'Đang thực hiện' },
  { status: 'completed', name: 'Hoàn thành' },
  { status: 'reject', name: 'Bị từ chối' }
]

// Computed property to filter orders by active tab
const filteredOrders = computed(() => {
  return orders.value.filter(order => order.status === activeTab.value)
})

// Get order count by status
const getOrderCountByStatus = (status) => {
  return orders.value.filter(order => order.status === status).length
}

// Get status display text
const getStatusText = (status) => {
  const statusMap = {
    'pending': 'Chờ xác nhận',
    'confirm': 'Đã xác nhận',
    'reject': 'Bị từ chối',
    'process': 'Đang thực hiện',
    'completed': 'Hoàn thành'
  }
  return statusMap[status] || status
}

// Get status CSS class
const getStatusClass = (status) => {
  const classMap = {
    'pending': 'status-pending',
    'confirm': 'status-confirm',
    'reject': 'status-reject',
    'process': 'status-process',
    'completed': 'status-completed'
  }
  return classMap[status] || ''
}

// Get empty message based on active tab
const getEmptyMessage = () => {
  const messageMap = {
    'pending': 'Không có đơn hàng nào đang chờ xác nhận.',
    'confirm': 'Không có đơn hàng nào đã được xác nhận.',
    'reject': 'Không có đơn hàng nào bị từ chối.',
    'process': 'Không có đơn hàng nào đang thực hiện.',
    'completed': 'Không có đơn hàng nào đã hoàn thành.'
  }
  return messageMap[activeTab.value] || 'Không có đơn hàng nào.'
}

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
    console.log('Type of response:', typeof res)
    
    // Xử lý nhiều format response khác nhau
    let ordersData = []
    if (Array.isArray(res)) {
      ordersData = res
    } else if (res.results && Array.isArray(res.results)) {
      ordersData = res.results
    } else if (res.data && Array.isArray(res.data)) {
      ordersData = res.data
    } else {
      console.warn('Unexpected response format:', res)
      ordersData = []
    }
    
    orders.value = ordersData
    console.log('Orders after processing:', orders.value)
    console.log('Orders length:', orders.value.length)
  } catch (e) {
    console.error('Error fetching orders:', e)
    error.value = 'Không thể tải danh sách đơn hàng: ' + e.message
  } finally {
    loading.value = false
  }
}

// Phương thức gửi feedback cho completed orders
const submitFeedback = async (orderId) => {
  const feedback = feedbackInputs.value[orderId]?.trim()
  if (!feedback) return
  
  try {
    // Gọi API để cập nhật feedback
    await CustomerOrderService.updateOrderFeedback(orderId, feedback)
    
    // Cập nhật local data
    const order = orders.value.find(o => o.id === orderId)
    if (order) {
      order.customer_feedback = feedback
    }
    
    // Clear input
    feedbackInputs.value[orderId] = ''
    
    // Hiển thị thông báo thành công
    showToastMessage('Phản hồi đã được gửi thành công!', 'success')
    
  } catch (e) {
    console.error('Error submitting feedback:', e)
    showToastMessage('Có lỗi xảy ra khi gửi phản hồi. Vui lòng thử lại.', 'error')
  }
}

// Hiển thị toast notification
const showToastMessage = (message, type = 'success') => {
  toastMessage.value = message
  toastType.value = type
  showToast.value = true
  
  // Tự động ẩn sau 3 giây
  setTimeout(() => {
    showToast.value = false
  }, 3000)
}

// Hàm xem hóa đơn
const viewInvoice = (order) => {
  const currentDate = new Date(order.created_at || new Date())
  // Sử dụng ID của đơn hàng làm invoiceNumber trực tiếp
  const invoiceNumber = order.id
  
  selectedInvoice.value = {
    invoiceNumber,
    orderInfo: {
      serviceName: order.service_details?.name || 'N/A',
      area: formatArea(order.area_m2),
      startTime: order.preferred_start_time,
      endTime: order.preferred_end_time,
      note: order.note || 'Không có',
      paymentMethod: order.payment_method === 'cash' ? 'Tiền mặt' : 'Chuyển khoản'
    },
    pricing: {
      subtotal: parseInt(order.cost_confirm) || 0,
      tax: Math.round((parseInt(order.cost_confirm) || 0) * 0.1),
      total: Math.round((parseInt(order.cost_confirm) || 0) * 1.1)
    },
    issueDate: currentDate.toLocaleDateString('vi-VN'),
    dueDate: new Date(currentDate.getTime() + 7 * 24 * 60 * 60 * 1000).toLocaleDateString('vi-VN')
  }
  
  showInvoiceModal.value = true
}

const closeInvoiceModal = () => {
  showInvoiceModal.value = false
  selectedInvoice.value = null
}

const downloadInvoice = () => {
  if (!selectedInvoice.value) return
  
  const invoice = selectedInvoice.value
  const htmlContent = `
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>Hóa đơn ${invoice.invoiceNumber}</title>
      <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { text-align: center; margin-bottom: 30px; background: #f8f9fa; padding: 20px; }
        .title { font-size: 24px; font-weight: bold; color: #333; }
        .invoice-number { font-size: 18px; margin: 10px 0; }
        .section { margin: 20px 0; padding: 15px; border: 1px solid #ddd; }
        .section h3 { margin: 0 0 15px 0; color: #555; }
        .row { display: flex; justify-content: space-between; margin: 8px 0; }
        .total { background: #e3f2fd; padding: 15px; font-weight: bold; font-size: 18px; }
      </style>
    </head>
    <body>
      <div class="header">
        <div class="title">HÓA ĐƠN DỊCH VỤ</div>
        <div class="invoice-number">Số: ${invoice.invoiceNumber}</div>
        <div>Ngày xuất: ${invoice.issueDate} | Hạn thanh toán: ${invoice.dueDate}</div>
      </div>
      
      <div class="section">
        <h3>Chi tiết dịch vụ</h3>
        <div class="row"><span>Dịch vụ:</span><span>${invoice.orderInfo.serviceName}</span></div>
        <div class="row"><span>Diện tích:</span><span>${invoice.orderInfo.area} m²</span></div>
        <div class="row"><span>Thời gian bắt đầu:</span><span>${formatDateTime(invoice.orderInfo.startTime)}</span></div>
        <div class="row"><span>Thời gian kết thúc:</span><span>${formatDateTime(invoice.orderInfo.endTime)}</span></div>
        <div class="row"><span>Phương thức thanh toán:</span><span>${invoice.orderInfo.paymentMethod}</span></div>
        ${invoice.orderInfo.note !== 'Không có' ? `<div class="row"><span>Ghi chú:</span><span>${invoice.orderInfo.note}</span></div>` : ''}
      </div>
      
      <div class="section">
        <h3>Thanh toán</h3>
        <div class="row"><span>Tạm tính:</span><span>${invoice.pricing.subtotal.toLocaleString('vi-VN')} VNĐ</span></div>
        <div class="row"><span>VAT (10%):</span><span>${invoice.pricing.tax.toLocaleString('vi-VN')} VNĐ</span></div>
        <div class="total"><span>Tổng cộng:</span><span>${invoice.pricing.total.toLocaleString('vi-VN')} VNĐ</span></div>
      </div>
      
      <div style="text-align: center; margin-top: 30px; color: #666;">
        Cảm ơn bạn đã sử dụng dịch vụ!
      </div>
    </body>
    </html>
  `
  
  const printWindow = window.open('', '_blank')
  if (printWindow) {
    printWindow.document.write(htmlContent)
    printWindow.document.close()
    printWindow.focus()
    printWindow.print()
    printWindow.onafterprint = () => printWindow.close()
  }
}

onMounted(fetchOrders)
</script>