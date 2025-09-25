<template>
  <div class="signup-container">
    <div class="form-wrapper">
      <form class="form" @submit.prevent="submitForm">
        <!-- Tiêu đề -->
        <div class="form-header">
          <h1 class="form-title">{{ $t('Create your account') }}</h1>
          <p class="form-subtitle">{{ $t('Sign up to get started') }}</p>
        </div>

        <!-- Hai cột -->
        <div class="signup-columns">
          <!-- Cột trái -->
          <div class="signup-column">
            <div class="form-group">
              <label>First Name</label>
              <div class="inputForm">
                <input v-model="form.first_name" type="text" class="input" placeholder="First Name" />
              </div>
            </div>

            <div class="form-group">
              <label>Last Name</label>
              <div class="inputForm">
                <input v-model="form.last_name" type="text" class="input" placeholder="Last Name" />
              </div>
            </div>

            <div class="form-group">
              <label>Full Name</label>
              <div class="inputForm">
                <input v-model="form.name" type="text" class="input" placeholder="Full Name" />
              </div>
            </div>

            <div class="form-group">
              <label>Email</label>
              <div class="inputForm" :class="{ 'error-border': emailError }">
                <input v-model="form.email" type="email" class="input" placeholder="Email" @blur="validateEmail" />
              </div>
              <span v-if="emailError" class="error-text">{{ emailError }}</span>
            </div>
          </div>

          <!-- Cột phải -->
          <div class="signup-column">
            <div class="form-group">
              <label>Password</label>
              <div class="inputForm" :class="{ 'error-border': passwordError }">
                <input v-model="form.password" type="password" class="input" placeholder="Password" @blur="validatePassword" />
              </div>
              <span v-if="passwordError" class="error-text">{{ passwordError }}</span>
            </div>

            <div class="form-group">
              <label>Phone</label>
              <div class="inputForm">
                <input v-model="form.phone" type="text" class="input" placeholder="Phone" />
              </div>
            </div>

            <div class="form-group">
              <label>Address</label>
              <div class="inputForm">
                <input v-model="form.address" type="text" class="input" placeholder="Address" />
              </div>
            </div>

            <div class="form-group">
              <label>Area</label>
              <div class="inputForm">
                <select v-model="form.area" class="input">
                  <option disabled value="">Select area</option>
                  <option value="urban">Urban</option>
                  <option value="suburban">Suburban</option>
                  <option value="vip">Vip</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        <!-- Nút submit -->
        <button type="submit" class="button-submit" :disabled="isLoading">
          <span v-if="isLoading">Đang đăng ký...</span>
          <span v-else>Đăng ký</span>
        </button>

        <!-- Thông báo thành công -->
        <p v-if="isSubmitted" class="p">
          {{ $t('Account created for', { email: form.email }) }}
        </p>

        <!-- Link đăng nhập -->
        <p class="p">
          Đã có tài khoản?
          <NuxtLink to="/" class="link">Đăng nhập</NuxtLink>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import IconAmoz from '~/assets/icons/BigLogo.svg'
import { ref } from 'vue'
import { ElNotification } from 'element-plus'
import OAuthService from '@/services/oauth'

definePageMeta({
  layout: 'anonymous'
})

const form = ref({
  email: '',
  password: '',
  first_name: '',
  last_name: '',
  name: '',
  phone: '',
  address: '',
  area: ''
})

const isLoading = ref(false)
const isSubmitted = ref(false)
const emailError = ref('')
const passwordError = ref('')

const validateEmail = () => {
  if (!form.value.email) {
    emailError.value = 'Email không được để trống'
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email)) {
    emailError.value = 'Email không hợp lệ'
  } else {
    emailError.value = ''
  }
}

const validatePassword = () => {
  if (!form.value.password) {
    passwordError.value = 'Mật khẩu không được để trống'
  } else if (form.value.password.length < 6) {
    passwordError.value = 'Mật khẩu tối thiểu 6 ký tự'
  } else {
    passwordError.value = ''
  }
}

const validateForm = () => {
  validateEmail()
  validatePassword()
  return !emailError.value && !passwordError.value
}

const submitForm = async () => {
  if (!validateForm()) return
  isLoading.value = true
  try {
    await OAuthService.registerCustomer(form.value)
    isSubmitted.value = true
    ElNotification({
      title: 'Thành công',
      message: 'Tài khoản đã được tạo',
      type: 'success',
      duration: 5000
    })
  } catch (error: any) {
    ElNotification({
      title: 'Lỗi',
      message: error.message || 'Có lỗi xảy ra khi đăng ký',
      type: 'error',
      duration: 5000
    })
  } finally {
    isLoading.value = false
  }
}
</script>
<style scoped>
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