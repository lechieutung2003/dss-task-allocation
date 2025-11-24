<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <!-- Header with Filter and Navigation -->
    <div class="mb-6">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-xl font-bold text-gray-900 flex items-center gap-2">
          <el-icon size="24"><component :is="icon" /></el-icon>
          {{ title }}
        </h3>
        
        <el-radio-group v-model="selectedPeriod" size="small" @change="handlePeriodChange">
          <el-radio-button label="week">Tuần</el-radio-button>
          <el-radio-button label="month">Tháng</el-radio-button>
          <el-radio-button label="year">Năm</el-radio-button>
        </el-radio-group>
      </div>
      
      <!-- Period Navigation -->
      <div class="flex items-center justify-between bg-gray-50 rounded-lg p-3">
        <el-button 
          size="small" 
          :icon="ArrowLeft" 
          @click="goToPreviousPeriod"
          :disabled="loading"
        >
          {{ getPeriodLabel('previous') }}
        </el-button>
        
        <div class="text-center flex-1 mx-4">
          <div class="text-lg font-semibold text-gray-900">
            {{ getCurrentPeriodLabel() }}
          </div>
          <div class="text-sm text-gray-500">
            {{ getPeriodDateRange() }}
          </div>
        </div>
        
        <el-button 
          size="small" 
          @click="goToNextPeriod"
          :disabled="loading || currentOffset === 0"
        >
          {{ getPeriodLabel('next') }}
          <el-icon class="ml-1"><ArrowRight /></el-icon>
        </el-button>
      </div>
    </div>

    <!-- Chart Content -->
    <div v-if="loading" class="animate-pulse h-64 bg-gray-100 rounded"></div>
    
    <div v-else-if="filteredData && filteredData.length > 0" style="height: 300px">
      <canvas ref="chartCanvas"></canvas>
    </div>

    <div v-else class="text-center py-12 text-gray-500">
      <el-icon size="48" class="mb-3"><Warning /></el-icon>
      <p>Chưa có dữ liệu cho khoảng thời gian đã chọn</p>
      <p class="text-sm mt-2">Thử chọn khoảng thời gian khác hoặc thêm dữ liệu mới</p>
    </div>

    <!-- Summary Stats -->
    <div v-if="!loading && summaryStats" class="grid grid-cols-3 gap-4 mt-6 pt-6 border-t">
      <div class="text-center">
        <div class="text-sm text-gray-500 mb-1">Tổng Doanh Thu</div>
        <div class="text-xl font-bold text-green-600">
          {{ formatCurrency(summaryStats.totalRevenue) }}
        </div>
      </div>
      <div class="text-center">
        <div class="text-sm text-gray-500 mb-1">Tổng Chi Phí</div>
        <div class="text-xl font-bold text-red-600">
          {{ formatCurrency(summaryStats.totalCost) }}
        </div>
      </div>
      <div class="text-center">
        <div class="text-sm text-gray-500 mb-1">Lợi Nhuận</div>
        <div class="text-xl font-bold text-blue-600">
          {{ formatCurrency(summaryStats.totalProfit) }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, nextTick } from 'vue';
import { Chart, registerables } from 'chart.js';
import { Warning, ArrowLeft, ArrowRight } from '@element-plus/icons-vue';

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
  data: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['period-change']);

const chartCanvas = ref(null);
const chartInstance = ref(null);
const selectedPeriod = ref('month');
const currentOffset = ref(0); // 0 = hiện tại, -1 = kỳ trước, -2 = 2 kỳ trước...

// Helper function để group data theo tuần
const groupByWeek = (data) => {
  const weeks = {};
  
  data.forEach(item => {
    const date = new Date(item.date);
    const weekStart = new Date(date);
    weekStart.setDate(date.getDate() - date.getDay()); // Chủ nhật đầu tuần
    const weekKey = weekStart.toISOString().split('T')[0];
    
    if (!weeks[weekKey]) {
      weeks[weekKey] = {
        date: weekKey,
        revenue: 0,
        cost: 0,
        profit: 0,
        count: 0
      };
    }
    
    weeks[weekKey].revenue += (item.revenue || item.amount || 0);
    weeks[weekKey].cost += (item.cost || 0);
    weeks[weekKey].profit += (item.profit || 0);
    weeks[weekKey].count++;
  });
  
  return Object.values(weeks).sort((a, b) => new Date(a.date) - new Date(b.date));
};

// Helper function để group data theo tháng
const groupByMonth = (data) => {
  const months = {};
  
  data.forEach(item => {
    const date = new Date(item.date);
    const monthKey = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
    
    if (!months[monthKey]) {
      months[monthKey] = {
        date: monthKey,
        revenue: 0,
        cost: 0,
        profit: 0,
        count: 0
      };
    }
    
    months[monthKey].revenue += (item.revenue || item.amount || 0);
    months[monthKey].cost += (item.cost || 0);
    months[monthKey].profit += (item.profit || 0);
    months[monthKey].count++;
  });
  
  return Object.values(months).sort((a, b) => a.date.localeCompare(b.date));
};

// Filter và group data theo period với offset
const filteredData = computed(() => {
  if (!props.data || props.data.length === 0) {
    console.log('⚠️ FilterableChart: No data provided');
    return [];
  }
  
  console.log('📊 FilterableChart received data:', props.data.length, 'items');
  
  const now = new Date();
  const offset = currentOffset.value;
  let startDate, endDate;
  let rawFiltered;
  
  switch (selectedPeriod.value) {
    case 'week': {
      // Tuần: hiển thị 7 ngày trong tuần được chọn
      const weekStart = new Date(now);
      weekStart.setDate(now.getDate() + (offset * 7) - now.getDay()); // Chủ nhật đầu tuần
      weekStart.setHours(0, 0, 0, 0);
      
      const weekEnd = new Date(weekStart);
      weekEnd.setDate(weekStart.getDate() + 6);
      weekEnd.setHours(23, 59, 59, 999);
      
      startDate = weekStart;
      endDate = weekEnd;
      
      rawFiltered = props.data.filter(item => {
        const itemDate = new Date(item.date);
        return itemDate >= startDate && itemDate <= endDate;
      });
      console.log('📊 Week view:', startDate.toLocaleDateString(), '-', endDate.toLocaleDateString());
      return rawFiltered;
    }
      
    case 'month': {
      // Tháng: hiển thị các tuần trong tháng được chọn
      const targetMonth = new Date(now);
      targetMonth.setMonth(now.getMonth() + offset);
      
      startDate = new Date(targetMonth.getFullYear(), targetMonth.getMonth(), 1);
      endDate = new Date(targetMonth.getFullYear(), targetMonth.getMonth() + 1, 0);
      endDate.setHours(23, 59, 59, 999);
      
      rawFiltered = props.data.filter(item => {
        const itemDate = new Date(item.date);
        return itemDate >= startDate && itemDate <= endDate;
      });
      const weeklyData = groupByWeek(rawFiltered);
      console.log('📊 Month view: grouped into', weeklyData.length, 'weeks for', targetMonth.toLocaleDateString('vi-VN', { month: 'long', year: 'numeric' }));
      return weeklyData;
    }
      
    case 'year': {
      // Năm: hiển thị các tháng trong năm được chọn
      const targetYear = now.getFullYear() + offset;
      
      startDate = new Date(targetYear, 0, 1);
      endDate = new Date(targetYear, 11, 31, 23, 59, 59, 999);
      
      rawFiltered = props.data.filter(item => {
        const itemDate = new Date(item.date);
        return itemDate >= startDate && itemDate <= endDate;
      });
      const monthlyData = groupByMonth(rawFiltered);
      console.log('📊 Year view: grouped into', monthlyData.length, 'months for year', targetYear);
      return monthlyData;
    }
      
    default:
      return props.data;
  }
});

// Tính summary stats từ filtered data
const summaryStats = computed(() => {
  if (!filteredData.value || filteredData.value.length === 0) return null;
  
  return filteredData.value.reduce((acc, item) => ({
    totalRevenue: acc.totalRevenue + (item.amount || item.revenue || 0),
    totalCost: acc.totalCost + (item.cost || 0),
    totalProfit: acc.totalProfit + (item.profit || 0)
  }), { totalRevenue: 0, totalCost: 0, totalProfit: 0 });
});

// Chart data formatted for Chart.js
const chartData = computed(() => {
  if (!filteredData.value || filteredData.value.length === 0) return null;
  
  return {
    labels: filteredData.value.map(item => formatDate(item.date)),
    datasets: [
      {
        label: 'Doanh Thu',
        data: filteredData.value.map(item => item.amount || item.revenue || 0),
        borderColor: '#10b981',
        backgroundColor: 'rgba(16, 185, 129, 0.1)',
        tension: 0.4,
        fill: true
      },
      {
        label: 'Chi Phí',
        data: filteredData.value.map(item => item.cost || 0),
        borderColor: '#ef4444',
        backgroundColor: 'rgba(239, 68, 68, 0.1)',
        tension: 0.4,
        fill: true
      },
      {
        label: 'Lợi Nhuận',
        data: filteredData.value.map(item => item.profit || 0),
        borderColor: '#3b82f6',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.4,
        fill: true
      }
    ]
  };
});

const formatDate = (dateStr) => {
  const date = new Date(dateStr);
  
  switch (selectedPeriod.value) {
    case 'week':
      // Tuần: hiển thị "Thứ 2, 21/11"
      const weekday = date.toLocaleDateString('vi-VN', { weekday: 'short' });
      const dayMonth = date.toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit' });
      return `${weekday}, ${dayMonth}`;
      
    case 'month':
      // Tháng: hiển thị "Tuần 1 (15/11)"
      const weekNum = Math.ceil((date.getDate()) / 7);
      const monthDay = date.toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit' });
      return `Tuần ${weekNum} (${monthDay})`;
      
    case 'year':
      // Năm: hiển thị "Tháng 11/2025"
      return date.toLocaleDateString('vi-VN', { month: '2-digit', year: 'numeric' });
      
    default:
      return date.toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit' });
  }
};

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND',
    notation: 'compact'
  }).format(amount);
};

// Navigation functions
const goToPreviousPeriod = () => {
  currentOffset.value--;
  updateChart();
};

const goToNextPeriod = () => {
  if (currentOffset.value < 0) {
    currentOffset.value++;
    updateChart();
  }
};

const handlePeriodChange = () => {
  currentOffset.value = 0; // Reset về kỳ hiện tại khi đổi period
  emit('period-change', selectedPeriod.value);
  updateChart();
};

// Helper functions for labels
const getPeriodLabel = (direction) => {
  const labels = {
    week: direction === 'previous' ? 'Tuần trước' : 'Tuần sau',
    month: direction === 'previous' ? 'Tháng trước' : 'Tháng sau',
    year: direction === 'previous' ? 'Năm trước' : 'Năm sau'
  };
  return labels[selectedPeriod.value] || '';
};

const getCurrentPeriodLabel = () => {
  const now = new Date();
  const offset = currentOffset.value;
  
  switch (selectedPeriod.value) {
    case 'week': {
      const targetDate = new Date(now);
      targetDate.setDate(now.getDate() + (offset * 7));
      const weekNum = getWeekNumber(targetDate);
      if (offset === 0) return `Tuần này (Tuần ${weekNum})`;
      if (offset === -1) return `Tuần trước (Tuần ${weekNum})`;
      return `Tuần ${weekNum}`;
    }
    case 'month': {
      const targetDate = new Date(now);
      targetDate.setMonth(now.getMonth() + offset);
      const monthName = targetDate.toLocaleDateString('vi-VN', { month: 'long', year: 'numeric' });
      if (offset === 0) return `Tháng này (${monthName})`;
      if (offset === -1) return `Tháng trước (${monthName})`;
      return monthName;
    }
    case 'year': {
      const year = now.getFullYear() + offset;
      if (offset === 0) return `Năm nay (${year})`;
      if (offset === -1) return `Năm trước (${year})`;
      return `Năm ${year}`;
    }
    default:
      return '';
  }
};

const getPeriodDateRange = () => {
  const now = new Date();
  const offset = currentOffset.value;
  
  switch (selectedPeriod.value) {
    case 'week': {
      const startDate = new Date(now);
      startDate.setDate(now.getDate() + (offset * 7) - now.getDay());
      const endDate = new Date(startDate);
      endDate.setDate(startDate.getDate() + 6);
      return `${formatDateShort(startDate)} - ${formatDateShort(endDate)}`;
    }
    case 'month': {
      const targetDate = new Date(now);
      targetDate.setMonth(now.getMonth() + offset);
      const firstDay = new Date(targetDate.getFullYear(), targetDate.getMonth(), 1);
      const lastDay = new Date(targetDate.getFullYear(), targetDate.getMonth() + 1, 0);
      return `${formatDateShort(firstDay)} - ${formatDateShort(lastDay)}`;
    }
    case 'year': {
      const year = now.getFullYear() + offset;
      return `01/01/${year} - 31/12/${year}`;
    }
    default:
      return '';
  }
};

const getWeekNumber = (date) => {
  const firstDayOfYear = new Date(date.getFullYear(), 0, 1);
  const pastDaysOfYear = (date - firstDayOfYear) / 86400000;
  return Math.ceil((pastDaysOfYear + firstDayOfYear.getDay() + 1) / 7);
};

const formatDateShort = (date) => {
  return date.toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit' });
};

const updateChart = () => {
  if (!chartCanvas.value || !chartData.value) {
    console.log('⚠️ Cannot update chart: missing canvas or data');
    return;
  }
  
  console.log('🎨 Updating chart with', filteredData.value.length, 'data points for period:', selectedPeriod.value);
  
  if (chartInstance.value) {
    chartInstance.value.destroy();
  }
  
  const ctx = chartCanvas.value.getContext('2d');
  
  // Sử dụng bar chart cho năm view, line chart cho tuần và tháng
  const chartType = selectedPeriod.value === 'year' ? 'bar' : 'line';
  
  chartInstance.value = new Chart(ctx, {
    type: chartType,
    data: chartData.value,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true,
          position: 'top',
          labels: {
            padding: 15,
            font: {
              size: 12
            }
          }
        },
        tooltip: {
          callbacks: {
            label: (context) => {
              return `${context.dataset.label}: ${formatCurrency(context.parsed.y)}`;
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: (value) => formatCurrency(value)
          }
        },
        x: {
          display: true,
          ticks: {
            maxRotation: 45,
            minRotation: 45
          }
        }
      },
      interaction: {
        mode: 'index',
        intersect: false
      }
    }
  });
  
  console.log('✅ Chart created successfully with type:', chartType);
};

watch(() => props.data, () => {
  nextTick(() => {
    updateChart();
  });
}, { deep: true });

onMounted(() => {
  nextTick(() => {
    updateChart();
  });
});
</script>
