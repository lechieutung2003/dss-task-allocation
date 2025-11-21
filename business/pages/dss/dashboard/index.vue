<script setup>
import { ref, reactive, computed, onMounted } from "vue";
import { ElMessage, ElLoading } from "element-plus";
import {
  Briefcase,
  User,
  Calendar,
  CircleCheckFilled,
  Warning,
  Location,
  TrendCharts,
  Wallet,
  Star,
  Clock,
  Plus,
  Refresh,
} from "@element-plus/icons-vue";
import dashboardService from "~/services/dss/dashboardService";
import InfoCard from "~/components/dashboard/InfoCard.vue";
import FilterableChart from "~/components/dashboard/FilterableChart.vue";
import PriorityOrdersTable from "~/components/dashboard/PriorityOrdersTable.vue";
import EmployeeKPITable from "~/components/dashboard/EmployeeKPITable.vue";
import ChartCard from "~/components/dashboard/ChartCard.vue";
import Card from "~/components/dashboard/Card.vue";

definePageMeta({ layout: "dss", middleware: ["auth", "role-based"] });

// State management
const loading = ref(false);
const refreshing = ref(false);
const loadingStates = reactive({
  stats: false,
  tasks: false,
  charts: false,
  activities: false,
});

// Cache để tránh load lại khi quay về trang
const dataCache = reactive({
  lastUpdate: null,
  cacheExpiry: 5 * 60 * 1000, // 5 phút
});

// Reactive dashboard data with real API integration
const dashboardData = reactive({
  overview: {
    totalTasks: 0,
    activeTasks: 0,
    completedTasks: 0,
    totalEmployees: 0,
    activeEmployees: 0,
    employeesWithOrders: 0,
    todayRevenue: 0,
    totalRevenue: 0,
    totalCost: 0,
    totalProfit: 0,
    profitMargin: 0,
    customerSatisfaction: 0,
    avgCompletionTime: 0,
    successRate: 0,
  },
  urgentTasks: [],
  chartData: null,
  employeeKPI: [],
  dailySummary: [],
});

// Computed properties
const completionRate = computed(() => {
  const { totalTasks, completedTasks } = dashboardData.overview;
  return totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;
});

const activeTasksPercentage = computed(() => {
  const { totalTasks, activeTasks } = dashboardData.overview;
  return totalTasks > 0 ? Math.round((activeTasks / totalTasks) * 100) : 0;
});

const formattedRevenue = computed(() => {
  return dashboardData.overview.todayRevenue.toLocaleString("vi-VN");
});

// Data loading functions với loading states riêng biệt
const loadDashboardStats = async () => {
  if (loadingStates.stats) return;

  loadingStates.stats = true;
  try {
    const response = await dashboardService.getDashboardStats();

    if (response.data?.overview) {
      Object.assign(dashboardData.overview, response.data.overview);
    }

    console.log("✅ Dashboard stats loaded:", dashboardData.overview);
  } catch (error) {
    console.error("❌ Error loading dashboard stats:", error);
    ElMessage.error("Không thể tải thống kê dashboard");
  } finally {
    loadingStates.stats = false;
  }
};

const loadUrgentTasks = async () => {
  if (loadingStates.tasks) return;

  loadingStates.tasks = true;
  try {
    const tasks = await dashboardService.getUrgentTasks();
    dashboardData.urgentTasks = Array.isArray(tasks) ? tasks : [];

    console.log(
      "✅ Urgent tasks loaded:",
      dashboardData.urgentTasks.length,
      "tasks"
    );
  } catch (error) {
    console.error("❌ Error loading urgent tasks:", error);
    ElMessage.error("Không thể tải danh sách nhiệm vụ ưu tiên");
  } finally {
    loadingStates.tasks = false;
  }
};

const loadChartData = async () => {
  if (loadingStates.charts) return;

  loadingStates.charts = true;
  try {
    const chartData = await dashboardService.getChartData();
    
    console.log("📊 Raw chart data from service:", chartData);
    console.log("📊 Revenue array:", chartData?.revenue);
    console.log("📊 Revenue array length:", chartData?.revenue?.length);
    
    dashboardData.chartData = chartData;
    
    // Lưu daily summary để dùng cho các biểu đồ
    dashboardData.dailySummary = chartData.dailySummary || [];

    console.log("✅ Chart data loaded and assigned:", {
      revenuePoints: chartData.revenue?.length || 0,
      dailySummary: chartData.dailySummary?.length || 0,
      tasks: chartData.tasks,
      chartDataRevenue: dashboardData.chartData?.revenue
    });
    
    console.log("📊 Data being passed to FilterableChart:", dashboardData.chartData?.revenue || []);
  } catch (error) {
    console.error("❌ Error loading chart data:", error);
  } finally {
    loadingStates.charts = false;
  }
};

const loadEmployeeKPI = async () => {
  if (loadingStates.activities) return;

  loadingStates.activities = true;
  try {
    const kpiData = await dashboardService.getEmployeeKPI();
    dashboardData.employeeKPI = kpiData || [];

    console.log("✅ Employee KPI loaded:", dashboardData.employeeKPI.length);
  } catch (error) {
    console.error("❌ Error loading employee KPI:", error);
  } finally {
    loadingStates.activities = false;
  }
};

// Check if data is cached and still valid
const isCacheValid = () => {
  if (!dataCache.lastUpdate) return false;
  const now = Date.now();
  return now - dataCache.lastUpdate < dataCache.cacheExpiry;
};

// Main refresh function với caching
const refreshDashboard = async (forceRefresh = false) => {
  if (refreshing.value) return;

  // Nếu có cache và không force refresh, skip loading
  if (!forceRefresh && isCacheValid()) {
    console.log("✅ Using cached dashboard data");
    return;
  }

  refreshing.value = true;
  console.log("🚀 Loading dashboard data...");

  try {
    // Load data song song nhưng hiển thị từng phần khi xong
    const promises = [
      loadDashboardStats(),
      loadUrgentTasks(),
      loadChartData(),
      loadEmployeeKPI(),
    ];

    // Đợi tất cả load xong
    await Promise.allSettled(promises);

    // Cập nhật cache timestamp
    dataCache.lastUpdate = Date.now();

    if (forceRefresh) {
      ElMessage.success("Dữ liệu dashboard đã được cập nhật");
    }
  } catch (error) {
    console.error("Error refreshing dashboard:", error);
    ElMessage.error("Có lỗi xảy ra khi tải dữ liệu");
  } finally {
    refreshing.value = false;
  }
};

// Quick actions
const handleQuickAction = (action) => {
  console.log(`Executing action: ${action}`);

  switch (action) {
    case "new-task":
      navigateTo("/dss/orders/create");
      break;
    case "assign-employee":
      navigateTo("/dss/orders");
      break;
    case "view-reports":
      navigateTo("/dss/reports");
      break;
    case "manage-customers":
      navigateTo("/dss/customers");
      break;
    default:
      ElMessage.info("Tính năng đang được phát triển");
  }
};

// Lifecycle
onMounted(() => {
  console.log("🚀 Dashboard mounted, checking cache...");
  refreshDashboard(false); // Sử dụng cache nếu có
});

// Helper functions
const formatDateTime = (dateStr) => {
  if (!dateStr) return "Chưa xác định";

  try {
    const date = new Date(dateStr);
    return date.toLocaleString("vi-VN", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  } catch {
    return dateStr;
  }
};

const getPriorityColor = (priority) => {
  switch (priority?.toLowerCase()) {
    case "cao":
    case "high":
      return { bg: "border-red-500", text: "bg-red-100 text-red-800" };
    case "trung bình":
    case "medium":
    case "normal":
      return { bg: "border-yellow-500", text: "bg-yellow-100 text-yellow-800" };
    case "thấp":
    case "low":
      return { bg: "border-green-500", text: "bg-green-100 text-green-800" };
    default:
      return { bg: "border-gray-300", text: "bg-gray-100 text-gray-800" };
  }
};

// Handle chart period change
const handleChartPeriodChange = (period) => {
  console.log(`Chart period changed to: ${period}`);
  // Data filtering is handled in FilterableChart component
};
</script>

<template>
  <div class="flex-auto pt-6 p-6 bg-gray-50 min-h-screen">
    <!-- Header with Refresh Button -->
    <div class="mb-8 flex items-center justify-between">
      <div>
        <h1
          class="text-3xl font-bold text-gray-900 mb-2 flex items-center gap-3"
        >
          <el-icon class="text-blue-600" size="32"><TrendCharts /></el-icon>
          Dashboard Quản Lý Dịch Vụ Dọn Dẹp
        </h1>
        <p class="text-gray-600">
          Tổng quan hiệu suất và hoạt động hệ thống DSS
        </p>
      </div>

      <el-button
        type="primary"
        :loading="refreshing"
        @click="refreshDashboard(true)"
        class="px-6"
      >
        <el-icon class="mr-2"><Refresh /></el-icon>
        {{ refreshing ? "Đang tải..." : "Làm mới" }}
      </el-button>
    </div>

    <!-- Primary Metrics Row -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div>
        <div
          v-if="loadingStates.stats"
          class="bg-white rounded-lg shadow-md p-6 animate-pulse"
        >
          <div class="flex items-center justify-between mb-4">
            <div class="h-4 bg-gray-200 rounded w-20"></div>
            <div class="h-8 w-8 bg-gray-200 rounded"></div>
          </div>
          <div class="h-8 bg-gray-200 rounded w-16 mb-2"></div>
          <div class="h-3 bg-gray-200 rounded w-12"></div>
        </div>
        <InfoCard
          v-else
          title="Tổng Nhiệm Vụ"
          :value="dashboardData.overview.totalTasks"
          :percentage="5"
          status="positive"
          bg-class="bg-gradient-to-br from-blue-600 to-blue-700"
          text-class="text-white"
          icon-class="text-blue-200"
          :icon-component="Briefcase"
          :subtitle="`${
            dashboardData.overview.completedTasks || 0
          } đã hoàn thành`"
        />
      </div>

      <div>
        <InfoCard
          title="Đang Thực Hiện"
          :value="dashboardData.overview.activeTasks"
          :percentage="activeTasksPercentage"
          status="neutral"
          bg-class="bg-gradient-to-br from-amber-500 to-amber-600"
          text-class="text-white"
          icon-class="text-amber-200"
          :icon-component="Calendar"
          subtitle="Cần hoàn thành"
        />
      </div>

      <div>
        <InfoCard
          title="Hoàn Thành"
          :value="dashboardData.overview.completedTasks"
          :percentage="completionRate"
          status="positive"
          bg-class="bg-gradient-to-br from-emerald-500 to-emerald-600"
          text-class="text-white"
          icon-class="text-emerald-200"
          :icon-component="CircleCheckFilled"
          :subtitle="`Tỷ lệ ${completionRate}%`"
        />
      </div>

      <div>
        <InfoCard
          title="Nhân Viên"
          :value="dashboardData.overview.totalEmployees"
          :percentage="12"
          status="positive"
          bg-class="bg-gradient-to-br from-violet-500 to-violet-600"
          text-class="text-white"
          icon-class="text-violet-200"
          :icon-component="User"
          :subtitle="`${
            dashboardData.overview.activeEmployees || 0
          } đang hoạt động`"
        />
      </div>
    </div>

    <!-- Performance Metrics -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <InfoCard
        title="Doanh Thu Hôm Nay"
        :value="`${formattedRevenue} ₫`"
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
        :icon-component="Star"
      />

      <InfoCard
        title="Thời Gian TB"
        :value="`${dashboardData.overview.avgCompletionTime}h`"
        :percentage="-5"
        status="negative"
        bg-class="bg-gradient-to-br from-indigo-500 to-indigo-600"
        text-class="text-white"
        icon-class="text-indigo-200"
        :icon-component="Clock"
      />

      <InfoCard
        title="Tỷ Lệ Thành Công"
        :value="`${dashboardData.overview.successRate}%`"
        :percentage="3"
        status="positive"
        bg-class="bg-gradient-to-br from-cyan-500 to-cyan-600"
        text-class="text-white"
        icon-class="text-cyan-200"
        :icon-component="TrendCharts"
      />
    </div>

    <!-- Filterable Revenue Chart (Full Width) -->
    <div class="mb-8">
      <FilterableChart 
        title="📊 Biểu Đồ Doanh Thu - Chi Phí - Lợi Nhuận"
        :icon="Wallet"
        :data="dashboardData.chartData?.revenue || []"
        :loading="loadingStates.charts"
        @period-change="handleChartPeriodChange"
      />
    </div>

    <!-- Charts Section -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
      <ChartCard
        title="📋 Trạng Thái Công Việc"
        type="tasks"
        :chart-data="dashboardData.chartData"
        :icon="Briefcase"
      />

      <ChartCard
        title="⭐ Hiệu Suất"
        type="performance"
        :chart-data="dashboardData.chartData"
        :icon="TrendCharts"
        :avg-rating="dashboardData.overview.customerSatisfaction"
        :avg-time="dashboardData.overview.avgCompletionTime"
        :performance="dashboardData.overview.successRate"
      />
    </div>

    <!-- Priority Orders Table (Full Width) -->
    <div class="mb-8">
      <PriorityOrdersTable 
        :orders-data="dashboardData.urgentTasks"
        :loading="loadingStates.tasks"
        @refresh="loadUrgentTasks"
        @view-detail="(id) => navigateTo(`/dss/orders/${id}`)"
      />
    </div>

    <!-- Employee KPI Table (Full Width) -->
    <div class="mb-8">
      <EmployeeKPITable 
        :employee-data="dashboardData.employeeKPI"
        :loading="loadingStates.activities"
        @refresh="loadEmployeeKPI"
      />
    </div>

    <!-- Main Content Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Urgent Tasks (Compact View for Quick Access) -->
      <div class="w-full">
        <Card title="🚨 Top 5 Nhiệm Vụ Ưu Tiên">
          <!-- Loading skeleton for tasks -->
          <div v-if="loadingStates.tasks" class="space-y-4">
            <div
              v-for="i in 3"
              :key="i"
              class="animate-pulse p-4 bg-gray-50 rounded-lg border-l-4 border-gray-200"
            >
              <div class="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
              <div class="h-3 bg-gray-200 rounded w-1/2 mb-2"></div>
              <div class="h-2 bg-gray-200 rounded w-full"></div>
            </div>
          </div>

          <div
            class="space-y-4"
            v-else-if="dashboardData.urgentTasks?.length > 0"
          >
            <div
              v-for="task in dashboardData.urgentTasks"
              :key="task.id"
              class="flex items-center justify-between p-4 bg-gray-50 rounded-lg border-l-4"
              :class="getPriorityColor(task.priority).bg"
            >
              <div class="flex-1">
                <h4 class="font-semibold text-gray-900">{{ task.title }}</h4>
                <div class="flex items-center mt-2 text-sm text-gray-600">
                  <el-icon class="mr-1"><Location /></el-icon>
                  <span class="mr-4">{{
                    task.location || "Chưa xác định"
                  }}</span>
                  <el-icon class="mr-1"><Calendar /></el-icon>
                  <span>{{ formatDateTime(task.deadline) }}</span>
                </div>

                <!-- Progress Bar -->
                <div class="mt-3">
                  <div class="flex items-center justify-between mb-1">
                    <span class="text-xs text-gray-500"
                      >Tiến độ: {{ task.progress }}%</span
                    >
                    <span class="text-xs text-gray-500">{{
                      task.assignee || "Chưa phân công"
                    }}</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div
                      class="bg-blue-600 h-2 rounded-full transition-all duration-300"
                      :style="{ width: task.progress + '%' }"
                    ></div>
                  </div>
                </div>
              </div>

              <div class="flex flex-col items-end gap-2 ml-4">
                <span
                  class="px-3 py-1 text-xs font-medium rounded-full"
                  :class="getPriorityColor(task.priority).text"
                >
                  {{ task.priority }}
                </span>
                <el-button
                  type="primary"
                  size="small"
                  @click="navigateTo(`/dss/orders/${task.id}`)"
                >
                  Chi Tiết
                </el-button>
              </div>
            </div>
          </div>

          <!-- Empty State -->
          <div v-else-if="!loadingStates.tasks" class="text-center py-8">
            <el-icon class="text-gray-400 text-4xl mb-2"><Warning /></el-icon>
            <p class="text-gray-500">Không có nhiệm vụ ưu tiên nào</p>
            <el-button
              type="primary"
              class="mt-3"
              @click="handleQuickAction('new-task')"
            >
              Tạo Nhiệm Vụ Mới
            </el-button>
          </div>
        </Card>
      </div>

      <!-- Quick Actions -->
      <div class="w-full">
        <Card title="⚡ Thao Tác Nhanh">
          <div class="grid grid-cols-1 gap-4">
            <!-- Nút 1 -->
            <el-button
              type="primary"
              size="large"
              class="h-16 w-full flex items-center gap-3 !justify-start !px-4 hover:transform hover:scale-105 transition-all duration-200"
              @click="handleQuickAction('new-task')"
            >
              <el-icon size="20"><Plus /></el-icon>
              <div class="text-left">
                <div class="font-semibold">Tạo Nhiệm Vụ Mới</div>
                <div class="text-xs opacity-80">Thêm công việc dọn dẹp</div>
              </div>
            </el-button>

            <!-- Nút 2 -->
            <el-button
              type="success"
              size="large"
              class="h-16 w-full flex items-center gap-3 !justify-start !px-4 hover:transform hover:scale-105 transition-all duration-200"
              @click="handleQuickAction('assign-employee')"
            >
              <el-icon size="20"><User /></el-icon>
              <div class="text-left">
                <div class="font-semibold">Phân Công Nhân Viên</div>
                <div class="text-xs opacity-80">Giao việc cho team</div>
              </div>
            </el-button>

            <!-- Nút 3 -->
            <el-button
              type="warning"
              size="large"
              class="h-16 w-full flex items-center gap-3 !justify-start !px-4 hover:transform hover:scale-105 transition-all duration-200"
              @click="handleQuickAction('view-reports')"
            >
              <el-icon size="20"><TrendCharts /></el-icon>
              <div class="text-left">
                <div class="font-semibold">Xem Báo Cáo</div>
                <div class="text-xs opacity-80">Thống kê hiệu suất</div>
              </div>
            </el-button>

            <!-- Nút 4 -->
            <el-button
              type="info"
              size="large"
              class="h-16 w-full flex items-center gap-3 !justify-start !px-4 hover:transform hover:scale-105 transition-all duration-200"
              @click="handleQuickAction('manage-customers')"
            >
              <el-icon size="20"><Star /></el-icon>
              <div class="text-left">
                <div class="font-semibold">Quản Lý Khách Hàng</div>
                <div class="text-xs opacity-80">Danh sách và đánh giá</div>
              </div>
            </el-button>
          </div>
        </Card>
      </div>
    </div>

    <!-- Loading State -->
    <el-loading
      v-if="loading"
      text="Đang tải dữ liệu dashboard..."
      background="rgba(0, 0, 0, 0.1)"
    />
  </div>
</template>

<style scoped>
@media (max-width: 768px) {
  .grid {
    grid-template-columns: 1fr !important;
  }
}

/* Increase sidebar height for dashboard page only */
:global(.layout-wrapper) {
  min-height: 150vh !important;
}

:global(.sidebar-container) {
  min-height: 150vh !important;
}

:global(.dss-layout .sidebar) {
  min-height: 150vh !important;
}
</style>
