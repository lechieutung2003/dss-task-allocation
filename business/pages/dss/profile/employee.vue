<!-- filepath: e:\Learning\CDCN\dss-task-allocation\business\pages\dss\profile\employee.vue -->
<template>
  <div class="p-6">
    <!-- Header -->
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900">{{ $t('my_profile') }}</h1>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center py-8">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
    </div>

    <!-- Employee Profile -->
    <div v-else-if="employee" class="space-y-6">
      <!-- Header Card -->
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <div class="flex-shrink-0">
              <img
                v-if="employee.avatar"
                :src="employee.avatar"
                :alt="employee.first_name"
                class="h-20 w-20 rounded-full object-cover"
              >
              <div
                v-else
                class="h-20 w-20 rounded-full bg-gray-300 flex items-center justify-center"
              >
                <span class="text-gray-600 text-xl font-medium">
                  {{ getInitials(employee.first_name, employee.last_name) }}
                </span>
              </div>
            </div>
            <div>
              <h2 class="text-2xl font-bold text-gray-900">
                {{ employee.first_name }} {{ employee.last_name }}
              </h2>
              <p class="text-gray-600">{{ employee.work_mail }}</p>
              
              <!-- Real-time status based on working hours -->
              <div class="flex items-center space-x-2 mt-2">
                <span
                  :class="[
                    'inline-flex items-center px-2 py-1 text-xs font-semibold rounded-full',
                    getCurrentStatus().isActive
                      ? 'bg-green-100 text-green-800'
                      : 'bg-red-100 text-red-800'
                  ]"
                >
                  <!-- Status indicator dot -->
                  <div 
                    :class="[
                      'w-2 h-2 rounded-full mr-1', 
                      getCurrentStatus().isActive ? 'bg-green-500 animate-pulse' : 'bg-red-500'
                    ]"
                  ></div>
                  {{ getCurrentStatus().text }}
                </span>
                
                <!-- Real-time clock -->
                <span class="text-xs text-gray-500">
                  {{ $t('current_time') }}: {{ currentTime }}
                </span>
              </div>
              
              <!-- Working hours info -->
              <div v-if="employee.working_start_time && employee.working_end_time" class="mt-1">
                <span class="text-xs text-gray-500">
                  {{ $t('working_hours') }}: {{ employee.working_start_time }} - {{ employee.working_end_time }}
                </span>
              </div>
            </div>
          </div>
          
          <div class="flex space-x-2">
            <button
              v-if="!isEditMode"
              @click="isEditMode = true"
              class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg"
            >
              {{ $t('edit_profile') }}
            </button>
            <template v-else>
              <button
                @click="saveProfile"
                :disabled="saving"
                class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg disabled:opacity-50"
              >
                {{ saving ? $t('saving') : $t('save') }}
              </button>
              <button
                @click="cancelEdit"
                class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg"
              >
                {{ $t('cancel') }}
              </button>
            </template>
          </div>
        </div>
      </div>

      <!-- Profile Information Tabs -->
      <div class="bg-white rounded-lg shadow">
        <!-- Tab Navigation -->
        <div class="border-b border-gray-200">
          <nav class="-mb-px flex space-x-8 px-6">
            <button
              v-for="tab in tabs"
              :key="tab.key"
              @click="activeTab = tab.key"
              :class="[
                'py-4 px-1 border-b-2 font-medium text-sm',
                activeTab === tab.key
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              ]"
            >
              {{ tab.label }}
            </button>
          </nav>
        </div>

        <!-- Tab Content -->
        <div class="p-6">
          <!-- Personal Information -->
          <div v-if="activeTab === 'personal'" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700">{{ $t('first_name') }}</label>
                <input
                  v-model="editableEmployee.first_name"
                  :disabled="!isEditMode"
                  type="text"
                  class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-50"
                >
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">{{ $t('last_name') }}</label>
                <input
                  v-model="editableEmployee.last_name"
                  :disabled="!isEditMode"
                  type="text"
                  class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-50"
                >
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">{{ $t('work_email') }}</label>
                <input
                  v-model="editableEmployee.work_mail"
                  :disabled="true"
                  type="email"
                  class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 text-gray-500"
                >
                <p class="text-xs text-gray-500 mt-1">{{ $t('work_email_cannot_be_changed') }}</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">{{ $t('personal_email') }}</label>
                <input
                  v-model="editableEmployee.personal_mail"
                  :disabled="!isEditMode"
                  type="email"
                  class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-50"
                >
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">{{ $t('phone') }}</label>
                <input
                  v-model="editableEmployee.phone"
                  :disabled="!isEditMode"
                  type="text"
                  class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-50"
                >
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">{{ $t('gender') }}</label>
                <select
                  v-model="editableEmployee.gender"
                  :disabled="!isEditMode"
                  class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-50"
                >
                  <option value="male">{{ $t('male') }}</option>
                  <option value="female">{{ $t('female') }}</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">{{ $t('date_of_birth') }}</label>
                <input
                  v-model="editableEmployee.date_of_birth"
                  :disabled="!isEditMode"
                  type="date"
                  class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-50"
                >
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">{{ $t('join_date') }}</label>
                <input
                  v-model="editableEmployee.join_date"
                  :disabled="true"
                  type="date"
                  class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 text-gray-500"
                >
                <p class="text-xs text-gray-500 mt-1">{{ $t('join_date_cannot_be_changed') }}</p>
              </div>
            </div>
          </div>

          <!-- Work Information -->
          <div v-if="activeTab === 'work'" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <!-- Area - Cho phép edit -->
              <div>
                <label class="block text-sm font-medium text-gray-700">{{ $t('area') }}</label>
                <input
                  v-model="editableEmployee.area"
                  :disabled="!isEditMode"
                  type="text"
                  class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-50"
                  :placeholder="$t('enter_work_area')"
                >
                <p v-if="!isEditMode" class="text-xs text-gray-500 mt-1">{{ $t('area_can_be_edited') }}</p>
              </div>
              
              <!-- Salary - Vẫn không cho edit -->
              <div>
                <label class="block text-sm font-medium text-gray-700">{{ $t('salary') }}</label>
                <input
                  v-model="editableEmployee.salary"
                  :disabled="true"
                  type="number"
                  class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 text-gray-500"
                >
                <p class="text-xs text-gray-500 mt-1">{{ $t('salary_managed_by_admin') }}</p>
              </div>
              
              <!-- Working Start Time - Cho phép edit -->
              <div>
                <label class="block text-sm font-medium text-gray-700">{{ $t('working_start_time') }}</label>
                <input
                  v-model="editableEmployee.working_start_time"
                  :disabled="!isEditMode"
                  type="time"
                  class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-50"
                  @change="validateWorkingHours"
                >
                <p v-if="!isEditMode" class="text-xs text-gray-500 mt-1">{{ $t('working_hours_can_be_edited') }}</p>
              </div>
              
              <!-- Working End Time - Cho phép edit -->
              <div>
                <label class="block text-sm font-medium text-gray-700">{{ $t('working_end_time') }}</label>
                <input
                  v-model="editableEmployee.working_end_time"
                  :disabled="!isEditMode"
                  type="time"
                  class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-50"
                  @change="validateWorkingHours"
                >
              </div>
            </div>

            <!-- Status Overview Card -->
            <div class="mt-6 p-4 border rounded-lg" :class="getCurrentStatus().isActive ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50'">
              <div class="flex items-center justify-between">
                <div>
                  <h4 class="font-medium" :class="getCurrentStatus().isActive ? 'text-green-900' : 'text-red-900'">
                    {{ $t('current_work_status') }}
                  </h4>
                  <p class="text-sm" :class="getCurrentStatus().isActive ? 'text-green-700' : 'text-red-700'">
                    {{ getCurrentStatus().text }}
                  </p>
                  <p class="text-xs" :class="getCurrentStatus().isActive ? 'text-green-600' : 'text-red-600'">
                    {{ getCurrentStatus().description }}
                  </p>
                </div>
                <div class="flex items-center">
                  <div 
                    :class="[
                      'w-4 h-4 rounded-full', 
                      getCurrentStatus().isActive ? 'bg-green-500 animate-pulse' : 'bg-red-500'
                    ]"
                  ></div>
                </div>
              </div>
            </div>

            <!-- Working Hours Summary -->
            <div v-if="editableEmployee.working_start_time && editableEmployee.working_end_time" class="mt-4 p-4 bg-blue-50 rounded-lg">
              <h4 class="text-sm font-medium text-blue-900">{{ $t('working_hours_summary') }}</h4>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-2">
                <div>
                  <p class="text-sm text-blue-700">
                    {{ $t('daily_working_hours') }}: {{ calculateDailyWorkingHours() }} {{ $t('hours') }}
                  </p>
                </div>
                <div>
                  <p class="text-sm text-blue-700">
                    {{ $t('shift_type') }}: {{ getShiftType() }}
                  </p>
                </div>
                <div>
                  <p class="text-sm text-blue-700">
                    {{ $t('time_until_next_change') }}: {{ getTimeUntilNextChange() }}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- Performance -->
          <div v-if="activeTab === 'performance'" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div class="bg-blue-50 p-4 rounded-lg">
                <div class="text-2xl font-bold text-blue-600">{{ employee.completed_orders_count || 0 }}</div>
                <div class="text-sm text-gray-600">{{ $t('completed_orders') }}</div>
              </div>
              <div class="bg-green-50 p-4 rounded-lg">
                <div class="text-2xl font-bold text-green-600">{{ employee.total_hours_worked || 0 }}h</div>
                <div class="text-sm text-gray-600">{{ $t('total_hours_worked') }}</div>
              </div>
              <div class="bg-purple-50 p-4 rounded-lg">
                <div class="text-2xl font-bold text-purple-600">
                  {{ calculateAverageHoursPerOrder() }}h
                </div>
                <div class="text-sm text-gray-600">{{ $t('avg_hours_per_order') }}</div>
              </div>
            </div>
            
            <!-- Performance Chart Placeholder -->
            <div class="mt-6 p-6 border-2 border-dashed border-gray-300 rounded-lg text-center">
              <p class="text-gray-500">{{ $t('performance_charts_coming_soon') }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Error State -->
    <div v-else class="text-center py-8">
      <h3 class="text-lg font-medium text-gray-900">{{ $t('profile_not_found') }}</h3>
      <p class="text-gray-500">{{ $t('cannot_load_profile') }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import EmployeeService from '@/services/dss/users/employees'
import { useOauthStore } from '@/stores/oauth'

const { t } = useI18n()
const oauthStore = useOauthStore()

// Reactive data
const employee = ref(null)
const editableEmployee = ref({})
const loading = ref(false)
const saving = ref(false)
const isEditMode = ref(false)
const activeTab = ref('personal')
const currentTime = ref('')
let timeInterval: NodeJS.Timeout | null = null

const tabs = computed(() => [
  { key: 'personal', label: t('personal_information') },
  { key: 'work', label: t('work_information') },
  { key: 'performance', label: t('performance') }
])

// Method tính current status dựa trên working hours
const getCurrentStatus = () => {
  if (!employee.value?.working_start_time || !employee.value?.working_end_time) {
    return {
      isActive: false,
      text: t('no_working_hours'),
      description: t('working_hours_not_set')
    }
  }

  const now = new Date()
  const currentTimeString = now.toTimeString().slice(0, 5) // HH:MM format
  
  const startTime = employee.value.working_start_time
  const endTime = employee.value.working_end_time
  
  let isActive = false
  let text = ''
  let description = ''

  // So sánh thời gian (string format HH:MM)
  if (startTime <= endTime) {
    // Normal working hours (same day)
    isActive = currentTimeString >= startTime && currentTimeString <= endTime
  } else {
    // Overnight shift
    isActive = currentTimeString >= startTime || currentTimeString <= endTime
  }

  if (isActive) {
    text = t('active_working')
    description = t('employee_currently_in_working_hours')
  } else {
    if (currentTimeString < startTime) {
      text = t('offline_not_started')
      description = t('work_starts_at').replace('{time}', startTime)
    } else {
      text = t('offline_ended')
      description = t('work_ended_at').replace('{time}', endTime)
    }
  }

  return { isActive, text, description }
}

// Update current time every second
const updateCurrentTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleTimeString('vi-VN', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

// Get shift type
const getShiftType = () => {
  if (!employee.value?.working_start_time || !employee.value?.working_end_time) {
    return t('not_set')
  }
  
  const startTime = employee.value.working_start_time
  const endTime = employee.value.working_end_time
  
  if (startTime <= endTime) {
    return t('regular_shift')
  } else {
    return t('overnight_shift')
  }
}

// Calculate time until next status change
const getTimeUntilNextChange = () => {
  if (!employee.value?.working_start_time || !employee.value?.working_end_time) {
    return t('not_available')
  }

  const now = new Date()
  const currentTimeString = now.toTimeString().slice(0, 5)
  const startTime = employee.value.working_start_time
  const endTime = employee.value.working_end_time
  
  const currentMinutes = parseInt(currentTimeString.split(':')[0]) * 60 + parseInt(currentTimeString.split(':')[1])
  const startMinutes = parseInt(startTime.split(':')[0]) * 60 + parseInt(startTime.split(':')[1])
  const endMinutes = parseInt(endTime.split(':')[0]) * 60 + parseInt(endTime.split(':')[1])
  
  let minutesUntilChange = 0
  let nextEvent = ''
  
  if (startTime <= endTime) {
    // Normal shift
    if (currentMinutes < startMinutes) {
      minutesUntilChange = startMinutes - currentMinutes
      nextEvent = t('work_starts')
    } else if (currentMinutes < endMinutes) {
      minutesUntilChange = endMinutes - currentMinutes
      nextEvent = t('work_ends')
    } else {
      minutesUntilChange = (24 * 60) - currentMinutes + startMinutes
      nextEvent = t('work_starts')
    }
  } else {
    // Overnight shift
    if (currentMinutes >= startMinutes || currentMinutes < endMinutes) {
      if (currentMinutes >= startMinutes) {
        minutesUntilChange = (24 * 60) - currentMinutes + endMinutes
      } else {
        minutesUntilChange = endMinutes - currentMinutes
      }
      nextEvent = t('work_ends')
    } else {
      minutesUntilChange = startMinutes - currentMinutes
      nextEvent = t('work_starts')
    }
  }
  
  const hours = Math.floor(minutesUntilChange / 60)
  const minutes = minutesUntilChange % 60
  
  if (hours > 0) {
    return `${hours}h ${minutes}m (${nextEvent})`
  } else {
    return `${minutes}m (${nextEvent})`
  }
}

// Validation cho working hours
const validateWorkingHours = () => {
  const startTime = editableEmployee.value.working_start_time
  const endTime = editableEmployee.value.working_end_time
  
  if (!startTime || !endTime) return true
  
  if (startTime === endTime) {
    alert(t('start_end_time_cannot_be_same'))
    return false
  }
  
  return true
}

// Methods
const loadMyProfile = async () => {
  loading.value = true
  try {
    const response = await EmployeeService.getMyProfile()
    console.log('My profile:', response)
    
    if (response) {
      employee.value = response
      editableEmployee.value = { ...response }
    } else {
      console.error('No profile data received')
    }
  } catch (error) {
    console.error('Error loading profile:', error)
    
    try {
      console.log('Trying fallback with employees list...')
      const employeesResponse = await EmployeeService.getEmployees()
      console.log('Employees response:', employeesResponse)
      
      if (employeesResponse.results && employeesResponse.results.length > 0) {
        employee.value = employeesResponse.results[0]
        editableEmployee.value = { ...employee.value }
      }
    } catch (fallbackError) {
      console.error('Fallback also failed:', fallbackError)
    }
  } finally {
    loading.value = false
  }
}

const saveProfile = async () => {
  if (!validateWorkingHours()) {
    return
  }
  
  saving.value = true
  try {
    const allowedFields = {
      first_name: editableEmployee.value.first_name,
      last_name: editableEmployee.value.last_name,
      personal_mail: editableEmployee.value.personal_mail,
      phone: editableEmployee.value.phone,
      gender: editableEmployee.value.gender,
      date_of_birth: editableEmployee.value.date_of_birth,
      area: editableEmployee.value.area,
      working_start_time: editableEmployee.value.working_start_time,
      working_end_time: editableEmployee.value.working_end_time
    }
    
    const response = await EmployeeService.updateMyProfile(allowedFields)
    employee.value = response
    editableEmployee.value = { ...response }
    isEditMode.value = false
    
    alert(t('profile_updated_successfully'))
  } catch (error) {
    console.error('Error saving profile:', error)
    alert(t('error_saving_profile'))
  } finally {
    saving.value = false
  }
}

const cancelEdit = () => {
  editableEmployee.value = { ...employee.value }
  isEditMode.value = false
}

const calculateAverageHoursPerOrder = () => {
  if (!employee.value || employee.value.completed_orders_count === 0) return 0
  return (employee.value.total_hours_worked / employee.value.completed_orders_count).toFixed(1)
}

const calculateDailyWorkingHours = () => {
  if (!editableEmployee.value.working_start_time || !editableEmployee.value.working_end_time) {
    return "0"
  }
  
  const startTime = editableEmployee.value.working_start_time
  const endTime = editableEmployee.value.working_end_time
  
  const start = new Date(`2000-01-01T${startTime}:00`)
  let end = new Date(`2000-01-01T${endTime}:00`)
  
  // Handle overnight shift
  if (end <= start) {
    end = new Date(`2000-01-02T${endTime}:00`) // Next day
  }
  
  const diffMs = end.getTime() - start.getTime()
  const diffHours = diffMs / (1000 * 60 * 60)
  
  return diffHours.toFixed(1)
}

const getInitials = (firstName: string, lastName: string) => {
  return `${firstName?.charAt(0) || ''}${lastName?.charAt(0) || ''}`.toUpperCase()
}

// Lifecycle
onMounted(() => {
  loadMyProfile()
  
  // Start real-time clock
  updateCurrentTime()
  timeInterval = setInterval(updateCurrentTime, 1000)
})

onUnmounted(() => {
  // Clean up interval
  if (timeInterval) {
    clearInterval(timeInterval)
  }
})
</script>