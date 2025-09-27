<template>
  <div class="bg-white rounded-lg shadow mb-6 p-4">
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('search') }}</label>
        <input
          :model-value="filters.search"
          @input="$emit('update:search', $event.target.value)"
          type="text"
          :placeholder="$t('search_employee')"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('area') }}</label>
        <select
          :model-value="filters.area"
          @change="$emit('update:area', $event.target.value)"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">{{ $t('all_areas') }}</option>
          <option v-for="area in areas" :key="area" :value="area">{{ area }}</option>
        </select>
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('status') }}</label>
        <select
          :model-value="filters.status"
          @change="$emit('update:status', $event.target.value)"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">{{ $t('all_status') }}</option>
          <option value="1">{{ $t('active') }}</option>
          <option value="0">{{ $t('inactive') }}</option>
        </select>
      </div>
      <div class="flex items-end">
        <button
          @click="$emit('reset')"
          class="w-full px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50"
        >
          {{ $t('reset') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

interface Props {
  filters: {
    search: string
    area: string
    status: string
  }
  areas: string[]
}

defineProps<Props>()

defineEmits<{
  'update:search': [value: string]
  'update:area': [value: string]  
  'update:status': [value: string]
  reset: []
}>()
</script>