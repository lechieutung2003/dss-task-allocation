<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { useOauthStore } from '@/stores/oauth';

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
  note: ''
});

// danh sách dịch vụ lấy từ API hoặc tạm thời mock
const serviceTypes = ref([]);

const fetchServiceTypes = async () => {
  try {
    const response = await axios.get('/api/v1/service-types/');
    serviceTypes.value = response.data;
  } catch (error) {
    console.error('Failed to fetch service types', error);
  }
};

const submitOrder = async () => {
  try {
    const payload = {
      customer: order.value.customer,
      service_type: order.value.service_type,
      area_m2: order.value.area_m2,
      requested_hours: order.value.requested_hours,
      preferred_start_time: order.value.preferred_start_time,
      preferred_end_time: order.value.preferred_end_time,
      note: order.value.note
    };

    await axios.post('/api/v1/orders/', payload);

    // chuyển về trang danh sách đơn sau khi tạo xong
    router.push('/dss/orders');
  } catch (error) {
    console.error('Failed to create order', error);
    alert('Tạo đơn thất bại, vui lòng kiểm tra thông tin.');
  }
};

onMounted(() => {
  fetchServiceTypes();
});
</script>

<template>
  <div class="create-order-page">
    <h2 class="page-title">Tạo đơn mới</h2>

    <form @submit.prevent="submitOrder" class="order-form">
      <div class="form-group">
        <label>Dịch vụ</label>
        <select v-model="order.service_type" required>
          <option value="" disabled>Chọn dịch vụ</option>
          <option v-for="service in serviceTypes" :key="service.id" :value="service.id">
            {{ service.name }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label>Diện tích (m²)</label>
        <input v-model.number="order.area_m2" type="number" min="0" step="0.01" required />
      </div>

      <div class="form-group">
        <label>Số giờ yêu cầu</label>
        <input v-model.number="order.requested_hours" type="number" min="0" step="0.01" required />
      </div>

      <div class="form-group">
        <label>Thời gian bắt đầu ưu tiên</label>
        <input v-model="order.preferred_start_time" type="datetime-local" required />
      </div>

      <div class="form-group">
        <label>Thời gian kết thúc ưu tiên</label>
        <input v-model="order.preferred_end_time" type="datetime-local" required />
      </div>

      <div class="form-group">
        <label>Ghi chú</label>
        <textarea v-model="order.note" placeholder="Nhập ghi chú (nếu có)"></textarea>
      </div>

      <button type="submit" class="submit-btn">Tạo đơn</button>
    </form>
  </div>
</template>

<style scoped>
.create-order-page {
  max-width: 600px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}

.page-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  color: #111827;
}

.order-form .form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 1rem;
}

.order-form label {
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: #374151;
}

.order-form input,
.order-form select,
.order-form textarea {
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 0.95rem;
}

.order-form input:focus,
.order-form select:focus,
.order-form textarea:focus {
  border-color: #383737;
  outline: none;
}

.submit-btn {
  background-color: #292828;
  color: white;
  padding: 0.6rem 1.2rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}

.submit-btn:hover {
  background-color: #000000;
  transform: translateY(-1px);
}
</style>
