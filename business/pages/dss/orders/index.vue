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
            <el-option label="Đang xử lý" value="processing" />
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
        <el-table-column prop="customerName" label="Khách hàng" />
        <el-table-column prop="createdAt" label="Ngày tạo" width="180" />
        <el-table-column prop="totalAmount" label="Tổng tiền" width="150">
          <template #default="{ row }">
            {{ formatCurrency(row.totalAmount) }}
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
            <p><strong>Ngày tạo:</strong> {{ selectedOrder.createdAt }}</p>
            <p><strong>Trạng thái:</strong> {{ getStatusLabel(selectedOrder.status) }}</p>
            <p><strong>Tổng tiền:</strong> {{ formatCurrency(selectedOrder.totalAmount) }}</p>
          </div>
          <div>
            <h3 class="text-lg font-medium mb-2">Thông tin khách hàng</h3>
            <p><strong>Tên khách hàng:</strong> {{ selectedOrder.customerName }}</p>
            <p><strong>Số điện thoại:</strong> {{ selectedOrder.customerPhone }}</p>
            <p><strong>Email:</strong> {{ selectedOrder.customerEmail }}</p>
            <p><strong>Địa chỉ:</strong> {{ selectedOrder.customerAddress }}</p>
          </div>
        </div>
        
        <h3 class="text-lg font-medium my-4">Chi tiết sản phẩm</h3>
        <el-table :data="selectedOrder.items" border>
          <el-table-column prop="productName" label="Sản phẩm" />
          <el-table-column prop="quantity" label="Số lượng" width="100" />
          <el-table-column prop="unitPrice" label="Đơn giá" width="150">
            <template #default="{ row }">
              {{ formatCurrency(row.unitPrice) }}
            </template>
          </el-table-column>
          <el-table-column label="Thành tiền" width="150">
            <template #default="{ row }">
              {{ formatCurrency(row.quantity * row.unitPrice) }}
            </template>
          </el-table-column>
        </el-table>
        
        <div class="flex justify-end mt-4">
          <p class="text-lg"><strong>Tổng tiền:</strong> {{ formatCurrency(selectedOrder.totalAmount) }}</p>
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
import { ElMessage, ElMessageBox } from 'element-plus';
import { useRouter } from 'vue-router';

const router = useRouter();
const loading = ref(false);
const orderList = ref([]);

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
  pageSize: 10,
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
    // TODO: Thay thế bằng API thực tế
    // const response = await api.getOrders({
    //   ...filters,
    //   page: pagination.currentPage,
    //   pageSize: pagination.pageSize
    // });
    
    // Dữ liệu mẫu
    const mockData = [
      {
        id: 'DH001',
        customerName: 'Nguyễn Văn A',
        customerPhone: '0987654321',
        customerEmail: 'nguyenvana@example.com',
        customerAddress: '123 Đường ABC, Quận 1, TP.HCM',
        createdAt: '2023-09-20 14:30:00',
        status: 'pending',
        totalAmount: 1500000,
        items: [
          { productName: 'Sản phẩm A', quantity: 2, unitPrice: 500000 },
          { productName: 'Sản phẩm B', quantity: 1, unitPrice: 500000 }
        ]
      },
      {
        id: 'DH002',
        customerName: 'Trần Thị B',
        customerPhone: '0912345678',
        customerEmail: 'tranthib@example.com',
        customerAddress: '456 Đường XYZ, Quận 2, TP.HCM',
        createdAt: '2023-09-19 10:15:00',
        status: 'processing',
        totalAmount: 2800000,
        items: [
          { productName: 'Sản phẩm C', quantity: 1, unitPrice: 1800000 },
          { productName: 'Sản phẩm D', quantity: 2, unitPrice: 500000 }
        ]
      },
      {
        id: 'DH003',
        customerName: 'Lê Văn C',
        customerPhone: '0901234567',
        customerEmail: 'levanc@example.com',
        customerAddress: '789 Đường DEF, Quận 3, TP.HCM',
        createdAt: '2023-09-18 09:00:00',
        status: 'completed',
        totalAmount: 4500000,
        items: [
          { productName: 'Sản phẩm E', quantity: 3, unitPrice: 1500000 }
        ]
      }
    ];

    orderList.value = mockData;
    pagination.total = mockData.length;
    
    // Khi có API thực tế:
    // orderList.value = response.data;
    // pagination.total = response.total;
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
const viewOrderDetail = (orderId) => {
  selectedOrder.value = orderList.value.find(order => order.id === orderId);
  if (selectedOrder.value) {
    orderDetailDialog.visible = true;
  } else {
    ElMessage.error('Không tìm thấy thông tin đơn hàng.');
  }
};

// Định dạng tiền tệ
const formatCurrency = (value) => {
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(value);
};

// Lấy nhãn trạng thái
const getStatusLabel = (status) => {
  const statusMap = {
    'pending': 'Chờ xử lý',
    'processing': 'Đang xử lý',
    'completed': 'Hoàn thành',
    'cancelled': 'Đã hủy'
  };
  return statusMap[status] || status;
};

// Lấy loại màu cho trạng thái
const getStatusType = (status) => {
  const statusTypeMap = {
    'pending': 'warning',
    'processing': 'info',
    'completed': 'success',
    'cancelled': 'danger'
  };
  return statusTypeMap[status] || '';
};

// Xử lý tạo đơn hàng mới
const handleCreateOrder = () => {
  router.push('/dss/orders/create');
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
      { value: 'processing', label: 'Đang xử lý' },
      { value: 'completed', label: 'Hoàn thành' }
    ]
  }).then(({ value }) => {
    // TODO: Gọi API cập nhật trạng thái
    // Giả lập cập nhật thành công
    const index = orderList.value.findIndex(item => item.id === order.id);
    if (index !== -1) {
      orderList.value[index].status = value;
      ElMessage.success('Cập nhật trạng thái thành công');
    }
  }).catch(() => {
    // Người dùng hủy thao tác
  });
};

// Xử lý hủy đơn hàng
const handleCancelOrder = (order) => {
  ElMessageBox.confirm(
    'Bạn có chắc chắn muốn hủy đơn hàng này không?',
    'Xác nhận hủy đơn hàng',
    {
      confirmButtonText: 'Đồng ý',
      cancelButtonText: 'Hủy bỏ',
      type: 'warning'
    }
  ).then(() => {
    // TODO: Gọi API hủy đơn hàng
    // Giả lập hủy thành công
    const index = orderList.value.findIndex(item => item.id === order.id);
    if (index !== -1) {
      orderList.value[index].status = 'cancelled';
      ElMessage.success('Hủy đơn hàng thành công');
    }
  }).catch(() => {
    // Người dùng hủy thao tác
  });
};

// Xử lý in đơn hàng
const handlePrintOrder = () => {
  // TODO: Implement in đơn hàng
  ElMessage.success('Đang chuẩn bị in đơn hàng');
  // Có thể mở tab mới với template in hoặc tạo PDF
};

// Load dữ liệu khi component được mount
onMounted(() => {
  fetchOrders();
});
</script>