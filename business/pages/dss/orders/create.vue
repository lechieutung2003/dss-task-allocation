<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue';
import { useRouter } from 'vue-router';
import CreateOrderService from '@/services/dss/users/customer';
import { useOauthStore } from '@/stores/oauth';
import serviceTypesApi from '@/services/dss/serviceTypes';
// Import hình ảnh QR
import qrImage from '@/assets/images/qr.jpg';
// Import customer CSS
import '@/assets/css/customer.css';

const store = useOauthStore();
const router = useRouter();

// Thông tin customer từ hr_customer
const customerInfo = ref<any>(null);
const loadingCustomer = ref(true);

const order = ref({
  customer: null as string | null, // Sẽ được cập nhật sau khi lấy thông tin customer
  service_type: null,
  area_m2: null,
  requested_hours: null as number | null,
  preferred_start_time: '',
  preferred_end_time: '',
  estimated_hours: null as number | null,
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

// Hàm lấy thông tin customer từ hr_customer
const fetchCustomerInfo = async () => {
  try {
    loadingCustomer.value = true;
    console.log('Loading customer info...');
    
    const response = await CreateOrderService.getUser();
    console.log('Customer API response:', response);
    
    const customer = response.data || response;
    customerInfo.value = customer;
    
    // Cập nhật customer ID vào order
    order.value.customer = customer.id;
    
    console.log('Customer info loaded:', customer);
    console.log('Order customer updated:', order.value.customer);
    
  } catch (error) {
    console.error('Error loading customer info:', error);
    alert('Không thể tải thông tin khách hàng. Vui lòng đăng nhập lại.');
  } finally {
    loadingCustomer.value = false;
  }
};

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
  // Sử dụng ID của đơn hàng làm invoiceNumber trực tiếp
  const invoiceNumber = orderResponse.id;
  
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
      name: customerInfo.value?.name || 'Khách hàng',
      email: customerInfo.value?.email || '',
      phone: customerInfo.value?.phone || ''
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
  if (printWindow) {
    printWindow.document.write(htmlContent);
    printWindow.document.close();
    printWindow.focus();
    printWindow.print();
    // Tự động đóng cửa sổ sau khi in
    printWindow.onafterprint = () => printWindow.close();
  } else {
    alert('Không thể mở cửa sổ in hóa đơn. Vui lòng kiểm tra trình duyệt của bạn.');
  }
};

// const submitOrder = async () => {
//   if (isSubmitting.value) return;
  
//   try {
//     isSubmitting.value = true;
//     const payload = { ...order.value };
    
//     if (estimatedPrice.value !== null) {
//       payload.cost_confirm = String(estimatedPrice.value);
//     }
    
//     // Thêm thông tin thanh toán
//     payload.payment_method = paymentMethod.value;

//     const response = await CreateOrderService.createOrder(payload) as any;
//     console.log('API response:', response);
    
//     if (response && response.id) {
//       closePaymentModal();
      
//       // Tạo hóa đơn sau khi đặt đơn thành công
//       generateInvoice(response);
      
//       // Không chuyển trang ngay mà cho người dùng xem hóa đơn trước
//       // router.push('/dss/customer-orders');
//     } else {
//       alert('Tạo đơn thất bại, vui lòng kiểm tra thông tin.');
//     }
//   } catch (error: any) {
//     console.error('Failed to create order', error?.response?.data || error);
//     alert('Tạo đơn thất bại, vui lòng kiểm tra thông tin.');
//   } finally {
//     isSubmitting.value = false;
//   }
// };


const submitOrder = async () => {
  if (isSubmitting.value) return;
  try {
    isSubmitting.value = true;
    
    // Tạo payload với format giống Postman
    const payload: any = {
      customer: order.value.customer, // ID từ hr_customer
      service_type: order.value.service_type,
      area_m2: order.value.area_m2,
      requested_hours: order.value.requested_hours,
      preferred_start_time: order.value.preferred_start_time,
      preferred_end_time: order.value.preferred_end_time,
      estimated_hours: order.value.estimated_hours,
      status: order.value.status,
      note: order.value.note || "",
    };
    
    // Thêm cost_confirm nếu có
    if (estimatedPrice.value !== null) {
      payload.cost_confirm = String(estimatedPrice.value);
    }

    // Log payload để kiểm tra
    console.log('Payload gửi lên (format Postman):', payload);

    const response = await CreateOrderService.createOrder(payload) as any;
    console.log('API response:', response);
    
    if (response && response.id) {
      closePaymentModal();
      generateInvoice(response);
      // Có thể chuyển trang sau khi xem hóa đơn
    } else {
      alert('Tạo đơn thất bại, vui lòng kiểm tra thông tin.');
    }
  } catch (error: any) {
    console.error('Lỗi chi tiết từ backend:', error?.response?.data || error);
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
  fetchCustomerInfo();
});
</script>

<template>
  <div class="about-page">
    <section class="stripe white">
      <div class="container">
        <div class="content-header">
          <h1 class="section-title">Tạo đơn mới</h1>
          <p class="section-subtitle">Nhập thông tin để tạo đơn dịch vụ</p>
          
          <!-- Customer info display -->
          <div v-if="loadingCustomer" class="customer-info loading">
            <p>Đang tải thông tin khách hàng...</p>
          </div>
          <div v-else-if="customerInfo" class="customer-info">
            <h3>Thông tin khách hàng</h3>
            <div class="customer-details">
              <div class="customer-item">
                <span class="label">Tên:</span>
                <span class="value">{{ customerInfo.name }}</span>
              </div>
              <div class="customer-item">
                <span class="label">Email:</span>
                <span class="value">{{ customerInfo.email }}</span>
              </div>
              <div class="customer-item" v-if="customerInfo.phone">
                <span class="label">SĐT:</span>
                <span class="value">{{ customerInfo.phone }}</span>
              </div>
              <div class="customer-item" v-if="customerInfo.address">
                <span class="label">Địa chỉ:</span>
                <span class="value">{{ customerInfo.address }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <form class="order-form" @submit.prevent="submitOrder">
          <div class="form-grid">
            <div class="form-column">
              <div class="form-group">
                <label>Dịch vụ</label>
                <div class="input-wrapper">
                  <select v-model="order.service_type" class="form-input" required>
                    <option value="" disabled>Chọn dịch vụ</option>
                    <option v-for="service in serviceTypes" :key="service.id" :value="service.id">
                      {{ service.name }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="form-group">
                <label>Diện tích (m²)</label>
                <div class="input-wrapper">
                  <input v-model="order.area_m2" type="number" class="form-input" min="0" step="any" placeholder="Nhập diện tích" required />
                </div>
              </div>
              <div class="form-group">
                <label>Ghi chú</label>
                <div class="input-wrapper">
                  <textarea v-model="order.note" class="form-input" placeholder="Nhập ghi chú (nếu có)" rows="3"></textarea>
                </div>
              </div>
            </div>
            
            <div class="form-column">
              <div class="form-group">
                <label>Tiền trên m²</label>
                <div class="input-wrapper">
                  <input 
                    type="text" 
                    :value="selectedServicePrice ? selectedServicePrice.toLocaleString('vi-VN') + ' VNĐ' : ''" 
                    class="form-input price-display" 
                    disabled 
                    placeholder="Chọn dịch vụ để xem giá" 
                  />
                </div>
              </div>
              <div class="form-group">
                <label>Thời gian bắt đầu ưu tiên</label>
                <div class="input-wrapper">
                  <input v-model="order.preferred_start_time" type="datetime-local" class="form-input" required />
                </div>
              </div>
              <div class="form-group">
                <label>Thời gian kết thúc ưu tiên</label>
                <div class="input-wrapper">
                  <input v-model="order.preferred_end_time" type="datetime-local" class="form-input" required />
                </div>
              </div>
            </div>
          </div>

          <!-- Calculation section -->
          <div class="calculation-section">
            <h3 class="calculation-title">Thông tin tính toán</h3>
            <div class="calculation-grid">
              <div class="form-group">
                <label>Số giờ ước tính</label>
                <div class="input-wrapper">
                  <input 
                    type="text" 
                    :value="order.estimated_hours !== null ? formatHourMinute(order.estimated_hours) : ''" 
                    class="form-input estimated-display" 
                    disabled 
                    placeholder="Số giờ ước tính sẽ tự động tính" 
                  />
                </div>
                <small v-if="productivity && order.area_m2" class="form-hint">
                  Tốc độ làm việc: {{ productivity }} m²/giờ
                </small>
              </div>
              <div class="form-group">
                <label>Số giờ yêu cầu</label>
                <div class="input-wrapper" :class="{ 'error': !isTimeValid }">
                  <input type="text" :value="order.requested_hours !== null ? formatHourMinute(order.requested_hours) : ''" class="form-input requested-display" readonly placeholder="Số giờ yêu cầu sẽ tự động tính" />
                </div>
                <div v-if="!isTimeValid && timeValidationMessage" class="error-message">
                   {{ timeValidationMessage }}
                </div>
                <small v-if="minRequiredHours" class="form-hint success">
                  Thời gian tối thiểu: {{ formatHourMinute(minRequiredHours) }}
                </small>
              </div>
              <div class="form-group">
                <label>Giá ước tính</label>
                <div class="input-wrapper">
                  <input type="text" :value="estimatedPrice !== null ? estimatedPrice.toLocaleString('vi-VN') + ' VNĐ' : ''" class="form-input price-estimated" disabled placeholder="Giá ước tính sẽ tự động tính" />
                </div>
                <small v-if="priceExplanation" class="form-hint">
                  {{ priceExplanation }}
                </small>
              </div>
              <div class="form-group">
                <!-- Empty space for layout balance -->
              </div>
            </div>
          </div>
          
          <button type="button" class="featured-cta" :disabled="!isTimeValid" @click="openPaymentModal">
            {{ !isTimeValid ? 'Thời gian không hợp lệ' : 'Tạo đơn' }}
          </button>
        </form>
      </div>
    </section>
    
    <!-- Modal thanh toán -->
    <div v-if="showPaymentModal" class="modal-overlay" @click="closePaymentModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Chọn phương thức thanh toán</h2>
          <button class="close-btn" @click="closePaymentModal">×</button>
        </div>
        
        <div class="modal-body">
          <!-- Thông tin đơn hàng -->
          <div class="t-card">
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
          <button class="btn-close" @click="closePaymentModal">Hủy</button>
          <button class="btn-download" @click="submitOrder" :disabled="isSubmitting">
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
              <div class="total-amount">
                <span><strong>Tổng cộng:</strong></span>
                <span class="total-price"><strong>{{ invoiceData.pricing.total.toLocaleString('vi-VN') }} VNĐ</strong></span>
              </div>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn-download" @click="downloadInvoice">� Tải xuống PDF</button>
          <button class="btn-close" @click="() => { closeInvoiceModal(); router.push('/dss/customer-orders'); }">
            Xem đơn hàng
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Customer info styles */
.customer-info {
  background: var(--bg-card);
  border: 1px solid rgba(59, 130, 246, 0.1);
  border-radius: 20px;
  padding: 1.5rem;
  margin: 2rem 0;
  box-shadow: var(--shadow);
}

.customer-info.loading {
  text-align: center;
  color: var(--text-light);
}

.customer-info h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--accent);
  margin: 0 0 1rem;
  text-align: center;
}

.customer-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.customer-item {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.customer-item .label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-light);
  min-width: 60px;
}

.customer-item .value {
  font-size: 0.875rem;
  color: var(--text-dark);
  font-weight: 500;
}

/* Form styles */
.order-form {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.form-column {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: var(--text-dark);
}

.input-wrapper {
  border: 1.5px solid #ecedec;
  border-radius: 10px;
  min-height: 50px;
  display: flex;
  align-items: center;
  padding: 0 1rem;
  transition: all 0.2s ease-in-out;
  background: var(--bg-card);
}

.input-wrapper:focus-within {
  border-color: var(--primary);
}

.input-wrapper.error {
  border-color: #ef4444;
  background-color: #fef2f2;
}

.form-input {
  border: none;
  width: 100%;
  height: 100%;
  background: transparent;
  color: var(--text-dark);
  font-size: 1rem;
}

.form-input:focus {
  outline: none;
}

.form-input:disabled {
  color: var(--text-light);
  cursor: not-allowed;
}

.form-input.price-display {
  color: var(--primary);
  font-weight: 600;
}

.form-input.estimated-display {
  color: var(--accent);
  font-weight: 700;
}

.form-input.requested-display {
  color: #ef4444;
  font-weight: 700;
}

.form-input.price-estimated {
  color: #ef4444;
  font-weight: 700;
}

.form-hint {
  color: var(--text-light);
  font-style: italic;
  margin-top: 0.25rem;
  display: block;
  font-size: 0.75rem;
}

.form-hint.success {
  color: var(--accent);
}

.error-message {
  color: #ef4444;
  font-size: 0.813rem;
  font-weight: 500;
  margin-top: 0.25rem;
  padding: 0.5rem 0.75rem;
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 8px;
}

/* Calculation section */
.calculation-section {
  background: var(--bg-light);
  border-radius: 16px;
  padding: 1.5rem;
  border: 1px solid rgba(59, 130, 246, 0.1);
}

.calculation-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-dark);
  margin: 0 0 1.5rem;
  text-align: center;
}

.calculation-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

/* Payment methods styles */
.payment-methods h3 {
  margin: 0 0 1rem;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-dark);
}

.payment-option {
  margin-bottom: 1rem;
}

.radio-container {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  transition: all 0.2s;
}

.radio-container:hover {
  border-color: var(--primary);
  background-color: var(--bg-light);
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
  border-color: var(--primary);
  background-color: var(--primary);
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
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-dark);
  margin-bottom: 0.25rem;
}

.payment-desc {
  font-size: 0.875rem;
  color: var(--text-light);
}

/* QR Section */
.qr-section {
  margin-top: 1.25rem;
  padding: 1.25rem;
  background: var(--bg-card);
  border-radius: 12px;
  border: 1px solid var(--primary);
}

.bank-info h4 {
  margin: 0 0 0.75rem;
  color: var(--primary);
  font-size: 1rem;
}

.bank-details {
  margin-bottom: 1.25rem;
}

.bank-details div {
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  color: var(--text-dark);
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
  margin-bottom: 0.75rem;
}

.qr-code p {
  margin: 0;
  font-size: 0.875rem;
  color: var(--text-light);
  font-style: italic;
}

/* Summary item styles */
.summary-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid #e5e7eb;
}

.summary-item:last-child {
  border-bottom: none;
}

.summary-item.total {
  font-weight: 600;
  font-size: 1rem;
  margin-top: 0.5rem;
  padding-top: 0.75rem;
  border-top: 2px solid #e5e7eb;
}

.summary-item .price {
  color: #ef4444;
  font-weight: 700;
}

/* Responsive */
@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .calculation-grid {
    grid-template-columns: 1fr;
  }
  
  .customer-details {
    grid-template-columns: 1fr;
  }
  
  .qr-code img {
    width: 160px;
    height: 160px;
  }
}
</style>
