<template>
  <div class="lg:py-10 py-6 lg:px-12 px-6 min-w-280 sm:w-full h-full bg-white rounded-lg drop-shadow-md">
    <main class="w-full">
      <div class="w-full md:max-w-[550px] max-w-[450px] mx-auto">
        <!-- Header -->
        <div class="form-header">
          <h1 class="form-title">Trang cá nhân</h1>
          <p class="form-subtitle">Xem thông tin và tạo đơn hàng</p>
        </div>

        <!-- Thông tin cá nhân -->
        <div class="flex-column mb-4">
          <label>Họ và tên</label>
          <div class="inputForm">
            <input v-model="user.name" type="text" class="input" disabled />
          </div>
        </div>

        <div class="flex-column mb-4">
          <label>Email</label>
          <div class="inputForm">
            <input v-model="user.email" type="email" class="input" disabled />
          </div>
        </div>

        <div class="flex-column mb-4">
          <label>Số điện thoại</label>
          <div class="inputForm">
            <input v-model="user.phone" type="text" class="input" disabled />
          </div>
        </div>

        <!-- Form tạo đơn hàng -->
        <form class="form" @submit.prevent="createOrder">
          <div class="form-header">
            <h2 class="form-title">Tạo đơn hàng</h2>
          </div>

          <div class="flex-column">
            <label>Sản phẩm</label>
          </div>
          <div class="inputForm">
            <select v-model="order.product" class="input">
              <option disabled value="">-- Chọn sản phẩm --</option>
              <option v-for="product in products" :key="product.id" :value="product.name">
                {{ product.name }}
              </option>
            </select>
          </div>

          <div class="flex-column">
            <label>Số lượng</label>
          </div>
          <div class="inputForm">
            <input v-model.number="order.quantity" type="number" min="1" class="input" />
          </div>

          <button type="submit" class="button-submit">
            Đặt hàng
          </button>
        </form>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from "vue";

const user = ref({
  name: "Nguyễn Văn A",
  email: "a6@gmail.com",
  phone: "0123456789",
});

const products = ref([
  { id: 1, name: "Sản phẩm 1" },
  { id: 2, name: "Sản phẩm 2" },
]);

const order = ref({
  product: "",
  quantity: 1,
});

const createOrder = () => {
  if (!order.value.product) {
    alert("Vui lòng chọn sản phẩm!");
    return;
  }
  alert(`Đã tạo đơn hàng: ${order.value.product} x ${order.value.quantity}`);
};
</script>

<style scoped>
/* Dùng lại style từ form login */
.form-header {
  text-align: center;
  margin-bottom: 20px;
}
.form-title {
  font-size: 22px;
  font-weight: 700;
  margin-bottom: 8px;
}
.form-subtitle {
  font-size: 14px;
  color: #666;
  margin: 0;
}
.inputForm {
  border: 1.5px solid #ecedec;
  border-radius: 10px;
  height: 45px;
  display: flex;
  align-items: center;
  padding: 0 10px;
  margin-bottom: 10px;
}
.input {
  border: none;
  width: 100%;
  background: transparent;
}
.input:focus {
  outline: none;
}
.button-submit {
  margin-top: 10px;
  background-color: #151717;
  border: none;
  color: white;
  font-size: 15px;
  font-weight: 500;
  border-radius: 10px;
  height: 45px;
  width: 100%;
  cursor: pointer;
}
.button-submit:hover {
  background-color: #252727;
}
</style>
