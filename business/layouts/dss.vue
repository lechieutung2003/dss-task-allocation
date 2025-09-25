<template>
  <div class="w-full h-full flex bg-tertiary-light align-center justify-center">
    <div v-if="!authenticated" class="lg:py-20 py-6">
      <LoginForm>
        <div class="flex text-center justify-center">
          <AmozLogo class="h-20" />
        </div>
        <div class="my-5">
          <p class="lg:text-l text-center font-bold">
            {{ $t("welcome_to_dss") }}
          </p>
        </div>
      </LoginForm>
    </div>
    <div v-else class="absolute w-full">
      <TopbarNav />
      <div class="flex flex-row">
        <aside>
          <Sidebar>
            <template #header>
              <h5 class="text-white font-bold">DSS</h5>
            </template>
            <el-menu-item index="/dss/dashboard">
              <span>Dashboard</span>
            </el-menu-item>
            <el-menu-item index="/dss/services">
              <span>Quản lý Dịch vụ</span>
            </el-menu-item>
            <el-menu-item index="/dss/orders">
              <span>Quản lý Đơn hàng</span>
            </el-menu-item>
            <el-menu-item index="/dss/employees">
              <span>Quản lý Nhân viên</span>
            </el-menu-item>
            <el-menu-item index="/dss/customers">
              <span>Quản lý Khách hàng</span>
            </el-menu-item>
            <el-menu-item index="/dss/tasks">
              <span>Giao task cho nhân viên</span>
            </el-menu-item>
            <el-menu-item index="/dss/profile">
              <span>Thông tin cá nhân</span>
            </el-menu-item>
          </Sidebar>
        </aside>
        <div class="flex-auto">
          <slot />
        </div>
      </div>
      <footer class="w-full bg-gray-100 flex justify-center">
        <FooterContent />
      </footer>
    </div>
  </div>
</template>

<script setup>
import AmozLogo from "/assets/icons/Logo.svg";
import { useOauthStore } from "@/stores/oauth";

const { t } = useI18n();

const oauthStore = useOauthStore();
const authenticated = computed(() => {
  const { tokenInfo } = oauthStore;
  if (!tokenInfo) return false;
  const { access_token } = tokenInfo;
  if (!access_token) return false;
  return access_token.length > 0;
});
</script>

<style scoped></style>
