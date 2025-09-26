<script setup>
definePageMeta({
  layout: "anonymous",
});

import { computed, watchEffect } from "vue";
import { useRouter } from "vue-router";
import { useOauthStore } from "@/stores/oauth";
import GuestInfo from "@/components/GuestInfo.vue";
import LoginForm from "@/components/LoginForm.vue";

const router = useRouter();
const oauthStore = useOauthStore();

// Xác định quyền
const isAdmin = computed(() => {
  return oauthStore.hasAllScopes([
    "users:view",
    "users:edit",
    "roles:view",
    "roles:edit",
  ]);
});

const isStaff = computed(() => {
  return oauthStore.hasOneOfScopes(["employees:view", "tasks:view-mine"]);
});

const isGuest = computed(() => {
  return (
    oauthStore.hasAllScopes(["users:view-mine"]) &&
    !oauthStore.hasOneOfScopes(["employees:view", "roles:view"])
  );
});
const isEmployee = computed(() => {
  return oauthStore.hasOneOfScopes(["employees:view"]);
});


const isLoggedIn = computed(() => !!oauthStore.tokenInfo?.access_token);

watchEffect(() => {
  if (isLoggedIn.value) {
    if (isAdmin.value || isEmployee.value || isStaff.value) {
      router.push("/dss/dashboard");
    } else if (isGuest.value) {
      router.push("/dss/home");
    }
  }
});



console.log("isAdmin:", isAdmin.value);
console.log("isStaff:", isStaff.value);
console.log("isGuest:", isGuest.value);
console.log("tokenInfo:", oauthStore.tokenInfo);
</script>

<template>
  <div class="center-container">
    <div style="width:100%;max-width:500px;">
      <LoginForm v-if="!isLoggedIn" />
      <div v-if="!isLoggedIn" class="welcome-text" style="text-align:center;margin-top:24px;color:#444;font-size:16px;">
        Chào mừng bạn đến với hệ thống quản lý dịch vụ!<br>
        Vui lòng đăng nhập để sử dụng các chức năng đặt dịch vụ, quản lý đơn hàng và xem thông tin cá nhân.
      </div>
      <GuestInfo v-else-if="isGuest" />
    </div>
  </div>
</template>
<style scoped>
.center-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
.welcome-text {
  margin-top: 24px;
  color: #444;
  font-size: 16px;
  text-align: center;
}
</style>