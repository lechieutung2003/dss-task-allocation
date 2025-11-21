<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <div class="flex items-center justify-between mb-6">
      <h3 class="text-xl font-bold text-gray-900 flex items-center gap-2">
        <el-icon size="24" class="text-blue-600"><User /></el-icon>
        KPI Nhân Viên
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
    <div v-if="loading" class="animate-pulse">
      <div v-for="i in 5" :key="i" class="h-16 bg-gray-100 rounded mb-3"></div>
    </div>

    <!-- Table -->
    <el-table 
      v-else
      :data="employeeData" 
      style="width: 100%"
      :default-sort="{ prop: 'kpi_score', order: 'descending' }"
      stripe
      @sort-change="handleSortChange"
    >
      <el-table-column prop="name" label="Nhân Viên" min-width="150">
        <template #default="{ row }">
          <div class="flex items-center gap-2">
            <el-avatar :size="32" class="bg-blue-500">
              {{ row.name.charAt(0) }}
            </el-avatar>
            <div>
              <div class="font-semibold">{{ row.name }}</div>
              <div class="text-xs text-gray-500">{{ row.area }}</div>
            </div>
          </div>
        </template>
      </el-table-column>

      <el-table-column prop="completed_orders" label="Đơn Hoàn Thành" width="140" sortable>
        <template #default="{ row }">
          <div class="text-center">
            <div class="font-bold text-green-600">{{ row.completed_orders }}</div>
            <div class="text-xs text-gray-500">/ {{ row.total_orders }} đơn</div>
          </div>
        </template>
      </el-table-column>

      <el-table-column prop="completion_rate" label="Tỷ Lệ" width="120" sortable>
        <template #default="{ row }">
          <el-progress 
            :percentage="row.completion_rate" 
            :color="getCompletionColor(row.completion_rate)"
            :stroke-width="8"
          />
        </template>
      </el-table-column>

      <el-table-column prop="avg_duration" label="Thời Gian TB" width="120" sortable>
        <template #default="{ row }">
          <div class="text-center">
            <el-icon class="text-blue-500"><Clock /></el-icon>
            {{ row.avg_duration }}h
          </div>
        </template>
      </el-table-column>

      <el-table-column prop="total_hours_worked" label="Tổng Giờ" width="120" sortable>
        <template #default="{ row }">
          <div class="text-center font-semibold">
            {{ Math.round(row.total_hours_worked) }}h
          </div>
        </template>
      </el-table-column>

      <el-table-column prop="kpi_score" label="KPI Score" width="140" sortable>
        <template #default="{ row }">
          <div class="flex items-center justify-center gap-2">
            <el-progress 
              type="circle" 
              :percentage="row.kpi_score" 
              :width="50"
              :color="getKPIColor(row.kpi_score)"
            />
            <span class="font-bold">{{ row.kpi_score }}</span>
          </div>
        </template>
      </el-table-column>

      <el-table-column label="Xếp Hạng" width="100">
        <template #default="{ row }">
          <el-tag 
            :type="getRankType(row.kpi_score)"
            size="large"
            effect="dark"
          >
            {{ getRankLabel(row.kpi_score) }}
          </el-tag>
        </template>
      </el-table-column>
    </el-table>

    <!-- Empty State -->
    <div v-if="!loading && (!employeeData || employeeData.length === 0)" 
         class="text-center py-12 text-gray-500">
      <el-icon size="48" class="mb-3"><UserFilled /></el-icon>
      <p>Chưa có dữ liệu KPI nhân viên</p>
    </div>
  </div>
</template>

<script setup>
import { User, Refresh, Clock, UserFilled } from '@element-plus/icons-vue';

defineProps({
  employeeData: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
});

defineEmits(['refresh']);

const getCompletionColor = (rate) => {
  if (rate >= 90) return '#10b981'; // green
  if (rate >= 70) return '#3b82f6'; // blue
  if (rate >= 50) return '#f59e0b'; // amber
  return '#ef4444'; // red
};

const getKPIColor = (score) => {
  if (score >= 80) return '#10b981';
  if (score >= 60) return '#3b82f6';
  if (score >= 40) return '#f59e0b';
  return '#ef4444';
};

const getRankType = (score) => {
  if (score >= 80) return 'success';
  if (score >= 60) return 'primary';
  if (score >= 40) return 'warning';
  return 'danger';
};

const getRankLabel = (score) => {
  if (score >= 80) return 'A';
  if (score >= 60) return 'B';
  if (score >= 40) return 'C';
  return 'D';
};

const handleSortChange = ({ prop, order }) => {
  console.log('Sort changed:', prop, order);
};
</script>
