<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <h3 class="text-xl font-bold text-gray-900 flex items-center gap-2">
        <el-icon size="24"><component :is="icon" /></el-icon>
        {{ title }}
      </h3>
    </div>

    <!-- Chart Content -->
    <div v-if="loading" class="animate-pulse h-64 bg-gray-100 rounded"></div>
    
    <!-- Pie Chart for Tasks Status -->
    <div v-else-if="type === 'tasks' && hasTasksData" class="relative">
      <canvas ref="tasksChartCanvas" style="max-height: 300px"></canvas>
      
      <!-- Summary Stats -->
      <div class="grid grid-cols-3 gap-4 mt-6 pt-6 border-t">
        <div class="text-center">
          <div class="text-sm text-gray-500 mb-1">{{ $t('chart_tasks_completed') }}</div>
          <div class="text-xl font-bold text-green-600">
            {{ chartData?.tasks?.completed || 0 }}
          </div>
        </div>
        <div class="text-center">
          <div class="text-sm text-gray-500 mb-1">{{ $t('chart_tasks_failed') }}</div>
          <div class="text-xl font-bold text-red-600">
            {{ chartData?.tasks?.failed || 0 }}
          </div>
        </div>
        <div class="text-center">
          <div class="text-sm text-gray-500 mb-1">{{ $t('chart_tasks_in_progress') }}</div>
          <div class="text-xl font-bold text-blue-600">
            {{ chartData?.tasks?.in_progress || chartData?.tasks?.pending || 0 }}
          </div>
        </div>
      </div>
    </div>

    <!-- Performance Metrics -->
    <div v-else-if="type === 'performance'" class="space-y-6">
      <!-- Average Rating -->
      <div class="flex items-center justify-between p-4 bg-gradient-to-r from-yellow-50 to-yellow-100 rounded-lg">
        <div>
          <div class="text-sm text-gray-600 mb-1">{{ $t('chart_avg_rating') }}</div>
          <div class="text-3xl font-bold text-yellow-600">
            {{ avgRating || 0 }} <span class="text-lg">/5.0</span>
          </div>
        </div>
        <div class="text-5xl">⭐</div>
      </div>

      <!-- Average Completion Time -->
      <div class="flex items-center justify-between p-4 bg-gradient-to-r from-blue-50 to-blue-100 rounded-lg">
        <div>
          <div class="text-sm text-gray-600 mb-1">{{ $t('chart_avg_completion_time') }}</div>
          <div class="text-3xl font-bold text-blue-600">
            {{ avgTime || 0 }} <span class="text-lg">giờ</span>
          </div>
        </div>
        <div class="text-5xl">⏱️</div>
      </div>

      <!-- Success Rate -->
      <div class="flex items-center justify-between p-4 bg-gradient-to-r from-green-50 to-green-100 rounded-lg">
        <div class="flex-1">
          <div class="text-sm text-gray-600 mb-1">{{ $t('chart_success_rate') }}</div>
          <div class="text-3xl font-bold text-green-600 mb-2">
            {{ performance || 0 }}%
          </div>
          <!-- Progress Bar -->
          <div class="w-full bg-gray-200 rounded-full h-3">
            <div
              class="bg-green-600 h-3 rounded-full transition-all duration-500"
              :style="{ width: `${performance || 0}%` }"
            ></div>
          </div>
        </div>
        <div class="text-5xl ml-4">📈</div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-12 text-gray-500">
      <el-icon size="48" class="mb-3"><Warning /></el-icon>
      <p>{{ $t('chart_no_data') }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, nextTick } from 'vue';
import { Chart, registerables } from 'chart.js';
import { Warning } from '@element-plus/icons-vue';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();
Chart.register(...registerables);

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  icon: {
    type: Object,
    required: true
  },
  type: {
    type: String,
    required: true,
    validator: (value) => ['tasks', 'performance'].includes(value)
  },
  chartData: {
    type: Object,
    default: () => null
  },
  loading: {
    type: Boolean,
    default: false
  },
  // Performance props
  avgRating: {
    type: Number,
    default: 0
  },
  avgTime: {
    type: Number,
    default: 0
  },
  performance: {
    type: Number,
    default: 0
  }
});

const tasksChartCanvas = ref(null);
const tasksChartInstance = ref(null);

// Check if tasks data exists
const hasTasksData = computed(() => {
  if (!props.chartData?.tasks) return false;
  const tasks = props.chartData.tasks;
  return (tasks.completed || 0) + (tasks.failed || 0) + (tasks.in_progress || tasks.pending || 0) > 0;
});

// Create Pie Chart for Tasks
const createTasksChart = () => {
  if (!tasksChartCanvas.value || !hasTasksData.value) return;
  
  if (tasksChartInstance.value) {
    tasksChartInstance.value.destroy();
  }
  
  const tasks = props.chartData.tasks;
  const ctx = tasksChartCanvas.value.getContext('2d');
  
  tasksChartInstance.value = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: [t('chart_tasks_completed'), t('chart_tasks_failed'), t('chart_tasks_in_progress')],
      datasets: [{
        data: [
          tasks.completed || 0,
          tasks.failed || 0,
          tasks.in_progress || tasks.pending || 0
        ],
        backgroundColor: [
          'rgba(16, 185, 129, 0.8)',   // Green for completed
          'rgba(239, 68, 68, 0.8)',     // Red for failed
          'rgba(59, 130, 246, 0.8)'     // Blue for in_progress
        ],
        borderColor: [
          'rgba(16, 185, 129, 1)',
          'rgba(239, 68, 68, 1)',
          'rgba(59, 130, 246, 1)'
        ],
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: {
          display: true,
          position: 'bottom',
          labels: {
            padding: 20,
            font: {
              size: 14
            }
          }
        },
        tooltip: {
          callbacks: {
            label: (context) => {
              const label = context.label || '';
              const value = context.parsed || 0;
              const total = context.dataset.data.reduce((a, b) => a + b, 0);
              const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0;
              return `${label}: ${value} (${percentage}%)`;
            }
          }
        }
      }
    }
  });
};

watch(() => props.chartData, () => {
  if (props.type === 'tasks') {
    nextTick(() => {
      createTasksChart();
    });
  }
}, { deep: true });

onMounted(() => {
  if (props.type === 'tasks') {
    nextTick(() => {
      createTasksChart();
    });
  }
});
</script>
