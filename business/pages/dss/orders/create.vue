<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import OrderService from '@/services/dss/order';
import { useOauthStore } from '@/stores/oauth';
import serviceTypesApi from '@/services/dss/serviceTypes';

const store = useOauthStore();
const router = useRouter();

// form data



const order = ref({
  customer: store.user?.id || null,
  service_type: null,
  area_m2: null,
  requested_hours: null,
  preferred_start_time: '',
  preferred_end_time: '',
  estimated_hours: null,
  status: 'pending',
  note: ''
});

const productivity = ref<number | null>(null);

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
    } else if (service.name?.toLowerCase().includes('regular')) {
      productivity.value = 40;
    } else if (service.name?.toLowerCase().includes('deep')) {
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
    return;
  }
  order.value.estimated_hours = +(area / productivity.value).toFixed(2);
};

watch(() => [order.value.service_type], calcProductivity);
watch(() => [order.value.area_m2, productivity.value], calcEstimatedHours);

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

import { watch } from 'vue';
watch(() => [order.value.preferred_start_time, order.value.preferred_end_time], calcRequestedHours);

const estimatedPrice = ref<number | null>(null);

const calcEstimatedPrice = () => {
  const serviceId = order.value.service_type;
  const area = order.value.area_m2;
  if (!serviceId || !area || area <= 0) {
    estimatedPrice.value = null;
    return;
  }
  let pricePerM2 = 0;
  // Tìm theo id dịch vụ
  const service = serviceTypes.value.find(s => s.id === serviceId);
  if (service) {
    // Nếu có trường price_per_m2 thì dùng luôn
    if (service.price_per_m2) {
      pricePerM2 = Number(service.price_per_m2);
    } else if (service.name?.toLowerCase().includes('deeplearning')) {
      pricePerM2 = 30000;
    } else if (service.name?.toLowerCase().includes('regularcleaning')) {
      pricePerM2 = 155000;
    }
  }
  let price = pricePerM2 > 0 ? pricePerM2 * area : null;
  // Áp dụng hệ số nếu thời gian khách chọn < giờ ước tính
  const requested = order.value.requested_hours;
  const estimated = order.value.estimated_hours;
  if (price && requested && estimated && requested < estimated) {
    const diff = estimated - requested ;
    let factor = 1;
    if (diff > 0.1 && diff <= 1) factor = 1.2;
    else if (diff > 1 && diff <= 2) factor = 1.3;
    else if (diff > 2) factor = 1.5;
    price = price * factor;
  }
  estimatedPrice.value = price;
};

// Theo dõi thay đổi dịch vụ, diện tích, requested_hours, estimated_hours để cập nhật giá
import { watch } from 'vue';
watch(() => [order.value.service_type, order.value.area_m2, order.value.requested_hours, order.value.estimated_hours], calcEstimatedPrice);

type ServiceType = { id: string; name: string; [key: string]: any };
const serviceTypes = ref<ServiceType[]>([]);
const fetchServiceTypes = async () => {
  const response = await serviceTypesApi.getAll();
  // Nếu response là object có results
  if (response && response.results) {
    serviceTypes.value = response.results;
  } else if (Array.isArray(response)) {
    serviceTypes.value = response;
  } else {
    serviceTypes.value = [];
  }
  console.log('serviceTypes.value:', serviceTypes.value);
};

const submitOrder = async () => {
  try {
    const payload = { ...order.value };
    const response = await OrderService.createOrder(payload);
    console.log('API response:', response);
    if (response && response.id) {
      alert('Tạo đơn thành công!');
      router.push('/dss/customer-orders');
    } else {
      alert('Tạo đơn thất bại, vui lòng kiểm tra thông tin.');
      console.error('Lỗi tạo đơn:', response);
    }
  } catch (error) {
    console.error('Failed to create order', error?.response?.data || error);
    alert('Tạo đơn thất bại, vui lòng kiểm tra thông tin.');
  }
};
// Format số giờ thập phân thành giờ và phút
function formatHourMinute(hours: number|null) {
  if (hours === null || isNaN(hours)) return '';
  // Nếu nhỏ hơn 1 phút thì hiện 1 phút
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
                <input v-model.number="order.area_m2" type="number" class="input" min="0" step="0.01" placeholder="Nhập diện tích" required />
              </div>
            </div>
            <div class="form-group">
              <label>Giá ước tính</label>
              <div class="inputForm">
                <input type="text" :value="estimatedPrice !== null ? estimatedPrice.toLocaleString('vi-VN') + ' VNĐ' : ''" class="input" disabled placeholder="Giá ước tính sẽ tự động tính" style="color:#ef4444;font-weight:700;" />
              </div>
            </div>
            <div class="form-group">
              <label>Số giờ yêu cầu</label>
              <div class="inputForm">
                  <input type="text" :value="order.requested_hours !== null ? formatHourMinute(order.requested_hours) : ''" class="input" readonly placeholder="Số giờ yêu cầu sẽ tự động tính" style="color:#ef4444;font-weight:700;" />
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
            <div class="form-group">
              <label>Trạng thái</label>
              <div class="inputForm">
                <select v-model="order.status" class="input" required>
                  <option value="pending">Chờ xử lý</option>
                  <option value="processing">Đang xử lý</option>
                  <option value="done">Hoàn thành</option>
                </select>
              </div>
            </div>
          </div>
        </div>
        <button type="submit" class="button-submit">Tạo đơn</button>
      </form>
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
</style>