# Enhanced Dashboard System - Complete Documentation

## 📊 Tổng Quan

Hệ thống Dashboard Nâng Cao gồm **3 modules chính**:

### 1️⃣ MODULE: BẢNG ĐƠN ƯU TIÊN (Priority Orders)
- **Top 10 đơn** ưu tiên nhất với phân trang (5 đơn/trang)
- **Auto-refresh** mỗi 30 giây
- **Quy tắc xếp hạng**:
  - Nếu 2 đơn cùng khoảng thời gian → so sánh `time_factor + price_factor`
  - Nếu khác khoảng thời gian → chỉ so sánh `time_factor`

#### Công Thức Tính Priority Score:
```
Time Factor (70%):
- (1,2] giờ: 0.7
- (2,3] giờ: 0.6
- (3,4] giờ: 0.5
- (4,5] giờ: 0.4
- (5,8] giờ: 0.3
- (8,12] giờ: 0.2
- (12,24] giờ: 0.1
- (24,...) giờ: 0

Price Factor (30%):
PF = 0.3 * min(price / 2,000,000, 1)

Priority Score = Time Factor + Price Factor
```

---

### 2️⃣ MODULE: KPI NHÂN VIÊN (Employee KPI)
- **Top 10 nhân viên** có điểm cao nhất với phân trang (5 nhân viên/trang)
- **Biểu đồ thanh ngang** hiển thị KPI Score
- **Popup chi tiết** khi click vào nhân viên

#### Công Thức Tính KPI:
```
Daily Standard = 8 giờ

WorkHourScore = min(total_worked_hours / 8, 1)

Early Completion Bonus:
- Nếu actual_end < expected_end:
  EarlyBonus += (expected_end - actual_end) / expected_duration

KPI Score = WorkHourScore + EarlyBonus
```

---

### 3️⃣ MODULE: DOANH THU - CHI PHÍ - LỢI NHUẬN
- **Line chart 3 đường**: Revenue, Cost, Profit
- **Bộ lọc thời gian**: 7 ngày, 30 ngày, quý, custom
- **Aggregate theo**: ngày, tuần, tháng

#### Công Thức Tính:
```
Revenue = cost_confirm của orders completed

Cost = 20 * (end - start in hours) * số nhân viên làm đơn

Profit = Revenue - Cost
```

---

## 🚀 Cài Đặt & Chạy

### Backend (Django)

1. **Restart Django server** để load các API mới:
```bash
cd /Volumes/KINGSTON/5.1/erp/dss-task-allocation/backend
python manage.py runserver 8008
```

2. **Test API endpoints**:
```bash
# Priority Orders
curl http://localhost:8008/api/v1/enhanced-dashboard/priority-orders?page=1&page_size=5

# Employee KPI
curl http://localhost:8008/api/v1/enhanced-dashboard/employee-kpi?page=1&page_size=5

# Employee KPI Detail
curl http://localhost:8008/api/v1/enhanced-dashboard/employee-kpi/1

# Revenue/Cost/Profit
curl "http://localhost:8008/api/v1/enhanced-dashboard/revenue-cost-profit?filter=30days&period=day"

# Full Dashboard
curl http://localhost:8008/api/v1/enhanced-dashboard/full
```

### Frontend (Nuxt 3)

1. **Chạy dev server**:
```bash
cd /Volumes/KINGSTON/5.1/erp/dss-task-allocation/business
npm run dev
```

2. **Truy cập dashboard**:
```
http://localhost:3000/dss/enhanced-dashboard
```

---

## 📁 Cấu Trúc File

### Backend
```
backend/
├── hr/
│   ├── services/
│   │   └── enhanced_dashboard_service.py  # Core business logic
│   ├── serializers/
│   │   └── enhanced_dashboard.py          # API serializers
│   ├── views/
│   │   └── enhanced_dashboard.py          # API endpoints
│   └── urls.py                            # URL routing
```

### Frontend
```
business/
├── services/dss/
│   └── enhancedDashboardService.js        # API service layer
├── components/enhanced-dashboard/
│   ├── PriorityOrdersTable.vue            # Module 1
│   ├── EmployeeKPITable.vue               # Module 2
│   └── RevenueCostProfitChart.vue         # Module 3
└── pages/dss/enhanced-dashboard/
    └── index.vue                          # Main dashboard page
```

---

## 🔧 API Endpoints

### 1. Priority Orders
```
GET /api/v1/enhanced-dashboard/priority-orders
Query params:
  - page: int (default: 1)
  - page_size: int (default: 5)

Response:
{
  "success": true,
  "data": [...],
  "pagination": {
    "page": 1,
    "page_size": 5,
    "total": 10,
    "total_pages": 2
  }
}
```

### 2. Employee KPI
```
GET /api/v1/enhanced-dashboard/employee-kpi
Query params:
  - page: int (default: 1)
  - page_size: int (default: 5)

Response:
{
  "success": true,
  "data": [...],
  "pagination": {...}
}
```

### 3. Employee KPI Detail
```
GET /api/v1/enhanced-dashboard/employee-kpi/{employee_id}

Response:
{
  "success": true,
  "data": {
    "employee_id": 1,
    "name": "...",
    "kpi_score": 1.5,
    "orders_detail": [...]
  }
}
```

### 4. Revenue/Cost/Profit
```
GET /api/v1/enhanced-dashboard/revenue-cost-profit
Query params:
  - filter: string (7days|30days|quarter|custom)
  - period: string (day|week|month)
  - start_date: string (YYYY-MM-DD) - required if filter=custom
  - end_date: string (YYYY-MM-DD) - required if filter=custom

Response:
{
  "success": true,
  "data": [...],
  "meta": {
    "filter": "30days",
    "period": "day",
    "start_date": "2025-10-22",
    "end_date": "2025-11-21"
  }
}
```

### 5. Full Dashboard
```
GET /api/v1/enhanced-dashboard/full

Response:
{
  "success": true,
  "data": {
    "priority_orders": [...],
    "employee_kpi": [...],
    "revenue_cost_profit": [...]
  }
}
```

---

## ✨ Tính Năng Nổi Bật

### ✅ Data Cleaning
- Loại bỏ records null, thời gian không hợp lệ
- Validate logic: `start_time < end_time`
- Filter chỉ lấy orders/employees hợp lệ

### ✅ Auto-refresh
- Priority Orders tự động refresh mỗi 30 giây
- Toggle ON/OFF auto-refresh
- Nút "Làm mới" để refresh toàn bộ dashboard

### ✅ Pagination
- Priority Orders: 5 đơn/trang
- Employee KPI: 5 nhân viên/trang
- Có thể chọn 5 hoặc 10 items/trang

### ✅ Interactive Charts
- **Bar Chart**: KPI Score của nhân viên (horizontal)
- **Line Chart**: Revenue/Cost/Profit với 3 đường
- Hover để xem chi tiết
- Responsive design

### ✅ Filters
- **Time filters**: 7 ngày, 30 ngày, quý, custom
- **Period aggregation**: ngày, tuần, tháng
- **Custom date range**: Chọn từ ngày đến ngày

### ✅ Employee Detail Popup
- Click vào nhân viên để xem chi tiết KPI
- Danh sách đơn hàng đã hoàn thành
- Early bonus cho từng đơn
- Tổng giờ làm việc, KPI score

---

## 🎨 UI Components

### 1. Priority Orders Table
- Highlight đơn urgent (1-2h) bằng màu đỏ nhạt
- Tag hiển thị time bucket
- Progress bar cho priority score
- Hiển thị time_factor và price_factor

### 2. Employee KPI Table
- Horizontal bar chart
- Hover row để highlight
- Click row để mở popup chi tiết
- Tag màu cho early bonus

### 3. Revenue/Cost/Profit Chart
- 3 line charts với màu khác nhau:
  - Revenue: Xanh lá (#67c23a)
  - Cost: Cam (#e6a23c)
  - Profit: Xanh dương (#409eff)
- Statistic cards hiển thị tổng
- Table hiển thị data chi tiết

---

## 🐛 Troubleshooting

### Lỗi: "Module not found"
```bash
# Đảm bảo đã import đúng trong urls.py
python manage.py check
```

### Lỗi: "CORS error"
```bash
# Kiểm tra CORS settings trong Django settings.py
# Thêm 'http://localhost:3000' vào CORS_ALLOWED_ORIGINS
```

### Chart không hiển thị
```bash
# Kiểm tra console log
# Đảm bảo Chart.js đã được cài đặt:
npm install chart.js
```

### Auto-refresh không hoạt động
```bash
# Kiểm tra prop :auto-refresh="true" trong component
# Kiểm tra interval trong PriorityOrdersTable.vue
```

---

## 📊 Data Requirements

### Bảng Orders cần có:
- `id`, `code`
- `customer_id`, `service_type_id`
- `preferred_start_time`, `preferred_end_time`
- `cost_confirm`
- `status` (pending, in_progress, completed)
- `area_m2`, `estimated_hours`
- `updated_at` (thời gian completed)

### Bảng Assignments cần có:
- `id`, `order_id`, `employee_id`
- `work_hours`, `cost`

### Bảng Employees cần có:
- `id`, `first_name`, `last_name`, `email`
- `is_staff`, `is_superuser`, `status`
- `area`

---

## 🚀 Performance Tips

1. **Database Indexing**:
```sql
CREATE INDEX idx_order_status ON hr_order(status);
CREATE INDEX idx_order_start_time ON hr_order(preferred_start_time);
CREATE INDEX idx_assignment_employee ON hr_assignment(employee_id);
```

2. **Caching** (optional):
```python
from django.core.cache import cache

# Cache priority orders for 30 seconds
cache_key = 'priority_orders_top10'
data = cache.get(cache_key)
if not data:
    data = EnhancedDashboardService.get_priority_orders_top10()
    cache.set(cache_key, data, 30)
```

3. **Frontend Optimization**:
- Debounce filter changes
- Lazy load charts
- Use computed properties

---

## 📝 Notes

- Ref price mặc định: **2,000,000 VND**
- Daily standard: **8 giờ**
- Cost per hour: **20 VND/giờ/nhân viên**
- Auto-refresh interval: **30 giây**
- Pagination default: **5 items/page**

---

## 🎉 Hoàn Thành!

Hệ thống dashboard đã hoàn chỉnh với:
- ✅ Backend: 5 API endpoints
- ✅ Frontend: 3 components + 1 main page
- ✅ Auto-refresh
- ✅ Pagination
- ✅ Interactive charts
- ✅ Data cleaning
- ✅ Filters

**Truy cập**: http://localhost:3000/dss/enhanced-dashboard
