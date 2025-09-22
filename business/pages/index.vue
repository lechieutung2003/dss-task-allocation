<template>
    <p>Test index page</p>
    <Dashboard v-if="isAdmin" />
    <EmployeeInfo v-else-if="isEmployee" />
    <GettingStarted v-else />
</template>

<script setup>
definePageMeta({
  layout: 'anonymous'
})

import { useOauthStore } from '@/stores/oauth';
import Dashboard from '@/components/Dashboard.vue'
import EmployeeInfo from '@/components/EmployeeInfo.vue'
const oauthStore = useOauthStore()


// const isAdmin = computed(() => {
//   if(oauthStore.hasOneOfScopes(['__all__'])){
//     const { tokenInfo } = oauthStore;
//     if (!tokenInfo) return false;
//     const { access_token } = tokenInfo;
//     if (!access_token) return false;
//     return access_token.length > 0;
//   }
// })

// const isEmployee = computed(() => {
//   if(oauthStore.hasOneOfScopes(['employees:view'])) {
//     const { tokenInfo } = oauthStore;
//     if (!tokenInfo) return false;
//     const { access_token } = tokenInfo;
//     if (!access_token) return false;
//     return access_token.length > 0;
//   }
// })

const isAdmin = computed(() => oauthStore.hasOneOfScopes(['admin:view']))
const isEmployee = computed(() => oauthStore.hasOneOfScopes(['employees:view']))

// console.log('oauthStore:', oauthStore)
// console.log('tokenInfo:', oauthStore.tokenInfo)
console.log('scope:', oauthStore.tokenInfo.scope)
console.log('isAdmin:', isAdmin.value)
console.log('isEmployee:', isEmployee.value)

</script>
