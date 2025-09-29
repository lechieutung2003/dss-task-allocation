<template>
  <div class="order-detail-container p-4">
    <!-- Tiêu đề trang -->
    <div class="mb-6 flex justify-between items-center">
      <h1 class="text-2xl font-bold">Chi tiết đơn hàng #{{ $route.params.id }}</h1>
      <div>
        <el-button type="primary" @click="handlePrintOrder">
          <i class="el-icon-printer mr-1"></i> In đơn hàng
        </el-button>
        <el-button @click="navigateBack">
          <i class="el-icon-back mr-1"></i> Quay lại
        </el-button>
      </div>
    </div>

    <el-tabs v-model="activeTab">
      <el-tab-pane label="Thông tin đơn hàng" name="details">
        <el-card v-loading="loading">
          <div v-if="order">
            <div class="grid grid-cols-2 gap-4 mb-4">
              <div>
                <h3 class="text-lg font-medium mb-2">Thông tin đơn hàng</h3>
                <p><strong>Mã đơn:</strong> {{ order.id }}</p>
                <p><strong>Ngày tạo:</strong> {{ formatDate(order.created_at) }}</p>
                <p>
                  <strong>Trạng thái:</strong> 
                  <el-tag :type="getStatusType(order.status)">
                    {{ getStatusLabel(order.status) }}
                  </el-tag>
                </p>
                <p><strong>Diện tích:</strong> {{ order.area_m2 }} m²</p>
                <p><strong>Thời gian yêu cầu:</strong> {{ order.requested_hours }} giờ</p>
                <p><strong>Thời gian ước tính:</strong> {{ order.estimated_hours }} giờ</p>
                <p><strong>Ghi chú:</strong> {{ order.note || 'Không có' }}</p>
              </div>
              <div>
                <h3 class="text-lg font-medium mb-2">Thông tin khách hàng</h3>
                <p><strong>Tên khách hàng:</strong> {{ order.customer_name }}</p>
                <p v-if="order.customer_details"><strong>Số điện thoại:</strong> {{ order.customer_details.phone }}</p>
                <p v-if="order.customer_details"><strong>Email:</strong> {{ order.customer_details.email }}</p>
                <p v-if="order.customer_details"><strong>Địa chỉ:</strong> {{ order.customer_details.address }}</p>
              </div>
            </div>
            
            <h3 class="text-lg font-medium my-4">Chi tiết dịch vụ</h3>
            <div class="bg-gray-50 p-4 rounded">
              <p><strong>Loại dịch vụ:</strong> {{ order.service_details?.name }}</p>
              <p><strong>Giá mỗi m²:</strong> {{ formatCurrency(order.service_details?.price_per_m2 || 0) }}</p>
              <p><strong>Tổng diện tích:</strong> {{ order.area_m2 }} m²</p>
              <p><strong>Tổng giá tiền:</strong> {{ formatCurrency(calculateTotalAmount(order)) }}</p>
            </div>
            
            <h3 class="text-lg font-medium my-4">Thời gian dự kiến</h3>
            <div class="bg-gray-50 p-4 rounded">
              <p><strong>Bắt đầu:</strong> {{ formatDateTime(order.preferred_start_time) }}</p>
              <p><strong>Kết thúc:</strong> {{ formatDateTime(order.preferred_end_time) }}</p>
            </div>

            <div class="mt-6" v-if="order.status !== 'cancelled'">
              <h3 class="text-lg font-medium mb-2">Hành động</h3>
              <el-button 
                type="success" 
                @click="handleUpdateStatus" 
                v-if="order.status !== 'completed'"
              >
                Cập nhật trạng thái
              </el-button>
              <el-button 
                type="danger" 
                @click="handleCancelOrder" 
                v-if="order.status !== 'completed'"
              >
                Hủy đơn hàng
              </el-button>
            </div>
          </div>
          <div v-else class="text-center p-10">
            <p>Không tìm thấy thông tin đơn hàng.</p>
          </div>
        </el-card>
      </el-tab-pane>

      <el-tab-pane label="Phân công nhân viên" name="assignment">
        <el-card v-loading="loading">
          <div v-if="order && order.status !== 'cancelled'">
            
            <!-- Thông tin đơn hàng cơ bản -->
            <div class="bg-blue-50 p-4 rounded mb-4">
              <p><strong>Khu vực:</strong> {{ order.customer_details.address }}</p>
              <p><strong>Khách hàng:</strong> {{ order.customer_name }}</p>
              <p><strong>Diện tích:</strong> {{ order.area_m2 }} m²</p>
              <p>
                <strong>Thời gian yêu cầu:</strong> 
                {{ formatDateTime(order.preferred_start_time) }} - {{ formatDateTime(order.preferred_end_time) }}
              </p>
            </div>

            <!-- Công cụ tìm kiếm và lọc nhân viên -->
            <div class="mb-4">
              <div class="grid grid-cols-2 gap-4">
                <el-input 
                  v-model="employeeFilter.keyword" 
                  placeholder="Tìm theo tên, kỹ năng..." 
                  clearable
                  @input="() => filterEmployees(true)"
                >
                  <template #prefix>
                    <i class="el-icon-search"></i>
                  </template>
                </el-input>
                
                <el-select 
                  v-model="employeeFilter.area" 
                  placeholder="Lọc theo khu vực" 
                  clearable
                  @change="() => filterEmployees(true)"
                >
                  <el-option 
                    v-for="area in availableAreas" 
                    :key="area" 
                    :label="area" 
                    :value="area"
                  />
                </el-select>
              </div>
            </div>

            <!-- Bảng danh sách nhân viên -->
            <div class="mb-6">
              <div class="flex justify-between items-center mb-2">
                <h4 class="text-md font-medium">Danh sách nhân viên</h4>
                <div>
                  <el-switch
                    v-model="showOnlyAvailable"
                    active-text="Chỉ hiện nhân viên khả dụng"
                    @change="() => filterEmployees(true)"
                  />
                </div>
              </div>
              
              <el-table 
                :data="paginatedEmployees" 
                border 
                v-loading="loadingEmployees"
                row-class-name="employee-row"
              >
                <el-table-column prop="id" label="Mã NV" width="120" sortable />
                <el-table-column label="Tên nhân viên" sortable>
                  <template #default="{ row }">
                    {{ row.first_name }} {{ row.last_name }}
                  </template>
                </el-table-column>
                <el-table-column prop="area" label="Khu vực" width="120" sortable />
                <el-table-column label="Kỹ năng" width="200">
                  <template #default="{ row }">
                    <el-tag 
                      v-for="skill in (row.skills || []).slice(0, 2)" 
                      :key="skill" 
                      size="small" 
                      class="mr-1"
                    >
                      {{ skill }}
                    </el-tag>
                    <el-tooltip 
                      v-if="(row.skills || []).length > 2" 
                      :content="row.skills.slice(2).join(', ')"
                    >
                      <el-tag size="small" type="info">+{{ row.skills.length - 2 }}</el-tag>
                    </el-tooltip>
                  </template>
                </el-table-column>
                <el-table-column label="Trạng thái" width="120">
                  <template #default="{ row }">
                    <el-tag 
                      :type="getEmployeeAvailability(row) ? 'success' : 'danger'" 
                      size="small"
                    >
                      {{ getEmployeeAvailability(row) ? 'Sẵn sàng' : 'Bận' }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column label="Thao tác" width="180">
                  <template #default="{ row }">
                    <el-button 
                      type="primary" 
                      size="small" 
                      @click="assignEmployee(row)"
                      :disabled="isEmployeeAssigned(row.id)"
                    >
                      {{ isEmployeeAssigned(row.id) ? 'Đã phân công' : 'Phân công' }}
                    </el-button>
                    <el-button 
                      type="info" 
                      size="small" 
                      @click="showEmployeeSchedule(row)"
                    >
                      <i class="el-icon-time"></i>
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
              
              <div class="flex justify-center mt-4">
                <el-pagination
                  v-model:currentPage="pagination.currentPage"
                  :page-size="pagination.pageSize"
                  :total="filteredEmployees.length"
                  layout="total, prev, pager, next"
                  @current-change="handleCurrentChange"
                />
              </div>
            </div>

            <!-- Danh sách nhân viên đã phân công -->
            <div>
              <h4 class="text-md font-medium mb-2">Nhân viên đã phân công ({{ assignedEmployees.length }})</h4>
              <el-table 
                :data="assignedEmployees" 
                border 
                empty-text="Chưa có nhân viên được phân công"
              >
                <el-table-column prop="id" label="Mã NV" width="80" />
                <el-table-column label="Tên nhân viên">
                  <template #default="{ row }">
                    {{ row.employee.first_name }} {{ row.employee.last_name }}
                  </template>
                </el-table-column>
                <el-table-column prop="employee.area" label="Khu vực" width="120" />
                <el-table-column label="Thời gian bắt đầu" width="180">
                  <template #default="{ row }">
                    <el-date-picker
                      v-model="row.start_time"
                      type="datetime"
                      placeholder="Chọn thời gian"
                      size="small"
                      style="width: 160px"
                      @change="updateAssignmentEndTime(row)"
                    />
                  </template>
                </el-table-column>
                <el-table-column label="Thời gian kết thúc" width="180">
                  <template #default="{ row }">
                    <el-date-picker
                      v-model="row.end_time"
                      type="datetime"
                      placeholder="Chọn thời gian"
                      size="small"
                      style="width: 160px"
                    />
                  </template>
                </el-table-column>
                <el-table-column label="Thao tác" width="120">
                  <template #default="{ row }">
                    <el-button 
                      type="danger" 
                      size="small" 
                      @click="removeAssignment(row.id)"
                    >
                      Hủy phân công
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>

              <div class="mt-4 flex justify-between items-center">
                <div>
                  <el-alert
                    v-if="assignedEmployees.length > 0 && assignedEmployees.length < (order.estimated_hours / 4)"
                    title="Cảnh báo: Số lượng nhân viên được phân công có thể không đủ để hoàn thành đơn hàng đúng thời gian"
                    type="warning"
                    show-icon
                    :closable="false"
                    class="mb-3"
                  />
                </div>
                <div>
                  <el-button @click="resetAssignments">Đặt lại</el-button>
                  <el-button 
                    type="success" 
                    @click="saveAssignments" 
                    :disabled="assignedEmployees.length === 0"
                  >
                    Lưu phân công
                  </el-button>
                </div>
              </div>
            </div>
          </div>
          <div v-else-if="order && order.status === 'cancelled'" class="text-center p-10">
            <el-alert
              title="Đơn hàng đã bị hủy"
              type="error"
              description="Không thể phân công nhân viên cho đơn hàng đã hủy"
              show-icon
              :closable="false"
            />
          </div>
          <div v-else class="text-center p-10">
            <p>Không tìm thấy thông tin đơn hàng.</p>
          </div>
        </el-card>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import OrderService from '../../../services/dss/order';
import EmployeeService from '../../../services/dss/users/employees';
import AssignmentService from '../../../services/dss/order-assignment';
import { ElMessage, ElMessageBox } from 'element-plus';
import { useRouter, useRoute } from 'vue-router';
import { formatCurrency, formatDate, formatDateTime } from '../../../utils/formatters';

const router = useRouter();
const route = useRoute();
const loading = ref(false);
const order = ref(null);
const activeTab = ref('details');
const assignedEmployees = ref([]);
const loadingEmployees = ref(false);
const allEmployees = ref([]);
const filteredEmployees = ref([]);
const showOnlyAvailable = ref(false);

// Phân trang
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
});

// Lọc nhân viên
const employeeFilter = reactive({
  keyword: '',
  area: '',
});

// Dialog hiển thị lịch
const scheduleDialog = reactive({
  visible: false,
  employee: null,
  schedule: [],
  loading: false,
});

definePageMeta({
  layout: "dss",
});

// Lấy danh sách khu vực
const availableAreas = computed(() => {
  if (!Array.isArray(allEmployees.value)) {
    return [];
  }
  
  const areas = new Set();
  allEmployees.value.forEach(emp => {
    if (emp?.area) {
      areas.add(emp.area);
    }
  });
  return [...areas].sort();
});

const getEmployeeAvailability = (employee) => {
  try {
    console.log('Checking availability for employee:', {
      id: employee.id,
      name: `${employee.first_name} ${employee.last_name}`,
      working_hours: `${employee.working_start_time} - ${employee.working_end_time}`
    });

    // 1. Kiểm tra working hours
    if (!employee.working_start_time || !employee.working_end_time) {
      console.warn('Employee has no working hours set');
      return false;
    }

    // 2. Kiểm tra thời gian đơn hàng
    if (!order.value?.preferred_start_time) {
      console.warn('Order has no start time');
      return false;
    }

    // 3. Parse và chuẩn hóa thời gian đơn hàng 
    const orderDateTime = new Date(order.value.preferred_start_time);
    const orderStartHour = orderDateTime.getHours();
    const orderStartMin = orderDateTime.getMinutes();
    const orderEndHour = orderStartHour + 2; // Cộng thêm 2 tiếng
    const orderEndMin = orderStartMin;

    // 4. Parse thời gian làm việc của nhân viên
    const [empStartHour, empStartMin] = employee.working_start_time.split(':');
    const [empEndHour, empEndMin] = employee.working_end_time.split(':');
    
    console.log('Time comparison:', {
      order: {
        start: `${orderStartHour}:${orderStartMin}`,
        end: `${orderEndHour}:${orderEndMin}`
      },
      employee: {
        start: `${empStartHour}:${empStartMin}`,
        end: `${empEndHour}:${empEndMin}`
      }
    });

    // 5. Chuyển tất cả về phút để so sánh
    const orderStartMins = orderStartHour * 60 + orderStartMin;
    const orderEndMins = orderEndHour * 60 + orderEndMin;
    const empStartMins = parseInt(empStartHour) * 60 + parseInt(empStartMin);
    const empEndMins = parseInt(empEndHour) * 60 + parseInt(empEndMin);

    // 6. So sánh thời gian
    if (empStartMins <= empEndMins) {
      // Ca làm việc bình thường (không qua đêm)
      const isAvailable = orderStartMins >= empStartMins && orderEndMins <= empEndMins;
      console.log('Normal shift check:', {
        isAvailable,
        orderStart: `${orderStartHour}:${orderStartMin}`,
        orderEnd: `${orderEndHour}:${orderEndMin}`,
        empStart: `${empStartHour}:${empStartMin}`,
        empEnd: `${empEndHour}:${empEndMin}`
      });
      return isAvailable;
    } else {
      // Ca làm việc qua đêm
      const isAvailable = (orderStartMins >= empStartMins) || (orderEndMins <= empEndMins);
      console.log('Overnight shift check:', {
        isAvailable,
        orderStart: `${orderStartHour}:${orderStartMin}`,
        orderEnd: `${orderEndHour}:${orderEndMin}`,
        empStart: `${empStartHour}:${empStartMin}`,
        empEnd: `${empEndHour}:${empEndMin}`
      });
      return isAvailable;
    }

  } catch (error) {
    console.error('Error in getEmployeeAvailability:', error);
    return false;
  }
};

// Fetch order details
const fetchOrderDetails = async () => {
  loading.value = true;
  try {
    const orderId = route.params.id;
    const data = await OrderService.getOrder(orderId);
    order.value = data;
  } catch (error) {
    console.error('Lỗi khi tải thông tin đơn hàng:', error);
    ElMessage.error('Không thể tải thông tin đơn hàng.');
  } finally {
    loading.value = false;
  }
};

// Fetch all employees
const fetchAllEmployees = async () => {
  loadingEmployees.value = true;
  try {
    const response = await EmployeeService.getEmployees({
      page: 1,
      page_size: 100 // Hoặc số lượng phù hợp
    });
    
    // Kiểm tra và xử lý response
    if (response && response.results) {
      allEmployees.value = response.results;
    } else {
      allEmployees.value = [];
      console.warn('Unexpected response format:', response);
    }
    
    console.log('Fetched employees:', allEmployees.value);
    filterEmployees();
  } catch (error) {
    console.error('Lỗi khi tải danh sách nhân viên:', error);
    ElMessage.error('Không thể tải danh sách nhân viên.');
    allEmployees.value = [];
  } finally {
    loadingEmployees.value = false;
  }
};

// Fetch assigned employees
const fetchAssignedEmployees = async () => {
  loading.value = true;
  try {
    const orderId = route.params.id;
    const data = await AssignmentService.getAssignments(orderId);
    assignedEmployees.value = data || [];
  } catch (error) {
    console.error('Lỗi khi tải thông tin phân công:', error);
    ElMessage.error('Không thể tải thông tin phân công.');
  } finally {
    loading.value = false;
  }
};

// Lọc nhân viên
const filterEmployees = (resetPage = false) => {
  if (!Array.isArray(allEmployees.value)) {
    console.warn('allEmployees.value không phải là mảng:', allEmployees.value);
    filteredEmployees.value = [];
    return;
  }

  let result = [...allEmployees.value];
  
  // Lọc theo từ khóa
  if (employeeFilter.keyword) {
    const keyword = employeeFilter.keyword.toLowerCase();
    result = result.filter(emp => {
      const fullName = `${emp.first_name || ''} ${emp.last_name || ''}`.toLowerCase();
      const workMail = (emp.work_mail || '').toLowerCase();
      return fullName.includes(keyword) || workMail.includes(keyword);
    });
  }
  
  // Lọc theo khu vực
  if (employeeFilter.area) {
    result = result.filter(emp => emp.area === employeeFilter.area);
  }
  
  // Lọc theo tình trạng khả dụng
  if (showOnlyAvailable.value) {
    result = result.filter(emp => getEmployeeAvailability(emp));
  }
  
  filteredEmployees.value = result;
  
  if (resetPage) {
    pagination.currentPage = 1;
  }
};

// Check if an employee is already assigned
const isEmployeeAssigned = (employeeId) => {
  return assignedEmployees.value.some(
    assignment => assignment.employee.id === employeeId
  );
};

// Assign employee to the order
const assignEmployee = (employee) => {
  if (isEmployeeAssigned(employee.id)) {
    ElMessage.warning('Nhân viên này đã được phân công.');
    return;
  }
  
  ElMessageBox.confirm(
    `Bạn có chắc chắn muốn phân công nhân viên ${employee.first_name} ${employee.last_name} cho đơn hàng này?`,
    'Xác nhận phân công',
    {
      confirmButtonText: 'Xác nhận',
      cancelButtonText: 'Hủy',
      type: 'info'
    }
  ).then(() => {
    // Use order's preferred times as default
    const assignment = {
      id: `temp-${Date.now()}`, // Temporary ID for UI
      employee: employee,
      order: order.value.id,
      start_time: order.value.preferred_start_time,
      end_time: order.value.preferred_end_time,
      status: 'assigned'
    };
    
    assignedEmployees.value.push(assignment);
    ElMessage.success('Đã thêm nhân viên vào danh sách phân công.');
  }).catch(() => {
    // User cancelled
  });
};

// Remove assignment
const removeAssignment = (assignmentId) => {
  ElMessageBox.confirm(
    'Bạn có chắc chắn muốn hủy phân công nhân viên này?',
    'Xác nhận hủy phân công',
    {
      confirmButtonText: 'Xác nhận',
      cancelButtonText: 'Hủy',
      type: 'warning'
    }
  ).then(() => {
    assignedEmployees.value = assignedEmployees.value.filter(
      assignment => assignment.id !== assignmentId
    );
    ElMessage.success('Đã hủy phân công nhân viên.');
  }).catch(() => {
    // User cancelled
  });
};

// Cập nhật giờ kết thúc dựa vào giờ bắt đầu
const updateAssignmentEndTime = (assignment) => {
  // Mặc định thời gian làm việc là 4 giờ
  if (assignment.start_time) {
    const startTime = new Date(assignment.start_time);
    const endTime = new Date(startTime);
    endTime.setHours(startTime.getHours() + 4);
    assignment.end_time = endTime;
  }
};

// Reset phân công
const resetAssignments = () => {
  ElMessageBox.confirm(
    'Bạn có chắc chắn muốn đặt lại tất cả phân công?',
    'Xác nhận đặt lại',
    {
      confirmButtonText: 'Xác nhận',
      cancelButtonText: 'Hủy',
      type: 'warning'
    }
  ).then(() => {
    assignedEmployees.value = [];
    ElMessage.success('Đã đặt lại danh sách phân công.');
  }).catch(() => {
    // User cancelled
  });
};

// Save all assignments
const saveAssignments = async () => {
  loading.value = true;
  try {
    const orderId = route.params.id;
    
    const newAssignments = assignedEmployees.value
      .filter(a => a.id.toString().startsWith('temp-'))
      .map(a => ({
        employee: a.employee.id,
        order: orderId,
        start_time: a.start_time,
        end_time: a.end_time,
        // Thêm các trường bắt buộc
        assigned_time: new Date().toISOString(), // Thời điểm phân công
        status: 'assigned', // Trạng thái mặc định
        work_hours: calculateWorkHours(a.start_time, a.end_time), // Tính số giờ làm
        cost: 0 // Có thể tính dựa vào work_hours và đơn giá
      }));
    
    if (newAssignments.length > 0) {
      await AssignmentService.createAssignments(orderId, newAssignments);
    }
    
    ElMessage.success('Phân công nhân viên thành công!');
    await fetchAssignedEmployees();
  } catch (error) {
    ElMessage.error('Không thể lưu phân công nhân viên.');
  } finally {
    loading.value = false;
  }
};

// Thêm hàm tính work_hours
const calculateWorkHours = (start, end) => {
  if (!start || !end) return 4; // Giá trị mặc định
  const hours = (new Date(end) - new Date(start)) / (1000 * 60 * 60);
  return Math.round(hours * 100) / 100; // Làm tròn 2 chữ số thập phân
};

// Hiển thị lịch làm việc của nhân viên
const showEmployeeSchedule = async (employee) => {
  scheduleDialog.visible = true;
  scheduleDialog.employee = employee;
  scheduleDialog.loading = true;
  
  try {
    // Lấy thời gian của đơn hàng để hiển thị lịch trong khoảng thời gian đó
    const startDate = new Date(order.value.preferred_start_time);
    startDate.setDate(startDate.getDate() - 3); // 3 ngày trước
    
    const endDate = new Date(order.value.preferred_end_time);
    endDate.setDate(endDate.getDate() + 3); // 3 ngày sau
    
    // Gọi API lấy lịch làm việc
    const schedule = await EmployeeService.getSchedule(employee.id, {
      start_date: startDate.toISOString().split('T')[0],
      end_date: endDate.toISOString().split('T')[0]
    });
    
    scheduleDialog.schedule = schedule || [];
  } catch (error) {
    console.error('Lỗi khi tải lịch làm việc:', error);
    ElMessage.error('Không thể tải lịch làm việc của nhân viên.');
  } finally {
    scheduleDialog.loading = false;
  }
};

// Màu cho độ phù hợp
const getMatchColor = (match) => {
  if (!match) return '#909399';
  if (match >= 80) return '#67c23a';
  if (match >= 60) return '#e6a23c';
  return '#f56c6c';
};

// Handle current change for pagination
const handleCurrentChange = (currentPage) => {
  pagination.currentPage = currentPage;
};

// Calculate total amount
const calculateTotalAmount = (order) => {
  if (!order || !order.service_details || !order.area_m2) return 0;
  const area = parseFloat(order.area_m2);
  const pricePerM2 = order.service_details.price_per_m2 || 0;
  return area * pricePerM2;
};

// Get status label
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

// Get status type for color
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

// Handle update status
const handleUpdateStatus = () => {
  ElMessageBox.prompt('Chọn trạng thái mới', 'Cập nhật trạng thái', {
    confirmButtonText: 'Xác nhận',
    cancelButtonText: 'Hủy',
    inputType: 'select',
    inputValue: order.value.status,
    inputPlaceholder: 'Chọn trạng thái',
    inputOptions: [
      { value: 'pending', label: 'Chờ xử lý' },
      { value: 'confirmed', label: 'Đã xác nhận' },
      { value: 'in_progress', label: 'Đang xử lý' },
      { value: 'completed', label: 'Hoàn thành' }
    ]
  }).then(({ value }) => {
    OrderService.updateOrderStatus(order.value.id, value)
      .then(() => {
        order.value.status = value;
        ElMessage.success('Cập nhật trạng thái thành công');
      })
      .catch((error) => {
        console.error('Lỗi khi cập nhật trạng thái:', error);
        ElMessage.error('Cập nhật trạng thái thất bại');
      });
  }).catch(() => {
    // User cancelled
  });
};

// Handle cancel order
const handleCancelOrder = () => {
  ElMessageBox.confirm('Bạn có chắc chắn muốn hủy đơn hàng này?', 'Xác nhận hủy', {
    confirmButtonText: 'Xác nhận',
    cancelButtonText: 'Hủy',
    type: 'warning'
  }).then(() => {
    OrderService.updateOrderStatus(order.value.id, 'cancelled')
      .then(() => {
        order.value.status = 'cancelled';
        ElMessage.success('Hủy đơn hàng thành công');
      })
      .catch((error) => {
        console.error('Lỗi khi hủy đơn hàng:', error);
        ElMessage.error('Hủy đơn hàng thất bại');
      });
  }).catch(() => {
    // User cancelled
  });
};

// Print order
const handlePrintOrder = () => {
  if (!order.value) return;
  
  // Create print content
  const printContent = `
    <html>
    <head>
      <title>Đơn hàng ${order.value.id}</title>
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
        <p><strong>Mã đơn:</strong> ${order.value.id}</p>
        <p><strong>Ngày tạo:</strong> ${formatDate(order.value.created_at)}</p>
        <p><strong>Trạng thái:</strong> ${getStatusLabel(order.value.status)}</p>
      </div>
      
      <div class="info-section">
        <h2>Thông tin khách hàng</h2>
        <p><strong>Tên:</strong> ${order.value.customer_name}</p>
        ${order.value.customer_details ? `
        <p><strong>Số điện thoại:</strong> ${order.value.customer_details.phone}</p>
        <p><strong>Email:</strong> ${order.value.customer_details.email}</p>
        <p><strong>Địa chỉ:</strong> ${order.value.customer_details.address}</p>
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
          <td>${order.value.service_details?.name || ''}</td>
          <td>${order.value.area_m2}</td>
          <td>${formatCurrency(order.value.service_details?.price_per_m2 || 0)}</td>
          <td>${formatCurrency(calculateTotalAmount(order.value))}</td>
        </tr>
      </table>
      
      <div class="total">
        <p>Tổng tiền: ${formatCurrency(calculateTotalAmount(order.value))}</p>
      </div>
      
      <div class="info-section">
        <h2>Thời gian dự kiến</h2>
        <p><strong>Bắt đầu:</strong> ${formatDateTime(order.value.preferred_start_time)}</p>
        <p><strong>Kết thúc:</strong> ${formatDateTime(order.value.preferred_end_time)}</p>
        <p><strong>Tổng thời gian yêu cầu:</strong> ${order.value.requested_hours} giờ</p>
        <p><strong>Ghi chú:</strong> ${order.value.note || 'Không có'}</p>
      </div>
    </body>
    </html>
  `;
  
  // Create a new window for printing
  const printWindow = window.open('', '_blank');
  printWindow.document.write(printContent);
  printWindow.document.close();
  printWindow.focus();
  
  // Print after resources loaded
  printWindow.onload = function() {
    printWindow.print();
    printWindow.onafterprint = function() {
      printWindow.close();
    };
  };
};

// Navigate back to orders list
const navigateBack = () => {
  router.push('/dss/orders');
};

onMounted(() => {
  fetchOrderDetails();
  fetchAllEmployees();
  fetchAssignedEmployees();
  
  // Check if we should activate assignment tab
  if (route.query.tab === 'assignment') {
    activeTab.value = 'assignment';
  }
});

const paginatedEmployees = computed(() => {
  const start = (pagination.currentPage - 1) * pagination.pageSize;
  const end = start + pagination.pageSize;
  return filteredEmployees.value.slice(start, end);
});
</script>

<style>
.order-detail-container .el-tabs__content {
  padding-top: 20px;
}
</style>