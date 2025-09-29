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
              <div class="info-row" v-if="selectedInvoice.orderInfo.note !== 'Không có'">
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
              <div class="info-row total-amount">
                <span><strong>Tổng cộng:</strong></span>
                <span class="total-price"><strong>{{ selectedInvoice.pricing.total.toLocaleString('vi-VN') }} VNĐ</strong></span>
              </div>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn-download" @click="downloadInvoice">� Tải xuống PDF</button>
          <button class="btn-close" @click="closeInvoiceModal">Đóng</button>
        </div>
      </div>
    </div>
    
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import CustomerOrderService from '@/services/dss/users/customer'

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

// Hàm xem hóa đơn
const viewInvoice = (order) => {
  const currentDate = new Date(order.created_at || new Date())
  const invoiceNumber = `HD${currentDate.getFullYear()}${String(currentDate.getMonth() + 1).padStart(2, '0')}${String(currentDate.getDate()).padStart(2, '0')}${String(order.id).padStart(4, '0')}`
  
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

<style scoped>
/* Styles đã được chuyển sang customer.css */
</style>