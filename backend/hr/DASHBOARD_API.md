# Dashboard API Documentation

## Tổng quan

Backend Django API đã được tạo để hỗ trợ dashboard admin cho web dịch vụ dọn dẹp. API thực hiện:

1. **Data Cleaning** - Làm sạch dữ liệu từ database
2. **Tính toán KPI** - Tính priority score cho orders, KPI nhân viên
3. **Tổng hợp dữ liệu** - Tổng hợp kinh doanh theo ngày
4. **JSON Response** - Trả về dữ liệu chuẩn cho frontend

## Cấu trúc dữ liệu

### Database Models
- **Order (hr_order)**: Đơn hàng từ khách hàng
- **Customer (hr_customer)**: Thông tin khách hàng
- **ServiceType (hr_service_type)**: Loại dịch vụ dọn dẹp
- **Assignment (hr_assignment)**: Phân công nhân viên cho đơn hàng
- **Employee (employees)**: Thông tin nhân viên

## API Endpoints

### 1. Dashboard Overview
```
GET /api/v1/dashboard/overview
```

**Mô tả**: Lấy tổng quan dashboard với các chỉ số tổng hợp

**Response**:
```json
{
  "total_orders": 150,
  "active_orders": 45,
  "completed_orders": 100,
  "rejected_orders": 5,
  "success_rate": 66.67,
  "total_revenue": 50000000.00,
  "total_cost": 30000000.00,
  "total_profit": 20000000.00,
  "profit_margin": 40.00,
  "active_employees": 20,
  "avg_completion_time": 4.5
}
```

### 2. Priority Orders
```
GET /api/v1/dashboard/priority-orders?limit=20
```

**Mô tả**: Lấy danh sách orders ưu tiên (đã tính priority score)

**Query Parameters**:
- `limit` (optional): Số lượng orders trả về (default: 20)

**Response**:
```json
[
  {
    "order_id": 123,
    "priority_score": 0.85,
    "priority_level": "high",
    "time_score": 0.55,
    "price_score": 0.30,
    "preferred_start_time": "2025-11-22T08:00:00Z",
    "preferred_end_time": "2025-11-22T12:00:00Z",
    "cost_confirm": 500000.00,
    "service_type": "Dọn dẹp căn hộ",
    "service_type_id": 1,
    "status": "pending",
    "customer_name": "Nguyễn Văn A",
    "customer_id": 45,
    "area_m2": 80.00,
    "estimated_hours": 4.00,
    "note": "Cần dọn trước 12h"
  }
]
```

**Priority Score Calculation**:
- **time_score** (0-0.6): Dựa trên thời gian còn lại đến deadline
  - < 0h (quá hạn): 0.6
  - < 24h: 0.5-0.6
  - < 72h: 0.3-0.5
  - < 1 tuần: 0.1-0.3
  - > 1 tuần: 0-0.1
  
- **price_score** (0-0.4): Dựa trên giá trị đơn hàng
  - Linear scaling từ 100k-10M VND
  
- **priority_score** = time_score + price_score
- **priority_level**:
  - >= 0.7: "high"
  - >= 0.4: "medium"
  - < 0.4: "low"

### 3. Employee KPI
```
GET /api/v1/dashboard/employee-kpi
```

**Mô tả**: Lấy KPI của tất cả nhân viên

**Response**:
```json
[
  {
    "employee_id": 10,
    "name": "Trần Thị B",
    "completed_orders": 45,
    "total_orders": 50,
    "avg_duration": 4.2,
    "completion_rate": 90.00,
    "kpi_score": 85.50,
    "total_hours_worked": 189.00,
    "area": "Hải Châu"
  }
]
```

**KPI Score Calculation**:
- 50% từ completion_rate
- 30% từ số đơn hoàn thành (normalized, max 100 đơn/tháng)
- 20% từ total hours worked (normalized, max 200h/tháng)

### 4. Daily Summary
```
GET /api/v1/dashboard/daily-summary?start_date=2025-10-01&end_date=2025-11-21
```

**Mô tả**: Lấy tổng hợp kinh doanh theo ngày

**Query Parameters**:
- `start_date` (optional): Ngày bắt đầu (YYYY-MM-DD, default: 30 ngày trước)
- `end_date` (optional): Ngày kết thúc (YYYY-MM-DD, default: hôm nay)

**Response**:
```json
[
  {
    "date": "2025-11-21",
    "revenue": 2500000.00,
    "cost": 1500000.00,
    "profit": 1000000.00,
    "complete_count": 5,
    "reject_count": 0,
    "pending_count": 3,
    "total_orders": 8
  }
]
```

**Calculation**:
- **revenue**: Tổng `cost_confirm` của orders có `status='completed'` trong ngày
- **cost**: Tổng `cost` từ bảng `Assignment` trong ngày
- **profit**: revenue - cost
- **complete_count**: Số orders `status='completed'`
- **reject_count**: Số orders `status='rejected'`
- **pending_count**: Số orders `status in ['pending', 'confirmed', 'in_progress']`

### 5. Full Dashboard (Tổng hợp tất cả)
```
GET /api/v1/dashboard/full?order_limit=20&start_date=2025-10-01&end_date=2025-11-21
```

**Mô tả**: Lấy tất cả dữ liệu dashboard trong 1 request

**Query Parameters**:
- `order_limit` (optional): Số lượng priority orders (default: 20)
- `start_date` (optional): Ngày bắt đầu cho daily summary (YYYY-MM-DD)
- `end_date` (optional): Ngày kết thúc cho daily summary (YYYY-MM-DD)

**Response**:
```json
{
  "overview": { /* DashboardOverview data */ },
  "priority_orders": [ /* Array of PriorityOrder */ ],
  "employee_kpi": [ /* Array of EmployeeKPI */ ],
  "daily_summary": [ /* Array of DailySummary */ ]
}
```

## Data Cleaning Logic

Backend thực hiện các bước cleaning sau:

1. **Loại bỏ đơn thiếu thông tin**:
   - `preferred_start_time IS NOT NULL`
   - `cost_confirm IS NOT NULL`
   - `cost_confirm > 0`

2. **Chuẩn hóa dữ liệu**:
   - Thời gian: Django `DateTimeField` tự động parse
   - Cost: `DecimalField` đảm bảo độ chính xác
   - Loại bỏ duplicate bằng `.distinct()`

3. **Select related data**:
   - Optimize query với `select_related('customer', 'service_type')`
   - Tránh N+1 query problem

## Frontend Integration

Frontend React dashboard sử dụng API này để:

1. **Render charts**:
   - Combo chart: revenue, profit, cost theo ngày/tuần/tháng
   - Pie chart: success/fail orders
   - Bar chart: KPI nhân viên

2. **Bảng dữ liệu**:
   - Bảng orders ưu tiên: sắp xếp theo `priority_score`, color code theo `priority_level`
   - Bảng nhân viên: hiển thị KPI, completion rate

3. **Filter**:
   - Filter tuần/tháng/năm: xử lý trên frontend từ `daily_summary` JSON
   - Query API với `start_date`/`end_date` khi cần refresh data

## Authentication

Tất cả endpoints yêu cầu authentication:
```python
permission_classes = [IsAuthenticated]
```

**Request Header**:
```
Authorization: Bearer <access_token>
```

hoặc
```
Authorization: Token <token>
```

## Error Handling

**400 Bad Request**:
```json
{
  "error": "Invalid date format: ..."
}
```

**500 Internal Server Error**:
```json
{
  "error": "Error message..."
}
```

## Files Structure

```
backend/hr/
├── services/
│   ├── __init__.py
│   └── dashboard_service.py       # Business logic & calculations
├── serializers/
│   └── dashboard.py               # JSON serializers
├── views/
│   └── dashboard.py               # API endpoints
└── urls.py                        # URL routing
```

## Testing

Để test API:

```bash
# Start Django server
cd backend
python manage.py runserver

# Test endpoints
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/v1/dashboard/overview

curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/v1/dashboard/priority-orders?limit=10

curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/v1/dashboard/employee-kpi

curl -H "Authorization: Bearer <token>" \
  "http://localhost:8000/api/v1/dashboard/daily-summary?start_date=2025-11-01&end_date=2025-11-21"

curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/v1/dashboard/full
```

## Next Steps

1. **Frontend Integration**:
   - Update `dashboardService.js` để gọi các endpoints mới
   - Thay thế logic tính toán client-side bằng API calls
   - Giữ lại filter/render logic trên frontend

2. **Caching** (optional):
   - Cache overview data (1-5 phút)
   - Cache employee KPI (10-15 phút)
   - Real-time cho priority orders

3. **Pagination** (nếu cần):
   - Thêm pagination cho employee KPI nếu có nhiều nhân viên
   - Thêm pagination cho daily summary khi query range lớn

## Performance Notes

- Giới hạn pageSize để tránh query quá lớn
- Dùng `select_related()` để optimize queries
- Index các trường hay query: `created_at`, `status`, `preferred_start_time`
- Consider caching cho data ít thay đổi (overview, employee KPI)
