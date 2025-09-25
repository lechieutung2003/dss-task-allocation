<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useOauthStore } from '@/stores/oauth'
import { useRouter } from 'vue-router'
import axios from 'axios'
import OAuthService from '@/services/oauth'

const store = useOauthStore()
const router = useRouter()
const userDetail = ref<any>(null)
const isCollapse = ref(true)

// Toggle dropdown
const toggleDetail = () => {
  isCollapse.value = !isCollapse.value
}

// Logout
const logout = async () => {
  try {
    await OAuthService.logout()
  } catch (err) {
    console.error(err)
  } finally {
    store.$reset()
    router.push('/')
  }
}

// Lấy thông tin user khi mounted
onMounted(async () => {
  if (store.accessToken) {
    try {
      const response = await axios.get('http://localhost:8008/api/v1/employees/userinfo', {
        headers: {
          Authorization: `Bearer ${store.accessToken}`
        }
      })
      userDetail.value = response.data
      console.log('User info:', userDetail.value)
    } catch (err) {
      console.error('Lấy thông tin user thất bại:', err)
    }
  }
})

// Đóng dropdown khi click ngoài
function handleClickOutside(event: MouseEvent) {
  const dropdownElement = document.querySelector('.user-menu')
  if (dropdownElement && !dropdownElement.contains(event.target as Node)) {
    isCollapse.value = true
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<template>
  <div class="user-menu">
    <div class="user-menu__wrapper" @click.stop="toggleDetail">
      <template v-if="userDetail">
        <div class="user-menu__info">
          <span class="user-menu__greeting">Hello,</span>
          <span class="user-menu__name">{{ userDetail.first_name }} {{ userDetail.last_name }}</span>
        </div>
      </template>

      <template v-else>
        <div class="user-menu__info user-menu__not-logged">
          <span>Not logged in</span>
        </div>
      </template>
    </div>

    <div v-if="userDetail && !isCollapse" class="user-menu__dropdown">

  <p><strong>First Name:</strong> {{ userDetail.first_name }}</p>
  <p><strong>Last Name:</strong> {{ userDetail.last_name }}</p>

  <button class="btn-logout" @click="logout">Logout</button>
</div>

  </div>
</template>
