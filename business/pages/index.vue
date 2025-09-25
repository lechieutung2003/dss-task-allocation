<script setup>
definePageMeta({
  layout: "anonymous",
});

import { useRouter } from "vue-router";
import { useOauthStore } from "@/stores/oauth";
import EmployeeInfo from "@/components/EmployeeInfo.vue";
import GuestInfo from "@/components/GuestInfo.vue";
import GettingStarted from "@/components/GettingStarted.vue";

const router = useRouter();
const oauthStore = useOauthStore();

const isAdmin = computed(() => {
  return oauthStore.hasAllScopes([
    "users:view",
    "users:edit",
    "roles:view",
    "roles:edit",
  ]);
});

const isEmployee = computed(() => {
  return oauthStore.hasOneOfScopes(["employees:view", "tasks:view-mine"]);
});

const isGuest = computed(() => {
  return (
    oauthStore.hasAllScopes(["users:view-mine"]) &&
    !oauthStore.hasOneOfScopes(["employees:view", "roles:view"])
  );
});

// redirect nếu là admin hoặc employee
watchEffect(() => {
  if (isAdmin.value || isEmployee.value) {
    router.push("/dss/dashboard");
  }
});

console.log("isAdmin:", isAdmin.value);
console.log("isEmployee:", isEmployee.value);
console.log("isGuest:", isGuest.value);
console.log("tokenInfo:", oauthStore.tokenInfo);
</script>

<template>
  <GuestInfo v-if="isGuest" />
  <GettingStarted v-else />
</template>