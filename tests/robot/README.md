# Robot Framework Test Suite - DSS Task Allocation

Thư mục này chứa các test cases tự động sử dụng Robot Framework để kiểm thử ứng dụng DSS Task Allocation.

## Cấu trúc thư mục

```
tests/robot/
├── requirements.txt              # Dependencies cho Robot Framework
├── README.md                     # File này
├── resources/                    # Shared resources
│   ├── common.robot             # Biến chung và config
│   └── create_order_keywords.robot  # Custom keywords
└── create_order/                # Test suite cho tạo đơn hàng
    └── negative_test_cases.robot    # Negative test cases
```

## Cài đặt

### 1. Cài đặt Python dependencies

```bash
pip install -r tests/robot/requirements.txt
```

### 2. Cài đặt WebDriver

Robot Framework sẽ tự động quản lý WebDriver thông qua webdriver-manager, hoặc bạn có thể cài đặt thủ công:

- **Chrome**: [ChromeDriver](https://chromedriver.chromium.org/)
- **Firefox**: [GeckoDriver](https://github.com/mozilla/geckodriver/releases)
- **Edge**: [EdgeDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)

## Chạy Tests

### Chạy tất cả test cases

```bash
cd tests/robot
robot create_order/negative_test_cases.robot
```

### Chạy test cases theo tag

```bash
# Chạy chỉ negative tests
robot --include negative create_order/negative_test_cases.robot

# Chạy test cases cho field Service
robot --include service create_order/negative_test_cases.robot

# Chạy test cases cho field Area
robot --include area create_order/negative_test_cases.robot

# Chạy test cases cho field Time
robot --include starttime OR endtime create_order/negative_test_cases.robot

# Chạy test cases cho field Note
robot --include note create_order/negative_test_cases.robot

# Chạy boundary value tests
robot --include boundary create_order/negative_test_cases.robot
```

### Chạy test case cụ thể

```bash
robot --test "TC_AREA_003 - Nhập diện tích âm" create_order/negative_test_cases.robot
```

### Options hữu ích

```bash
# Chạy với browser khác
robot --variable BROWSER:Firefox create_order/negative_test_cases.robot

# Chạy với base URL khác
robot --variable BASE_URL:http://staging.example.com create_order/negative_test_cases.robot

# Tạo report với tên tùy chỉnh
robot --outputdir results --name CreateOrderTests create_order/negative_test_cases.robot

# Chạy với log level debug
robot --loglevel DEBUG create_order/negative_test_cases.robot

# Chạy trong chế độ headless (không mở browser)
robot --variable BROWSER:headlesschrome create_order/negative_test_cases.robot
```

## Test Cases Overview

### 📋 Danh sách Test Cases (45 test cases)

#### **1. Dịch vụ (Service Type)** - 2 TCs

- TC_SERVICE_001: Không chọn dịch vụ ❌
- TC_SERVICE_002: Kiểm tra list dịch vụ từ hệ thống ✅

#### **2. Tiền (Price)** - 4 TCs

- TC_PRICE_001: Tự động tính giá Regular Cleaning ✅
- TC_PRICE_002: Tự động tính giá Deep Cleaning ✅
- TC_PRICE_003: Tính tổng tiền với VAT 10% ✅
- TC_PRICE_004: Áp dụng hệ số phạt ✅

#### **3. Thời gian bắt đầu (Start Time)** - 4 TCs

- TC_STARTTIME_001: Không nhập thời gian bắt đầu ❌
- TC_STARTTIME_002: Thời gian < 1 tiếng (59 phút) ❌
- TC_STARTTIME_003: Thời gian = 1 tiếng (boundary) ✅
- TC_STARTTIME_004: Thời gian trong quá khứ ❌

#### **4. Thời gian kết thúc (End Time)** - 5 TCs

- TC_ENDTIME_001: Không nhập thời gian kết thúc ❌
- TC_ENDTIME_002: End time = Start time ❌
- TC_ENDTIME_003: End time < Start time ❌
- TC_ENDTIME_004: End time = Start + 1 phút (boundary) ✅
- TC_ENDTIME_005: Thời gian < 60% estimated ❌

#### **5. Diện tích (Area)** - 9 TCs

- TC_AREA_001: Không nhập diện tích ❌
- TC_AREA_002: Diện tích = 0 ❌
- TC_AREA_003: Diện tích âm ❌
- TC_AREA_004: Nhập text thay vì số ❌
- TC_AREA_005: Nhập ký tự đặc biệt ❌
- TC_AREA_006: Diện tích rất lớn (boundary) ⚠️
- TC_AREA_007: Diện tích nhỏ nhất 0.01 (boundary) ✅
- TC_AREA_008: Diện tích số thập phân ✅
- TC_AREA_009: Nhiều dấu chấm ❌

#### **6. Ghi chú (Note)** - 6 TCs

- TC_NOTE_001: Không nhập ghi chú (optional) ✅
- TC_NOTE_002: Đúng 50 từ (boundary) ✅
- TC_NOTE_003: 51 từ (vượt quá) ❌
- TC_NOTE_004: 100 từ ❌
- TC_NOTE_005: Ký tự đặc biệt & emoji ✅
- TC_NOTE_006: Chỉ có khoảng trắng ⚠️

#### **7. Tổng hợp (Combined)** - 4 TCs

- TC_COMBINED_001: Tất cả trống ❌
- TC_COMBINED_002: Happy path (tất cả hợp lệ) ✅
- TC_COMBINED_003: Nhiều lỗi cùng lúc ❌
- TC_COMBINED_004: Button disable khi invalid ❌

**Tổng cộng: 34 test cases** covering:

- ✅ 11 positive tests (happy path)
- ❌ 20 negative tests (validation errors)
- ⚠️ 3 edge cases

## Kết quả Test

Sau khi chạy xong, Robot Framework sẽ tạo ra:

```
tests/robot/
├── log.html          # Chi tiết từng bước test
├── report.html       # Tổng quan kết quả test
└── output.xml        # Output dạng XML
```

Mở `report.html` trong browser để xem kết quả chi tiết.

## Configuration

### Thay đổi Base URL

Sửa trong file `resources/common.robot`:

```robot
${BASE_URL}    http://your-domain.com
```

Hoặc override khi chạy:

```bash
robot --variable BASE_URL:http://localhost:3001 create_order/
```

### Thay đổi Browser

Sửa trong `resources/common.robot` hoặc override:

```bash
robot --variable BROWSER:Firefox create_order/
```

Các browser được hỗ trợ:

- Chrome (mặc định)
- Firefox
- Edge
- Safari
- headlesschrome
- headlessfirefox

## Troubleshooting

### Lỗi: WebDriver not found

```bash
pip install --upgrade webdriver-manager
```

### Lỗi: Browser không mở được

Kiểm tra browser đã được cài đặt và WebDriver tương thích:

```bash
# Kiểm tra Chrome version
chrome --version

# Cài đặt ChromeDriver tương thích
pip install webdriver-manager
```

### Lỗi: Element not found

- Tăng timeout: Sửa `${TIMEOUT_MEDIUM}` trong `common.robot`
- Kiểm tra selector: Có thể UI đã thay đổi
- Kiểm tra trang đã load xong: Thêm `Wait Until Page Contains Element`

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Robot Framework Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: |
          pip install -r tests/robot/requirements.txt

      - name: Run tests
        run: |
          cd tests/robot
          robot --variable BROWSER:headlesschrome create_order/

      - name: Upload results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: robot-results
          path: tests/robot/*.html
```

## Best Practices

1. **Tổ chức test cases**: Group theo feature/module
2. **Sử dụng tags**: Để dễ dàng filter và chạy selective tests
3. **Custom keywords**: Tái sử dụng logic chung trong keywords
4. **Data-driven testing**: Sử dụng template tests cho các test case tương tự
5. **Wait strategies**: Sử dụng explicit waits thay vì sleep cố định
6. **Screenshots**: Tự động capture khi test fail

## Contributing

Khi thêm test cases mới:

1. Đặt tên test case theo format: `TC_FEATURE_XXX - Mô tả ngắn gọn`
2. Thêm tags phù hợp: `[Tags] negative area validation`
3. Viết documentation rõ ràng
4. Update README này

## License

MIT

## Contact

- **Project**: DSS Task Allocation
- **Testing Framework**: Robot Framework v6.1.1
- **Last Updated**: November 2025
