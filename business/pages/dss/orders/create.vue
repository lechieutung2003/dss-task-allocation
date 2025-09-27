<template>
  <div class="create-order-container p-4">
    <!-- Tiêu đề trang -->
    <div class="mb-6 flex justify-between items-center">
      <h1 class="text-2xl font-bold">Tạo đơn hàng mới</h1>
      <el-button @click="navigateBack">
        <i class="el-icon-back mr-1"></i> Quay lại
      </el-button>
    </div>

    <!-- Form tạo đơn hàng -->
    <el-card>
      <el-form
        ref="orderFormRef"
        :model="orderForm"
        :rules="rules"
        label-position="top"
        v-loading="loading"
      >
        <!-- Thông tin khách hàng -->
        <h2 class="text-lg font-medium mb-4">Thông tin khách hàng</h2>
        <div class="grid grid-cols-2 gap-4 mb-6">
          <el-form-item label="Tên khách hàng" prop="customer_name">
            <el-input v-model="orderForm.customer_name" placeholder="Nhập tên khách hàng" />
          </el-form-item>

          <el-form-item label="Số điện thoại" prop="customer_phone">
            <el-input v-model="orderForm.customer_phone" placeholder="Nhập số điện thoại" />
          </el-form-item>

          <el-form-item label="Email" prop="customer_email">
            <el-input v-model="orderForm.customer_email" placeholder="Nhập email" />
          </el-form-item>

          <el-form-item label="Địa chỉ" prop="customer_address">
            <el-input v-model="orderForm.customer_address" placeholder="Nhập địa chỉ" />
          </el-form-item>
        </div>

        <!-- Thông tin dịch vụ -->
        <h2 class="text-lg font-medium mb-4">Thông tin dịch vụ</h2>
        <div class="grid grid-cols-2 gap-4 mb-6">
          <el-form-item label="Loại dịch vụ" prop="service_type">
            <el-select 
              v-model="orderForm.service_type" 
              placeholder="Chọn loại dịch vụ"
              @change="handleServiceTypeChange"
              clearable
            >
              <el-option 
                v-for="service in serviceTypes" 
                :key="service.id" 
                :label="service.name" 
                :value="service.id" 
              />
            </el-select>
          </el-form-item>

          <el-form-item label="Diện tích (m²)" prop="area_m2">
            <el-input-number 
              v-model="orderForm.area_m2" 
              :min="1" 
              :precision="0" 
              style="width: 100%"
              @change="calculateTotalPrice"
            />
          </el-form-item>

          <el-form-item label="Giá dịch vụ" class="readonly-item">
            <el-input 
              v-model="priceDisplay" 
              readonly 
              placeholder="Giá sẽ hiển thị sau khi chọn dịch vụ" 
            />
          </el-form-item>

          <el-form-item label="Tổng tiền" class="readonly-item">
            <el-input 
              v-model="totalPriceDisplay" 
              readonly 
              placeholder="Tổng tiền sẽ được tính tự động" 
            />
          </el-form-item>
        </div>

        <!-- Thời gian thực hiện -->
        <h2 class="text-lg font-medium mb-4">Thời gian thực hiện</h2>
        <div class="grid grid-cols-2 gap-4 mb-6">
          <el-form-item label="Ngày thực hiện" prop="service_date">
            <el-date-picker
              v-model="orderForm.service_date"
              type="date"
              placeholder="Chọn ngày thực hiện"
              style="width: 100%"
              :disabled-date="disablePastDates"
            />
          </el-form-item>

          <el-form-item label="Giờ bắt đầu" prop="start_time">
            <el-time-select
              v-model="orderForm.start_time"
              start="07:00"
              step="01:00"
              end="20:00"
              placeholder="Chọn giờ bắt đầu"
              style="width: 100%"
            />
          </el-form-item>

          <el-form-item label="Số giờ dự kiến" prop="requested_hours">
            <el-input-number
              v-model="orderForm.requested_hours"
              :min="1"
              :max="12"
              :precision="0"
              style="width: 100%"
              @change="updateEndTime"
            />
          </el-form-item>

          <el-form-item label="Giờ kết thúc dự kiến" class="readonly-item">
            <el-input v-model="endTimeDisplay" readonly />
          </el-form-item>
        </div>

        <!-- Ghi chú -->
        <h2 class="text-lg font-medium mb-4">Ghi chú bổ sung</h2>
        <el-form-item prop="note">
          <el-input
            v-model="orderForm.note"
            type="textarea"
            rows="4"
            placeholder="Nhập ghi chú, yêu cầu đặc biệt (nếu có)"
          />
        </el-form-item>

        <!-- Nút submit -->
        <div class="flex justify-center mt-6">
          <el-button @click="resetForm">Đặt lại</el-button>
          <el-button type="primary" @click="submitOrder">Tạo đơn hàng</el-button>
          <el-button type="danger" @click="cancelOrderCreation">Hủy</el-button>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import OrderService from '../../../services/dss/order';
import ServiceTypeService from '../../../services/dss/order-serviceType';
import { ElMessage, ElMessageBox } from 'element-plus';
import { useRouter } from 'vue-router';
import { formatCurrency } from '../../../utils/formatters';

const router = useRouter();
const loading = ref(false);
const orderFormRef = ref(null);
const serviceTypes = ref([]);
const selectedService = ref(null);
const hasChanges = ref(false);

definePageMeta({
  layout: "dss",
});

// Form data
const orderForm = reactive({
  customer_name: '',
  customer_phone: '',
  customer_email: '',
  customer_address: '',
  service_type: '',
  area_m2: 50,
  service_date: '',
  start_time: '',
  requested_hours: 2,
  note: ''
});

const watchFormChanges = () => {
  if (orderForm.customer_name || orderForm.customer_phone || orderForm.service_type || 
      orderForm.service_date || orderForm.start_time) {
    hasChanges.value = true;
  }
};

// Form validation rules
const rules = {
  customer_name: [
    { required: true, message: 'Vui lòng nhập tên khách hàng', trigger: 'blur' }
  ],
  customer_phone: [
    { required: true, message: 'Vui lòng nhập số điện thoại', trigger: 'blur' },
    { pattern: /^[0-9]{10,11}$/, message: 'Số điện thoại không hợp lệ', trigger: 'blur' }
  ],
  customer_email: [
    { type: 'email', message: 'Email không hợp lệ', trigger: 'blur' }
  ],
  customer_address: [
    { required: true, message: 'Vui lòng nhập địa chỉ', trigger: 'blur' }
  ],
  service_type: [
    { required: true, message: 'Vui lòng chọn loại dịch vụ', trigger: 'change' }
  ],
  area_m2: [
    { required: true, message: 'Vui lòng nhập diện tích', trigger: 'change' },
    { type: 'number', min: 1, message: 'Diện tích phải lớn hơn 0', trigger: 'change' }
  ],
  service_date: [
    { required: true, message: 'Vui lòng chọn ngày thực hiện', trigger: 'change' }
  ],
  start_time: [
    { required: true, message: 'Vui lòng chọn giờ bắt đầu', trigger: 'change' }
  ],
  requested_hours: [
    { required: true, message: 'Vui lòng nhập số giờ dự kiến', trigger: 'change' },
    { type: 'number', min: 1, message: 'Số giờ phải lớn hơn 0', trigger: 'change' }
  ]
};

// Computed properties
const priceDisplay = computed(() => {
  if (selectedService.value && selectedService.value.price_per_m2) {
    return formatCurrency(selectedService.value.price_per_m2);
  }
  return 'Chưa có thông tin';
});

const totalPriceDisplay = computed(() => {
  if (selectedService.value && selectedService.value.price_per_m2 && orderForm.area_m2) {
    const total = selectedService.value.price_per_m2 * orderForm.area_m2;
    return formatCurrency(total);
  }
  return 'Chưa có thông tin';
});

const endTimeDisplay = computed(() => {
  if (!orderForm.start_time || !orderForm.requested_hours) {
    return 'Chưa có thông tin';
  }
  
  const [hours, minutes] = orderForm.start_time.split(':').map(Number);
  const startDate = new Date();
  startDate.setHours(hours, minutes, 0);
  
  const endDate = new Date(startDate);
  endDate.setTime(startDate.getTime() + orderForm.requested_hours * 60 * 60 * 1000);
  
  return `${endDate.getHours().toString().padStart(2, '0')}:${endDate.getMinutes().toString().padStart(2, '0')}`;
});

// Fetch service types
const fetchServiceTypes = async () => {
  loading.value = true;
  try {
    const response = await ServiceTypeService.getServiceTypes();
    serviceTypes.value = response || [];
  } catch (error) {
    console.error('Lỗi khi tải danh sách dịch vụ:', error);
    ElMessage.error('Không thể tải danh sách dịch vụ. Vui lòng thử lại sau.');
  } finally {
    loading.value = false;
  }
};

// Handle service type change
const handleServiceTypeChange = () => {
  selectedService.value = serviceTypes.value.find(s => s.id === orderForm.service_type) || null;
  calculateTotalPrice();
};

// Calculate total price
const calculateTotalPrice = () => {
  if (selectedService.value && selectedService.value.price_per_m2 && orderForm.area_m2) {
    return selectedService.value.price_per_m2 * orderForm.area_m2;
  }
  return 0;
};

// Update end time
const updateEndTime = () => {
  // The end time display will automatically update via computed property
};

// Disable past dates
const disablePastDates = (date) => {
  return date < new Date(new Date().setHours(0, 0, 0, 0));
};

// Submit order
const submitOrder = async () => {
  if (!orderFormRef.value) return;
  
  await orderFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true;
      
      try {
        // Format date and time
        const serviceDate = new Date(orderForm.service_date);
        const [startHour, startMinute] = orderForm.start_time.split(':').map(Number);
        
        // Create start time
        const preferredStartTime = new Date(serviceDate);
        preferredStartTime.setHours(startHour, startMinute, 0);
        
        // Create end time
        const preferredEndTime = new Date(preferredStartTime);
        preferredEndTime.setTime(preferredStartTime.getTime() + (orderForm.requested_hours * 60 * 60 * 1000));
        
        // Prepare order data
        const orderData = {
          customer_name: orderForm.customer_name,
          customer_details: {
            phone: orderForm.customer_phone,
            email: orderForm.customer_email,
            address: orderForm.customer_address
          },
          service_type: orderForm.service_type,
          area_m2: orderForm.area_m2,
          preferred_start_time: preferredStartTime.toISOString(),
          preferred_end_time: preferredEndTime.toISOString(),
          requested_hours: orderForm.requested_hours,
          note: orderForm.note,
          status: 'pending',
          estimated_hours: Math.ceil(orderForm.area_m2 / 50) // Rough estimate
        };
        
        // Submit order
        const response = await OrderService.createOrder(orderData);
        
        ElMessage.success('Đơn hàng đã được tạo thành công!');
        
        // Show confirmation dialog
        ElMessageBox.confirm(
          'Đơn hàng đã được tạo thành công. Bạn muốn làm gì tiếp theo?',
          'Tạo đơn thành công',
          {
            confirmButtonText: 'Xem chi tiết đơn hàng',
            cancelButtonText: 'Tạo đơn hàng khác',
            type: 'success'
          }
        ).then(() => {
          // Navigate to order details
          router.push(`/dss/orders/${response.id}`);
        }).catch(() => {
          // Reset form to create another order
          resetForm();
        });
        
      } catch (error) {
        console.error('Lỗi khi tạo đơn hàng:', error);
        ElMessage.error('Không thể tạo đơn hàng. Vui lòng thử lại sau.');
      } finally {
        loading.value = false;
      }
    } else {
      ElMessage.warning('Vui lòng điền đầy đủ thông tin bắt buộc.');
      return false;
    }
  });
};

// Reset form
const resetForm = () => {
  if (orderFormRef.value) {
    orderFormRef.value.resetFields();
  }
  
  // Reset some fields to default values
  orderForm.area_m2 = 50;
  orderForm.requested_hours = 2;
  selectedService.value = null;
};

// Cancel order creation
const cancelOrderCreation = () => {
  if (hasChanges.value) {
    ElMessageBox.confirm(
      'Bạn có dữ liệu chưa lưu. Bạn có chắc chắn muốn hủy việc tạo đơn hàng này?',
      'Xác nhận hủy',
      {
        confirmButtonText: 'Có, hủy đơn hàng',
        cancelButtonText: 'Không, tiếp tục chỉnh sửa',
        type: 'warning'
      }
    ).then(() => {
      router.push('/dss/orders');
    }).catch(() => {
      // User canceled the operation
    });
  } else {
    router.push('/dss/orders');
  }
};

// Navigate back
const navigateBack = () => {
  if (hasChanges.value) {
    ElMessageBox.confirm(
      'Bạn có dữ liệu chưa lưu. Bạn có chắc chắn muốn rời khỏi trang?',
      'Xác nhận rời khỏi',
      {
        confirmButtonText: 'Rời khỏi',
        cancelButtonText: 'Ở lại',
        type: 'warning'
      }
    ).then(() => {
      router.push('/dss/orders');
    }).catch(() => {
      // User canceled the operation
    });
  } else {
    router.push('/dss/orders');
  }
};

onMounted(() => {
  fetchServiceTypes();
});
</script>

<style>
.create-order-container h2 {
  border-bottom: 1px solid #eaeaea;
  padding-bottom: 8px;
  margin-top: 12px;
}

.readonly-item .el-input__inner {
  background-color: #f5f7fa;
  cursor: not-allowed;
}
</style>