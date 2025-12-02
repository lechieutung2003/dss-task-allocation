<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <div class="flex items-center justify-between mb-6">
      <h3 class="text-xl font-bold text-gray-900 flex items-center gap-2">
        <el-icon size="24" class="text-red-600"><Warning /></el-icon>
        Orders Ưu Tiên (Sorted by Priority Score)
      </h3>
      
      <el-button 
        :icon="Refresh" 
        @click="$emit('refresh')"
        :loading="loading"
        size="small"
      >
        Làm mới
      </el-button>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="animate-pulse space-y-3">
      <div v-for="i in 5" :key="i" class="h-24 bg-gray-100 rounded-lg"></div>
    </div>

    <!-- Table -->
    <el-table 
      v-else
      :data="ordersData" 
      style="width: 100%"
      :row-class-name="getRowClassName"
      stripe
    >
      <el-table-column label="Priority" width="100" fixed>
        <template #default="{ row }">
          <div class="text-center">
            <div class="text-2xl font-bold" :class="getPriorityScoreColor(row.priority_score)">
              {{ row.priority_score }}
            </div>
            <el-tag 
              :type="getPriorityTagType(row.priority_level)"
              size="small"
              effect="dark"
            >
              {{ row.priority }}
            </el-tag>
          </div>
        </template>
      </el-table-column>

      <el-table-column prop="title" label="Nhiệm Vụ" min-width="200">
        <template #default="{ row }">
          <div>
            <div class="font-semibold text-gray-900">{{ row.title }}</div>
            <div class="text-xs text-gray-500 mt-1">{{ row.note }}</div>
          </div>
        </template>
      </el-table-column>

      <el-table-column label="Khách Hàng" width="150">
        <template #default="{ row }">
          <div class="text-sm">
            <div class="font-medium">{{ row.customer_name }}</div>
            <div class="text-gray-500 text-xs">
              <el-icon><Location /></el-icon>
              {{ row.location }}
            </div>
          </div>
        </template>
      </el-table-column>

      <el-table-column label="Deadline" width="160">
        <template #default="{ row }">
          <div class="text-sm">
            <el-icon class="text-red-500"><Calendar /></el-icon>
            {{ formatDateTime(row.deadline) }}
          </div>
        </template>
      </el-table-column>

      <el-table-column label="Chi Tiết" width="180">
        <template #default="{ row }">
          <div class="text-xs space-y-1">
            <div>
              <el-icon><Grid /></el-icon>
              {{ row.area }}
            </div>
            <div>
              <el-icon><Clock /></el-icon>
              {{ row.estimatedHours }}
            </div>
            <div v-if="row.cost" class="font-semibold text-green-600">
              <el-icon><Money /></el-icon>
              {{ formatCurrency(row.cost) }}
            </div>
          </div>
        </template>
      </el-table-column>

      <el-table-column label="Trạng Thái" width="120">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">
            {{ formatStatus(row.status) }}
          </el-tag>
        </template>
      </el-table-column>

      <el-table-column label="Tiến Độ" width="150">
        <template #default="{ row }">
          <div>
            <div class="flex items-center justify-between mb-1 text-xs text-gray-600">
              <span>{{ row.progress }}%</span>
              <span>{{ row.assignee }}</span>
            </div>
            <el-progress 
              :percentage="row.progress" 
              :color="getProgressColor(row.progress)"
              :stroke-width="8"
            />
          </div>
        </template>
      </el-table-column>

      <el-table-column label="Actions" width="100" fixed="right">
        <template #default="{ row }">
          <el-button 
            type="primary" 
            size="small"
            @click="$emit('view-detail', row.id)"
          >
            Chi Tiết
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- Empty State -->
    <div v-if="!loading && (!ordersData || ordersData.length === 0)" 
         class="text-center py-12 text-gray-500">
      <el-icon size="48" class="mb-3"><DocumentChecked /></el-icon>
      <p>Không có orders ưu tiên</p>
    </div>
  </div>
</template>

<script setup>
import { Warning, Refresh, Location, Calendar, Clock, Grid, Money, DocumentChecked } from '@element-plus/icons-vue';

defineProps({
  ordersData: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
});

defineEmits(['refresh', 'view-detail']);

const getRowClassName = ({ row }) => {
  if (row.priority_score >= 0.7) return 'bg-red-50';
  if (row.priority_score >= 0.4) return 'bg-yellow-50';
  return '';
};

const getPriorityScoreColor = (score) => {
  if (score >= 0.7) return 'text-red-600';
  if (score >= 0.4) return 'text-yellow-600';
  return 'text-green-600';
};

const getPriorityTagType = (level) => {
  if (level === 'high') return 'danger';
  if (level === 'medium') return 'warning';
  return 'success';
};

const getStatusType = (status) => {
  const mapping = {
    'pending': 'info',
    'pending_payment': 'warning',
    'confirmed': 'primary',
    'in_progress': 'warning',
    'completed': 'success',
    'failed': 'danger'
  };
  return mapping[status] || 'info';
};

const formatStatus = (status) => {
  const mapping = {
    'pending': 'Chờ xử lý (Tiền mặt)',
    'pending_payment': 'Chờ thanh toán (Chuyển khoản)',
    'confirmed': 'Đã xác nhận',
    'in_progress': 'Đang thực hiện',
    'completed': 'Hoàn thành',
    'failed': 'Thất bại'
  };
  return mapping[status] || status;
};

const getProgressColor = (progress) => {
  if (progress >= 80) return '#10b981';
  if (progress >= 50) return '#3b82f6';
  if (progress >= 20) return '#f59e0b';
  return '#ef4444';
};

const formatDateTime = (dateStr) => {
  if (!dateStr) return 'N/A';
  try {
    return new Date(dateStr).toLocaleString('vi-VN', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  } catch {
    return dateStr;
  }
};

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND'
  }).format(amount);
};
</script>

<style scoped>
:deep(.el-table .bg-red-50) {
  background-color: #fef2f2;
}
:deep(.el-table .bg-yellow-50) {
  background-color: #fffbeb;
}
</style>
