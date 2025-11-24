import ApiService from "@/services/api";

const baseUrl = "http://localhost:8008/api/v1/dashboard";

class DashboardService {
  // Lấy tất cả dữ liệu dashboard trong 1 request (optimize performance)
  async getFullDashboard(params = {}) {
    try {
      const requestParams = {
        order_limit: params.orderLimit || 20,
        start_date: params.startDate || this.getDefaultStartDate(),
        end_date: params.endDate || this.getDefaultEndDate()
      };
      
      console.log('🚀 Calling dashboard API:', `${baseUrl}/full`, requestParams);
      
      const response = await ApiService.get(`${baseUrl}/full`, { params: requestParams });
      
      console.log('✅ Full API response object:', response);
      console.log('Response type:', typeof response);
      
      if (!response) {
        console.error('❌ Response is null or undefined');
        return null;
      }
      
      // Check if response has the expected structure
      if (response.overview || response.priority_orders || response.employee_kpi || response.daily_summary) {
        console.log('✅ Valid dashboard data structure found');
        return response;
      }
      
      console.warn('⚠️ Unexpected response structure:', Object.keys(response));
      return response;
      
    } catch (error) {
      console.error('❌ Error fetching full dashboard:', error);
      console.error('Error type:', error.constructor.name);
      console.error('Error message:', error.message);
      console.error('Error response:', error.response);
      console.error('Error data:', error.data);
      return null;
    }
  }

  // Lấy thống kê tổng quan từ Django API
  async getDashboardStats() {
    try {
      const fullData = await this.getFullDashboard();
      if (!fullData || !fullData.overview) {
        return this.getDefaultStats();
      }
      
      // Map field names từ backend sang frontend format
      return {
        data: {
          overview: {
            totalTasks: fullData.overview.total_orders || 0,
            activeTasks: fullData.overview.active_orders || 0,
            completedTasks: fullData.overview.completed_orders || 0,
            failedTasks: fullData.overview.rejected_orders || 0,
            successRate: fullData.overview.success_rate || 0,
            totalRevenue: fullData.overview.total_revenue || 0,
            totalCost: fullData.overview.total_cost || 0,
            totalProfit: fullData.overview.total_profit || 0,
            profitMargin: fullData.overview.profit_margin || 0,
            activeEmployees: fullData.overview.active_employees || 0,
            avgCompletionTime: fullData.overview.avg_completion_time || 0,
            todayRevenue: fullData.overview.total_revenue || 0, // Tạm dùng total revenue
            totalEmployees: fullData.overview.active_employees || 0,
            employeesWithOrders: 0,
            // customerSatisfaction: 4.8, // Default value
          }
        }
      };
    } catch (error) {
      console.error('Error in getDashboardStats:', error);
      return this.getDefaultStats();
    }
  }

  // DEPRECATED: Không còn cần tính toán client-side, backend đã xử lý

  // Lấy nhiệm vụ ưu tiên từ full dashboard API
  async getUrgentTasks() {
    try {
      const fullData = await this.getFullDashboard({ orderLimit: 20 });
      if (!fullData || !fullData.priority_orders) {
        return this.getDefaultUrgentTasks();
      }
      
      const orders = fullData.priority_orders || [];
      
      return orders.slice(0, 10).map(order => ({
        id: order.order_id,
        title: `${order.service_type} - ${order.customer_name}`,
        deadline: order.preferred_end_time,
        location: 'N/A',
        priority: this.mapPriorityLevel(order.priority_level),
        priorityScore: order.priority_score,
        timeScore: order.time_score,
        priceScore: order.price_score,
        assignee: 'Chưa phân công',
        progress: this.calculateProgressFromStatus(order.status),
        area: `${order.area_m2}m²`,
        estimatedHours: `${order.estimated_hours}h`,
        status: order.status,
        note: order.note || '',
        cost: parseFloat(order.cost_confirm) || 0,
        customer_name: order.customer_name
      }));
    } catch (error) {
      console.error('Error fetching urgent tasks:', error);
      return this.getDefaultUrgentTasks();
    }
  }

  // Lấy dữ liệu cho biểu đồ từ full dashboard API
  async getChartData(startDate = null, endDate = null) {
    try {
      const fullData = await this.getFullDashboard({
        startDate: startDate || this.getDefaultStartDate(),
        endDate: endDate || this.getDefaultEndDate()
      });
      
      if (!fullData || !fullData.daily_summary) {
        console.warn('⚠️ No daily_summary data found');
        return { revenue: [], tasks: { completed: 0, in_progress: 0, failed: 0 }, dailySummary: [] };
      }
      
      const dailyData = fullData.daily_summary || [];
      
      console.log('📊 Processing daily summary data:', dailyData.length, 'days');
      
      // Format data cho charts - FilterableChart expects array with date, amount, cost, profit
      const revenueData = dailyData.map(day => ({
        date: day.date,
        amount: day.revenue || 0,
        revenue: day.revenue || 0,
        cost: day.cost || 0,
        profit: day.profit || 0
      }));

      // Tính tổng tasks theo status
      const tasksSummary = dailyData.reduce((acc, day) => ({
        completed: acc.completed + (day.complete_count || 0),
        in_progress: acc.in_progress + (day.pending_count || 0),
        failed: acc.failed + (day.reject_count || 0),
        pending: acc.pending + (day.pending_count || 0)
      }), { completed: 0, in_progress: 0, failed: 0, pending: 0 });

      console.log('✅ Chart data formatted:', {
        revenueDataPoints: revenueData.length,
        tasksSummary,
        sampleData: revenueData.slice(0, 2)
      });

      return {
        revenue: revenueData,
        tasks: tasksSummary,
        dailySummary: dailyData
      };
    } catch (error) {
      console.error('Error generating chart data:', error);
      return { revenue: [], tasks: { completed: 0, in_progress: 0, failed: 0 }, dailySummary: [] };
    }
  }

  // Lấy KPI nhân viên từ full dashboard API
  async getEmployeeKPI() {
    try {
      const fullData = await this.getFullDashboard();
      if (!fullData || !fullData.employee_kpi) {
        return [];
      }
      
      return fullData.employee_kpi || [];
    } catch (error) {
      console.error('Error fetching employee KPI:', error);
      return [];
    }
  }

  // Helper: Lấy ngày bắt đầu mặc định (30 ngày trước)
  getDefaultStartDate() {
    const date = new Date();
    date.setDate(date.getDate() - 30);
    return date.toISOString().split('T')[0];
  }

  // Helper: Lấy ngày kết thúc mặc định (hôm nay)
  getDefaultEndDate() {
    return new Date().toISOString().split('T')[0];
  }

  // Helper: Map priority level từ backend
  mapPriorityLevel(level) {
    const mapping = {
      'high': 'Cao',
      'medium': 'Trung bình',
      'low': 'Thấp'
    };
    return mapping[level] || 'Trung bình';
  }

  // Helper: Tính progress từ status
  calculateProgressFromStatus(status) {
    switch (status) {
      case 'completed': return 100;
      case 'in_progress': return 60;
      case 'confirmed': return 30;
      case 'pending': return 10;
      default: return 0;
    }
  }

  // DEPRECATED: Các method cũ để fallback
  async getRecentActivities() {
    return { data: [] };
  }

  // Default fallback chỉ cho trường hợp API lỗi
  getDefaultStats() {
    return {
      data: {
        overview: {
          totalTasks: 0,
          activeTasks: 0,
          completedTasks: 0,
          totalEmployees: 0,
          activeEmployees: 0,
          employeesWithOrders: 0,
          todayRevenue: 0,
          totalRevenue: 0,
          customerSatisfaction: 0,
          avgCompletionTime: 0,
          successRate: 0,
        }
      }
    };
  }

  getDefaultUrgentTasks() {
    return []; // Return empty array instead of mock data
  }

}

export default new DashboardService();