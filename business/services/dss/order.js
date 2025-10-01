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
    return this.request().put(`${this.entity}/${id}`, { status });
  }
}

export default new OrderService();