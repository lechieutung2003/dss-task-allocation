<template>
  <div class="p-6">

     <!-- Success Alert -->
    <div
      v-if="showSuccessAlert"
      class="fixed top-4 right-4 z-50 max-w-sm w-full bg-green-50 border border-green-200 rounded-lg shadow-lg p-4 flex items-start animate-slide-in"
    >
      <div class="flex-shrink-0">
        <svg class="h-5 w-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
        </svg>
      </div>
      <div class="ml-3 flex-1">
        <p class="text-sm font-medium text-green-800">
          {{ $t('employee_created_success') }}
        </p>
      </div>
      <button @click="showSuccessAlert = false" class="ml-auto text-green-400 hover:text-green-600">
        <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
        </svg>
      </button>
    </div>

    <!-- Error Alert -->
    <div
      v-if="showErrorAlert"
      class="fixed top-4 right-4 z-50 max-w-sm w-full bg-red-50 border border-red-200 rounded-lg shadow-lg p-4 flex items-start animate-slide-in"
    >
      <div class="flex-shrink-0">
        <svg class="h-5 w-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
        </svg>
      </div>
      <div class="ml-3 flex-1">
        <p class="text-sm font-medium text-red-800">
          {{ errorMessage }}
        </p>
      </div>
      <button @click="showErrorAlert = false" class="ml-auto text-red-400 hover:text-red-600">
        <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
        </svg>
      </button>
    </div>


    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
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

    <!-- Filters Component -->
    <EmployeeFilters
      :filters="filters"
      :areas="areas"
      @update:search="handleSearchUpdate"
      @update:area="updateFilters('area', $event)"
      @update:status="updateFilters('status', $event)"
      @reset="resetFilters"
    />

    <!-- Employee Table Component -->
    <EmployeeListTable
      :employees="employees"
      :loading="loading"
      @view="viewEmployee"
      @edit="editEmployee"
      @delete="confirmDeleteEmployee"
    />

    <!-- Pagination Component -->
    <Pagination
      :current-page="currentPage"
      :page-size="pageSize"
      :total-items="totalItems"
      :total-pages="totalPages"
      @page-change="goToPage"
    />

    <!-- Create Employee Modal Component -->
    <EmployeeCreateModal
      :show="showCreateModal"
      :new-employee="newEmployee"
      :available-areas="availableAreas"
      :loading="creating"
      @close="closeCreateModal"
      @success="handleCreateSuccess"
      @error="handleCreateError"
    />

    <!-- Delete Confirmation Modal Component -->
    <DeleteConfirmation
      :show="showDeleteModal"
      :employee="employeeToDelete"
      :loading="deleting"
      @close="closeDeleteModal"
      @confirm="handleDeleteEmployee"
    />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useI18n } from 'vue-i18n'

// IMPORT: Components
import EmployeeFilters from '@/components/employee/EmployeeFilters.vue'
import EmployeeListTable from '@/components/employee/EmployeeListTable.vue'
import Pagination from '@/components/employee/Pagination.vue'
import EmployeeCreateModal from '@/components/employee/EmployeeCreateModal.vue'
import DeleteConfirmation from '@/components/employee/DeleteConfirmation.vue'

// IMPORT: Composables
import { useEmployeeManagement } from '@/composables/useEmployeeManagement'
import { useEmployeeCrud } from '@/composables/useEmployeeCRUD'

definePageMeta({
  layout: 'dss',
  middleware: 'auth'
})

const { t } = useI18n()
const showSuccessAlert = ref(false)
const showErrorAlert = ref(false)
const errorMessage = ref('')

// USE: Employee Management Composable
const {
  employees,
  loading,
  areas,
  currentPage,
  pageSize,
  totalItems,
  totalPages,
  filters,
  availableAreas,
  loadEmployees,
  loadAllAreas,
  handleSearchUpdate,
  updateFilters,
  resetFilters,
  goToPage
} = useEmployeeManagement()

// USE: Employee CRUD Composable
const {
  showCreateModal,
  creating,
  showDeleteModal,
  employeeToDelete,
  deleting,
  newEmployee,
  viewEmployee,
  editEmployee,
  confirmDeleteEmployee,
  closeDeleteModal,
  deleteEmployee,
  closeCreateModal,
  createEmployee,
  initializeForm
} = useEmployeeCrud()

// HANDLERS: Success callbacks
const handleCreateSuccess = async (message: string) => {
  // Show success alert
  showSuccessAlert.value = true
  
  // Auto hide after 3 seconds
  setTimeout(() => {
    showSuccessAlert.value = false
  }, 3000)
  
  // Refresh data
  if (currentPage.value === 1) {
    await loadEmployees()
  } else {
    currentPage.value = 1
    await loadEmployees()
  }
  
  // Reload areas in case new area was added
  await loadAllAreas()
}

const handleCreateError = (message: string) => {
  errorMessage.value = message || t('employee_created_failed')
  showErrorAlert.value = true
  
  // Auto hide after 5 seconds
  setTimeout(() => {
    showErrorAlert.value = false
  }, 5000)
}


const handleDeleteEmployee = async () => {
  await deleteEmployee(() => {
    // Refresh current page
    loadEmployees()
    
    // If current page becomes empty and not page 1, go to previous page
    if (employees.value.length === 1 && currentPage.value > 1) {
      currentPage.value = currentPage.value - 1
      setTimeout(() => loadEmployees(), 100)
    }
  })
}

// LIFECYCLE
onMounted(() => {
  loadEmployees()
  loadAllAreas() // Load areas separately
  initializeForm() // Initialize form with current date
})
</script>

<style scoped>
@keyframes slide-in {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.animate-slide-in {
  animation: slide-in 0.3s ease-out;
}
</style>