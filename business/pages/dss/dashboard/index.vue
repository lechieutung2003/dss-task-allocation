<script setup>
import { ref, reactive, computed } from "vue";
import {
  Briefcase,
  User,
  Calendar,
  CircleCheckFilled,
  Warning,
  Location,
  TrendCharts,
  Wallet,
} from "@element-plus/icons-vue";

definePageMeta({ layout: "dss", middleware: ["auth"] });

// Mock data - trong thực tế sẽ lấy từ API
const dashboardData = reactive({
  overview: {
    totalTasks: 156,
    activeTasks: 45,
    completedTasks: 98,
    totalEmployees: 28,
    todayRevenue: 12500000,
    customerSatisfaction: 4.8,
  },
  urgentTasks: [
    {
      id: 1,
      title: "Vệ sinh văn phòng ABC Corp",
      deadline: "2025-09-28 14:00",
      location: "Quận 1, TP.HCM",
      priority: "Cao",
    },
    {
      id: 2,
      title: "Dọn dẹp nhà riêng",
      deadline: "2025-09-28 16:30",
      location: "Quận 7, TP.HCM",
      priority: "Trung bình",
    },
    {
      id: 3,
      title: "Vệ sinh khách sạn XYZ",
      deadline: "2025-09-29 08:00",
      location: "Quận 3, TP.HCM",
      priority: "Cao",
    },
  ],
  recentActivities: [
    {
      id: 1,
      activity: "Nhân viên Nguyễn Văn A hoàn thành nhiệm vụ tại Building DEF",
      time: "10 phút trước",
    },
    {
      id: 2,
      activity: "Phân công nhiệm vụ mới cho nhóm 3",
      time: "25 phút trước",
    },
    {
      id: 3,
      activity: "Khách hàng GHI Corp đánh giá 5 sao",
      time: "1 giờ trước",
    },
  ],
});

// Computed properties for percentages
const completionRate = computed(() => {
  return Math.round(
    (dashboardData.overview.completedTasks /
      dashboardData.overview.totalTasks) *
      100
  );
});

const activeTasksPercentage = computed(() => {
  return Math.round(
    (dashboardData.overview.activeTasks / dashboardData.overview.totalTasks) *
      100
  );
});
</script>

<template>
  <div class="flex-auto pt-20 p-6 bg-gray-50 min-h-screen">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">
        Dashboard Quản Lý Dịch Vụ Dọn Dẹp
      </h1>
      <p class="text-gray-600">Tổng quan hiệu suất và hoạt động hệ thống DSS</p>
    </div>

    <!-- Overview Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <InfoCard
        title="Tổng Nhiệm Vụ"
        :value="dashboardData.overview.totalTasks"
        :percentage="5"
        status="positive"
        bg-class="bg-gradient-to-br from-blue-500 to-blue-600"
        text-class="text-white"
        icon-class="text-blue-200"
        :icon-component="Briefcase"
      />

      <InfoCard
        title="Đang Thực Hiện"
        :value="dashboardData.overview.activeTasks"
        :percentage="activeTasksPercentage"
        status="neutral"
        bg-class="bg-gradient-to-br from-orange-500 to-orange-600"
        text-class="text-white"
        icon-class="text-orange-200"
        :icon-component="Calendar"
      />

      <InfoCard
        title="Hoàn Thành"
        :value="dashboardData.overview.completedTasks"
        :percentage="completionRate"
        status="positive"
        bg-class="bg-gradient-to-br from-green-500 to-green-600"
        text-class="text-white"
        icon-class="text-green-200"
        :icon-component="CircleCheckFilled"
      />

      <InfoCard
        title="Nhân Viên"
        :value="dashboardData.overview.totalEmployees"
        :percentage="12"
        status="positive"
        bg-class="bg-gradient-to-br from-purple-500 to-purple-600"
        text-class="text-white"
        icon-class="text-purple-200"
        :icon-component="User"
      />
    </div>

    <!-- Revenue and Satisfaction Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
      <InfoCard
        title="Doanh Thu Hôm Nay"
        :value="`${dashboardData.overview.todayRevenue.toLocaleString(
          'vi-VN'
        )} ₫`"
        :percentage="8"
        status="positive"
        bg-class="bg-gradient-to-br from-emerald-500 to-emerald-600"
        text-class="text-white"
        icon-class="text-emerald-200"
        :icon-component="Wallet"
      />

      <InfoCard
        title="Đánh Giá Khách Hàng"
        :value="`${dashboardData.overview.customerSatisfaction}/5.0`"
        :percentage="15"
        status="positive"
        bg-class="bg-gradient-to-br from-pink-500 to-pink-600"
        text-class="text-white"
        icon-class="text-pink-200"
        :icon-component="TrendCharts"
      />
    </div>

    <!-- Main Content Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Urgent Tasks -->
      <div class="lg:col-span-2">
        <Card title="Nhiệm Vụ Ưu Tiên">
          <div class="space-y-4">
            <div
              v-for="task in dashboardData.urgentTasks"
              :key="task.id"
              class="flex items-center justify-between p-4 bg-gray-50 rounded-lg border-l-4"
              :class="{
                'border-red-500': task.priority === 'Cao',
                'border-yellow-500': task.priority === 'Trung bình',
                'border-green-500': task.priority === 'Thấp',
              }"
            >
              <div class="flex-1">
                <h4 class="font-semibold text-gray-900">{{ task.title }}</h4>
                <div class="flex items-center mt-2 text-sm text-gray-600">
                  <el-icon class="mr-1"><Location /></el-icon>
                  <span class="mr-4">{{ task.location }}</span>
                  <el-icon class="mr-1"><Calendar /></el-icon>
                  <span>{{ task.deadline }}</span>
                </div>
              </div>
              <div class="flex items-center">
                <span
                  class="px-2 py-1 text-xs font-medium rounded-full"
                  :class="{
                    'bg-red-100 text-red-800': task.priority === 'Cao',
                    'bg-yellow-100 text-yellow-800':
                      task.priority === 'Trung bình',
                    'bg-green-100 text-green-800': task.priority === 'Thấp',
                  }"
                >
                  {{ task.priority }}
                </span>
                <el-button type="primary" size="small" class="ml-3">
                  Xem Chi Tiết
                </el-button>
              </div>
            </div>
          </div>
        </Card>
      </div>

      <!-- Recent Activities -->
      <div>
        <Card title="Hoạt Động Gần Đây">
          <div class="space-y-4">
            <div
              v-for="activity in dashboardData.recentActivities"
              :key="activity.id"
              class="flex items-start space-x-3"
            >
              <div
                class="flex-shrink-0 w-2 h-2 bg-blue-500 rounded-full mt-2"
              ></div>
              <div class="flex-1">
                <p class="text-sm text-gray-900">{{ activity.activity }}</p>
                <p class="text-xs text-gray-500 mt-1">{{ activity.time }}</p>
              </div>
            </div>
          </div>
        </Card>
      </div>
    </div>

    <!-- Map and Analytics Section -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
      <!-- Task Map Placeholder -->
      <Card title="Bản Đồ Nhiệm Vụ">
        <div
          class="h-64 bg-gray-100 rounded-lg flex items-center justify-center"
        >
          <div class="text-center">
            <el-icon size="48" class="text-gray-400 mb-4"><Location /></el-icon>
            <p class="text-gray-500">Bản đồ nhiệm vụ đang được phát triển</p>
            <p class="text-sm text-gray-400 mt-1">
              Sẽ hiển thị vị trí các nhiệm vụ đang thực hiện
            </p>
          </div>
        </div>
      </Card>

      <!-- Quick Actions -->
      <Card title="Thao Tác Nhanh">
        <div class="grid grid-cols-2 gap-4">
          <el-button type="primary" size="large" class="h-16">
            <div class="text-center">
              <div>Tạo Nhiệm Vụ</div>
              <div class="text-xs opacity-80">Mới</div>
            </div>
          </el-button>
          <el-button type="success" size="large" class="h-16">
            <div class="text-center">
              <div>Phân Công</div>
              <div class="text-xs opacity-80">Nhân Viên</div>
            </div>
          </el-button>
          <el-button type="warning" size="large" class="h-16">
            <div class="text-center">
              <div>Báo Cáo</div>
              <div class="text-xs opacity-80">Thống Kê</div>
            </div>
          </el-button>
          <el-button type="info" size="large" class="h-16">
            <div class="text-center">
              <div>Khách Hàng</div>
              <div class="text-xs opacity-80">Quản Lý</div>
            </div>
          </el-button>
        </div>
      </Card>
    </div>
  </div>
</template>
