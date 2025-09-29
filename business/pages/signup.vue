<template>
  <div class="h-screen w-full flex justify-center items-center bg-gray-50">
    <div class="form">
      <div class="form-header">
        <h1 class="form-title">{{ $t('create_account_title') }}</h1>
        <p class="form-subtitle">{{ $t('create_account_subtitle') }}</p>
      </div>
      <form @submit.prevent="submitForm" class="grid grid-cols-1 md:grid-cols-2 gap-3">
        <!-- First Name -->
        <div class="flex-column">
          <label>{{ $t('first_name') }}</label>
          <div class="inputForm">
            <input
              v-model="form.first_name"
              type="text"
              class="input"
              :placeholder="$t('first_name')"
            />
          </div>
        </div>

        <!-- Last Name -->
        <div class="flex-column">
          <label>{{ $t('last_name') }}</label>
          <div class="inputForm">
            <input
              v-model="form.last_name"
              type="text"
              class="input"
              :placeholder="$t('last_name')"
            />
          </div>
        </div>

        <!-- Email -->
        <div class="flex-column">
          <label>{{ $t('email') }}</label>
          <div class="inputForm" :class="{ 'error-border': emailError }">
            <input
              v-model="form.email"
              type="email"
              class="input"
              :placeholder="$t('email')"
              @blur="validateEmail"
            />
          </div>
          <span v-if="emailError" class="error-text">{{ emailError }}</span>
        </div>

        <!-- Password -->
        <div class="flex-column">
          <label>{{ $t('password') }}</label>
          <div class="inputForm" :class="{ 'error-border': passwordError }">
            <input
              v-model="form.password"
              type="password"
              class="input"
              :placeholder="$t('password')"
              @blur="validatePassword"
            />
          </div>
          <span v-if="passwordError" class="error-text">{{ passwordError }}</span>
        </div>

        <!-- Phone -->
        <div class="flex-column">
          <label>{{ $t('phone') }}</label>
          <div class="inputForm">
            <input
              v-model="form.phone"
              type="text"
              class="input"
              :placeholder="$t('phone')"
            />
          </div>
        </div>

        <!-- Address -->
        <div class="flex-column">
          <label>{{ $t('Address') }}</label>
          <div class="inputForm">
            <input
              v-model="form.address"
              type="text"
              class="input"
              :placeholder="$t('Address')"
            />
          </div>
        </div>

        <!-- Area -->
        <div class="flex-column col-span-2">
          <label>{{ $t('area') }}</label>
          <div class="inputForm">
            <input
              v-model="form.area"
              type="text"
              class="input"
              :placeholder="$t('area_placeholder')"
            />
          </div>
        </div>

        <!-- Submit Button -->
        <div class="col-span-2">
          <button type="submit" class="button-submit" :disabled="isLoading">
            <span v-if="isLoading">{{ $t('Registering') }}</span>
            <span v-else>{{ $t('Register') }}</span>
          </button>
        </div>

        <!-- Success Message -->
        <p v-if="isSubmitted" class="p col-span-2">
          {{ $t('Account created for', { email: form.email }) }}
        </p>

        <!-- Login Link -->
        <div class="flex justify-center items-center col-span-2">
          <p class="text-center">
            {{ $t('have_an_account') }}
            <NuxtLink to="/" class="span font-semibold">
              {{ $t('Login') }}
            </NuxtLink>
          </p>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import IconAmoz from '~/assets/icons/BigLogo.svg'
import { ref } from 'vue'
import { ElNotification } from 'element-plus'
import OAuthService from '@/services/oauth'
import '@/assets/css/form.css'

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
.form {
  width: 70%;
  max-width: 80%; 
  height: 87%;
  padding: 40px; 
  background-color: #fff; 
  border-radius: 10px; 
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1); 
  margin-top: 5%;
}
.input {
  width: 400px; 
}
.error-text {
  margin-top: 0.25rem; 
}
</style>