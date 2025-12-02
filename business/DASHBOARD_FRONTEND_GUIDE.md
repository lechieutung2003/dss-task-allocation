# Dashboard Frontend Integration Guide

## Tổng Quan

Frontend đã được cập nhật để sử dụng Django Backend API mới với đầy đủ tính năng:

### ✅ Đã Hoàn Thành

1. **Service Layer** (`business/services/dss/dashboardService.js`)
   - `getDashboardStats()` - Gọi `/api/v1/hr/dashboard/overview`
   - `getUrgentTasks()` - Gọi `/api/v1/hr/dashboard/priority-orders` (với priority_score)
   - `getChartData()` - Gọi `/api/v1/hr/dashboard/daily-summary` (revenue, cost, profit)
   - `getEmployeeKPI()` - Gọi `/api/v1/hr/dashboard/employee-kpi`
   - `getFullDashboard()` - Gọi `/api/v1/hr/dashboard/full` (optimize 1 request)

2. **Components Mới**
   - `PriorityOrdersTable.vue` - Bảng orders ưu tiên với highlight priority_score
   - `EmployeeKPITable.vue` - Bảng KPI nhân viên với completion_rate, KPI score
   - `FilterableChart.vue` - Biểu đồ combo có filter tuần/tháng/năm

3. **Dashboard Page** (`pages/dss/dashboard/index.vue`)
   - Hiển thị overview metrics từ backend
   - Render Priority Orders table (sorted by priority_score)
   - Render Employee KPI table (sorted by KPI score)
   - Filterable charts (revenue, cost, profit)

## Cách Sử Dụng

### 1. Chạy Backend Django

```bash
cd backend
source .venv/bin/activate  # Mac/Linux
python manage.py runserver
```

Backend sẽ chạy tại: `http://localhost:8000`

### 2. Chạy Frontend Nuxt

```bash
cd business
npm run dev
# hoặc
pnpm dev
```

Frontend sẽ chạy tại: `http://localhost:3000`

### 3. Truy Cập Dashboard

Đăng nhập và truy cập: `http://localhost:3000/dss/dashboard`

## Các Tính Năng

### 📊 Overview Metrics

Hiển thị từ `/api/v1/hr/dashboard/overview`:
- Tổng nhiệm vụ / Đang thực hiện / Hoàn thành
- Tổng nhân viên / Active / Có orders
- Doanh thu hôm nay / Tổng doanh thu / Chi phí / Lợi nhuận
- Tỷ lệ thành công / Thời gian TB hoàn thành

### 🔥 Priority Orders Table

- **Dữ liệu từ**: `/api/v1/hr/dashboard/priority-orders?limit=20`
- **Sắp xếp**: Theo `priority_score` (giảm dần)
- **Highlight**:
  - Đỏ: priority_score >= 0.7 (high)
  - Vàng: priority_score >= 0.4 (medium)
  - Xanh: priority_score < 0.4 (low)
- **Hiển thị**:
  - Priority score (time_score + price_score)
  - Thông tin khách hàng
  - Deadline
  - Chi tiết (area, estimated hours, cost)
  - Trạng thái
  - Tiến độ

### 👥 Employee KPI Table

- **Dữ liệu từ**: `/api/v1/hr/dashboard/employee-kpi`
- **Sắp xếp**: Theo `kpi_score` (giảm dần)
- **Hiển thị**:
  - Số đơn hoàn thành / Tổng đơn
  - Completion rate (%)
  - Thời gian trung bình
  - Tổng giờ làm việc
  - KPI Score (0-100)
  - Xếp hạng (A/B/C/D)

### 📈 Filterable Charts

- **Dữ liệu từ**: `/api/v1/hr/dashboard/daily-summary`
- **Filter**: Tuần / Tháng / Năm (xử lý trên frontend)
- **Biểu đồ combo**:
  - Line chart: Doanh thu (xanh lá)
  - Line chart: Chi phí (đỏ)
  - Line chart: Lợi nhuận (xanh dương)
- **Summary**:
  - Tổng doanh thu trong period
  - Tổng chi phí trong period
  - Tổng lợi nhuận trong period

## API Endpoints Sử Dụng

```javascript
// Overview
GET /api/v1/hr/dashboard/overview

// Priority Orders
GET /api/v1/hr/dashboard/priority-orders?limit=20

// Employee KPI
GET /api/v1/hr/dashboard/employee-kpi

// Daily Summary
GET /api/v1/hr/dashboard/daily-summary?start_date=2025-10-21&end_date=2025-11-21

// Full Dashboard (1 request)
GET /api/v1/hr/dashboard/full?order_limit=20&start_date=2025-10-21&end_date=2025-11-21
```

## Cấu Trúc File

```
business/
├── services/dss/
│   └── dashboardService.js          # Service gọi API backend
├── components/
│   └── dashboard/
│       ├── PriorityOrdersTable.vue  # Bảng orders ưu tiên
│       ├── EmployeeKPITable.vue     # Bảng KPI nhân viên
│       └── FilterableChart.vue      # Biểu đồ có filter
└── pages/dss/dashboard/
    └── index.vue                     # Dashboard chính
```

## Data Flow

```
Frontend Request
    ↓
dashboardService.js
    ↓
Django Backend API
    ↓
DashboardService (Python)
    ├── Data Cleaning (loại bỏ thiếu data, duplicate)
    ├── Priority Score Calculation (time + price)
    ├── KPI Calculation (completion rate, hours, score)
    └── Daily Summary Aggregation (revenue, cost, profit by date)
    ↓
JSON Response
    ↓
Frontend Components (Vue)
    ├── Filter (tuần/tháng/năm)
    ├── Sort (by priority_score, kpi_score)
    ├── Highlight (color code by level)
    └── Render Charts (Chart.js)
```

## Lưu Ý

### Backend Chịu Trách Nhiệm

✅ Data cleaning (loại thiếu data, duplicate)
✅ Tính toán priority_score (time_score + price_score)
✅ Tính toán KPI (completion_rate, kpi_score)
✅ Tổng hợp daily summary (revenue, cost, profit)
✅ Normalization (VND, datetime)

### Frontend Chịu Trách Nhiệm

✅ Filter theo period (tuần/tháng/năm) từ daily summary
✅ Render charts (Chart.js)
✅ Color code / Highlight theo level
✅ Tooltip / Hover effects
✅ Sort / Pagination (client-side)

## Optimization

### Caching

Dashboard sử dụng cache 5 phút:

```javascript
const dataCache = reactive({
  lastUpdate: null,
  cacheExpiry: 5 * 60 * 1000, // 5 phút
});
```

### Single Request Optimization

Thay vì gọi 4-5 requests riêng, có thể dùng `/full` endpoint:

```javascript
const fullData = await dashboardService.getFullDashboard({
  orderLimit: 20,
  startDate: '2025-10-21',
  endDate: '2025-11-21'
});

// fullData chứa:
// - overview
// - priority_orders
// - employee_kpi
// - daily_summary
```

## Testing

### 1. Test Backend API

```bash
# Overview
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/v1/hr/dashboard/overview

# Priority Orders
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/v1/hr/dashboard/priority-orders?limit=5

# Employee KPI
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/v1/hr/dashboard/employee-kpi

# Daily Summary
curl -H "Authorization: Bearer <token>" \
  "http://localhost:8000/api/v1/hr/dashboard/daily-summary?start_date=2025-11-01&end_date=2025-11-21"
```

### 2. Test Frontend

1. Mở browser DevTools (F12)
2. Vào tab Network
3. Refresh dashboard page
4. Kiểm tra các requests đến `/api/v1/hr/dashboard/*`
5. Kiểm tra response data

## Troubleshooting

### Lỗi CORS

Nếu gặp lỗi CORS, kiểm tra `backend/core/settings/base.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

### Lỗi Authentication

Đảm bảo token được gửi trong header:

```javascript
// services/base.js
headers: {
  Authorization: `Bearer ${token}`
}
```

### Không có dữ liệu

1. Chạy script seed data:
   ```bash
   cd backend
   python create_order_data.py --count 200 --apply
   ```

2. Kiểm tra backend logs:
   ```bash
   python manage.py runserver
   # Xem console output
   ```

## Next Steps

1. **Real-time Updates**: Thêm WebSocket để cập nhật real-time
2. **Export**: Thêm tính năng export PDF/Excel
3. **Advanced Filters**: Thêm filter theo location, service type, employee
4. **Predictive Analytics**: Tích hợp ML model để dự đoán demand

## Dependencies

### Frontend

```json
{
  "chart.js": "^4.x",
  "element-plus": "^2.x"
}
```

### Backend

```txt
djangorestframework==3.15.1
drf-yasg==1.21.7  # Swagger docs
```

Install:

```bash
cd business
npm install chart.js

cd ../backend
pip install drf-yasg
```
