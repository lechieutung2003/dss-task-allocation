<template>
  <form @submit.prevent="handleSubmit">
    <!-- Personal Information Section -->
    <div class="mb-6">
      <h4 class="text-md font-medium text-gray-900 mb-3">{{ $t('personal_information') }}</h4>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            {{ $t('first_name') }} <span class="text-red-500">*</span>
          </label>
          <input
            v-model="localEmployee.first_name"
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
            v-model="localEmployee.last_name"
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
            v-model="localEmployee.work_mail"
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
            v-model="localEmployee.phone"
            type="tel"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :placeholder="$t('enter_phone')"
          >
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('personal_email') }}</label>
          <input
            v-model="localEmployee.personal_mail"
            type="email"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :placeholder="$t('enter_personal_email')"
          >
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('gender') }}</label>
          <select
            v-model="localEmployee.gender"
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
            v-model="localEmployee.date_of_birth"
            type="date"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('join_date') }}</label>
          <input
            v-model="localEmployee.join_date"
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
            v-model="localEmployee.area"
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
            v-model="localEmployee.salary"
            type="number"
            step="0.01"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            :placeholder="$t('enter_salary')"
          >
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('working_start_time') }}</label>
          <input
            v-model="localEmployee.working_start_time"
            type="time"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('working_end_time') }}</label>
          <input
            v-model="localEmployee.working_end_time"
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
        @click="$emit('cancel')"
        :disabled="loading"
        class="px-4 py-2 bg-gray-300 text-gray-700 text-base font-medium rounded-md shadow-sm hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 disabled:opacity-50"
      >
        {{ $t('cancel') }}
      </button>
      <button
        type="submit"
        :disabled="loading"
        class="px-4 py-2 bg-blue-600 text-white text-base font-medium rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
      >
        {{ loading ? $t('creating') : $t('create_employee') }}
      </button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

interface Props {
  employee: any
  availableAreas: any[]
  loading: boolean
}

const props = defineProps<Props>()

const emit = defineEmits<{
  submit: [data: any]
  cancel: []
}>()

const localEmployee = ref({ ...props.employee })

watch(() => props.employee, (newEmployee) => {
  localEmployee.value = { ...newEmployee }
}, { deep: true })

const handleSubmit = () => {
  emit('submit', localEmployee.value)
}
</script>