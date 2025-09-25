<template>
  <div class="order-list-container p-4">
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
          <el-input v-model="filters.keyword" placeholder="Tìm theo mã đơn, khách hàng..." />
        </el-form-item>
        <el-form-item label="Trạng thái">
          <el-select v-model="filters.status" placeholder="Chọn trạng thái" clearable>
            <el-option label="Chờ xử lý" value="pending" />
            <el-option label="Đã xác nhận" value="confirmed" />
            <el-option label="Đang xử lý" value="in_progress" />
            <el-option label="Hoàn thành" value="completed" />
            <el-option label="Hủy" value="cancelled" />
          </el-select>
        </el-form-item>
        <el-form-item label="Từ ngày">
          <el-date-picker v-model="filters.startDate" type="date" placeholder="Chọn ngày" />
        </el-form-item>
        <el-form-item label="Đến ngày">
          <el-date-picker v-model="filters.endDate" type="date" placeholder="Chọn ngày" />
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
          <template #default="{ row }">
            {{ row.area_m2 }} m²
          </template>
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
        <el-table-column label="Thao tác" width="250">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="viewOrderDetail(row.id)">
              Chi tiết
            </el-button>
            <el-button type="success" size="small" @click="handleUpdateStatus(row)" 
                      v-if="row.status !== 'completed' && row.status !== 'cancelled'">
              Cập nhật
            </el-button>
            <el-button type="danger" size="small" @click="handleCancelOrder(row)"
                      v-if="row.status !== 'completed' && row.status !== 'cancelled'">
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

    <!-- Dialog xem chi tiết đơn hàng -->
    <el-dialog v-model="orderDetailDialog.visible" title="Chi tiết đơn hàng" width="70%">
      <div v-if="selectedOrder">
        <div class="grid grid-cols-2 gap-4 mb-4">
          <div>
            <h3 class="text-lg font-medium mb-2">Thông tin đơn hàng</h3>
            <p><strong>Mã đơn:</strong> {{ selectedOrder.id }}</p>
            <p><strong>Ngày tạo:</strong> {{ formatDate(selectedOrder.created_at) }}</p>
            <p><strong>Trạng thái:</strong> {{ getStatusLabel(selectedOrder.status) }}</p>
            <p><strong>Diện tích:</strong> {{ selectedOrder.area_m2 }} m²</p>
            <p><strong>Thời gian yêu cầu:</strong> {{ selectedOrder.requested_hours }} giờ</p>
            <p><strong>Thời gian ước tính:</strong> {{ selectedOrder.estimated_hours }} giờ</p>
            <p><strong>Ghi chú:</strong> {{ selectedOrder.note || 'Không có' }}</p>
          </div>
          <div>
            <h3 class="text-lg font-medium mb-2">Thông tin khách hàng</h3>
            <p><strong>Tên khách hàng:</strong> {{ selectedOrder.customer_name }}</p>
            <p v-if="selectedOrder.customer_details"><strong>Số điện thoại:</strong> {{ selectedOrder.customer_details.phone }}</p>
            <p v-if="selectedOrder.customer_details"><strong>Email:</strong> {{ selectedOrder.customer_details.email }}</p>
            <p v-if="selectedOrder.customer_details"><strong>Địa chỉ:</strong> {{ selectedOrder.customer_details.address }}</p>
          </div>
        </div>
        
        <h3 class="text-lg font-medium my-4">Chi tiết dịch vụ</h3>
        <div class="bg-gray-50 p-4 rounded">
          <p><strong>Loại dịch vụ:</strong> {{ selectedOrder.service_details?.name }}</p>
          <p><strong>Giá mỗi m²:</strong> {{ formatCurrency(selectedOrder.service_details?.price_per_m2 || 0) }}</p>
          <p><strong>Tổng diện tích:</strong> {{ selectedOrder.area_m2 }} m²</p>
          <p><strong>Tổng giá tiền:</strong> {{ formatCurrency(calculateTotalAmount(selectedOrder)) }}</p>
        </div>
        
        <h3 class="text-lg font-medium my-4">Thời gian dự kiến</h3>
        <div class="bg-gray-50 p-4 rounded">
          <p><strong>Bắt đầu:</strong> {{ formatDateTime(selectedOrder.preferred_start_time) }}</p>
          <p><strong>Kết thúc:</strong> {{ formatDateTime(selectedOrder.preferred_end_time) }}</p>
        </div>
      </div>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="orderDetailDialog.visible = false">Đóng</el-button>
          <el-button type="primary" @click="handlePrintOrder" v-if="selectedOrder">
            In đơn hàng
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import OrderService from '../../../services/dss/order';
import { ElMessage, ElMessageBox } from 'element-plus';
import { useRouter } from 'vue-router';

const router = useRouter();
const loading = ref(false);
const orderList = ref([]);

definePageMeta({
  layout: "dss",
});

// Bộ lọc
const filters = reactive({
  keyword: '',
  status: '',
  startDate: '',
  endDate: ''
});

// Phân trang
const pagination = reactive({
  currentPage: 1,
  pageSize: 4,
  total: 0
});

// Chi tiết đơn hàng
const orderDetailDialog = reactive({
  visible: false
});
const selectedOrder = ref(null);

// Hàm lấy danh sách đơn hàng
const fetchOrders = async () => {
  loading.value = true;
  try {
    const response = await OrderService.getOrders({
      ...filters,
      page: pagination.currentPage,
      pageSize: pagination.pageSize
    });
    
    orderList.value = response.results || [];
    pagination.total = response.count || 0;
    console.log('Dữ liệu đơn hàng:', orderList.value);
  } catch (error) {
    console.error('Lỗi khi tải danh sách đơn hàng:', error);
    ElMessage.error('Không thể tải danh sách đơn hàng. Vui lòng thử lại sau.');
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
  Object.keys(filters).forEach(key => {
    filters[key] = '';
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
const viewOrderDetail = async (orderId) => {
  try {
    loading.value = true;
    const order = await OrderService.getOrder(orderId);
    selectedOrder.value = order;
    orderDetailDialog.visible = true;
    console.log('Chi tiết đơn hàng:', order);
  } catch (error) {
    console.error('Lỗi khi tải chi tiết đơn hàng:', error);
    ElMessage.error('Không thể tải thông tin đơn hàng.');
  } finally {
    loading.value = false;
  }
};

// Tính tổng số tiền dựa trên diện tích và giá
const calculateTotalAmount = (order) => {
  if (!order || !order.service_details || !order.area_m2) return 0;
  const area = parseFloat(order.area_m2);
  const pricePerM2 = order.service_details.price_per_m2 || 0;
  return area * pricePerM2;
};

// Định dạng tiền tệ
const formatCurrency = (value) => {
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(value || 0);
};

// Định dạng ngày
const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('vi-VN', { 
    year: 'numeric', 
    month: '2-digit', 
    day: '2-digit' 
  }).format(date);
};

// Định dạng ngày giờ đầy đủ
const formatDateTime = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('vi-VN', { 
    year: 'numeric', 
    month: '2-digit', 
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date);
};

// Lấy nhãn trạng thái
const getStatusLabel = (status) => {
  const statusMap = {
    'pending': 'Chờ xử lý',
    'confirmed': 'Đã xác nhận',
    'in_progress': 'Đang xử lý',
    'completed': 'Hoàn thành',
    'cancelled': 'Đã hủy'
  };
  return statusMap[status] || status;
};

// Lấy loại màu cho trạng thái
const getStatusType = (status) => {
  const statusTypeMap = {
    'pending': 'warning',
    'confirmed': 'primary',
    'in_progress': 'info',
    'completed': 'success',
    'cancelled': 'danger'
  };
  return statusTypeMap[status] || '';
};

// Xử lý cập nhật trạng thái
const handleUpdateStatus = (order) => {
  ElMessageBox.prompt('Chọn trạng thái mới', 'Cập nhật trạng thái', {
    confirmButtonText: 'Xác nhận',
    cancelButtonText: 'Hủy',
    inputType: 'select',
    inputValue: order.status,
    inputPlaceholder: 'Chọn trạng thái',
    inputOptions: [
      { value: 'pending', label: 'Chờ xử lý' },
      { value: 'confirmed', label: 'Đã xác nhận' },
      { value: 'in_progress', label: 'Đang xử lý' },
      { value: 'completed', label: 'Hoàn thành' }
    ]
  }).then(({ value }) => {
    OrderService.updateOrderStatus(order.id, value)
      .then(() => {
        const index = orderList.value.findIndex(item => item.id === order.id);
        if (index !== -1) {
          orderList.value[index].status = value;
        }
        ElMessage.success('Cập nhật trạng thái thành công');
      })
      .catch((error) => {
        console.error('Lỗi khi cập nhật trạng thái:', error);
        ElMessage.error('Cập nhật trạng thái thất bại');
      });
  }).catch(() => {
    // Người dùng đã hủy cập nhật
  });
};

// Xử lý hủy đơn hàng
const handleCancelOrder = (order) => {
  ElMessageBox.confirm('Bạn có chắc chắn muốn hủy đơn hàng này?', 'Xác nhận hủy', {
    confirmButtonText: 'Xác nhận',
    cancelButtonText: 'Hủy',
    type: 'warning'
  }).then(() => {
    OrderService.updateOrderStatus(order.id, 'cancelled')
      .then(() => {
        const index = orderList.value.findIndex(item => item.id === order.id);
        if (index !== -1) {
          orderList.value[index].status = 'cancelled';
        }
        ElMessage.success('Hủy đơn hàng thành công');
      })
      .catch((error) => {
        console.error('Lỗi khi hủy đơn hàng:', error);
        ElMessage.error('Hủy đơn hàng thất bại');
      });
  }).catch(() => {
    // Người dùng đã hủy thao tác
  });
};

// Xử lý in đơn hàng
const handlePrintOrder = () => {
  if (!selectedOrder.value) return;
  
  // Tạo nội dung để in
  const printContent = `
    <html>
    <head>
      <title>Đơn hàng ${selectedOrder.value.id}</title>
      <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { text-align: center; }
        .info-section { margin-bottom: 20px; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        .total { font-weight: bold; margin-top: 20px; text-align: right; }
      </style>
    </head>
    <body>
      <h1>CHI TIẾT ĐƠN HÀNG</h1>
      
      <div class="info-section">
        <h2>Thông tin đơn hàng</h2>
        <p><strong>Mã đơn:</strong> ${selectedOrder.value.id}</p>
        <p><strong>Ngày tạo:</strong> ${formatDate(selectedOrder.value.created_at)}</p>
        <p><strong>Trạng thái:</strong> ${getStatusLabel(selectedOrder.value.status)}</p>
      </div>
      
      <div class="info-section">
        <h2>Thông tin khách hàng</h2>
        <p><strong>Tên:</strong> ${selectedOrder.value.customer_name}</p>
        ${selectedOrder.value.customer_details ? `
        <p><strong>Số điện thoại:</strong> ${selectedOrder.value.customer_details.phone}</p>
        <p><strong>Email:</strong> ${selectedOrder.value.customer_details.email}</p>
        <p><strong>Địa chỉ:</strong> ${selectedOrder.value.customer_details.address}</p>
        ` : ''}
      </div>
      
      <h2>Chi tiết dịch vụ</h2>
      <table>
        <tr>
          <th>Dịch vụ</th>
          <th>Diện tích (m²)</th>
          <th>Đơn giá</th>
          <th>Thành tiền</th>
        </tr>
        <tr>
          <td>${selectedOrder.value.service_details?.name || ''}</td>
          <td>${selectedOrder.value.area_m2}</td>
          <td>${formatCurrency(selectedOrder.value.service_details?.price_per_m2 || 0)}</td>
          <td>${formatCurrency(calculateTotalAmount(selectedOrder.value))}</td>
        </tr>
      </table>
      
      <div class="total">
        <p>Tổng tiền: ${formatCurrency(calculateTotalAmount(selectedOrder.value))}</p>
      </div>
      
      <div class="info-section">
        <h2>Thời gian dự kiến</h2>
        <p><strong>Bắt đầu:</strong> ${formatDateTime(selectedOrder.value.preferred_start_time)}</p>
        <p><strong>Kết thúc:</strong> ${formatDateTime(selectedOrder.value.preferred_end_time)}</p>
        <p><strong>Tổng thời gian yêu cầu:</strong> ${selectedOrder.value.requested_hours} giờ</p>
        <p><strong>Ghi chú:</strong> ${selectedOrder.value.note || 'Không có'}</p>
      </div>
    </body>
    </html>
  `;
  
  // Tạo cửa sổ in mới
  const printWindow = window.open('', '_blank');
  printWindow.document.write(printContent);
  printWindow.document.close();
  printWindow.focus();
  
  // In sau khi tài nguyên đã tải xong
  printWindow.onload = function() {
    printWindow.print();
    printWindow.onafterprint = function() {
      printWindow.close();
    };
  };
};

// Xử lý tạo đơn mới
const handleCreateOrder = () => {
  router.push('/dss/orders/create');
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