<script setup>
definePageMeta({ layout: "anonymous", middleware: ["auth"] });
import Sidebar from "@/components/sidebar/index.vue";
import { useOauthStore } from "@/stores/oauth";
const oauthStore = useOauthStore();

const isAdmin = computed(() =>
  oauthStore.hasAllScopes([
    "users:view",
    "users:edit",
    "roles:view",
    "roles:edit",
  ])
);
const isUser = computed(() =>
  oauthStore.hasOneOfScopes(["employees:view", "tasks:view-mine"])
);
</script>

<template>
  <div class="flex flex-row w-full h-full">
    <Sidebar>
      <template #header>
        <h3 class="text-lg font-bold text-white py-2">DSS Dashboard</h3>
      </template>
      <el-menu-item v-if="isAdmin" index="/dss/users">
        <span>Quản lý nhân viên</span>
      </el-menu-item>
      <el-menu-item v-if="isAdmin" index="/dss/services">
        <span>Quản lý dịch vụ</span>
      </el-menu-item>
      <el-menu-item v-if="isAdmin || isUser" index="/dss/orders">
        <span>Quản lý đơn hàng</span>
      </el-menu-item>
      <el-menu-item index="/dss/profile/employee">
        <span>Thông tin cá nhân</span>
      </el-menu-item>
    </Sidebar>
    <div class="flex-auto p-4">
      <h2 class="text-xl font-semibold mb-4">Dashboard DSS</h2>
      <!-- Nội dung dashboard ở đây -->
    </div>
  </div>
</template>
