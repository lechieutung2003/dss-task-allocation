<template>
  <div
    v-if="show"
    class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
    @click="$emit('close')"
  >
    <div class="relative top-10 mx-auto p-5 border w-full max-w-4xl shadow-lg rounded-md bg-white" @click.stop>
      <div class="mt-3">
        <!-- Modal Header -->
        <div class="flex items-center justify-between pb-4 border-b">
          <h3 class="text-lg font-medium text-gray-900">{{ $t('add_new_employee') }}</h3>
          <button
            @click="$emit('close')"
            class="text-gray-400 hover:text-gray-600"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <!-- Modal Body -->
        <div class="py-4 max-h-[500px] overflow-y-auto">
          <EmployeeForm
            :employee="newEmployee"
            :available-areas="availableAreas"
            :loading="saving"
            :skills-list="skillsList"
            :skills-loading="skillsLoading"
            @submit="onSubmit"
            @cancel="$emit('close')"
          />
          <p v-if="errorMsg" class="mt-2 text-sm text-red-600">{{ errorMsg }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import SkillService from '@/services/dss/users/skill'
import EmployeeService from '@/services/dss/users/employees'

const { t } = useI18n()
const skillsList = ref<any[]>([])
const skillsLoading = ref(false)
const saving = ref(false)
const errorMsg = ref('')

onMounted(async () => {
  skillsLoading.value = true
  try {
    const result = await SkillService.getSkills()
    console.log('[EmployeeCreateModal] SkillService.getSkills result:', result)
    skillsList.value = Array.isArray(result.results) ? result.results : (Array.isArray(result) ? result : [])
    console.log('[EmployeeCreateModal] skillsList.value:', skillsList.value)
  } catch (e) {
    console.error('[EmployeeCreateModal] Error loading skills:', e)
    skillsList.value = []
  }
  skillsLoading.value = false
})

interface Props {
  show: boolean
  newEmployee: any
  availableAreas: any[]
  loading: boolean
}

defineProps<Props>()

const emit = defineEmits<{
  close: []
  success: [message?: string]
  error: [message: string]
}>()

const onSubmit = async (formData: any) => {
  errorMsg.value = ''
  const first = formData.first_name?.trim()
  const last = formData.last_name?.trim()
  const mail = formData.work_mail?.trim()

  // Validate required fields
  if (!first || !last || !mail) {
    const message = t('please_fill_required_fields')
    errorMsg.value = message
    emit('error', message)
    return
  }

  // Set default password
  if (!formData.password) {
    formData.password = '123456'
  }

  try {
    saving.value = true
    
    console.log('[EmployeeCreateModal] Creating employee with data:', formData)
    const response = await EmployeeService.createEmployee(formData)
    console.log('[EmployeeCreateModal] Employee created successfully:', response)

    // ✅ Check status từ response
    if (response.status && response.status == "404") {
      // Error case
      const message = response.work_mail 
        ? (Array.isArray(response.work_mail) ? response.work_mail[0] : response.work_mail)
        : (response.detail || t('error_saving_employee'))
      
      errorMsg.value = message
      emit('error', message)
      emit('close')
      
    } else {
      // Success case
      console.log("Creating employee succeeded")
      emit('success','Creating employee succeeded')
      emit('close')
    }
    
  } catch (e: any) {
    // Network error hoặc exception khác
    console.error('[EmployeeCreateModal] Exception:', e)
    const message = e.message || t('error_saving_employee')
    errorMsg.value = message
    emit('error', message)
    
  } finally {
    saving.value = false
  }
}
</script>