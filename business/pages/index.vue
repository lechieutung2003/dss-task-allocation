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

// redirect nếu là admin hoặc employee
watchEffect(() => {
  if (isAdmin.value || isEmployee.value) {
    router.push("/dss/dashboard");

  } 
  else if (isGuest.value) {
    router.push("/dss/home");
  } else if (isAdmin.value || isStaff.value) {
    router.push("/dss/dashboard");
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