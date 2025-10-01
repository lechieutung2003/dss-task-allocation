import BaseService from "../base";

class OrderService extends BaseService {
  get entity() {
    return "orders";
  }
  
  // Lấy tất cả đơn hàng với bộ lọc tùy chọn
  getOrders(filters = {}) {
    let queryParams = new URLSearchParams();
    
    if (filters.keyword) {
      queryParams.append('search', filters.keyword);
    }
    
    if (filters.status) {
      queryParams.append('status', filters.status);
    }
    
    if (filters.startDate) {
      // Định dạng ngày thành chuỗi ISO nếu là đối tượng Date
      const startDate = filters.startDate instanceof Date 
        ? filters.startDate.toISOString().split('T')[0] 
        : filters.startDate;
      queryParams.append('start_date', startDate);
    }
    
    if (filters.endDate) {
      // Định dạng ngày thành chuỗi ISO nếu là đối tượng Date
      const endDate = filters.endDate instanceof Date 
        ? filters.endDate.toISOString().split('T')[0] 
        : filters.endDate;
      queryParams.append('end_date', endDate);
    }
    
    if (filters.page) {
      queryParams.append('page', filters.page);
    }
    
    if (filters.pageSize) {
      queryParams.append('page_size', filters.pageSize);
    }
    
    const queryString = queryParams.toString() ? `?${queryParams.toString()}` : '';
    return this.request().get(`${this.entity}${queryString}`);
  }
  
  // Lấy một đơn hàng cụ thể
  getOrder(id) {
    return this.request().get(`${this.entity}/${id}`);
  }
  
  // Tạo đơn hàng mới
  createOrder(orderData) {
    return this.request().post('create-order', orderData);
  }
  
  // Lấy danh sách phân công cho một đơn hàng
  getOrderAssignments(id) {
    return this.request().get(`${this.entity}/${id}/assignments`);
  }
  
  // Cập nhật trạng thái đơn hàng
  updateOrderStatus(id, status) {
    // Nếu status là string, chuyển thành đối tượng
    const statusData = typeof status === 'string' ? { status } : status;
    
    // Kiểm tra token
    const token = localStorage.getItem('access_token');
    
    // Thêm token vào headers nếu cần
    const headers = {
      'Content-Type': 'application/json'
    };
    
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    
    // Sử dụng URL không có trailing slash "/" ở cuối
    // Và thêm /api/v1/ vào đầu URL nếu không có trong this.entity
    const baseUrl = 'http://127.0.0.1:8008/api/v1/orders';
    const url = `${baseUrl}/${id}/updateStatus`;
    
    return this.request()
      .patch(url, statusData, { headers })
      .then(response => {
        // console.log('Update successful!');
        // console.log('Response:', response);
        return response;
      })
      .catch(error => {
        // console.error('Update failed:', error);
        if (error.response) {
          // console.error('Response status:', error.response.status);
          // console.error('Response data:', error.response.data);
        }
        throw error;
      });
  }
}

export default new OrderService();