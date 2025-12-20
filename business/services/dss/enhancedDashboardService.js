import ApiService from '~/services/api'

/**
 * Enhanced Dashboard Service - Complete 3 Modules
 * 1. Priority Orders (top 10 with pagination)
 * 2. Employee KPI (top 10 with pagination + detail popup)
 * 3. Revenue/Cost/Profit (with filters: 7days, 30days, quarter, custom)
 */

const BASE_URL = 'http://localhost:8008/api/v1/enhanced-dashboard'

export default {
  // ==================== MODULE 1: PRIORITY ORDERS ====================
  
  /**
   * Get top 10 priority orders with pagination
   * @param {Object} params - { page: 1, page_size: 5 }
   */
  async getPriorityOrders(params = {}) {
    try {
      const response = await ApiService.get(`${BASE_URL}/priority-orders`, { params })
      return response
    } catch (error) {
      console.error('❌ Error fetching priority orders:', error)
      throw error
    }
  },

  // ==================== MODULE 2: EMPLOYEE KPI ====================
  
  /**
   * Get top 10 employees by KPI with pagination
   * @param {Object} params - { page: 1, page_size: 5, period: 'week' | 'month', start_date, end_date }
   */
  async getEmployeeKPI(params = {}) {
    try {
      const response = await ApiService.get(`${BASE_URL}/employee-kpi`, { params })
      return response
    } catch (error) {
      console.error('❌ Error fetching employee KPI:', error)
      throw error
    }
  },

  /**
   * Get detailed KPI for specific employee (for popup)
   * @param {Number} employeeId
   * @param {Object} params - { period: 'week' | 'month', start_date, end_date }
   */
  async getEmployeeKPIDetail(employeeId, params = {}) {
    try {
      const response = await ApiService.get(`${BASE_URL}/employee-kpi/${employeeId}`, { params })
      return response
    } catch (error) {
      console.error('❌ Error fetching employee KPI detail:', error)
      throw error
    }
  },

  // ==================== MODULE 3: REVENUE - COST - PROFIT ====================
  
  /**
   * Get Revenue/Cost/Profit data with filters
   * @param {Object} params - { 
   *   filter: '7days'|'30days'|'quarter'|'custom',
   *   period: 'day'|'week'|'month',
   *   start_date?: 'YYYY-MM-DD',
   *   end_date?: 'YYYY-MM-DD'
   * }
   */
  async getRevenueCostProfit(params = {}) {
    try {
      const response = await ApiService.get(`${BASE_URL}/revenue-cost-profit`, { params })
      return response
    } catch (error) {
      console.error('❌ Error fetching revenue/cost/profit:', error)
      throw error
    }
  },

  // ==================== MODULE 4: SERVICE TYPE PIE ====================
  
  /**
   * Get counts grouped by service type for pie chart
   * @param {Object} params - { start_date?: 'YYYY-MM-DD', end_date?: 'YYYY-MM-DD', date_field?: 'updated_at' }
   */
  async getServiceTypeCounts(params = {}) {
    try {
      const response = await ApiService.get(`${BASE_URL}/service-types`, { params })
      return response
    } catch (error) {
      console.error('❌ Error fetching service type counts:', error)
      throw error
    }
  },

  /**
   * Alias kept for backward compatibility
   */
  async getServiceTypePie(params = {}) {
    return this.getServiceTypeCounts(params)
  },

  // ==================== MODULE 5: SERVICE STATUS PIE ====================
  /**
   * Get counts grouped by order status (completed / rejected / other)
   * params: { start_date?, end_date?, date_field?: 'updated_at' }
   */
  async getServiceStatusCounts(params = {}) {
    try {
      const response = await ApiService.get(`${BASE_URL}/service-status`, { params })
      return response
    } catch (error) {
      console.error('❌ Error fetching service status counts:', error)
      throw error
    }
  },
  async getServiceStatusPie(params = {}) {
    return this.getServiceStatusCounts(params)
  },

  // ==================== COMBINED DASHBOARD ====================
  
  /**
   * Get full enhanced dashboard (all 3 modules)
   */
  async getFullDashboard() {
    try {
      const response = await ApiService.get(`${BASE_URL}/full`)
      return response
    } catch (error) {
      console.error('❌ Error fetching full enhanced dashboard:', error)
      throw error
    }
  }
}
