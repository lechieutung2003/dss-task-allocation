<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue';
import { useRouter } from 'vue-router';
import CreateOrderService from '@/services/dss/users/customer';
import { useOauthStore } from '@/stores/oauth';
import serviceTypesApi from '@/services/dss/serviceTypes';
// Import hình ảnh QR
import qrImage from '@/assets/images/qr.jpg';

const store = useOauthStore();
const router = useRouter();

const order = ref({
  customer: store.user?.id || null,
  service_type: null,
  area_m2: null,
  requested_hours: null,
  preferred_start_time: '',
  preferred_end_time: '',
  estimated_hours: null,
  status: 'pending',
  note: '',
  cost_confirm: '',
  payment_method: 'cash' as 'cash' | 'transfer'
});

const productivity = ref<number | null>(null);
const estimatedPrice = ref<number | null>(null);
const priceExplanation = ref<string>(''); // 🆕 label mô tả cách tính
const minRequiredHours = ref<number | null>(null); // 🆕 thời gian tối thiểu
const isTimeValid = ref<boolean>(true); // 🆕 kiểm tra thời gian hợp lệ
const timeValidationMessage = ref<string>(''); // 🆕 thông báo lỗi thời gian

// 🆕 Modal thanh toán
const showPaymentModal = ref<boolean>(false);
const paymentMethod = ref<'cash' | 'transfer'>('cash');
const isSubmitting = ref<boolean>(false);

// 🆕 Modal hóa đơn
const showInvoiceModal = ref<boolean>(false);
const invoiceData = ref<any>(null);

// 🆕 Thông tin QR code cho chuyển khoản
const qrCodeData = ref<string>('');
const bankInfo = {
  bankName: 'Vietcombank',
  accountNumber: '1020567669',
  accountHolder: 'VO THU THAO',
  qrCode: qrImage // Sử dụng hình ảnh đã import
};

type ServiceType = { id: string; name: string; [key: string]: any };
const serviceTypes = ref<ServiceType[]>([]);

// Computed property để lấy giá dịch vụ được chọn
const selectedServicePrice = computed(() => {
  if (!order.value.service_type) return null;
  
  const service = serviceTypes.value.find(s => s.id === order.value.service_type);
  if (!service) return null;
  
  if (service.price_per_m2) {
    return Number(service.price_per_m2);
  } else if (service.name?.toLowerCase().includes('deep cleaning')) {
    return 3000;
  } else if (service.name?.toLowerCase().includes('regular cleaning')) {
    return 155000;
  }
  
  return null;
});

const fetchServiceTypes = async () => {
  const response = await serviceTypesApi.getAll();
  if (response && response.results) {
    serviceTypes.value = response.results;
  } else if (Array.isArray(response)) {
    serviceTypes.value = response;
  } else {
    serviceTypes.value = [];
  }
  console.log('serviceTypes.value:', serviceTypes.value);
};

const calcProductivity = () => {
  const serviceId = order.value.service_type;
  if (!serviceId) {
    productivity.value = null;
    return;
  }
  const service = serviceTypes.value.find(s => s.id === serviceId);
  if (service) {
    if (service.cleaning_rate_m2_per_h) {
      productivity.value = Number(service.cleaning_rate_m2_per_h);
    } else if (service.name?.toLowerCase().includes('regular cleaning')) {
      productivity.value = 40;
    } else if (service.name?.toLowerCase().includes('deep cleaning')) {
      productivity.value = 35;
    } else {
      productivity.value = null;
    }
  } else {
    productivity.value = null;
  }
};

const calcEstimatedHours = () => {
  const area = order.value.area_m2;
  if (!area || !productivity.value || productivity.value <= 0) {
    order.value.estimated_hours = null;
    minRequiredHours.value = null;
    return;
  }
  order.value.estimated_hours = +(area / productivity.value).toFixed(2);
  // Tính thời gian tối thiểu = 60% thời gian ước tính
  minRequiredHours.value = +(order.value.estimated_hours * 0.6).toFixed(2);
};

//  Hàm kiểm tra thời gian yêu cầu hợp lệ
const validateRequestedTime = () => {
  const requested = order.value.requested_hours;
  const minRequired = minRequiredHours.value;
  const estimated = order.value.estimated_hours;
  
  if (!requested || !minRequired || !estimated) {
    isTimeValid.value = true;
    timeValidationMessage.value = '';
    return;
  }
  
  if (requested < minRequired) {
    isTimeValid.value = false;
    timeValidationMessage.value = `Thời gian yêu cầu tối thiểu là ${formatHourMinute(minRequired)} (60% của ${formatHourMinute(estimated)})`;
  } else {
    isTimeValid.value = true;
    timeValidationMessage.value = '';
  }
};

const calcRequestedHours = () => {
  const start = order.value.preferred_start_time;
  const end = order.value.preferred_end_time;
  if (!start || !end) {
    order.value.requested_hours = null;
    return;
  }
  const startDate = new Date(start);
  const endDate = new Date(end);
  const diffMs = endDate.getTime() - startDate.getTime();
  if (diffMs > 0) {
    order.value.requested_hours = +(diffMs / (1000 * 60 * 60)).toFixed(2);
  } else {
    order.value.requested_hours = null;
  }
};

const calcEstimatedPrice = () => {
  const serviceId = order.value.service_type;
  const area = order.value.area_m2;
  if (!serviceId || !area || area <= 0) {
    estimatedPrice.value = null;
    priceExplanation.value = '';
    return;
  }
  let pricePerM2 = 0;
  const service = serviceTypes.value.find(s => s.id === serviceId);
  if (service) {
    if (service.price_per_m2) {
      pricePerM2 = Number(service.price_per_m2);
    } else if (service.name?.toLowerCase().includes('deep cleaning')) {
      pricePerM2 = 3000;
    } else if (service.name?.toLowerCase().includes('regular cleaning')) {
      pricePerM2 = 155000;
    }
  }

  let price = pricePerM2 > 0 ? pricePerM2 * area : null;
  let explanation = `Giá cơ bản: ${pricePerM2.toLocaleString('vi-VN')} x ${area} m² = ${(price || 0).toLocaleString('vi-VN')} VNĐ`;

  const requested = order.value.requested_hours;
  const estimated = order.value.estimated_hours;
  if (price && requested && estimated && requested < estimated) {
    const diff = estimated - requested;
    let factor = 1;
    if (diff > 0.1 && diff <= 1) factor = 1.2;
    else if (diff > 1 && diff <= 2) factor = 1.3;
    else if (diff > 2) factor = 1.5;

    if (factor > 1) {
      explanation += ` (áp dụng hệ số ${factor} do số giờ yêu cầu < số giờ ước tính)`;
      price = price * factor;
    }
  }

  estimatedPrice.value = price;
  priceExplanation.value = explanation;
};

// Theo dõi thay đổi để tính toán
watch(() => [order.value.service_type], calcProductivity);
watch(() => [order.value.area_m2, productivity.value], calcEstimatedHours);
watch(() => [order.value.preferred_start_time, order.value.preferred_end_time], () => {
  calcRequestedHours();
  validateRequestedTime();
});
watch(() => [order.value.service_type, order.value.area_m2, order.value.requested_hours, order.value.estimated_hours], calcEstimatedPrice);
watch(() => [order.value.requested_hours, minRequiredHours.value], validateRequestedTime);

const openPaymentModal = () => {
  if (!isTimeValid.value) {
    alert('Không thể tạo đơn: ' + timeValidationMessage.value);
    return;
  }
  
  // Sử dụng QR code tĩnh từ assets cho học tập
  const amount = estimatedPrice.value || 0;
  const description = `Thanh toan don hang DSS - ${amount.toLocaleString('vi-VN')} VND`;
  qrCodeData.value = bankInfo.qrCode; // Sử dụng QR tĩnh từ assets
  
  showPaymentModal.value = true;
};

const closePaymentModal = () => {
  showPaymentModal.value = false;
  paymentMethod.value = 'cash';
  isSubmitting.value = false;
};

// 🆕 Hàm tạo hóa đơn
const generateInvoice = (orderResponse: any) => {
  const currentDate = new Date();
  const invoiceNumber = `HD${currentDate.getFullYear()}${String(currentDate.getMonth() + 1).padStart(2, '0')}${String(currentDate.getDate()).padStart(2, '0')}${String(orderResponse.id).padStart(4, '0')}`;
  
  invoiceData.value = {
    invoiceNumber,
    orderInfo: {
      id: orderResponse.id,
      serviceName: serviceTypes.value.find(s => s.id === order.value.service_type)?.name || 'N/A',
      area: order.value.area_m2,
      workingHours: formatHourMinute(order.value.requested_hours),
      startTime: order.value.preferred_start_time,
      endTime: order.value.preferred_end_time,
      note: order.value.note || 'Không có',
      paymentMethod: paymentMethod.value === 'cash' ? 'Tiền mặt' : 'Chuyển khoản'
    },
    customerInfo: {
      name: store.user?.name || 'Khách hàng',
      email: store.user?.email || '',
      phone: store.user?.phone || ''
    },
    pricing: {
      subtotal: estimatedPrice.value || 0,
      tax: Math.round((estimatedPrice.value || 0) * 0.1), // VAT 10%
      total: Math.round((estimatedPrice.value || 0) * 1.1)
    },
    issueDate: currentDate.toLocaleDateString('vi-VN'),
    dueDate: new Date(currentDate.getTime() + 7 * 24 * 60 * 60 * 1000).toLocaleDateString('vi-VN') // 7 ngày sau
  };
  
  showInvoiceModal.value = true;
};

const closeInvoiceModal = () => {
  showInvoiceModal.value = false;
  invoiceData.value = null;
};

const downloadInvoice = () => {
  // Tạo hóa đơn PDF
  const invoice = invoiceData.value;
  
  // Tạo HTML content cho PDF
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
        <h3>Thông tin khách hàng</h3>
        <div class="row"><span>Họ tên:</span><span>${invoice.customerInfo.name}</span></div>
        ${invoice.customerInfo.email ? `<div class="row"><span>Email:</span><span>${invoice.customerInfo.email}</span></div>` : ''}
        ${invoice.customerInfo.phone ? `<div class="row"><span>Số điện thoại:</span><span>${invoice.customerInfo.phone}</span></div>` : ''}
      </div>
      
      <div class="section">
        <h3>Chi tiết dịch vụ</h3>
        <div class="row"><span>Dịch vụ:</span><span>${invoice.orderInfo.serviceName}</span></div>
        <div class="row"><span>Diện tích:</span><span>${invoice.orderInfo.area} m²</span></div>
        <div class="row"><span>Thời gian làm việc:</span><span>${invoice.orderInfo.workingHours}</span></div>
        <div class="row"><span>Thời gian bắt đầu:</span><span>${new Date(invoice.orderInfo.startTime).toLocaleString('vi-VN')}</span></div>
        <div class="row"><span>Thời gian kết thúc:</span><span>${new Date(invoice.orderInfo.endTime).toLocaleString('vi-VN')}</span></div>
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
  `;
  
  // Tạo PDF từ HTML bằng cách in
  const printWindow = window.open('', '_blank');
  printWindow.document.write(htmlContent);
  printWindow.document.close();
  printWindow.focus();
  printWindow.print();
  
  // Tự động đóng cửa sổ sau khi in
  printWindow.onafterprint = () => printWindow.close();
};

const submitOrder = async () => {
  if (isSubmitting.value) return;
  
  try {
    isSubmitting.value = true;
    const payload = { ...order.value };
    
    if (estimatedPrice.value !== null) {
      payload.cost_confirm = String(estimatedPrice.value);
    }
    
    // Thêm thông tin thanh toán
    payload.payment_method = paymentMethod.value;

    const response = await CreateOrderService.createOrder(payload) as any;
    console.log('API response:', response);
    
    if (response && response.id) {
      closePaymentModal();
      
      // Tạo hóa đơn sau khi đặt đơn thành công
      generateInvoice(response);
      
      // Không chuyển trang ngay mà cho người dùng xem hóa đơn trước
      // router.push('/dss/customer-orders');
    } else {
      alert('Tạo đơn thất bại, vui lòng kiểm tra thông tin.');
    }
  } catch (error: any) {
    console.error('Failed to create order', error?.response?.data || error);
    alert('Tạo đơn thất bại, vui lòng kiểm tra thông tin.');
  } finally {
    isSubmitting.value = false;
  }
};

function formatHourMinute(hours: number|null) {
  if (hours === null || isNaN(hours)) return '';
  if (hours > 0 && hours * 60 < 1) return '1 phút';
  const h = Math.floor(hours);
  let m = Math.round((hours - h) * 60);
  if (h === 0) return `${m} phút`;
  if (m === 0) return `${h} giờ`;
  return `${h} giờ ${m} phút`;
}

onMounted(() => {
  fetchServiceTypes();
});
</script>

<template>
  <div class="create-order-container">
    <div class="form-wrapper">
      <form class="form" @submit.prevent="submitOrder">
        <div class="form-header">
          <h1 class="form-title">Tạo đơn mới</h1>
          <p class="form-subtitle">Nhập thông tin để tạo đơn dịch vụ</p>
        </div>
        <div class="signup-columns">
          <div class="signup-column">
            <div class="form-group">
              <label>Dịch vụ</label>
              <div class="inputForm">
                <select v-model="order.service_type" class="input" required>
                  <option value="" disabled>Chọn dịch vụ</option>
                  <option v-for="service in serviceTypes" :key="service.id" :value="service.id">
                    {{ service.name }}
                  </option>
                </select>
              </div>
            </div>
            <div class="form-group">
              <label>Diện tích (m²)</label>
              <div class="inputForm">
                <input v-model="order.area_m2" type="number" class="input" min="0" step="any" placeholder="Nhập diện tích" required />
              </div>
            </div>
            <div class="form-group">
              <label>Ghi chú</label>
              <div class="inputForm">
                <textarea v-model="order.note" class="input" placeholder="Nhập ghi chú (nếu có)" style="height: 50px;"></textarea>
              </div>
            </div>
            
          </div>
          <div class="signup-column">
            <div class="form-group">
              <label>Tiền trên m²</label>
              <div class="inputForm">
                <input 
                  type="text" 
                  :value="selectedServicePrice ? selectedServicePrice.toLocaleString('vi-VN') + ' VNĐ' : ''" 
                  class="input" 
                  disabled 
                  placeholder="Chọn dịch vụ để xem giá" 
                  style="color:#2d79f3;font-weight:600;" 
                />
              </div>
            </div>
            <div class="form-group">
              <label>Thời gian bắt đầu ưu tiên</label>
              <div class="inputForm">
                <input v-model="order.preferred_start_time" type="datetime-local" class="input" required />
              </div>
            </div>
            <div class="form-group">
              <label>Thời gian kết thúc ưu tiên</label>
              <div class="inputForm">
                <input v-model="order.preferred_end_time" type="datetime-local" class="input" required />
              </div>
            </div>
          </div>
        </div>

        <!-- Dấu gạch ngang phân cách -->
        <div class="divider"></div>

        <!-- Phần tính toán giá và thời gian -->
        <div class="calculation-section">
          <h3 class="calculation-title">Thông tin tính toán</h3>
          <div class="calculation-row">
            <div class="form-group">
              <label>Giá ước tính</label>
              <div class="inputForm">
                <input type="text" :value="estimatedPrice !== null ? estimatedPrice.toLocaleString('vi-VN') + ' VNĐ' : ''" class="input" disabled placeholder="Giá ước tính sẽ tự động tính" style="color:#ef4444;font-weight:700;" />
              </div>
              <small v-if="priceExplanation" style="color:#6b7280; font-style:italic; margin-top:4px; display:block;">
                {{ priceExplanation }}
              </small>
            </div>
            <div class="form-group">
              <label>Số giờ yêu cầu</label>
              <div class="inputForm" :class="{ 'error': !isTimeValid }">
                <input type="text" :value="order.requested_hours !== null ? formatHourMinute(order.requested_hours) : ''" class="input" readonly placeholder="Số giờ yêu cầu sẽ tự động tính" style="color:#ef4444;font-weight:700;" />
              </div>
              <!-- Hiển thị thông báo lỗi thời gian -->
              <div v-if="!isTimeValid && timeValidationMessage" class="error-message">
                 {{ timeValidationMessage }}
              </div>
              <!-- Hiển thị thông tin thời gian tối thiểu -->
              <small v-if="minRequiredHours" class="time-info">
                Thời gian tối thiểu: {{ formatHourMinute(minRequiredHours) }}
              </small>
            </div>
          </div>
        </div>
        <button type="button" class="button-submit" :disabled="!isTimeValid" @click="openPaymentModal">
          {{ !isTimeValid ? 'Thời gian không hợp lệ' : 'Tạo đơn' }}
        </button>
      </form>
    </div>
    
    <!-- Modal thanh toán -->
    <div v-if="showPaymentModal" class="modal-overlay" @click="closePaymentModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Chọn phương thức thanh toán</h2>
          <button class="close-btn" @click="closePaymentModal">×</button>
        </div>
        
        <div class="modal-body">
          <!-- Thông tin đơn hàng -->
          <div class="order-summary">
            <h3>Thông tin đơn hàng</h3>
            <div class="summary-item">
              <span>Dịch vụ:</span>
              <span>{{ serviceTypes.find(s => s.id === order.service_type)?.name || 'N/A' }}</span>
            </div>
            <div class="summary-item">
              <span>Diện tích:</span>
              <span>{{ order.area_m2 }} m²</span>
            </div>
            <div class="summary-item">
              <span>Thời gian yêu cầu:</span>
              <span>{{ formatHourMinute(order.requested_hours) }}</span>
            </div>
            <div class="summary-item total">
              <span>Tổng tiền:</span>
              <span class="price">{{ estimatedPrice?.toLocaleString('vi-VN') || '0' }} VNĐ</span>
            </div>
          </div>

          <!-- Chọn phương thức thanh toán -->
          <div class="payment-methods">
            <h3>Phương thức thanh toán</h3>
            
            <div class="payment-option">
              <label class="radio-container">
                <input type="radio" v-model="paymentMethod" value="cash">
                <span class="checkmark"></span>
                <div class="payment-info">
                  <div class="payment-title">💰 Thanh toán tiền mặt</div>
                  <div class="payment-desc">Thanh toán trực tiếp khi hoàn thành dịch vụ</div>
                </div>
              </label>
            </div>

            <div class="payment-option">
              <label class="radio-container">
                <input type="radio" v-model="paymentMethod" value="transfer">
                <span class="checkmark"></span>
                <div class="payment-info">
                  <div class="payment-title">🏦 Chuyển khoản ngân hàng</div>
                  <div class="payment-desc">Chuyển khoản qua QR Code</div>
                </div>
              </label>
            </div>

            <!-- QR Code cho chuyển khoản -->
            <div v-if="paymentMethod === 'transfer'" class="qr-section">
              <div class="bank-info">
                <h4>Thông tin chuyển khoản:</h4>
                <div class="bank-details">
                  <div><strong>Ngân hàng:</strong> {{ bankInfo.bankName }}</div>
                  <div><strong>Số tài khoản:</strong> {{ bankInfo.accountNumber }}</div>
                  <div><strong>Chủ tài khoản:</strong> {{ bankInfo.accountHolder }}</div>
                  <div><strong>Số tiền:</strong> <span class="amount">{{ estimatedPrice?.toLocaleString('vi-VN') }} VNĐ</span></div>
                </div>
              </div>
              
              <div class="qr-code">
                <img :src="qrCodeData" alt="QR Code thanh toán" />
                <p>Quét mã QR để thanh toán</p>
              </div>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn-cancel" @click="closePaymentModal">Hủy</button>
          <button class="btn-confirm" @click="submitOrder" :disabled="isSubmitting">
            {{ isSubmitting ? 'Đang xử lý...' : 'Xác nhận tạo đơn' }}
          </button>
        </div>
      </div>
    </div>
    
    <!-- Modal Hóa đơn -->
    <div v-if="showInvoiceModal && invoiceData" class="modal-overlay" @click="closeInvoiceModal">
      <div class="modal-content invoice-modal" @click.stop>
        <div class="modal-header">
          <h2>🧾 Hóa đơn dịch vụ</h2>
          <button class="close-btn" @click="closeInvoiceModal">×</button>
        </div>
        
        <div class="modal-body">
          <div class="invoice-header">
            <div class="invoice-title">HÓA ĐƠN DỊCH VỤ</div>
            <div class="invoice-number">Số: {{ invoiceData.invoiceNumber }}</div>
            <div class="invoice-date">
              <div>Ngày xuất: {{ invoiceData.issueDate }}</div>
              <div>Hạn thanh toán: {{ invoiceData.dueDate }}</div>
            </div>
          </div>

          <div class="invoice-section">
            <h4>Thông tin khách hàng</h4>
            <div class="info-row">
              <span>Họ tên:</span>
              <span>{{ invoiceData.customerInfo.name }}</span>
            </div>
            <div class="info-row" v-if="invoiceData.customerInfo.email">
              <span>Email:</span>
              <span>{{ invoiceData.customerInfo.email }}</span>
            </div>
            <div class="info-row" v-if="invoiceData.customerInfo.phone">
              <span>Số điện thoại:</span>
              <span>{{ invoiceData.customerInfo.phone }}</span>
            </div>
          </div>

          <div class="invoice-section">
            <h4>Chi tiết dịch vụ</h4>
            <div class="service-details">
              <div class="info-row">
                <span>Dịch vụ:</span>
                <span>{{ invoiceData.orderInfo.serviceName }}</span>
              </div>
              <div class="info-row">
                <span>Diện tích:</span>
                <span>{{ invoiceData.orderInfo.area }} m²</span>
              </div>
              <div class="info-row">
                <span>Thời gian làm việc:</span>
                <span>{{ invoiceData.orderInfo.workingHours }}</span>
              </div>
              <div class="info-row">
                <span>Thời gian bắt đầu:</span>
                <span>{{ new Date(invoiceData.orderInfo.startTime).toLocaleString('vi-VN') }}</span>
              </div>
              <div class="info-row">
                <span>Thời gian kết thúc:</span>
                <span>{{ new Date(invoiceData.orderInfo.endTime).toLocaleString('vi-VN') }}</span>
              </div>
              <div class="info-row">
                <span>Phương thức thanh toán:</span>
                <span>{{ invoiceData.orderInfo.paymentMethod }}</span>
              </div>
              <div class="info-row" v-if="invoiceData.orderInfo.note !== 'Không có'">
                <span>Ghi chú:</span>
                <span>{{ invoiceData.orderInfo.note }}</span>
              </div>
            </div>
          </div>

          <div class="invoice-section">
            <h4>Thanh toán</h4>
            <div class="pricing-details">
              <div class="info-row">
                <span>Tạm tính:</span>
                <span>{{ invoiceData.pricing.subtotal.toLocaleString('vi-VN') }} VNĐ</span>
              </div>
              <div class="info-row">
                <span>VAT (10%):</span>
                <span>{{ invoiceData.pricing.tax.toLocaleString('vi-VN') }} VNĐ</span>
              </div>
              <div class="info-row total-amount">
                <span><strong>Tổng cộng:</strong></span>
                <span class="total-price"><strong>{{ invoiceData.pricing.total.toLocaleString('vi-VN') }} VNĐ</strong></span>
              </div>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn-download" @click="downloadInvoice">�️ 📥 Tải xuống PDF</button>
          <button class="btn-confirm" @click="() => { closeInvoiceModal(); router.push('/dss/customer-orders'); }">
            Xem đơn hàng
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.create-order-container {
  display: flex;
  justify-content: center;
  padding: 40px 20px;
}
.form-wrapper {
  width: 100%;
  max-width: 900px;
  background-color: #fff;
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}
.form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.form-header {
  text-align: center;
  margin-bottom: 10px;
}
.signup-columns {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
}
.signup-column {
  display: flex;
  flex-direction: column;
  gap: 15px;
}
.form-group {
  display: flex;
  flex-direction: column;
}
.form-group label {
  font-weight: 600;
  margin-bottom: 5px;
}
.inputForm {
  border: 1.5px solid #ecedec;
  border-radius: 10px;
  height: 50px;
  display: flex;
  align-items: center;
  padding-left: 10px;
  transition: 0.2s ease-in-out;
}
.input {
  margin-left: 10px;
  border-radius: 10px;
  border: none;
  width: 100%;
  height: 100%;
  background: transparent;
}
.input:focus {
  outline: none;
}
.inputForm:focus-within {
  border-color: #2d79f3;
}
.button-submit {
  background-color: #151717;
  border: none;
  color: white;
  font-size: 15px;
  font-weight: 500;
  border-radius: 10px;
  height: 50px;
  width: 100%;
  cursor: pointer;
  transition: background 0.2s ease-in-out;
}
.button-submit:hover {
  background-color: #252727;
}
.button-submit:disabled {
  background-color: #666;
  cursor: not-allowed;
}
@media (max-width: 768px) {
  .signup-columns {
    grid-template-columns: 1fr;
  }
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

/* Divider styles */
.divider {
  height: 1px;
  background: linear-gradient(to right, transparent, #e5e7eb, transparent);
  margin: 30px 0;
  position: relative;
}

.divider::before {
  content: '';
  position: absolute;
  top: -1px;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 3px;
  background: #2d79f3;
  border-radius: 2px;
}

/* Calculation section styles */
.calculation-section {
  background-color: #f8fafc;
  border-radius: 16px;
  padding: 25px;
  border: 1px solid #e5e7eb;
}

.calculation-title {
  font-size: 18px;
  font-weight: 600;
  color: #374151;
  margin: 0 0 20px 0;
  text-align: center;
  position: relative;
}

.calculation-title::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  width: 40px;
  height: 2px;
  background: #ef4444;
  border-radius: 1px;
}

.calculation-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

@media (max-width: 768px) {
  .calculation-row {
    grid-template-columns: 1fr;
  }
}

/* Error states */
.inputForm.error {
  border-color: #ef4444 !important;
  background-color: #fef2f2;
}

.error-message {
  color: #ef4444;
  font-size: 13px;
  font-weight: 500;
  margin-top: 5px;
  padding: 8px 12px;
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.time-info {
  color: #059669;
  font-size: 12px;
  font-style: italic;
  margin-top: 4px;
  display: block;
}

/* Service price info styles */
.service-price-info {
  color: #2d79f3;
  font-size: 12px;
  font-weight: 600;
  margin-top: 4px;
  display: block;
  padding: 4px 8px;
  background-color: #f0f9ff;
  border-radius: 6px;
  border: 1px solid #bae6fd;
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 16px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 24px 0;
  border-bottom: 1px solid #e5e7eb;
  margin-bottom: 24px;
}

.modal-header h2 {
  font-size: 20px;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #6b7280;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s;
}

.close-btn:hover {
  background-color: #f3f4f6;
  color: #374151;
}

.modal-body {
  padding: 0 24px 24px;
}

/* Order summary */
.order-summary {
  background: #f8fafc;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 24px;
}

.order-summary h3 {
  margin: 0 0 16px 0;
  font-size: 16px;
  font-weight: 600;
  color: #374151;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #e5e7eb;
}

.summary-item:last-child {
  border-bottom: none;
}

.summary-item.total {
  font-weight: 600;
  font-size: 16px;
  margin-top: 8px;
  padding-top: 12px;
  border-top: 2px solid #e5e7eb;
}

.summary-item .price {
  color: #ef4444;
  font-weight: 700;
}

/* Payment methods */
.payment-methods h3 {
  margin: 0 0 16px 0;
  font-size: 16px;
  font-weight: 600;
  color: #374151;
}

.payment-option {
  margin-bottom: 16px;
}

.radio-container {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 16px;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  transition: all 0.2s;
}

.radio-container:hover {
  border-color: #2d79f3;
  background-color: #f8fafc;
}

.radio-container input[type="radio"] {
  display: none;
}

.checkmark {
  width: 20px;
  height: 20px;
  border: 2px solid #d1d5db;
  border-radius: 50%;
  margin-right: 12px;
  position: relative;
  transition: all 0.2s;
}

.radio-container input[type="radio"]:checked + .checkmark {
  border-color: #2d79f3;
  background-color: #2d79f3;
}

.radio-container input[type="radio"]:checked + .checkmark::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 8px;
  height: 8px;
  background: white;
  border-radius: 50%;
}

.payment-info {
  flex: 1;
}

.payment-title {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 4px;
}

.payment-desc {
  font-size: 14px;
  color: #6b7280;
}

/* QR Section */
.qr-section {
  margin-top: 20px;
  padding: 20px;
  background: #f0f9ff;
  border-radius: 12px;
  border: 1px solid #0ea5e9;
}

.bank-info h4 {
  margin: 0 0 12px 0;
  color: #0c4a6e;
  font-size: 16px;
}

.bank-details {
  margin-bottom: 20px;
}

.bank-details div {
  margin-bottom: 8px;
  font-size: 14px;
  color: #374151;
}

.bank-details .amount {
  color: #ef4444;
  font-weight: 700;
}

.qr-code {
  text-align: center;
}

.qr-code img {
  width: 200px;
  height: 200px;
  border-radius: 12px;
  border: 2px solid #e5e7eb;
  margin-bottom: 12px;
}

.qr-code p {
  margin: 0;
  font-size: 14px;
  color: #6b7280;
  font-style: italic;
}

/* Modal footer */
.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 0 24px 24px;
  border-top: 1px solid #e5e7eb;
  margin-top: 24px;
  padding-top: 24px;
}

.btn-cancel, .btn-confirm {
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-cancel {
  background: #f3f4f6;
  border: 1px solid #d1d5db;
  color: #374151;
}

.btn-cancel:hover {
  background: #e5e7eb;
}

.btn-confirm {
  background: #2d79f3;
  border: 1px solid #2d79f3;
  color: white;
}

.btn-confirm:hover:not(:disabled) {
  background: #1d4ed8;
}

.btn-confirm:disabled {
  background: #9ca3af;
  border-color: #9ca3af;
  cursor: not-allowed;
}

@media (max-width: 640px) {
  .modal-content {
    width: 95%;
    margin: 10px;
  }
  
  .modal-header, .modal-body, .modal-footer {
    padding-left: 16px;
    padding-right: 16px;
  }
  
  .qr-code img {
    width: 160px;
    height: 160px;
  }
  
  .modal-footer {
    flex-direction: column;
  }
  
  .btn-cancel, .btn-confirm {
    width: 100%;
  }
}

/* Invoice Modal Styles - Chủ đạo đen trắng */
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
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
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

.btn-confirm {
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

.btn-confirm:hover {
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
  
  .btn-download, .btn-confirm {
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
