import ApiService from "@/services/api";

const baseUrl = "http://127.0.0.1:8008/api/v1/customer";
const customerApi = {
	// Lấy danh sách đơn hàng của customer
	async getOrders(params) {
		return ApiService.get(baseUrl + "/orders", { params });
	},

	// Lấy chi tiết một đơn hàng
	async getOrder(id) {
		return ApiService.get(`${baseUrl}/orders/${id}`);
	},

	// Tạo đơn hàng mới cho customer
	async createOrder(orderData) {
		return ApiService.post(`${baseUrl}/create-order`, orderData);
	},

};

export default customerApi;
