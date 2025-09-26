<script setup>
definePageMeta({
  layout: "anonymous",
});

import { computed, watchEffect } from "vue";
import { useRouter } from "vue-router";
import { useOauthStore } from "@/stores/oauth";
import GuestInfo from "@/components/GuestInfo.vue";

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
  <!-- Guest sẽ hiển thị component riêng -->
  <GuestInfo v-if="isGuest" />
  <!-- Admin/Staff sẽ redirect nên không cần hiển thị gì ở đây -->
</template>
