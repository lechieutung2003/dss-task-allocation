<script setup lang="ts">
import { useOauthStore } from '@/stores/oauth';
import { useRouter } from 'vue-router';

const store = useOauthStore();
const router = useRouter();

// Hàm điều hướng tới trang tạo đơn
const goToCreateOrder = () => {
  router.push('/dss/orders/create');
};
</script>

<template>
  <nav class="user-menu">
    <div class="user-menu__wrapper">
      <!-- Nếu đã đăng nhập -->
      <template v-if="store.user">
        <div class="user-menu__info">
          <span class="user-menu__greeting">Hello,</span>
          <span class="user-menu__name">{{ store.user.first_name }} {{ store.user.last_name }}</span>
        </div>

        <!-- Button tạo đơn -->
        <button
          class="create-order-btn"
          @click="goToCreateOrder"
        >
          Tạo đơn
        </button>
      </template>

      <!-- Nếu chưa đăng nhập -->
      <template v-else>
        <div class="user-menu__info user-menu__not-logged">
          <span>Not logged in</span>
        </div>
      </template>
    </div>
  </nav>
</template>

<style scoped>
.user-menu {
  display: flex;
  justify-content: flex-start; /* nằm bên trái */
  padding: 1.5rem 2rem;
  background-color: #f3f4f6;
  box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}

.user-menu__wrapper {
  display: flex;
  align-items: center;
  gap: 1rem;
  background-color: #fff;
  padding: 0.5rem 1.25rem;
  border-radius: 12px;
  box-shadow: 0 3px 12px rgba(0,0,0,0.08);
  transition: all 0.2s ease-in-out;
}

.user-menu__wrapper:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(0,0,0,0.1);
}

.user-menu__info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.user-menu__greeting {
  font-weight: 500;
  color: #111827;
}

.user-menu__name {
  font-weight: 700;
  color: #2563eb;
}

.create-order-btn {
  padding: 0.3rem 0.8rem;
  background-color: #000000;
  color: white;
  font-weight: 600;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}

.create-order-btn:hover {
  background-color: #000000;
  transform: translateY(-1px);
}

.user-menu__not-logged {
  font-weight: 500;
  color: #6b7280;
}

/* Responsive cho mobile */
@media (max-width: 768px) {
  .user-menu {
    justify-content: center; /* mobile vẫn center */
    padding: 1rem;
  }
  .user-menu__wrapper {
    padding: 0.5rem 1rem;
    gap: 0.75rem;
  }
  .create-order-btn {
    margin-left: 0;
  }
}
</style>
