<script setup>
import { useOauthStore } from '@/stores/oauth';

const store = useOauthStore();
const user = store.user;
</script>

<template>
  <div class="signup-container">
    <div class="form-wrapper">
      <div class="form">
        <!-- Tiêu đề -->
        <div class="form-header">
          <h1 class="form-title">Thông tin tài khoản</h1>
          <p class="form-subtitle">Thông tin cá nhân của bạn được hiển thị tại đây</p>
        </div>

        <div v-if="user" class="signup-columns">
          <div class="signup-column">
            <div class="form-group">
              <label>Email</label>
              <div class="inputForm">
                <span class="input">{{ user.email }}</span>
              </div>
            </div>

            <div class="form-group">
              <label>Họ tên</label>
              <div class="inputForm">
                <span class="input">{{ user.first_name }} {{ user.last_name }}</span>
              </div>
            </div>

            <div class="form-group">
              <label>User Name</label>
              <div class="inputForm">
                <span class="input">{{ user.name }}</span>
              </div>
            </div>
          </div>

          <div class="signup-column">
            <div class="form-group">
              <label>Số điện thoại</label>
              <div class="inputForm">
                <span class="input">{{ user.phone }}</span>
              </div>
            </div>

            <div class="form-group">
              <label>Địa chỉ</label>
              <div class="inputForm">
                <span class="input">{{ user.address }}</span>
              </div>
            </div>

            <div class="form-group">
              <label>Khu vực</label>
              <div class="inputForm">
                <span class="input">{{ user.area }}</span>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="p">
          Không tìm thấy thông tin người dùng.
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* tái sử dụng style của form đăng ký */
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
}

.input {
  margin-left: 10px;
  color: #151717;
  font-size: 15px;
}
</style>
