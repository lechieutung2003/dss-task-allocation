import ApiService from '@/services/api';

class RecommendationService {
  constructor() {
    this.baseUrl = 'http://127.0.0.1:8008/api/v1';
  }

  getRecommendations(orderId) {
    return ApiService.get(`${this.baseUrl}/orders/${orderId}/recommendations`);
  }
}

export default new RecommendationService();