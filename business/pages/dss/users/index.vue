<template>
  <div class="p-6">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6 mt-14">
      <button 
        @click="showCreateModal = true"
        class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center gap-2"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
        </svg>
        {{ $t('add_employee') }}
      </button>
    </div>

    <!-- Filters -->
    <EmployeeFilters
      :filters="filters"
      :areas="areas"
      @update:search="handleSearchUpdate"
      @update:area="updateFilters('area', $event)"
      @update:status="updateFilters('status', $event)"
      @reset="resetFilters"
    />

    <!-- Employee Table -->
    <EmployeeListTable
      :employees="employees"
      :loading="loading"
      @view="viewEmployee"
      @edit="editEmployee"
      @delete="confirmDeleteEmployee"
    />

    <!-- Pagination -->
    <EmployeePagination
      :current-page="currentPage"
      :page-size="pageSize"
      :total-items="totalItems"
      :total-pages="totalPages"
      @page-change="goToPage"
    />

    <!-- Create Employee Modal -->
    <EmployeeCreateModal
      :show="showCreateModal"
      :new-employee="newEmployee"
      :available-areas="availableAreas"
      :loading="creating"
      @close="closeCreateModal"
      @create="createEmployee"
    />

    <!-- Delete Modal -->
    <EmployeeDeleteModal
      :show="showDeleteModal"
      :employee="employeeToDelete"
      :loading="deleting"
      @close="closeDeleteModal"
      @confirm="deleteEmployee"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import EmployeeService from '@/services/dss/users/employees'
import { debounce } from 'lodash-es'

definePageMeta({
  layout: 'dss',
  middleware: 'auth'
})

const { t } = useI18n()
const router = useRouter()

// Reactive data
const employees = ref([])
const loading = ref(false)
const showCreateModal = ref(false)
const creating = ref(false)
const showDeleteModal = ref(false)
const employeeToDelete = ref(null)
const deleting = ref(false)

// Pagination
const currentPage = ref(1)
const pageSize = ref(3)
const totalItems = ref(0)
const totalPages = computed(() => Math.ceil(totalItems.value / pageSize.value))

// Filters
const filters = ref({
  search: '',
  area: '',
  status: ''
})

const areas = ref([])

// New employee form data
const newEmployee = ref({
  first_name: '',
  last_name: '',
  work_mail: '',
  personal_mail: '',
  phone: '',
  gender: '',
  date_of_birth: '',
  join_date: '',
  area: '',
  salary: '',
  working_start_time: '',
  working_end_time: '',
  status: 1
})

const availableAreas = computed(() => {
  const uniqueAreas = [...new Set(employees.value.map(emp => emp.area).filter(Boolean))]
  return uniqueAreas.map(area => ({ value: area, label: area }))
})

// Methods
const loadEmployees = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
    }
    
    if (filters.value.area) params.area = filters.value.area
    if (filters.value.status !== '') params.status = filters.value.status
    
    const response = await EmployeeService.getEmployees(params)
    employees.value = response.results || []
    totalItems.value = response.count || 0
    
    const uniqueAreas = [...new Set(employees.value.map(emp => emp.area).filter(Boolean))]
    areas.value = uniqueAreas
    
  } catch (error) {
    console.error('Error loading employees:', error)
    employees.value = []
    totalItems.value = 0
  } finally {
    loading.value = false
  }
}

const handleSearchUpdate = debounce((value: string) => {
  filters.value.search = value
  currentPage.value = 1
  loadEmployees()
}, 300)

const updateFilters = (key: string, value: any) => {
  filters.value[key] = value
  currentPage.value = 1
  loadEmployees()
}

const resetFilters = () => {
  filters.value = {
    search: '',
    area: '',
    status: ''
  }
  currentPage.value = 1
  loadEmployees()
}

const goToPage = (page: number) => {
  currentPage.value = page
  loadEmployees()
}

const viewEmployee = (employee: any) => {
  router.push(`/dss/users/${employee.id}`)
}

const editEmployee = (employee: any) => {
  router.push(`/dss/users/${employee.id}?edit=true`)
}

const confirmDeleteEmployee = (employee: any) => {
  employeeToDelete.value = employee
  showDeleteModal.value = true
}

const closeDeleteModal = () => {
  showDeleteModal.value = false
  employeeToDelete.value = null
  deleting.value = false
}

const resetNewEmployee = () => {
  newEmployee.value = {
    first_name: '',
    last_name: '',
    work_mail: '',
    personal_mail: '',
    phone: '',
    gender: '',
    date_of_birth: '',
    join_date: '',
    area: '',
    salary: '',
    working_start_time: '',
    working_end_time: '',
    status: 1
  }
}

const closeCreateModal = () => {
  showCreateModal.value = false
  resetNewEmployee()
  creating.value = false
}

const createEmployee = async (employeeData: any) => {
  creating.value = true
  try {
    if (!employeeData.first_name || !employeeData.last_name || 
        !employeeData.work_mail || !employeeData.phone) {
      alert(t('please_fill_required_fields'))
      return
    }

    const dataToSend = {
      first_name: employeeData.first_name?.trim(),
      last_name: employeeData.last_name?.trim(),
      work_mail: employeeData.work_mail?.trim(),
      phone: employeeData.phone?.trim(),
      ...(employeeData.personal_mail && { personal_mail: employeeData.personal_mail.trim() }),
      ...(employeeData.gender && { gender: employeeData.gender }),
      ...(employeeData.date_of_birth && { date_of_birth: employeeData.date_of_birth }),
      ...(employeeData.join_date && { join_date: employeeData.join_date }),
      ...(employeeData.area && { area: employeeData.area.trim() }),
      ...(employeeData.salary && { salary: parseFloat(employeeData.salary) }),
      ...(employeeData.working_start_time && { working_start_time: employeeData.working_start_time }),
      ...(employeeData.working_end_time && { working_end_time: employeeData.working_end_time }),
      status: 1
    }

    const response = await EmployeeService.createEmployee(dataToSend)
    employees.value.unshift(response)
    totalItems.value = totalItems.value + 1
    
    alert(`Đã tạo nhân viên ${dataToSend.first_name} ${dataToSend.last_name} thành công!`)
    closeCreateModal()
    
    if (currentPage.value === 1) {
      loadEmployees()
    }
    
  } catch (error) {
    console.error('Error creating employee:', error)
    let errorMessage = 'Có lỗi xảy ra khi tạo nhân viên'
    
    if (error.response?.status === 400) {
      errorMessage = 'Dữ liệu nhập vào không hợp lệ'
    } else if (error.response?.status === 409) {
      errorMessage = 'Email hoặc số điện thoại đã được sử dụng'
    } else if (error.message) {
      errorMessage = error.message
    }
    
    alert(errorMessage)
  } finally {
    creating.value = false
  }
}

const deleteEmployee = async () => {
  if (!employeeToDelete.value) return
  
  deleting.value = true
  try {
    await EmployeeService.deleteEmployee(employeeToDelete.value.id)
    
    employees.value = employees.value.filter(emp => emp.id !== employeeToDelete.value.id)
    totalItems.value = totalItems.value - 1

    alert(`Đã xóa nhân viên ${employeeToDelete.value.first_name} ${employeeToDelete.value.last_name} thành công!`)
    
    if (employees.value.length === 0 && currentPage.value > 1) {
      currentPage.value = currentPage.value - 1
      loadEmployees()
    }
    
  } catch (error) {
    console.error('Error deleting employee:', error)
    alert(`Có lỗi xảy ra khi xóa nhân viên: ${error.message || 'Vui lòng thử lại'}`)
  } finally {
    deleting.value = false
    closeDeleteModal()
  }
}

// Lifecycle
onMounted(() => {
  loadEmployees()
  newEmployee.value.join_date = new Date().toISOString().split('T')[0]
})
</script>