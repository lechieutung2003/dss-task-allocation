<template>
  <div class="p-6">
    <!-- Back Button -->
    <div class="mb-6">
      <BackButton @click="$router.push('/dss/users')" />
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center py-8">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
    </div>

    <!-- Employee Details -->
    <div v-else-if="employee" class="space-y-6">
      <!-- Header -->
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
              <h1 class="text-2xl font-bold text-gray-900">
                {{ employee.first_name }} {{ employee.last_name }}
              </h1>
              <p class="text-gray-600">{{ employee.work_mail }}</p>
              <span
                :class="[
                  'inline-flex px-2 py-1 text-xs font-semibold rounded-full mt-1',
                  employee.status === 1
                    ? 'bg-green-100 text-green-800'
                    : 'bg-red-100 text-red-800'
                ]"
              >
                {{ employee.status === 1 ? $t('active') : $t('inactive') }}
              </span>
            </div>
          </div>
          <div class="flex space-x-2">
            <button
              v-if="!isEditMode"
              @click="isEditMode = true"
              class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg"
            >
              {{ $t('edit') }}
            </button>
            <template v-else>
              <button
                @click="saveEmployee"
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

      <!-- Employee Information Tabs -->
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
                  :disabled="!isEditMode"
                  type="date"
                  class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-50"
                >
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
                >
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">{{ $t('salary') }}</label>
                <input
                  v-model="editableEmployee.salary"
                  :disabled="!isEditMode"
                  type="number"
                  step="0.01"
                  class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-50"
                >
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">{{ $t('working_start_time') }}</label>
                <input
                  v-model="editableEmployee.working_start_time"
                  :disabled="!isEditMode"
                  type="time"
                  class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-50"
                >
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">{{ $t('working_end_time') }}</label>
                <input
                  v-model="editableEmployee.working_end_time"
                  :disabled="!isEditMode"
                  type="time"
                  class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-50"
                >
              </div>
            </div>
          </div>

          <!-- Performance -->
          <div v-if="activeTab === 'performance'" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div class="bg-blue-50 p-4 rounded-lg">
                <div class="text-2xl font-bold text-blue-600">{{ employee.completed_orders_count }}</div>
                <div class="text-sm text-gray-600">{{ $t('completed_orders') }}</div>
              </div>
              <div class="bg-green-50 p-4 rounded-lg">
                <div class="text-2xl font-bold text-green-600">{{ employee.total_hours_worked }}h</div>
                <div class="text-sm text-gray-600">{{ $t('total_hours_worked') }}</div>
              </div>
              <div class="bg-purple-50 p-4 rounded-lg">
                <div class="text-2xl font-bold text-purple-600">
                  {{ calculateAverageHoursPerOrder() }}h
                </div>
                <div class="text-sm text-gray-600">{{ $t('avg_hours_per_order') }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Not Found -->
    <div v-else class="text-center py-8">
      <h3 class="text-lg font-medium text-gray-900">{{ $t('employee_not_found') }}</h3>
      <p class="text-gray-500">{{ $t('employee_not_found_description') }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import EmployeeService from '@/services/dss/users/employees'
import BackButton from '@/components/BackButton.vue'

definePageMeta({
  layout: 'dss',
  middleware: 'auth'
})

const { t } = useI18n()
const route = useRoute()
const router = useRouter()

// Reactive data
const employee = ref(null)
const editableEmployee = ref({})
const loading = ref(false)
const saving = ref(false)
const isEditMode = ref(false)
const activeTab = ref('personal')

// Tabs
const tabs = computed(() => [
  { key: 'personal', label: t('personal_information') },
  { key: 'work', label: t('work_information') },
  { key: 'performance', label: t('performance') }
])

// Methods
const loadEmployee = async () => {
  loading.value = true
  try {
    const response = await EmployeeService.getEmployee(route.params.id)
    employee.value = response
    editableEmployee.value = { ...response }
    
    // Check if edit mode from query
    if (route.query.edit === 'true') {
      isEditMode.value = true
    }
  } catch (error) {
    console.error('Error loading employee:', error)
  } finally {
    loading.value = false
  }
}

const saveEmployee = async () => {
  saving.value = true
  try {
    const response = await EmployeeService.updateEmployee(route.params.id, editableEmployee.value)
    employee.value = response
    editableEmployee.value = { ...response }
    isEditMode.value = false
    // Show success notification
  } catch (error) {
    console.error('Error saving employee:', error)
    // Show error notification
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

const getInitials = (firstName: string, lastName: string) => {
  return `${firstName?.charAt(0) || ''}${lastName?.charAt(0) || ''}`.toUpperCase()
}

// Lifecycle
onMounted(() => {
  loadEmployee()
})
</script>