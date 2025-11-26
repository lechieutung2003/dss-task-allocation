<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import CreateOrderService from '@/services/dss/users/customer';
import { useOauthStore } from '@/stores/oauth';
import serviceTypesApi from '@/services/dss/serviceTypes';
// Import CSS
import '@/assets/css/customer.css';
import '@/assets/css/payment-modal.css';
definePageMeta({
  middleware: 'role-based'
})
const store = useOauthStore();
const router = useRouter();
const { t } = useI18n();

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
const isStartTimeValid = ref<boolean>(true); // 🆕 kiểm tra thời gian bắt đầu hợp lệ
const startTimeValidationMessage = ref<string>(''); // 🆕 thông báo lỗi thời gian bắt đầu
const areaError = ref<string>('');
const endTimeError = ref<string>('');
const noteError = ref<string>('');
const formErrors = ref<string[]>([]);
// Modal thanh toán
const showPaymentModal = ref<boolean>(false);
const showBankTransferModal = ref<boolean>(false);
const showPendingPaymentModal = ref<boolean>(false);
const paymentMethod = ref<'transfer'>('transfer');
const isSubmitting = ref<boolean>(false);
const paymentTime = ref<string>('');
const orderResponse = ref<any>(null);

// Bank transfer info
const bankInfo = ref({
  accountName: 'CTY TNHH CLEANZY',
  accountNumber: '012345678',
  bankName: 'Ngân hàng ABC',
  transferDescription: ''
});

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
    alert(t('create_order_customer_error'));
  } finally {
    loadingCustomer.value = false;
  }
};

// Hàm lấy thông tin ngân hàng từ backend
const fetchBankInfo = async () => {
  try {
    // Gọi API lấy bank info từ backend
    // Ví dụ: GET /api/v1/payment/bank-info
    // Nếu backend chưa có, sử dụng hardcoded
    // const response = await api.get('/payment/bank-info');
    // bankInfo.value = response.data;
    
    // Tạm thời sử dụng giá trị mặc định
    bankInfo.value = {
      accountName: 'CTY TNHH CLEANZY',
      accountNumber: '012345678',
      bankName: 'Ngân hàng ABC',
      transferDescription: ''
    };
  } catch (error) {
    console.error('Error loading bank info:', error);
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

//  Hàm kiểm tra thời gian bắt đầu hợp lệ
const validateStartTime = () => {
  const startTime = order.value.preferred_start_time;
  
  if (!startTime) {
    isStartTimeValid.value = true;
    startTimeValidationMessage.value = '';
    return;
  }
  
  const startDate = new Date(startTime);
  const currentDate = new Date();
  const oneHourLater = new Date(currentDate.getTime() + 60 * 60 * 1000); // Thêm 1 tiếng
  
  if (startDate < oneHourLater) {
    isStartTimeValid.value = false;
    startTimeValidationMessage.value = `Thời gian bắt đầu phải cách thời điểm hiện tại ít nhất 1 tiếng (sau ${oneHourLater.toLocaleString('vi-VN')})`;
  } else {
    isStartTimeValid.value = true;
    startTimeValidationMessage.value = '';
  }
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
    timeValidationMessage.value = t('create_order_validation_error', { 
      message: `${t('create_order_min_time', { time: formatHourMinute(minRequired) })} (60% của ${formatHourMinute(estimated)})` 
    });
  } else {
    isTimeValid.value = true;
    timeValidationMessage.value = '';
  }
};

const validateArea = () => {
  const area = order.value.area_m2;
  if (area !== null && area < 0) {
    areaError.value = 'Diện tích không được âm';
    return false;
  } else if (area !== null && area === 0) {
    areaError.value = 'Diện tích phải lớn hơn 0';
    return false;
  } else {
    areaError.value = '';
    return true;
  }
};

const validateEndTime = () => {
  const startTime = order.value.preferred_start_time;
  const endTime = order.value.preferred_end_time;
  
  if (!startTime || !endTime) {
    endTimeError.value = '';
    return true;
  }
  
  const startDate = new Date(startTime);
  const endDate = new Date(endTime);
  
  if (endDate <= startDate) {
    endTimeError.value = 'Thời gian kết thúc phải sau thời gian bắt đầu';
    return false;
  } else {
    endTimeError.value = '';
    return true;
  }
};

const validateNote = () => {
  const note = order.value.note || '';
  const wordCount = note.trim().split(/\s+/).filter(word => word.length > 0).length;
  
  if (wordCount > 50) {
    noteError.value = `Ghi chú chỉ được tối đa 50 từ (hiện tại: ${wordCount} từ)`;
    return false;
  } else {
    noteError.value = '';
    return true;
  }
};

const validateForm = () => {
  const errors: string[] = [];
  
  // Kiểm tra các trường bắt buộc
  if (!order.value.service_type) {
    errors.push('Vui lòng chọn loại dịch vụ');
  }
  
  if (!order.value.area_m2 || order.value.area_m2 <= 0) {
    errors.push('Vui lòng nhập diện tích hợp lệ');
  }
  
  if (!order.value.preferred_start_time) {
    errors.push('Vui lòng chọn thời gian bắt đầu');
  }
  
  if (!order.value.preferred_end_time) {
    errors.push('Vui lòng chọn thời gian kết thúc');
  }
  
  // Kiểm tra validation riêng lẻ
  if (!validateArea()) {
    errors.push(areaError.value);
  }
  
  if (!validateEndTime()) {
    errors.push(endTimeError.value);
  }
  
  if (!validateNote()) {
    errors.push(noteError.value);
  }
  
  formErrors.value = errors;
  return errors.length === 0;
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

  let basePrice = pricePerM2 > 0 ? pricePerM2 * area : null;
  let explanation = `Giá cơ bản: ${pricePerM2.toLocaleString('vi-VN')} x ${area} m² = ${(basePrice || 0).toLocaleString('vi-VN')} VNĐ`;

  const requested = order.value.requested_hours;
  const estimated = order.value.estimated_hours;
  if (basePrice && requested && estimated && requested < estimated) {
    const diff = estimated - requested;
    let factor = 1;
    if (diff > 0.1 && diff <= 1) factor = 1.2;
    else if (diff > 1 && diff <= 2) factor = 1.3;
    else if (diff > 2) factor = 1.5;

    if (factor > 1) {
      explanation += ` (áp dụng hệ số ${factor} do số giờ yêu cầu < số giờ ước tính)`;
      basePrice = basePrice * factor;
    }
  }

  // Thêm 10% VAT vào giá cuối cùng
  if (basePrice) {
    const vatAmount = Math.round(basePrice * 0.1);
    const finalPrice = basePrice + vatAmount;
    explanation += `\nGiá gốc: ${basePrice.toLocaleString('vi-VN')} VNĐ + VAT 10% (${vatAmount.toLocaleString('vi-VN')} VNĐ) = ${finalPrice.toLocaleString('vi-VN')} VNĐ`;
    estimatedPrice.value = finalPrice;
  } else {
    estimatedPrice.value = null;
  }

  priceExplanation.value = explanation;
};

// Theo dõi thay đổi để tính toán
watch(() => [order.value.service_type], calcProductivity);
watch(() => order.value.area_m2, () => {
  validateArea();
  calcEstimatedHours();
});
watch(() => [order.value.area_m2, productivity.value], calcEstimatedHours);
watch(() => [order.value.preferred_start_time], () => {
  validateStartTime();
});
watch(() => [order.value.preferred_start_time, order.value.preferred_end_time], () => {
  calcRequestedHours();
  validateEndTime();
  validateRequestedTime();
});
watch(() => [order.value.service_type, order.value.area_m2, order.value.requested_hours, order.value.estimated_hours], calcEstimatedPrice);
watch(() => [order.value.requested_hours, minRequiredHours.value], validateRequestedTime);
watch(() => order.value.note, validateNote);

// Theo dõi tất cả các thay đổi để validate form liên tục
watch(() => [
  order.value.service_type,
  order.value.area_m2,
  order.value.preferred_start_time,
  order.value.preferred_end_time,
  order.value.note,
  areaError.value,
  endTimeError.value,
  noteError.value
], () => {
  validateForm();
}, { deep: true });
const openPaymentModal = () => {
  if (!validateForm()) {
    // Hiển thị lỗi đầu tiên
    if (formErrors.value.length > 0) {
      alert(`Lỗi: ${formErrors.value[0]}`);
    }
    return;
  }
  
  if (!isTimeValid.value) {
    alert(t('create_order_validation_error', { message: timeValidationMessage.value }));
    return;
  }
  
  if (!isStartTimeValid.value) {
    alert(`Lỗi thời gian: ${startTimeValidationMessage.value}`);
    return;
  }
  
  // Submit order to get order ID, then show payment modal
  submitOrder();
};

const closePaymentModal = () => {
  showPaymentModal.value = false;
  isSubmitting.value = false;
};

const closeBankTransferModal = () => {
  showBankTransferModal.value = false;
};

const closePendingPaymentModal = () => {
  showPendingPaymentModal.value = false;
};

const copyToClipboard = (text: string) => {
  navigator.clipboard.writeText(text).then(() => {
    alert('Đã sao chép: ' + text);
  }).catch(() => {
    alert('Không thể sao chép, vui lòng thử lại');
  });
};

const proceedToBankTransfer = () => {
  // Validate order was created
  if (!orderResponse.value?.id) {
    alert('Lỗi: Đơn hàng chưa được tạo. Vui lòng thử lại.');
    return;
  }
  
  // Update transfer description với order ID
  bankInfo.value.transferDescription = `CLEANZY${orderResponse.value.id}`;
  
  // Close payment modal and show bank transfer
  closePaymentModal();
  showBankTransferModal.value = true;
};

const confirmBankTransfer = async () => {
  if (isSubmitting.value) return;
  try {
    isSubmitting.value = true;
    
    // Record payment time
    const now = new Date();
    paymentTime.value = now.toLocaleString('vi-VN');
    
    // Close bank transfer modal and show pending payment
    closeBankTransferModal();
    showPendingPaymentModal.value = true;
    
    // Auto-redirect to customer orders after 5 seconds
    setTimeout(() => {
      if (showPendingPaymentModal.value) {
        closePendingPaymentModal();
        router.push('/dss/customer-orders?status=pending');
      }
    }, 5000);
  } finally {
    isSubmitting.value = false;
  }
};

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
      // Save order response FIRST
      orderResponse.value = response;
      console.log('Order saved:', orderResponse.value);
      
      // Then show payment modal
      showPaymentModal.value = true;
      return response;
    } else {
      alert(t('create_order_error'));
      throw new Error('Không tạo được đơn hàng');
    }
  } catch (error: any) {
    console.error('Lỗi chi tiết từ backend:', error?.response?.data || error);
    alert(t('create_order_error'));
    throw error;
  } finally {
    isSubmitting.value = false;
  }
};
function formatHourMinute(hours: number|null) {
  if (hours === null || isNaN(hours)) return '';
  if (hours > 0 && hours * 60 < 1) return t('create_order_time_one_minute');
  const h = Math.floor(hours);
  let m = Math.round((hours - h) * 60);
  if (h === 0) return t('create_order_time_minutes', { minutes: m });
  if (m === 0) return t('create_order_time_hours', { hours: h });
  return t('create_order_time_hours_minutes', { hours: h, minutes: m });
}

onMounted(() => {
  fetchServiceTypes();
  fetchCustomerInfo();
  fetchBankInfo();
});
</script>

<template>
  <div class="about-page">
    <section class="stripe white">
      <div class="container">
        <div class="content-header">
          <h1 class="section-title">{{ t('create_order_title') }}</h1>
          <p class="section-subtitle">{{ t('create_order_subtitle') }}</p>
          
          <!-- Customer info display -->
          <div v-if="loadingCustomer" class="customer-info loading">
            <p>{{ t('create_order_loading_customer') }}</p>
          </div>
          <div v-else-if="customerInfo" class="customer-info">
            <h3>{{ t('create_order_customer_info') }}</h3>
            <div class="customer-details">
              <div class="customer-item">
                <span class="label">{{ t('create_order_customer_name') }}</span>
                <span class="value">{{ customerInfo.name }}</span>
              </div>
              <div class="customer-item">
                <span class="label">{{ t('create_order_customer_email') }}</span>
                <span class="value">{{ customerInfo.email }}</span>
              </div>
              <div class="customer-item" v-if="customerInfo.phone">
                <span class="label">{{ t('create_order_customer_phone') }}</span>
                <span class="value">{{ customerInfo.phone }}</span>
              </div>
              <div class="customer-item" v-if="customerInfo.address">
                <span class="label">{{ t('create_order_customer_address') }}</span>
                <span class="value">{{ customerInfo.address }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <form class="order-form" @submit.prevent="submitOrder">
          <div class="form-grid">
            <div class="form-column">
              <div class="form-group">
                <label>{{ t('create_order_service') }}</label>
                <div class="input-wrapper">
                  <select v-model="order.service_type" class="form-input" required>
                    <option value="" disabled>{{ t('create_order_service_placeholder') }}</option>
                    <option v-for="service in serviceTypes" :key="service.id" :value="service.id">
                      {{ service.name }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="form-group">
                <label>{{ t('create_order_area') }}</label>
                <div class="input-wrapper" :class="{ 'error': areaError }">
                  <input v-model="order.area_m2" type="number" class="form-input" min="0" step="any" :placeholder="t('create_order_area_placeholder')" required />
                </div>
                <div v-if="areaError" class="error-message">
                  {{ areaError }}
                </div>
              </div>
              <div class="form-group">
                <label>{{ t('create_order_note') }}</label>
                <div class="input-wrapper" :class="{ 'error': noteError }">
                  <textarea v-model="order.note" class="form-input" :placeholder="t('create_order_note_placeholder')" rows="3"></textarea>
                </div>
                <div v-if="noteError" class="error-message">
                  {{ noteError }}
                </div>
                <small class="form-hint">
                  Ghi chú không được vượt quá 50 từ
                </small>
              </div>
            </div>
            
            <div class="form-column">
              <div class="form-group">
                <label>{{ t('create_order_price_per_m2') }}</label>
                <div class="input-wrapper">
                  <input 
                    type="text" 
                    :value="selectedServicePrice ? selectedServicePrice.toLocaleString('vi-VN') + ' VNĐ' : ''" 
                    class="form-input price-display" 
                    disabled 
                    :placeholder="t('create_order_price_placeholder')" 
                  />
                </div>
              </div>
              <div class="form-group">
                <label>{{ t('create_order_start_time') }}</label>
                <div class="input-wrapper" :class="{ 'error': !isStartTimeValid }">
                  <input v-model="order.preferred_start_time" type="datetime-local" class="form-input" required />
                </div>
                <div v-if="!isStartTimeValid && startTimeValidationMessage" class="error-message">
                  {{ startTimeValidationMessage }}
                </div>
                <small class="form-hint">
                  Thời gian bắt đầu phải cách thời điểm hiện tại ít nhất 1 tiếng
                </small>
              </div>
              <div class="form-group">
                <label>{{ t('create_order_end_time') }}</label>
                <div class="input-wrapper" :class="{ 'error': endTimeError }">
                  <input v-model="order.preferred_end_time" type="datetime-local" class="form-input" required />
                </div>
                <div v-if="endTimeError" class="error-message">
                  {{ endTimeError }}
                </div>
                <small class="form-hint">
                  Thời gian kết thúc phải sau thời gian bắt đầu
                </small>
              </div>
            </div>
          </div>

          <!-- Calculation section -->
          <div class="calculation-section">
            <h3 class="calculation-title">{{ t('create_order_calculation_title') }}</h3>
            <div class="calculation-grid">
              <div class="form-group">
                <label>{{ t('create_order_estimated_hours') }}</label>
                <div class="input-wrapper">
                  <input 
                    type="text" 
                    :value="order.estimated_hours !== null ? formatHourMinute(order.estimated_hours) : ''" 
                    class="form-input estimated-display" 
                    disabled 
                    :placeholder="t('create_order_estimated_hours_placeholder')" 
                  />
                </div>
                <small v-if="productivity && order.area_m2" class="form-hint">
                  {{ t('create_order_productivity', { productivity }) }}
                </small>
              </div>
              <div class="form-group">
                <label>{{ t('create_order_requested_hours') }}</label>
                <div class="input-wrapper" :class="{ 'error': !isTimeValid }">
                  <input type="text" :value="order.requested_hours !== null ? formatHourMinute(order.requested_hours) : ''" class="form-input requested-display" readonly :placeholder="t('create_order_requested_hours_placeholder')" />
                </div>
                <div v-if="!isTimeValid && timeValidationMessage" class="error-message">
                   {{ timeValidationMessage }}
                </div>
                <small v-if="minRequiredHours" class="form-hint success">
                  {{ t('create_order_min_time', { time: formatHourMinute(minRequiredHours) }) }}
                </small>
              </div>
              <div class="form-group">
                <label>{{ t('create_order_estimated_price') }}</label>
                <div class="input-wrapper">
                  <input type="text" :value="estimatedPrice !== null ? estimatedPrice.toLocaleString('vi-VN') + ' VNĐ' : ''" class="form-input price-estimated" disabled :placeholder="t('create_order_estimated_price_placeholder')" />
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
          
          <!-- Hiển thị lỗi form validation -->
          <div v-if="formErrors.length > 0" class="form-errors">
            <h4>Vui lòng kiểm tra lại:</h4>
            <ul>
              <li v-for="error in formErrors" :key="error" class="error-item">
                {{ error }}
              </li>
            </ul>
          </div>
          
          <button type="button" class="featured-cta" :disabled="!isTimeValid || !isStartTimeValid || formErrors.length > 0" @click="openPaymentModal">
            {{ !isTimeValid || !isStartTimeValid ? t('create_order_time_invalid') : formErrors.length > 0 ? 'Vui lòng kiểm tra thông tin' : t('create_order_create_button') }}
          </button>
        </form>
      </div>
    </section>
    
    <!-- Modal thanh toán -->
    <div v-if="showPaymentModal" class="modal-overlay" @click="closePaymentModal">
      <div class="modal-content payment-modal-web" @click.stop>
        <div class="modal-header">
          <h2>Xác nhận đơn hàng</h2>
          <button class="close-btn" @click="closePaymentModal">×</button>
        </div>
        
        <div class="payment-modal-body">
          <!-- Left: Order Details -->
          <div class="payment-left">
            <div class="order-summary">
              <h3>📋 Thông tin đơn hàng</h3>
              
              <div class="summary-grid">
                <div class="summary-item">
                  <span class="label">Dịch vụ</span>
                  <span class="value">{{ serviceTypes.find(s => s.id === order.service_type)?.name || 'N/A' }}</span>
                </div>
                
                <div class="summary-item">
                  <span class="label">Diện tích</span>
                  <span class="value">{{ order.area_m2 }} m²</span>
                </div>
                
                <div class="summary-item">
                  <span class="label">Thời gian</span>
                  <span class="value">{{ formatHourMinute(order.requested_hours) }}</span>
                </div>
                
                <div class="summary-item">
                  <span class="label">Ngày bắt đầu</span>
                  <span class="value">{{ new Date(order.preferred_start_time).toLocaleDateString('vi-VN') }}</span>
                </div>
                
                <div class="summary-item">
                  <span class="label">Giờ bắt đầu</span>
                  <span class="value">{{ new Date(order.preferred_start_time).toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' }) }}</span>
                </div>
                
                <div v-if="order.note" class="summary-item">
                  <span class="label">Ghi chú</span>
                  <span class="value">{{ order.note }}</span>
                </div>
              </div>
              
              <div class="total-amount-box">
                <span class="total-label">Tổng cộng</span>
                <span class="total-value">{{ estimatedPrice?.toLocaleString('vi-VN') || '0' }} VNĐ</span>
              </div>
            </div>
          </div>

          <!-- Middle: Customer Info -->
          <div class="payment-middle">
            <div class="customer-summary">
              <h3>👤 Khách hàng</h3>
              
              <div class="summary-grid">
                <div class="summary-item">
                  <span class="label">Tên</span>
                  <span class="value">{{ customerInfo?.name || 'N/A' }}</span>
                </div>
                
                <div class="summary-item">
                  <span class="label">Email</span>
                  <span class="value">{{ customerInfo?.email || 'N/A' }}</span>
                </div>
                
                <div class="summary-item">
                  <span class="label">Điện thoại</span>
                  <span class="value">{{ customerInfo?.phone || 'N/A' }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Right: Payment Method -->
          <div class="payment-right">
            <div class="payment-method-container">
              <h3>💳 Thanh toán</h3>
              
              <div class="payment-option-card selected">
                <div class="option-icon">🏦</div>
                <div class="option-content">
                  <h4>Chuyển khoản</h4>
                  <p>Ngân hàng</p>
                </div>
                <div class="option-radio">
                  <input type="radio" v-model="paymentMethod" value="transfer" checked>
                </div>
              </div>

              <div class="payment-info-box">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"></circle>
                  <line x1="12" y1="16" x2="12" y2="12"></line>
                  <line x1="12" y1="8" x2="12.01" y2="8"></line>
                </svg>
                <span>Giao dịch được xác nhận tự động</span>
              </div>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn-cancel" @click="closePaymentModal">Huỷ</button>
          <button class="btn-continue" @click="proceedToBankTransfer" :disabled="isSubmitting">
            {{ isSubmitting ? 'Đang xử lý...' : 'Tiếp tục →' }}
          </button>
        </div>
      </div>
    </div>
    
    <!-- Modal Bank Transfer -->
    <div v-if="showBankTransferModal" class="modal-overlay" @click="closeBankTransferModal">
      <div class="modal-content bank-transfer-modal-web" @click.stop>
        <div class="modal-header">
          <h2>Thông tin chuyển khoản</h2>
          <button class="close-btn" @click="closeBankTransferModal">×</button>
        </div>
        
        <div class="bank-modal-body">
          <!-- Left: QR Code -->
          <div class="bank-left">
            <div class="qr-box">
              <h4>Quét mã QR để thanh toán</h4>
              <div class="qr-display">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" style="width: 160px; height: 160px;">
                  <rect width="100" height="100" fill="white"/>
                  <text x="50" y="50" text-anchor="middle" dy="0.3em" font-size="20" fill="#999">QR Code</text>
                </svg>
              </div>
              <p class="qr-hint">Sử dụng ứng dụng ngân hàng hoặc mobile banking</p>
            </div>
          </div>

          <!-- Right: Bank Info -->
          <div class="bank-right">
            <div class="info-section">
              <h4>Hoặc nhập thông tin thủ công</h4>
              
              <div class="bank-field">
                <label>Tên chủ tài khoản</label>
                <div class="field-with-copy">
                  <input type="text" :value="bankInfo.accountName" disabled class="bank-input" />
                  <button type="button" class="copy-btn-small" @click="copyToClipboard(bankInfo.accountName)" title="Sao chép">
                    📋
                  </button>
                </div>
              </div>

              <div class="bank-field">
                <label>Số tài khoản</label>
                <div class="field-with-copy">
                  <input type="text" :value="bankInfo.accountNumber" disabled class="bank-input" />
                  <button type="button" class="copy-btn-small" @click="copyToClipboard(bankInfo.accountNumber)" title="Sao chép">
                    📋
                  </button>
                </div>
              </div>

              <div class="bank-field">
                <label>Số tiền</label>
                <div class="field-with-copy">
                  <input type="text" :value="estimatedPrice?.toLocaleString('vi-VN') + ' VNĐ' || ''" disabled class="bank-input" />
                  <button type="button" class="copy-btn-small" @click="copyToClipboard(String(estimatedPrice))" title="Sao chép">
                    📋
                  </button>
                </div>
              </div>

              <div class="bank-field">
                <label>Nội dung chuyển khoản</label>
                <div class="field-with-copy">
                  <input type="text" :value="bankInfo.transferDescription" disabled class="bank-input" />
                  <button type="button" class="copy-btn-small" @click="copyToClipboard(bankInfo.transferDescription)" title="Sao chép">
                    📋
                  </button>
                </div>
              </div>

              <div class="note-box">
                <strong>Lưu ý:</strong> Vui lòng nhập đúng nội dung chuyển khoản để hệ thống có thể tự động xác nhận thanh toán của bạn.
              </div>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn-cancel" @click="closeBankTransferModal">Quay lại</button>
          <button class="btn-continue" @click="confirmBankTransfer" :disabled="isSubmitting">
            {{ isSubmitting ? 'Đang xử lý...' : 'Tôi đã chuyển khoản →' }}
          </button>
        </div>
      </div>
    </div>
    
    <!-- Modal Pending Payment -->
    <div v-if="showPendingPaymentModal" class="modal-overlay" @click.prevent>
      <div class="modal-content pending-payment-modal-web" @click.stop>
        <div class="pending-header">
          <div class="pending-icon-large">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" style="width: 80px; height: 80px;">
              <circle cx="50" cy="50" r="40" fill="none" stroke="#fbbf24" stroke-width="2"/>
              <circle cx="50" cy="35" r="3" fill="#fbbf24"/>
              <path d="M 50 42 L 50 50" stroke="#fbbf24" stroke-width="2" stroke-linecap="round"/>
              <path d="M 50 50 L 60 60" stroke="#fbbf24" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </div>
          <h2>Đang xác nhận thanh toán</h2>
          <p class="pending-subtitle">Vui lòng chờ, chúng tôi đang kiểm tra giao dịch của bạn...</p>
        </div>
        
        <div class="pending-body">
          <div class="pending-details-grid">
            <div class="detail-card">
              <span class="detail-label">Số tiền</span>
              <span class="detail-value">{{ estimatedPrice?.toLocaleString('vi-VN') || '0' }} VNĐ</span>
            </div>
            
            <div class="detail-card">
              <span class="detail-label">Phương thức</span>
              <span class="detail-value">Chuyển khoản ngân hàng</span>
            </div>
            
            <div class="detail-card">
              <span class="detail-label">Thời gian xác nhận</span>
              <span class="detail-value">{{ paymentTime }}</span>
            </div>
            
            <div class="detail-card">
              <span class="detail-label">Trạng thái</span>
              <span class="detail-value status-pending">Chờ xác nhận</span>
            </div>
          </div>

          <div class="pending-info">
            <div class="loading-animation">
              <div class="dot"></div>
              <div class="dot"></div>
              <div class="dot"></div>
            </div>
            <p>Tự động chuyển hướng sau vài giây...</p>
          </div>

          <div class="pending-support">
            <h4>Cần hỗ trợ?</h4>
            <p>Liên hệ chúng tôi nếu thanh toán chậm được xác nhận</p>
            <div class="support-contacts">
              <a href="tel:+84123456789" class="contact-link">
                <span>📞</span> +84-123-456-789
              </a>
              <a href="mailto:support@cleanzy.com" class="contact-link">
                <span>✉️</span> support@cleanzy.com
              </a>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn-continue" @click="() => { closePendingPaymentModal(); router.push('/dss/customer-orders?status=pending'); }">
            Xem đơn hàng của tôi →
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

/* Form errors styles */
.form-errors {
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 12px;
  padding: 1rem;
  margin: 1rem 0;
}

.form-errors h4 {
  color: #ef4444;
  font-size: 1rem;
  font-weight: 600;
  margin: 0 0 0.75rem 0;
}

.form-errors ul {
  margin: 0;
  padding: 0;
  list-style: none;
}

.error-item {
  color: #ef4444;
  font-size: 0.875rem;
  margin: 0.5rem 0;
  padding: 0.25rem 0;
  border-bottom: 1px solid #fecaca;
}

.error-item:last-child {
  border-bottom: none;
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

/* Bank Transfer Modal Styles */
.bank-transfer-modal {
  max-width: 500px;
}

.qr-section {
  text-align: center;
  margin-bottom: 2rem;
}

.qr-container {
  display: flex;
  justify-content: center;
  margin-bottom: 1rem;
}

.qr-border {
  border: 6px solid #8fbef6;
  padding: 10px;
  background: white;
  border-radius: 8px;
}

.qr-inner {
  width: 150px;
  height: 150px;
  background: #f3f4f6;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
}

.qr-hint {
  font-size: 0.875rem;
  color: var(--text-light);
  margin: 0;
}

.bank-form {
  margin: 1.5rem 0;
}

.bank-form h3 {
  font-size: 1rem;
  font-weight: 600;
  margin: 0 0 1rem;
  color: var(--text-dark);
}

.bank-form .form-group {
  margin-bottom: 1rem;
}

.bank-form .form-group label {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-light);
  margin-bottom: 0.5rem;
}

.bank-form .input-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 0 0.75rem;
}

.bank-form .form-input {
  flex: 1;
  border: none;
  padding: 0.75rem 0;
  background: transparent;
  color: var(--text-dark);
  font-weight: 500;
}

.copy-btn {
  background: #e6f0ee;
  border: none;
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.75rem;
  font-weight: 600;
  color: #047857;
  transition: all 0.2s;
  white-space: nowrap;
}

.copy-btn:hover {
  background: #d1fae5;
}

/* Pending Payment Modal Styles */
.pending-payment-modal {
  max-width: 450px;
  text-align: center;
}

.pending-icon-container {
  display: flex;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.pending-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #047857;
  margin: 0 0 0.5rem;
}

.pending-subtitle {
  font-size: 0.875rem;
  color: var(--text-light);
  margin: 0 0 1.5rem;
}

.payment-details-box {
  background: var(--bg-light);
  border-radius: 12px;
  padding: 1rem;
  margin: 1rem 0;
  border: 1px solid rgba(4, 120, 87, 0.1);
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid #e5e7eb;
}

.detail-row:last-child {
  border-bottom: none;
}

.detail-label {
  font-size: 0.875rem;
  color: var(--text-light);
  font-weight: 500;
}

.detail-value {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-dark);
}

/* Contact Box */
.contact-box {
  background: #d1fae5;
  border-radius: 12px;
  padding: 1rem;
  margin: 1.5rem 0;
}

.contact-box h4 {
  font-size: 0.875rem;
  color: #6b7280;
  margin: 0 0 1rem;
  line-height: 1.4;
  font-weight: 600;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
  font-size: 0.875rem;
  color: #1f2937;
}

.contact-item:last-child {
  margin-bottom: 0;
}

.contact-icon {
  font-size: 1.25rem;
  min-width: 20px;
}

.radio-container.selected {
  border-color: var(--primary);
  background-color: var(--bg-light);
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
}
</style>
