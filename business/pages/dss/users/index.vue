<template>
  <div class="p-6">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6 mt-10">
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
    <div class="bg-white rounded-lg shadow mb-6 p-4">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('search') }}</label>
          <input
            v-model="filters.search"
            type="text"
            :placeholder="$t('search_employee')"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            @input="debouncedSearch"
          >
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('area') }}</label>
          <select
            v-model="filters.area"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            @change="loadEmployees"
          >
            <option value="">{{ $t('all_areas') }}</option>
            <option v-for="area in areas" :key="area" :value="area">{{ area }}</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('status') }}</label>
          <select
            v-model="filters.status"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            @change="loadEmployees"
          >
            <option value="">{{ $t('all_status') }}</option>
            <option value="1">{{ $t('active') }}</option>
            <option value="0">{{ $t('inactive') }}</option>
          </select>
        </div>
        <div class="flex items-end">
          <button
            @click="resetFilters"
            class="w-full px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50"
          >
            {{ $t('reset') }}
          </button>
        </div>
      </div>
    </div>

    <!-- Employee Table -->
    <div class="bg-white rounded-lg shadow overflow-hidden">
      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center py-8">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>

      <!-- Create Employee Modal -->
    <div
      v-if="showCreateModal"
      class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
      @click="closeCreateModal"
    >
      <div class="relative top-10 mx-auto p-5 border w-full max-w-4xl shadow-lg rounded-md bg-white" @click.stop>
        <div class="mt-3">
          <!-- Modal Header -->
          <div class="flex items-center justify-between pb-4 border-b">
            <h3 class="text-lg font-medium text-gray-900">{{ $t('add_new_employee') }}</h3>
            <button
              @click="closeCreateModal"
              class="text-gray-400 hover:text-gray-600"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>

          <!-- Modal Body -->
          <div class="py-4 max-h-[500px] overflow-y-auto">
            <form @submit.prevent="createEmployee">
              <!-- Personal Information Section -->
              <div class="mb-6">
                <h4 class="text-md font-medium text-gray-900 mb-3">{{ $t('personal_information') }}</h4>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      {{ $t('first_name') }} <span class="text-red-500">*</span>
                    </label>
                    <input
                      v-model="newEmployee.first_name"
                      type="text"
                      required
                      class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      :placeholder="$t('enter_first_name')"
                    >
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      {{ $t('last_name') }} <span class="text-red-500">*</span>
                    </label>
                    <input
                      v-model="newEmployee.last_name"
                      type="text"
                      required
                      class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      :placeholder="$t('enter_last_name')"
                    >
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      {{ $t('work_email') }} <span class="text-red-500">*</span>
                    </label>
                    <input
                      v-model="newEmployee.work_mail"
                      type="email"
                      required
                      class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      :placeholder="$t('enter_work_email')"
                    >
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      {{ $t('phone') }} <span class="text-red-500">*</span>
                    </label>
                    <input
                      v-model="newEmployee.phone"
                      type="tel"
                      required
                      class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      :placeholder="$t('enter_phone')"
                    >
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('personal_email') }}</label>
                    <input
                      v-model="newEmployee.personal_mail"
                      type="email"
                      class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      :placeholder="$t('enter_personal_email')"
                    >
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('gender') }}</label>
                    <select
                      v-model="newEmployee.gender"
                      class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="">{{ $t('select_gender') }}</option>
                      <option value="male">{{ $t('male') }}</option>
                      <option value="female">{{ $t('female') }}</option>
                    </select>
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('date_of_birth') }}</label>
                    <input
                      v-model="newEmployee.date_of_birth"
                      type="date"
                      class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('join_date') }}</label>
                    <input
                      v-model="newEmployee.join_date"
                      type="date"
                      class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                  </div>
                </div>
              </div>

              <!-- Work Information Section -->
              <div class="mb-6">
                <h4 class="text-md font-medium text-gray-900 mb-3">{{ $t('work_information') }}</h4>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-4xl">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('area') }}</label>
                    <select
                      v-model="newEmployee.area"
                      class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                      <option value="">{{ $t('select_area') }}</option>
                      <option v-for="area in availableAreas" :key="area.value" :value="area.value">
                      {{ area.label }}
                      </option>
                    </select>
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('salary') }}</label>
                    <input
                      v-model="newEmployee.salary"
                      type="number"
                      step="0.01"
                      class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      :placeholder="$t('enter_salary')"
                    >
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('working_start_time') }}</label>
                    <input
                      v-model="newEmployee.working_start_time"
                      type="time"
                      class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('working_end_time') }}</label>
                    <input
                      v-model="newEmployee.working_end_time"
                      type="time"
                      class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                  </div>
                </div>
              </div>

              <!-- Modal Footer -->
              <div class="flex items-center justify-end pt-4 border-t space-x-3">
                <button
                  type="button"
                  @click="closeCreateModal"
                  :disabled="creating"
                  class="px-4 py-2 bg-gray-300 text-gray-700 text-base font-medium rounded-md shadow-sm hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 disabled:opacity-50"
                >
                  {{ $t('cancel') }}
                </button>
                <button
                  type="submit"
                  :disabled="creating"
                  class="px-4 py-2 bg-blue-600 text-white text-base font-medium rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
                >
                  {{ creating ? $t('creating') : $t('create_employee') }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

      <!-- Table -->
      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                {{ $t('employee') }}
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                {{ $t('contact') }}
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                {{ $t('work_info') }}
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                {{ $t('performance') }}
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                {{ $t('status') }}
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                {{ $t('actions') }}
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="employee in employees" :key="employee.id" class="hover:bg-gray-50">
              <!-- Employee Info -->
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="flex-shrink-0 h-10 w-10">
                    <img
                      v-if="employee.avatar"
                      :src="employee.avatar"
                      :alt="employee.first_name"
                      class="h-10 w-10 rounded-full object-cover"
                    >
                    <div
                      v-else
                      class="h-10 w-10 rounded-full bg-gray-300 flex items-center justify-center"
                    >
                      <span class="text-gray-600 font-medium">
                        {{ getInitials(employee.first_name, employee.last_name) }}
                      </span>
                    </div>
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900">
                      {{ employee.first_name }} {{ employee.last_name }}
                    </div>
                    <div class="text-sm text-gray-500">
                      ID: {{ employee.id }}
                    </div>
                  </div>
                </div>
              </td>

              <!-- Contact Info -->
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">{{ employee.work_mail }}</div>
                <div class="text-sm text-gray-500">{{ employee.phone }}</div>
              </td>

              <!-- Work Info -->
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">{{ employee.area || 'N/A' }}</div>
                <div class="text-sm text-gray-500">
                  {{ formatWorkingHours(employee.working_start_time, employee.working_end_time) }}
                </div>
                <div class="text-sm text-gray-500">
                  {{ $t('salary') }}: {{ formatCurrency(employee.salary) }}
                </div>
              </td>

              <!-- Performance -->
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">
                  {{ $t('completed_orders') }}: {{ employee.completed_orders_count || 0 }}
                </div>
                <div class="text-sm text-gray-500">
                  {{ $t('total_hours') }}: {{ employee.total_hours_worked || 0 }}h
                </div>
              </td>

              <!-- Status -->
              <td class="px-6 py-4 whitespace-nowrap">
                <span
                  :class="[
                    'inline-flex px-2 py-1 text-xs font-semibold rounded-full',
                    employee.status === 1
                      ? 'bg-green-100 text-green-800'
                      : 'bg-red-100 text-red-800'
                  ]"
                >
                  {{ employee.status === 1 ? $t('active') : $t('inactive') }}
                </span>
              </td>

              <!-- Actions -->
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <div class="flex space-x-2">
                  <button
                    @click="viewEmployee(employee)"
                    class="text-blue-600 hover:text-blue-900"
                  >
                    {{ $t('view') }}
                  </button>
                  <button
                    @click="editEmployee(employee)"
                    class="text-green-600 hover:text-green-900"
                  >
                    {{ $t('edit') }}
                  </button>
                  <button
                    @click="confirmDeleteEmployee(employee)"
                    class="text-red-600 hover:text-red-900"
                  >
                    {{ $t('delete') }}
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Empty State -->
        <div v-if="!loading && employees.length === 0" class="text-center py-8">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">{{ $t('no_employees') }}</h3>
          <p class="mt-1 text-sm text-gray-500">{{ $t('no_employees_description') }}</p>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="bg-gray-50 px-6 py-3">
        <div class="flex items-center justify-between">
          <div class="text-sm text-gray-700">
            {{ $t('showing') }} {{ (currentPage - 1) * pageSize + 1 }} {{ $t('to') }} 
            {{ Math.min(currentPage * pageSize, totalItems) }} {{ $t('of') }} {{ totalItems }} {{ $t('results') }}
          </div>
          <div class="flex space-x-2">
            <button
              @click="goToPage(currentPage - 1)"
              :disabled="currentPage === 1"
              class="px-3 py-1 border border-gray-300 rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
            >
              {{ $t('previous') }}
            </button>
            <button
              v-for="page in visiblePages"
              :key="page"
              @click="goToPage(page)"
              :class="[
                'px-3 py-1 border rounded-md',
                page === currentPage
                  ? 'bg-blue-600 border-blue-600 text-white'
                  : 'border-gray-300 hover:bg-gray-50'
              ]"
            >
              {{ page }}
            </button>
            <button
              @click="goToPage(currentPage + 1)"
              :disabled="currentPage === totalPages"
              class="px-3 py-1 border border-gray-300 rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
            >
              {{ $t('next') }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Modal -->
    <div
      v-if="showDeleteModal"
      class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
      @click="closeDeleteModal"
    >
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white" @click.stop>
        <div class="mt-3 text-center">
          <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100">
            <svg class="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.5 0L4.268 15.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-900 mt-2">{{ $t('confirm_delete') }}</h3>
          <div class="mt-2 px-7 py-3">
            <p class="text-sm text-gray-500">
              {{ $t('confirm_delete_employee_message', { 
                name: `${employeeToDelete?.first_name} ${employeeToDelete?.last_name}` 
              }) }}
            </p>
            <p class="text-xs text-red-500 mt-2">
              {{ $t('this_action_cannot_be_undone') }}
            </p>
          </div>
          <div class="items-center px-4 py-3">
            <div class="flex space-x-3">
              <button
                @click="deleteEmployee"
                :disabled="deleting"
                class="w-full px-4 py-2 bg-red-600 text-white text-base font-medium rounded-md shadow-sm hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 disabled:opacity-50"
              >
                {{ deleting ? $t('deleting') : $t('delete') }}
              </button>
              <button
                @click="closeDeleteModal"
                :disabled="deleting"
                class="w-full px-4 py-2 bg-gray-300 text-gray-700 text-base font-medium rounded-md shadow-sm hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 disabled:opacity-50"
              >
                {{ $t('cancel') }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
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

const availableAreas = computed(() => {
  const uniqueAreas = [...new Set(employees.value.map(emp => emp.area).filter(Boolean))]
  return uniqueAreas.map(area => ({ value: area, label: area }))
})
  
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
  status: 1 // Default active
})

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

const createEmployee = async () => {
  creating.value = true
  try {
    // Validate required fields
    if (!newEmployee.value.first_name || !newEmployee.value.last_name || 
        !newEmployee.value.work_mail || !newEmployee.value.phone) {
      alert(t('please_fill_required_fields'))
      return
    }

    // Prepare data for API
    const employeeData = {
      first_name: newEmployee.value.first_name?.trim(),
      last_name: newEmployee.value.last_name?.trim(),
      work_mail: newEmployee.value.work_mail?.trim(),
      phone: newEmployee.value.phone?.trim(),
      // Optional fields - chỉ gửi nếu có giá trị
      ...(newEmployee.value.personal_mail && { 
        personal_mail: newEmployee.value.personal_mail.trim() 
      }),
      ...(newEmployee.value.gender && { 
        gender: newEmployee.value.gender 
      }),
      ...(newEmployee.value.date_of_birth && { 
        date_of_birth: newEmployee.value.date_of_birth 
      }),
      ...(newEmployee.value.join_date && { 
        join_date: newEmployee.value.join_date 
      }),
      ...(newEmployee.value.area && { 
        area: newEmployee.value.area.trim() 
      }),
      ...(newEmployee.value.salary && { 
        salary: parseFloat(newEmployee.value.salary) 
      }),
      ...(newEmployee.value.working_start_time && { 
        working_start_time: newEmployee.value.working_start_time 
      }),
      ...(newEmployee.value.working_end_time && { 
        working_end_time: newEmployee.value.working_end_time 
      }),
      status: 1 // Default active
    }

    // Convert salary to number if provided
    if (employeeData.salary) {
      employeeData.salary = parseFloat(employeeData.salary)
    }

    // Call API to create employee
    const response = await EmployeeService.createEmployee(employeeData)
    
    // Add new employee to local list
    employees.value.unshift(response)
    totalItems.value = totalItems.value + 1
    
    // Show success message
    alert(`Đã tạo nhân viên ${employeeData.first_name} ${employeeData.last_name} thành công!`)
    
    // Close modal
    closeCreateModal()
    
    // Optionally reload first page to get fresh data
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

const showDeleteModal = ref(false)
const employeeToDelete = ref(null)
const deleting = ref(false)

// Pagination
const currentPage = ref(1)
const pageSize = ref(4)
const totalItems = ref(0)
const totalPages = computed(() => Math.ceil(totalItems.value / pageSize.value))

// Filters
const filters = ref({
  search: '',
  area: '',
  status: ''
})

const areas = ref([])

// Computed
const visiblePages = computed(() => {
  const pages = []
  const start = Math.max(1, currentPage.value - 2)
  const end = Math.min(totalPages.value, currentPage.value + 2)
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  return pages
})

// Methods
const loadEmployees = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
    }
    
    // Chỉ thêm params có giá trị
    if (filters.value.area) {
      params.area = filters.value.area
    }
    if (filters.value.status !== '') {
      params.status = filters.value.status
    }
    
    const response = await EmployeeService.getEmployees(params)
    employees.value = response.results || []
    totalItems.value = response.count || 0
    
    // Extract unique areas for filter
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

const debouncedSearch = debounce(() => {
  currentPage.value = 1
  loadEmployees()
}, 300)

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

const deleteEmployee = async () => {
  if (!employeeToDelete.value) return
  
  deleting.value = true
  try {
    await EmployeeService.deleteEmployee(employeeToDelete.value.id)
    
    // Xóa employee khỏi danh sách local
    employees.value = employees.value.filter(emp => emp.id !== employeeToDelete.value.id)
    totalItems.value = totalItems.value - 1

    alert(`Đã xóa nhân viên ${employeeToDelete.value.first_name} ${employeeToDelete.value.last_name} thành công!`)
    
    // Show success notification
    console.log(`Employee ${employeeToDelete.value.first_name} ${employeeToDelete.value.last_name} deleted successfully`)
    
    // Nếu trang hiện tại không có dữ liệu và không phải trang đầu thì về trang trước
    if (employees.value.length === 0 && currentPage.value > 1) {
      currentPage.value = currentPage.value - 1
      loadEmployees()
    }
    
  } catch (error) {
    console.error('Error deleting employee:', error)
    alert(`Có lỗi xảy ra khi xóa nhân viên: ${error.message || 'Vui lòng thử lại'}`)
  } finally {
    deleting.value = false
    // Đóng modal
    closeDeleteModal()
  }
}

// Utility functions
const getInitials = (firstName: string, lastName: string) => {
  const first = firstName?.trim()?.charAt(0)?.toUpperCase() || ''
  const last = lastName?.trim()?.charAt(0)?.toUpperCase() || ''
  return (first + last) || 'N/A'
}

const formatWorkingHours = (startTime: string, endTime: string) => {
  if (!startTime || !endTime) return 'N/A'
  return `${startTime} - ${endTime}`
}

const formatCurrency = (amount: number) => {
  if (!amount) return 'N/A'
  return new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(amount)
}

// Lifecycle
onMounted(() => {
  loadEmployees()
  newEmployee.value.join_date = new Date().toISOString().split('T')[0]
})
</script>