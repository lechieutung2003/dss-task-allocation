<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import serviceTypesApi from "@/services/dss/serviceTypes.js";

const router = useRouter();
const services = ref([]);
const loading = ref(false);
const error = ref("");

const fetchServices = async () => {
  loading.value = true;
  error.value = "";
  try {
    const res = await serviceTypesApi.getAll();
    services.value = Array.isArray(res.results)
      ? res.results
      : Array.isArray(res)
      ? res
      : [];
  } catch (e) {
    error.value = "Không thể tải danh sách dịch vụ";
  } finally {
    loading.value = false;
  }
};

onMounted(fetchServices);
</script>

<template>
  <div class="signup-container">
    <div class="form-wrapper">
      <div class="form-header">
        <h1 class="form-title">Danh sách dịch vụ hệ thống</h1>
        <p class="form-subtitle">Chọn dịch vụ để đặt đơn hàng</p>
      </div>
      <div v-if="error" class="text-red-600 mb-2">{{ error }}</div>
      <div class="form">
        <div class="service-grid">
          <div v-for="service in services" :key="service.id" class="service-card">
            <div class="service-image">
              <img v-if="service.image_url" :src="service.image_url" alt="Hình dịch vụ" />
              <div v-else class="image-placeholder">Ảnh dịch vụ</div>
            </div>
            <div class="service-info">
              <div class="service-title">{{ service.name }}</div>
              <div class="service-detail"><b>Giá/m2:</b> {{ service.price_per_m2 }}</div>
              <div class="service-detail"><b>Tốc độ (m2/h):</b> {{ service.cleaning_rate_m2_per_h }}</div>
              <div class="service-detail"><b>Mô tả:</b> {{ service.description || 'Chưa có mô tả' }}</div>
            </div>
            <el-button class="button-submit" size="small" @click="router.push(`/dss/orders/create?service=${service.id}`)">
              Đặt dịch vụ này
            </el-button>
          </div>
        </div>
        <div v-if="!loading && services.length === 0" class="text-center text-gray-500 py-8">
          Không có dữ liệu
        </div>
      </div>

 </div>
  </div>
</template>

<style scoped>
/* Card dịch vụ */
.service-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 24px;
}

.service-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  min-height: 320px;
}

.service-image {
  width: 100%;
  max-width: 180px;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f6f6f6;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 10px;
}
.service-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.image-placeholder {
  color: #aaa;
  font-size: 15px;
}
.service-info {
  width: 100%;
  text-align: left;
  margin-bottom: 8px;
}
.service-title {
  font-size: 18px;
  font-weight: 700;
  color: #151717;
  margin-bottom: 6px;
}
.service-detail {
  font-size: 15px;
  color: #444;
  margin-bottom: 3px;
}
   
.signup-container {
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

.error-border {
  border-color: #ef4444 !important;
}

.error-text {
  color: #ef4444;
  font-size: 12px;
  margin-top: 3px;
}

.button-submit {
  background-color: #151717;
  border: none;
  color: white;
  font-size: 15px;
  font-weight: 500;
  border-radius: 10px;
  height: 40px;
  min-width: 120px;
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

.p {
  text-align: center;
  font-size: 14px;
  margin: 5px 0;
}

.link {
  color: #2d79f3;
  font-weight: 500;
  text-decoration: none;
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
  color: #6b7280; /* xám nhạt */
  font-weight: 400;
  margin: 0;
}
</style>
