import BaseService from "../base";
import orderService from "./order";
import employeeService from "./users/employees";
import customerService from "./customer";

class DashboardService extends BaseService {
  get entity() {
    return "dashboard";
  }
  // Lấy thống kê tổng quan
  async getDashboardStats() {
    try {
      // TODO: Gọi API dashboard khi có endpoint thật
      // return await this.request().get(`${this.entity}/stats`);
      
      // Tạm thời tính toán từ các service khác
      console.log('Calculating dashboard stats from existing services...');
      return this.calculateStatsFromServices();
    } catch (error) {
      console.error('Error in getDashboardStats:', error);
      // Fallback: return default data
      return this.getDefaultStats();
    }
  }

  // Tính toán thống kê từ các service khác
  async calculateStatsFromServices() {
    try {
      // Chỉ lấy 100 records để tính toán nhanh hơn
      const [ordersResponse, employeesResponse] = await Promise.all([
        orderService.getOrders({ pageSize: 100 }), // Giảm từ 1000 xuống 100
        employeeService.getEmployees({ page_size: 50 }), // Giảm từ 1000 xuống 50
      ]);

      const orders = ordersResponse.data?.results || ordersResponse.data || [];
      const employees = employeesResponse.data?.results || employeesResponse.data || [];

      // Tính toán các thông số
      const totalTasks = orders.length;
      const activeTasks = orders.filter(order => 
        ['in_progress', 'assigned', 'pending'].includes(order.status)
      ).length;
      const completedTasks = orders.filter(order => 
        order.status === 'completed'
      ).length;

      // Tính doanh thu hôm nay (giả định có field amount và created_at)
      const today = new Date().toISOString().split('T')[0];
      const todayRevenue = orders
        .filter(order => 
          order.created_at && 
          order.created_at.startsWith(today) && 
          order.status === 'completed'
        )
        .reduce((sum, order) => sum + (parseFloat(order.amount) || 0), 0);

      // Tính customer satisfaction (giả định có field rating)
      const completedOrdersWithRating = orders.filter(order => 
        order.status === 'completed' && order.rating
      );
      const avgRating = completedOrdersWithRating.length > 0
        ? completedOrdersWithRating.reduce((sum, order) => sum + order.rating, 0) / completedOrdersWithRating.length
        : 4.8;

      return {
        data: {
          overview: {
            totalTasks,
            activeTasks,
            completedTasks,
            totalEmployees: employees.length,
            todayRevenue,
            customerSatisfaction: Math.round(avgRating * 10) / 10,
            avgCompletionTime: 2.3, // Default value
            successRate: totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0,
          }
        }
      };
    } catch (error) {
      console.error('Error calculating stats:', error);
      // Return default data if calculation fails
      return this.getDefaultStats();
    }
  }

  // Lấy nhiệm vụ ưu tiên
  async getUrgentTasks() {
    try {
      const response = await orderService.getOrders({
        status: 'pending,assigned,in_progress',
        pageSize: 5 // Giảm từ 10 xuống 5 để load nhanh hơn
      });
      
      const orders = response.data?.results || response.data || [];
      
      return orders.map(order => ({
        id: order.id,
        title: order.title || order.service_type || 'Nhiệm vụ dọn dẹp',
        deadline: order.deadline || order.scheduled_date,
        location: order.address || order.location,
        priority: this.getPriority(order),
        assignee: order.assigned_employee?.name || order.employee_name || 'Chưa phân công',
        progress: this.calculateProgress(order),
      }));
    } catch (error) {
      console.error('Error fetching urgent tasks:', error);
      return this.getDefaultUrgentTasks();
    }
  }

  // Lấy dữ liệu cho biểu đồ - tạm thời return default data vì chưa có API
  async getChartData() {
    try {
      // TODO: Thay bằng API thật khi có
      // const response = await this.request().get(`${this.entity}/charts`);
      // return response.data;
      
      console.log('Using default chart data (no API endpoint yet)');
      return this.generateDefaultChartData();
    } catch (error) {
      console.error('Error fetching chart data:', error);
      return this.generateDefaultChartData();
    }
  }

  // Lấy hoạt động gần đây - tạm thời return default data vì chưa có API
  async getRecentActivities() {
    try {
      // TODO: Thay bằng API thật khi có
      // return await this.request().get(`${this.entity}/activities`);
      
      console.log('Using default activities data (no API endpoint yet)');
      return this.getDefaultActivities();
    } catch (error) {
      console.error('Error fetching activities:', error);
      return this.getDefaultActivities();
    }
  }

  // Helper methods
  getPriority(order) {
    if (order.priority) return order.priority;
    
    // Tính priority based on deadline
    if (order.deadline) {
      const deadline = new Date(order.deadline);
      const now = new Date();
      const hoursLeft = (deadline - now) / (1000 * 60 * 60);
      
      if (hoursLeft < 24) return 'Cao';
      if (hoursLeft < 72) return 'Trung bình';
      return 'Thấp';
    }
    
    return 'Trung bình';
  }

  calculateProgress(order) {
    if (order.progress !== undefined) return order.progress;
    
    // Calculate based on status
    switch (order.status) {
      case 'completed': return 100;
      case 'in_progress': return Math.floor(Math.random() * 60) + 30; // 30-90%
      case 'assigned': return Math.floor(Math.random() * 30) + 10; // 10-40%
      default: return 0;
    }
  }

  // Default data fallbacks
  getDefaultStats() {
    return {
      data: {
        overview: {
          totalTasks: 156,
          activeTasks: 45,
          completedTasks: 98,
          totalEmployees: 28,
          todayRevenue: 12500000,
          customerSatisfaction: 4.8,
          avgCompletionTime: 2.3,
          successRate: 96.5,
        }
      }
    };
  }

  getDefaultUrgentTasks() {
    return [
      {
        id: 1,
        title: "Vệ sinh văn phòng ABC Corp",
        deadline: "2025-09-28 14:00",
        location: "Quận 1, TP.HCM",
        priority: "Cao",
        assignee: "Nguyễn Văn A",
        progress: 75,
      },
      {
        id: 2,
        title: "Dọn dẹp nhà riêng VIP",
        deadline: "2025-09-28 16:30",
        location: "Quận 7, TP.HCM",
        priority: "Trung bình",
        assignee: "Trần Thị B",
        progress: 45,
      },
      {
        id: 3,
        title: "Vệ sinh khách sạn XYZ",
        deadline: "2025-09-29 08:00",
        location: "Quận 3, TP.HCM",
        priority: "Cao",
        assignee: "Lê Văn C",
        progress: 20,
      },
    ];
  }

  getDefaultActivities() {
    return {
      data: [
        {
          id: 1,
          type: 'success',
          title: 'Hoàn thành nhiệm vụ',
          description: 'Vệ sinh văn phòng Building DEF đã được hoàn thành xuất sắc',
          time: '10 phút trước',
          user: 'Nguyễn Văn A',
          location: 'Quận 1, TP.HCM'
        }
      ]
    };
  }

  generateDefaultChartData() {
    return {
      revenue: [
        { date: '2025-09-21', amount: 8500000 },
        { date: '2025-09-22', amount: 12000000 },
        { date: '2025-09-23', amount: 9500000 },
        { date: '2025-09-24', amount: 11000000 },
        { date: '2025-09-25', amount: 13500000 },
        { date: '2025-09-26', amount: 10500000 },
        { date: '2025-09-27', amount: 14000000 },
      ],
      tasks: {
        completed: [15, 22, 18, 25, 20, 28, 24],
        pending: [8, 12, 10, 15, 11, 9, 13],
        in_progress: [12, 8, 14, 10, 16, 11, 15]
      }
    };
  }
}

export default new DashboardService();