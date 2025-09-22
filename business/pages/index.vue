<template>
  <Dashboard v-if="isAdmin" />
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

const isAdmin = computed(() => {
  return !oauthStore.tokenInfo.isGuest && oauthStore.tokenInfo.isStaff && oauthStore.tokenInfo.isSuperuser;
});

const isEmployee = computed(() => {
  return !oauthStore.tokenInfo.isGuest && oauthStore.tokenInfo.isStaff && !oauthStore.tokenInfo.isSuperuser;
});

const isGuest = computed(() => {
  return oauthStore.tokenInfo.isGuest && !oauthStore.tokenInfo.isStaff && !oauthStore.tokenInfo.isSuperuser;
});


console.log('isStaff:', oauthStore.tokenInfo.isStaff)
console.log('isSuperuser:', oauthStore.tokenInfo.isSuperuser)
console.log('isGuest:', oauthStore.tokenInfo.isGuest)


</script>
