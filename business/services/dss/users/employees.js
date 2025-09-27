import BaseService from '@/services/base.js'

class EmployeeService extends BaseService {
  get entity() {
    return 'employees';
  }

  async getEmployees(params = {}) {
    // Lọc bỏ empty parameters và search
    const cleanParams = {}

    Object.entries(params).forEach(([key, value]) => {
      // Bỏ qua search parameter và empty values
            if (key === 'search') {
        if (value && value.trim() !== '') {
          cleanParams[key] = value.trim()
        }
        return
      }

      if (key === 'computed_status') {
        // Only exclude null/undefined, allow 0, 1, 2
        if (value !== null && value !== undefined && value !== '') {
          cleanParams[key] = value
        }
        return
      }

      if (value !== null && value !== undefined && value !== '' && value !== 0) {
        cleanParams[key] = value
      }
    })

    console.log('Clean params sent to API:', cleanParams)

    // Nếu không có params nào thì gọi không có params
    if (Object.keys(cleanParams).length === 0) {
      return this.gets()
    }

    return this.gets(cleanParams)
  }

  async searchEmployees(searchTerm, params = {}) {
    // Tạo method riêng cho search 
    const searchParams = {
      ...params,
      first_name__icontains: searchTerm, // field search phù hợp
    }
    return this.gets(searchParams)
  }
  async getEmployee(id) {
    // Sử dụng get(id) cho một item
    return this.get(id)  // BaseService.get(id) 
  }

  async createEmployee(data) {
    // Sử dụng create() 
    return this.create(data)  // BaseService.create()
  }

  async updateEmployee(id, data) {
    // Thêm id vào data và dùng update()
    const updateData = { ...data, id }
    return this.update(updateData)  // BaseService.update()
  }

  async deleteEmployee(id) {
    // Sử dụng delete(id)
    return this.delete(id)  // BaseService.delete(id)
  }

  async updateEmployeeStatus(id, status) {
    // Để tạm method này (có thể cần custom endpoint)
    return this.request().patch(`${this.entity}/${id}`, { status })
  }

  async getMyProfile() {
    // Sử dụng endpoint my-profile thay vì filter
    return this.request().get(`${this.entity}/my-profile`)
  }

  async updateMyProfile(data) {
    // Sử dụng endpoint update-my-profile
    return this.request().patch(`${this.entity}/update-my-profile`, data)
  }
}

export default new EmployeeService()