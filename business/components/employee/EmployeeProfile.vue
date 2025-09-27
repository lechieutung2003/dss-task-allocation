<template>
  <div class="space-y-6">
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
              
              <!-- Single Status Badge - Auto-computed -->
              <div class="flex items-center space-x-2 mt-2">
                <span :class="getStatusBadgeClass()">
                  {{ getStatusText() }}
                </span>
                
                <!-- Current Time Display -->
                <div class="inline-flex items-center px-2 py-1 text-xs font-medium rounded bg-gray-100 text-gray-600 space-x-1">
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  <span>{{ getCurrentTime() }}</span>
                  <span class="text-gray-400">ICT</span>
                </div>
              </div>
            </div>
          </div>
          
          <div class="flex space-x-2">
            <button
              v-if="!isEditMode"
              @click="toggleEditMode"
              class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg"
            >
              {{ isAdminView ? $t('edit') : $t('edit_profile') }}
            </button>
            <template v-else>
              <button
                @click="handleSave"
                :disabled="saving"
                class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg disabled:opacity-50"
              >
                {{ saving ? $t('saving') : $t('save') }}
              </button>
              <button
                @click="handleCancel"
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
                  :disabled="!isEditMode || !isAdminView"
                  type="email"
                  :class="[
                    'mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                    (!isEditMode || !isAdminView) ? 'bg-gray-50 text-gray-500' : ''
                  ]"
                >
                <p v-if="!isAdminView" class="text-xs text-gray-500 mt-1">{{ $t('work_email_cannot_be_changed') }}</p>
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
                  <option value="">{{ $t('select_gender') }}</option>
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
                  :disabled="!isEditMode || !isAdminView"
                  type="date"
                  :class="[
                    'mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                    (!isEditMode || !isAdminView) ? 'bg-gray-50 text-gray-500' : ''
                  ]"
                >
                <p v-if="!isAdminView" class="text-xs text-gray-500 mt-1">{{ $t('join_date_cannot_be_changed') }}</p>
              </div>
            </div>
          </div>

          <!-- Work Information -->
          <div v-if="activeTab === 'work'" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700">{{ $t('area') }}</label>
                <input
                  v-model="editableEmployee.area"
                  :disabled="!isEditMode"
                  type="text"
                  class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-50"
                  :placeholder="$t('enter_work_area')"
                >
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700">{{ $t('salary') }}</label>
                <input
                  v-model="editableEmployee.salary"
                  :disabled="!isEditMode || !isAdminView"
                  type="number"
                  step="0.01"
                  :class="[
                    'mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                    (!isEditMode || !isAdminView) ? 'bg-gray-50 text-gray-500' : ''
                  ]"
                >
                <p v-if="!isAdminView" class="text-xs text-gray-500 mt-1">{{ $t('salary_managed_by_admin') }}</p>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700">
                  {{ $t('working_start_time') }}
                </label>
                <input
                  v-model="editableEmployee.working_start_time"
                  :disabled="!isEditMode"
                  type="time"
                  class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-50"
                  @change="validateWorkingHours"
                >
                <p class="text-xs text-gray-500 mt-1">{{ $t('status_auto_calculated') }}</p>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700">
                  {{ $t('working_end_time') }}
                </label>
                <input
                  v-model="editableEmployee.working_end_time"
                  :disabled="!isEditMode"
                  type="time"
                  class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-50"
                  @change="validateWorkingHours"
                >
                <p class="text-xs text-gray-500 mt-1">{{ $t('status_auto_calculated') }}</p>
              </div>
            </div>

            <!-- Status Summary Card - Read-only -->
            <div class="mt-6 p-4 rounded-lg" :class="getStatusCardClass()">
              <div class="flex items-center justify-between">
                <div>
                  <h4 class="font-medium" :class="getStatusTextClass()">
                    {{ $t('working_status') }}
                  </h4>
                  <p class="text-sm" :class="getStatusTextClass()">
                    {{ getStatusText() }}
                  </p>
                  <p class="text-xs mt-1" :class="getStatusTextClass()">
                    {{ getStatusDescription() }}
                  </p>
                </div>
                <div class="flex items-center">
                  <div :class="getStatusIconClass()"></div>
                </div>
              </div>
            </div>

            <!-- ❌ REMOVED: Working Hours Summary section -->
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
      <h3 class="text-lg font-medium text-gray-900">
        {{ isAdminView ? $t('employee_not_found') : $t('profile_not_found') }}
      </h3>
      <p class="text-gray-500">
        {{ isAdminView ? $t('employee_not_found_description') : $t('cannot_load_profile') }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

// Props
interface Props {
  employee?: any
  loading?: boolean
  saving?: boolean
  isAdminView?: boolean
  editMode?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  employee: null,
  loading: false,
  saving: false,
  isAdminView: false,
  editMode: false
})

// Emits
const emit = defineEmits<{
  save: [data: any]
  cancel: []
  'update:editMode': [value: boolean]
}>()

// Reactive data
const editableEmployee = ref({})
const isEditMode = ref(props.editMode)
const activeTab = ref('personal')

// Current time reactive
const currentTime = ref(new Date())
let timeInterval: NodeJS.Timeout | null = null

// Computed
const tabs = computed(() => [
  { key: 'personal', label: t('personal_information') },
  { key: 'work', label: t('work_information') },
  { key: 'performance', label: t('performance') }
])

// Watch props changes
watch(() => props.employee, (newEmployee) => {
  if (newEmployee) {
    editableEmployee.value = { ...newEmployee }
  }
}, { immediate: true })

watch(() => props.editMode, (newValue) => {
  isEditMode.value = newValue
})

// Helper function to get actual status consistently
const getActualStatus = () => {
  const emp = props.employee || editableEmployee.value
  
  // Force check: if no working hours then status = 0 (YELLOW)
  if (!emp?.working_start_time || !emp?.working_end_time) {
    return 0
  }
  
  // Has working hours, use status from backend
  return emp.computed_status ?? emp.status ?? 1
}

// Status badge class function
const getStatusBadgeClass = () => {
  const actualStatus = getActualStatus()
  
  console.log('=== DEBUG STATUS ===')
  console.log('Employee:', props.employee || editableEmployee.value)
  console.log('Actual status:', actualStatus)
  console.log('====================')
  
  const baseClass = 'inline-flex px-2 py-1 text-xs font-semibold rounded-full'
  
  switch (actualStatus) {
    case 0: // No working hours - YELLOW
      console.log('Applying YELLOW badge')
      return `${baseClass} bg-yellow-100 text-yellow-800`
    case 1: // Active - GREEN
      console.log('Applying GREEN badge')
      return `${baseClass} bg-green-100 text-green-800`
    case 2: // Inactive - RED
      console.log('Applying RED badge')
      return `${baseClass} bg-red-100 text-red-800`
    default:
      console.log('Applying GRAY badge (unknown status)')
      return `${baseClass} bg-gray-100 text-gray-800`
  }
}

// Status card class function
const getStatusCardClass = () => {
  const actualStatus = getActualStatus()
  
  console.log('Card status:', actualStatus)
  
  switch (actualStatus) {
    case 0: return 'border-yellow-200 bg-yellow-50'
    case 1: return 'border-green-200 bg-green-50'
    case 2: return 'border-red-200 bg-red-50'
    default: return 'border-gray-200 bg-gray-50'
  }
}

// Status text class function
const getStatusTextClass = () => {
  const actualStatus = getActualStatus()
  
  console.log('Text status:', actualStatus)
  
  switch (actualStatus) {
    case 0: return 'text-yellow-700'
    case 1: return 'text-green-700'
    case 2: return 'text-red-700'
    default: return 'text-gray-700'
  }
}

// Status icon class function
const getStatusIconClass = () => {
  const actualStatus = getActualStatus()
  
  console.log('Icon status:', actualStatus)
  
  const baseClass = 'w-4 h-4 rounded-full'
  
  switch (actualStatus) {
    case 0: return `${baseClass} bg-yellow-500`
    case 1: return `${baseClass} bg-green-500`
    case 2: return `${baseClass} bg-red-500`
    default: return `${baseClass} bg-gray-500`
  }
}

// Get status text
const getStatusText = () => {
  // Use backend computed status text if available
  if (props.employee?.status_text) {
    return props.employee.status_text
  }
  
  // Fallback: compute on frontend
  const emp = props.employee || editableEmployee.value
  
  if (!emp?.working_start_time || !emp?.working_end_time) {
    return t('no_working_hours_set')
  }
  
  return t('status_will_be_calculated')
}

// Get status description
const getStatusDescription = () => {
  const emp = props.employee || editableEmployee.value
  
  if (!emp?.working_start_time || !emp?.working_end_time) {
    return t('please_set_working_hours')
  }
  
  return t('status_auto_updated_by_system')
}

// Current time functions
const getCurrentTime = () => {
  const now = currentTime.value
  
  // Format in Vietnam timezone
  const options: Intl.DateTimeFormatOptions = {
    timeZone: 'Asia/Ho_Chi_Minh',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
  }
  
  return new Intl.DateTimeFormat('en-GB', options).format(now)
}

const updateCurrentTime = () => {
  currentTime.value = new Date()
}

const startTimeUpdate = () => {
  updateCurrentTime()
  timeInterval = setInterval(updateCurrentTime, 1000)
}

const stopTimeUpdate = () => {
  if (timeInterval) {
    clearInterval(timeInterval)
    timeInterval = null
  }
}

// Methods
const toggleEditMode = () => {
  isEditMode.value = !isEditMode.value
  emit('update:editMode', isEditMode.value)
}

const handleSave = () => {
  if (!validateWorkingHours()) {
    return
  }
  
  let dataToSave = { ...editableEmployee.value }
  
  if (!props.isAdminView) {
    dataToSave = {
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
  }
  
  emit('save', dataToSave)
}

const handleCancel = () => {
  if (props.employee) {
    editableEmployee.value = { ...props.employee }
  }
  isEditMode.value = false
  emit('update:editMode', false)
  emit('cancel')
}

const validateWorkingHours = () => {
  const startTime = editableEmployee.value.working_start_time
  const endTime = editableEmployee.value.working_end_time
  
  if ((startTime && !endTime) || (!startTime && endTime)) {
    alert(t('both_start_end_time_required'))
    return false
  }
  
  if (startTime && endTime && startTime === endTime) {
    alert(t('start_end_time_cannot_be_same'))
    return false
  }
  
  return true
}

// Utility functions
const getInitials = (firstName: string, lastName: string) => {
  return `${firstName?.charAt(0) || ''}${lastName?.charAt(0) || ''}`.toUpperCase()
}

const calculateAverageHoursPerOrder = () => {
  if (!props.employee || props.employee.completed_orders_count === 0) return 0
  return (props.employee.total_hours_worked / props.employee.completed_orders_count).toFixed(1)
}

// Lifecycle hooks
onMounted(() => {
  if (props.employee) {
    editableEmployee.value = { ...props.employee }
  }
  
  startTimeUpdate()
})

onUnmounted(() => {
  stopTimeUpdate()
})
</script>