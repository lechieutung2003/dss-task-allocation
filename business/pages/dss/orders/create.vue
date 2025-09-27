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
              <label>Số giờ yêu cầu</label>
              <div class="inputForm">
                <input v-model.number="order.requested_hours" type="number" class="input" min="0" step="0.01" placeholder="Nhập số giờ" required />
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
              <label>Giờ ước tính</label>
              <div class="inputForm">
                <input v-model.number="order.estimated_hours" type="number" class="input" min="0" step="0.01" placeholder="Nhập giờ ước tính" required />
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