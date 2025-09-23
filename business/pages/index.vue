<template>
  <EmployeeInfo v-if="isAdmin" />
  <EmployeeInfo v-else-if="isEmployee" />
  <GuestInfo v-else-if="isGuest" />
  <GettingStarted v-else />
</template>

<script setup>
definePageMeta({
  layout: 'anonymous'
})

import { useOauthStore } from '@/stores/oauth';
import Dashboard from '@/components/Dashboard.vue'
import EmployeeInfo from '@/components/EmployeeInfo.vue'
import GuestInfo from '@/components/GuestInfo.vue'
const oauthStore = useOauthStore()

// const isAdmin = computed(() => {
//   return !oauthStore.tokenInfo.isGuest && oauthStore.tokenInfo.isStaff && oauthStore.tokenInfo.isSuperuser;
// });

// const isEmployee = computed(() => {
//   return !oauthStore.tokenInfo.isGuest && oauthStore.tokenInfo.isStaff && !oauthStore.tokenInfo.isSuperuser;
// });

// const isGuest = computed(() => {
//   return oauthStore.tokenInfo.isGuest && !oauthStore.tokenInfo.isStaff && !oauthStore.tokenInfo.isSuperuser;
// });

const isAdmin = computed(() => {
  return oauthStore.hasAllScopes(['users:view', 'users:edit', 'roles:view', 'roles:edit']);
});

const isEmployee = computed(() => {
  return oauthStore.hasOneOfScopes(['employees:view', 'tasks:view-mine']);
});

const isGuest = computed(() => {
  return oauthStore.hasAllScopes(['users:view-mine']) && 
         !oauthStore.hasOneOfScopes(['employees:view', 'roles:view']);
});

console.log('isAdmin:', isAdmin.value);
console.log('isEmployee:', isEmployee.value);
console.log('isGuest:', isGuest.value);
console.log('tokenInfo:', oauthStore.tokenInfo);

</script>
