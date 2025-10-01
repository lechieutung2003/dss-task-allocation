<template>
  <div class="order-list-container p-6">
    <!-- Tiêu đề trang -->
    <div class="mb-6 flex justify-between items-center">
      <h1 class="text-2xl font-bold">Danh sách/Lịch sử đơn hàng</h1>
      <el-button type="primary" size="large" @click="handleCreateOrder">
        <i class="el-icon-plus mr-1"></i> Tạo đơn mới
      </el-button>
    </div>

    <!-- Bộ lọc -->
    <el-card class="mb-6 filter-card">
      <div class="grid grid-cols-4 gap-4">
        <el-form-item label="Từ khóa">
          <el-input
            v-model="filters.keyword"
            placeholder="Tìm theo mã đơn, khách hàng..."
          />
        </el-form-item>
        <el-form-item label="Trạng thái">
          <el-select
            v-model="filters.status"
            placeholder="Chọn trạng thái"
            clearable
          >
            <el-option label="Chờ xử lý" value="pending" />
            <el-option label="Đã xác nhận" value="confirmed" />
            <el-option label="Đang xử lý" value="in_progress" />
            <el-option label="Hoàn thành" value="completed" />
            <el-option label="Hủy" value="cancelled" />
          </el-select>
        </el-form-item>
        <el-form-item label="Từ ngày">
          <el-date-picker
            v-model="filters.startDate"
            type="date"
            placeholder="Chọn ngày"
          />
        </el-form-item>
        <el-form-item label="Đến ngày">
          <el-date-picker
            v-model="filters.endDate"
            type="date"
            placeholder="Chọn ngày"
          />
        </el-form-item>
      </div>
      <div class="flex justify-end mt-4">
        <el-button type="primary" @click="handleSearch">Tìm kiếm</el-button>
        <el-button @click="resetFilters">Đặt lại</el-button>
      </div>
    </el-card>

    <!-- Bảng dữ liệu -->
    <el-card class="order-table">
      <el-table :data="orderList" border stripe v-loading="loading">
        <el-table-column prop="id" label="Mã đơn hàng" width="150" />
        <el-table-column prop="customer_name" label="Khách hàng" />
        <el-table-column label="Ngày tạo" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="Diện tích" width="100">
          <template #default="{ row }"> {{ row.area_m2 }} m² </template>
        </el-table-column>
        <el-table-column label="Tổng tiền" width="150">
          <template #default="{ row }">
            {{ formatCurrency(calculateTotalAmount(row)) }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="Trạng thái" width="150">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="Thao tác" width="280">
          <template #default="{ row }">
            <el-button
              type="primary"
              size="small"
              @click="viewOrderDetail(row.id)"
            >
              Chi tiết
            </el-button>
            <el-button
              type="warning"
              size="small"
              @click="navigateToOrderAssignment(row.id)"
              v-if="row.status !== 'cancelled'"
            >
              Phân công
            </el-button>
            <el-button
              type="danger"
              size="small"
              @click="handleCancelOrder(row)"
              v-if="row.status !== 'completed' && row.status !== 'cancelled'"
            >
              Hủy
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- Phân trang -->
      <div class="flex justify-center mt-4">
        <el-pagination
          v-model:currentPage="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
          :total="pagination.total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import OrderService from "../../../services/dss/order";
import { ElMessage, ElMessageBox } from "element-plus";
import { useRouter } from "vue-router";
import {
  formatCurrency,
  formatDate,
  formatDateTime,
} from "../../../utils/time";

const router = useRouter();
const loading = ref(false);
const orderList = ref([]);

definePageMeta({
  layout: "dss",
  middleware: ["auth", "role-based"],
});

// Bộ lọc
const filters = reactive({
  keyword: "",
  status: "",
  startDate: "",
  endDate: "",
});

// Phân trang
const pagination = reactive({
  currentPage: 1,
  pageSize: 3,
  total: 0,
});

// Hàm lấy danh sách đơn hàng
const fetchOrders = async () => {
  loading.value = true;
  try {
    const response = await OrderService.getOrders({
      ...filters,
      page: pagination.currentPage,
      pageSize: pagination.pageSize,
    });

    orderList.value = response.results || [];
    pagination.total = response.count || 0;
  } catch (error) {
    console.error("Lỗi khi tải danh sách đơn hàng:", error);
    ElMessage.error("Không thể tải danh sách đơn hàng. Vui lòng thử lại sau.");
  } finally {
    loading.value = false;
  }
};

// Xử lý tìm kiếm
const handleSearch = () => {
  pagination.currentPage = 1;
  fetchOrders();
};

// Đặt lại bộ lọc
const resetFilters = () => {
  Object.keys(filters).forEach((key) => {
    filters[key] = "";
  });
  handleSearch();
};

// Xử lý thay đổi kích thước trang
const handleSizeChange = (size) => {
  pagination.pageSize = size;
  fetchOrders();
};

// Xử lý thay đổi trang hiện tại
const handleCurrentChange = (page) => {
  pagination.currentPage = page;
  fetchOrders();
};

// Xem chi tiết đơn hàng
const viewOrderDetail = (orderId) => {
  router.push(`/dss/orders/${orderId}`);
};

// Chuyển đến trang phân công
const navigateToOrderAssignment = (orderId) => {
  router.push(`/dss/orders/${orderId}?tab=assignment`);
};

// Tính tổng số tiền dựa trên diện tích và giá
const calculateTotalAmount = (order) => {
  if (!order || !order.service_details || !order.area_m2) return 0;
  const area = parseFloat(order.area_m2);
  const pricePerM2 = order.service_details.price_per_m2 || 0;
  return area * pricePerM2;
};

// Lấy nhãn trạng thái
const getStatusLabel = (status) => {
  const statusMap = {
    pending: "Chờ xử lý",
    confirmed: "Đã xác nhận",
    in_progress: "Đang xử lý",
    completed: "Hoàn thành",
    cancelled: "Đã hủy",
  };
  return statusMap[status] || status;
};

// Lấy loại màu cho trạng thái
const getStatusType = (status) => {
  const statusTypeMap = {
    pending: "warning",
    confirmed: "primary",
    in_progress: "info",
    completed: "success",
    cancelled: "danger",
  };
  return statusTypeMap[status] || "";
};

// Xử lý cập nhật trạng thái
const handleUpdateStatus = (order) => {
  ElMessageBox.prompt("Chọn trạng thái mới", "Cập nhật trạng thái", {
    confirmButtonText: "Xác nhận",
    cancelButtonText: "Hủy",
    inputType: "select",
    inputValue: order.status,
    inputPlaceholder: "Chọn trạng thái",
    inputOptions: [
      { value: "pending", label: "Chờ xử lý" },
      { value: "confirmed", label: "Đã xác nhận" },
      { value: "in_progress", label: "Đang xử lý" },
      { value: "completed", label: "Hoàn thành" },
    ],
  })
    .then(({ value }) => {
      OrderService.updateOrderStatus(order.id, value)
        .then(() => {
          const index = orderList.value.findIndex(
            (item) => item.id === order.id
          );
          if (index !== -1) {
            orderList.value[index].status = value;
          }
          ElMessage.success("Cập nhật trạng thái thành công");
        })
        .catch((error) => {
          console.error("Lỗi khi cập nhật trạng thái:", error);
          ElMessage.error("Cập nhật trạng thái thất bại");
        });
    })
    .catch(() => {
      // Người dùng đã hủy cập nhật
    });
};

// Xử lý hủy đơn hàng
const handleCancelOrder = (order) => {
  ElMessageBox.confirm(
    "Bạn có chắc chắn muốn hủy đơn hàng này?",
    "Xác nhận hủy",
    {
      confirmButtonText: "Xác nhận",
      cancelButtonText: "Hủy",
      type: "warning",
    }
  )
    .then(() => {
      OrderService.updateOrderStatus(order.id, "cancelled")
        .then(() => {
          const index = orderList.value.findIndex(
            (item) => item.id === order.id
          );
          if (index !== -1) {
            orderList.value[index].status = "cancelled";
          }
          ElMessage.success("Hủy đơn hàng thành công");
        })
        .catch((error) => {
          console.error("Lỗi khi hủy đơn hàng:", error);
          ElMessage.error("Hủy đơn hàng thất bại");
        });
    })
    .catch(() => {
      // Người dùng đã hủy thao tác
    });
};

// Xử lý tạo đơn mới
const handleCreateOrder = () => {
  router.push("/dss/orders/create");
};

// Load dữ liệu khi component được mount
onMounted(() => {
  fetchOrders();
});
</script>

<style>
.filter-card .el-form-item {
  margin-bottom: 0;
}

.order-table {
  min-height: 400px;
}
</style>
