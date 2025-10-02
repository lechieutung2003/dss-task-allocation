<template>
  <el-card v-loading="loading">
    <div v-if="order && order.status !== 'cancelled'">
      
      <!-- Thông tin đơn hàng cơ bản -->
      <div class="order-summary bg-blue-50 p-3 rounded mb-4 border-l-4 border-blue-400">
        <div class="grid grid-cols-4 md:grid-cols-7 gap-2">
            <!-- Khu vực - mở rộng gấp đôi -->
            <div class="col-span-2 md:col-span-2">
            <span class="text-xs text-gray-500 block">Khu vực</span>
            <strong class="text-sm truncate block">{{ order.customer_details?.address || 'Không có' }}</strong>
            </div>
            
            <!-- Khách hàng - thu nhỏ -->
            <div class="col-span-1 md:col-span-1">
            <span class="text-xs text-gray-500 block">Khách hàng</span>
            <strong class="text-sm">{{ order.customer_name }}</strong>
            </div>
            
            <!-- Diện tích - thu nhỏ -->
            <div class="col-span-1 md:col-span-1">
            <span class="text-xs text-gray-500 block">Diện tích</span>
            <strong class="text-sm">{{ order.area_m2 }} m²</strong>
            </div>
            
            <!-- Thời gian yêu cầu - mở rộng -->
            <div class="col-span-4 md:col-span-3">
            <span class="text-xs text-gray-500 block">Thời gian yêu cầu</span>
            <div class="flex items-center">
                <strong class="text-sm">
                {{ formatDateTime(order.preferred_start_time) }}
                </strong>
                <span class="mx-1 text-gray-500">→</span>
                <strong class="text-sm">
                {{ formatDateTime(order.preferred_end_time) }}
                </strong>
            </div>
            </div>
        </div>
      </div>

      <!-- Phần nút chuyển đổi DSS -->
      <div class="flex justify-between items-center mb-4">
        <h4 class="text-md font-medium">Danh sách nhân viên</h4>
        
        <div>
          <el-tooltip 
            content="Hệ thống gợi ý thông minh giúp tìm nhân viên phù hợp nhất cho đơn hàng này" 
            placement="top"
          >
            <el-button 
              :type="useDSS ? 'primary' : 'default'" 
              @click="toggleDSS"
              size="default"
              icon="el-icon-magic-stick"
            >
              {{ useDSS ? 'Tắt chế độ gợi ý thông minh' : 'Bật chế độ gợi ý thông minh' }}
            </el-button>
          </el-tooltip>
        </div>
      </div>

      <!-- Phần hiển thị khuyến nghị khi bật DSS -->
      <div v-if="useDSS" class="bg-blue-50 p-4 rounded mb-4">
        <div class="flex justify-between items-center">
          <span class="font-medium">Top 5 nhân viên phù hợp nhất</span>
          <el-button
            type="primary"
            size="small"
            @click="getRecommendations"
            :loading="loadingRecommendations"
          >
            <i class="el-icon-refresh mr-1"></i> Cập nhật đề xuất
          </el-button>
        </div>
        
        <el-table
          v-if="recommendations.length > 0"
          :data="recommendations"
          style="width: 100%"
          class="mt-4"
        >
          <el-table-column label="Xếp hạng" width="80" type="index" :index="1" />
          
          <el-table-column label="Nhân viên" width="300">
            <template #default="{ row }">
              <div class="flex items-center">
                <el-avatar 
                  :size="32" 
                  :src="row.employee?.avatar_url || ''" 
                  class="mr-2"
                />
                <div>
                  <div>{{ row.employee?.first_name || '' }} {{ row.employee?.last_name || '' }}</div>
                  <div class="text-gray-500 text-sm">{{ row.employee?.area || 'Không có khu vực' }}</div>
                </div>
              </div>
            </template>
          </el-table-column>

          <el-table-column label="Độ phù hợp" width="150">
            <template #default="{ row }">
              <div>
                <!-- Hiển thị thanh progress không có text -->
                <el-progress 
                  :percentage="(row.score || 0)"
                  :color="getMatchColor((row.score || 0))"
                  :show-text="false"
                />
                <!-- Hiển thị điểm số dạng score/100 -->
                <div class="text-center text-xs text-gray-600 mt-1">
                  {{ Math.round(row.score || 0) }}/100
                </div>
              </div>
            </template>
          </el-table-column>

          <el-table-column width="auto" />

          <el-table-column label="Lý do phù hợp" width="450">
            <template #default="{ row }">
              <ul class="list-disc list-inside">
                <li v-for="(reason, index) in (row.reasons || [])" 
                    :key="index" 
                    class="text-sm text-gray-600"
                >
                  {{ reason }}
                </li>
              </ul>
            </template>
          </el-table-column>

          <el-table-column label="Thao tác" width="120" align="center">
            <template #default="{ row }">
              <el-button
                type="primary"
                size="small"
                @click="assignEmployee(row.employee)"
                :disabled="!row.employee || isEmployeeAssigned(row.employee?.id)"
              >
                Phân công
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        
        <el-empty 
          v-else-if="!loadingRecommendations"
          description="Chưa có đề xuất nào"
        >
          <template #description>
            <p>Chưa có đề xuất nào. Nhấn vào nút 'Cập nhật đề xuất' để tìm nhân viên phù hợp.</p>
          </template>
          <el-button type="primary" @click="getRecommendations">Tìm nhân viên phù hợp</el-button>
        </el-empty>
      </div>

      <!-- Bảng danh sách nhân viên -->
      <div class="mb-6" v-if="!useDSS">
        <!-- Công cụ tìm kiếm và lọc nhân viên -->
        <div class="mb-4">
            <div class="grid grid-cols-2 gap-4">
            <el-input 
                v-model="employeeFilter.keyword" 
                placeholder="Tìm theo tên" 
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
          <el-table-column label="Thao tác" width="120" align="center">
            <template #default="{ row }">
              <el-button 
                type="primary" 
                size="small" 
                @click="assignEmployee(row)"
                :disabled="isEmployeeAssigned(row.id)"
              >
                {{ isEmployeeAssigned(row.id) ? 'Đã phân công' : 'Phân công' }}
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
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { formatDateTime } from '../../../utils/time';
import EmployeeService from '../../../services/dss/users/employees';
import AssignmentService from '../../../services/dss/order-assignment';
import RecommendationService from '../../../services/dss/recommendationService';
import OrderService from '../../../services/dss/order';

const props = defineProps({
  order: Object,
  loading: Boolean,
});

// Reactive states
const useDSS = ref(false);
const loadingRecommendations = ref(false);
const recommendations = ref([]);
const assignedEmployees = ref([]);
const loadingEmployees = ref(false);
const allEmployees = ref([]);
const filteredEmployees = ref([]);
const showOnlyAvailable = ref(false);

// Phân trang
const pagination = reactive({
  currentPage: 1,
  pageSize: 4,
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

// Employees sau khi phân trang
const paginatedEmployees = computed(() => {
  const start = (pagination.currentPage - 1) * pagination.pageSize;
  const end = start + pagination.pageSize;
  return filteredEmployees.value.slice(start, end);
});

// Thêm methods
const toggleDSS = () => {
  useDSS.value = !useDSS.value;
  
  if (useDSS.value) {
    ElMessage({
      message: 'Đã bật chế độ gợi ý thông minh',
      type: 'success',
      duration: 2000
    });
    
    // Tự động tìm đề xuất khi bật chế độ DSS
    if (recommendations.value.length === 0) {
      getRecommendations();
    }
  } else {
    ElMessage({
      message: 'Đã tắt chế độ gợi ý thông minh',
      type: 'info',
      duration: 2000
    });
  }
};

const getRecommendations = async () => {
  if (!props.order) return;
  
  loadingRecommendations.value = true;
  
  try {
    const response = await RecommendationService.getRecommendations(props.order.id);
    console.log('Raw API response:', response);
    
    let tempRecommendations = [];
    
    // Xử lý các định dạng response khác nhau
    if (Array.isArray(response)) {
      tempRecommendations = response;
    } 
    else if (response && Array.isArray(response.results)) {
      tempRecommendations = response.results;
    }
    else if (response && !Array.isArray(response)) {
      tempRecommendations = [response];
    }
    
    // Kiểm tra dữ liệu hợp lệ
    tempRecommendations = tempRecommendations.filter(item => 
      item && item.employee && item.score !== undefined
    );
    
    // Sắp xếp theo score cao nhất
    tempRecommendations.sort((a, b) => b.score - a.score);
    
    // Lấy 5 nhân viên có score cao nhất
    recommendations.value = tempRecommendations.slice(0, 5);
    
    console.log('Top 5 recommendations:', recommendations.value);
    
    if (recommendations.value.length === 0) {
      ElMessage.info('Không có đề xuất nào cho đơn hàng này.');
    } else if (recommendations.value.length < 5) {
      ElMessage.info(`Chỉ tìm thấy ${recommendations.value.length} nhân viên phù hợp.`);
    } else {
      ElMessage.success(`Đã tìm thấy top 5 nhân viên phù hợp nhất.`);
    }
  } catch (error) {
    console.error('Lỗi khi lấy đề xuất:', error);
    ElMessage.error('Không thể lấy danh sách đề xuất.');
  } finally {
    loadingRecommendations.value = false;
  }
};

const getMatchColor = (score) => {
  if (score >= 80) return '#67c23a';  // Xanh lá
  if (score >= 60) return '#e6a23c';  // Cam
  return '#f56c6c';  // Đỏ
};

const getEmployeeAvailability = (employee) => {
  if (!props.order) return false;
  
  try {
    // 1. Kiểm tra working hours
    if (!employee.working_start_time || !employee.working_end_time) {
      return false;
    }

    // 2. Kiểm tra thời gian đơn hàng
    if (!props.order?.preferred_start_time) {
      return false;
    }

    // 3. Parse và chuẩn hóa thời gian đơn hàng 
    const orderDateTime = new Date(props.order.preferred_start_time);
    const orderStartHour = orderDateTime.getHours();
    const orderStartMin = orderDateTime.getMinutes();
    const orderEndHour = orderStartHour + 2; // Cộng thêm 2 tiếng
    const orderEndMin = orderStartMin;

    // 4. Parse thời gian làm việc của nhân viên
    const [empStartHour, empStartMin] = employee.working_start_time.split(':');
    const [empEndHour, empEndMin] = employee.working_end_time.split(':');

    // 5. Chuyển tất cả về phút để so sánh
    const orderStartMins = orderStartHour * 60 + orderStartMin;
    const orderEndMins = orderEndHour * 60 + orderEndMin;
    const empStartMins = parseInt(empStartHour) * 60 + parseInt(empStartMin);
    const empEndMins = parseInt(empEndHour) * 60 + parseInt(empEndMin);

    // 6. So sánh thời gian
    if (empStartMins <= empEndMins) {
      // Ca làm việc bình thường (không qua đêm)
      return orderStartMins >= empStartMins && orderEndMins <= empEndMins;
    } else {
      // Ca làm việc qua đêm
      return (orderStartMins >= empStartMins) || (orderEndMins <= empEndMins);
    }

  } catch (error) {
    console.error('Error in getEmployeeAvailability:', error);
    return false;
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
  if (!props.order) return;
  
  try {
    const orderId = props.order.id;
    const data = await AssignmentService.getAssignments(orderId);
    assignedEmployees.value = data || [];
  } catch (error) {
    console.error('Lỗi khi tải thông tin phân công:', error);
    ElMessage.error('Không thể tải thông tin phân công.');
  }
};

// Lọc nhân viên
const filterEmployees = (resetPage = false) => {
  if (!Array.isArray(allEmployees.value)) {
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

  result.sort((a, b) => {
    const aAvailable = getEmployeeAvailability(a);
    const bAvailable = getEmployeeAvailability(b);
    
    // Nhân viên "sẵn sàng" lên đầu
    if (aAvailable && !bAvailable) return -1;
    if (!aAvailable && bAvailable) return 1;
    
    // Nếu cùng trạng thái, sắp xếp theo tên
    const aName = `${a.first_name || ''} ${a.last_name || ''}`;
    const bName = `${b.first_name || ''} ${b.last_name || ''}`;
    return aName.localeCompare(bName);
  });
  
  filteredEmployees.value = result;
  
  if (resetPage) {
    pagination.currentPage = 1;
  }
};

// Check if an employee is already assigned
const isEmployeeAssigned = (employeeId) => {
  if (!employeeId) return false;
  
  return assignedEmployees.value.some(
    assignment => {
      const assignedId = assignment.employee?.id || assignment.employee;
      return assignedId === employeeId;
    }
  );
};

// Assign employee to the order
const assignEmployee = (employee) => {
  if (!props.order) return;
  
  // Kiểm tra employee có tồn tại không
  if (!employee) {
    ElMessage.error('Không tìm thấy thông tin nhân viên');
    return;
  }
  
  // Lấy ID của employee
  const employeeId = employee.id || employee._id;
  
  if (!employeeId) {
    ElMessage.error('ID nhân viên không hợp lệ');
    return;
  }
  
  if (isEmployeeAssigned(employeeId)) {
    ElMessage.warning('Nhân viên này đã được phân công.');
    return;
  }
  
  ElMessageBox.confirm(
    `Bạn có chắc chắn muốn phân công nhân viên ${employee.first_name || ''} ${employee.last_name || ''} cho đơn hàng này?`,
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
      order: props.order.id,
      start_time: props.order.preferred_start_time,
      end_time: props.order.preferred_end_time,
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

const updateOrderStatus = async (orderId, status) => {
  try {
    console.log('Updating order status:', orderId, status);
    
    // Đảm bảo status là một string đơn giản
    const statusValue = typeof status === 'string' ? status : status.status;

    await OrderService.updateOrderStatus(orderId, statusValue);
    
    ElMessage.success(`Đơn hàng đã được chuyển sang trạng thái ${status}`);
  } catch (error) {
    console.error('Error updating order status:', error);
    ElMessage.warning('Đã phân công nhân viên nhưng không thể cập nhật trạng thái đơn hàng.');
  }
};

// Save all assignments
const saveAssignments = async () => {
  if (!props.order) return;
  
  try {
    const orderId = props.order.id;
    
    const newAssignments = assignedEmployees.value
      .filter(a => a.id.toString().startsWith('temp-'))
      .map(a => ({
        employee: a.employee.id,
        order: orderId,
        start_time: a.start_time,
        end_time: a.end_time,
        assigned_time: new Date().toISOString(), // Thời điểm phân công
        status: 'assigned', // Trạng thái mặc định
        work_hours: calculateWorkHours(a.start_time, a.end_time), // Tính số giờ làm
        cost: 0 // Có thể tính dựa vào work_hours và đơn giá
      }));
    
    if (newAssignments.length > 0) {
      await AssignmentService.createAssignments(orderId, newAssignments);
    }

    await OrderService.updateOrderStatus(orderId, 'confirmed');

    ElMessage.success('Phân công nhân viên thành công!');
    await fetchAssignedEmployees();
  } catch (error) {
    ElMessage.error('Không thể lưu phân công nhân viên.');
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
  if (!props.order) return;
  
  scheduleDialog.visible = true;
  scheduleDialog.employee = employee;
  scheduleDialog.loading = true;
  
  try {
    // Lấy thời gian của đơn hàng để hiển thị lịch trong khoảng thời gian đó
    const startDate = new Date(props.order.preferred_start_time);
    startDate.setDate(startDate.getDate() - 3); // 3 ngày trước
    
    const endDate = new Date(props.order.preferred_end_time);
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

// Handle current change for pagination
const handleCurrentChange = (currentPage) => {
  pagination.currentPage = currentPage;
};

// Watch order changes to fetch data when order becomes available
watch(() => props.order, (newOrder) => {
  if (newOrder) {
    fetchAssignedEmployees();
  }
}, { immediate: true });

onMounted(() => {
  fetchAllEmployees();
});
</script>