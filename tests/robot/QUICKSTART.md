# Quick Start Guide - Robot Framework Tests

## Cài đặt nhanh

```powershell
# 1. Di chuyển vào thư mục tests
cd tests\robot

# 2. Cài đặt dependencies
pip install -r requirements.txt

# 3. Chạy tests
robot create_order\negative_test_cases.robot
```

## Chạy từng loại test

```powershell
# Test validation Dịch vụ (2 tests)
robot --include service create_order\negative_test_cases.robot

# Test tính Tiền tự động (4 tests)
robot --include price create_order\negative_test_cases.robot

# Test Thời gian bắt đầu (4 tests)
robot --include starttime create_order\negative_test_cases.robot

# Test Thời gian kết thúc (5 tests)
robot --include endtime create_order\negative_test_cases.robot

# Test Diện tích (9 tests)
robot --include area create_order\negative_test_cases.robot

# Test Ghi chú (6 tests)
robot --include note create_order\negative_test_cases.robot

# Test tổng hợp (4 tests)
robot --include combined create_order\negative_test_cases.robot
```

## Test Cases Summary

### 🔴 **NEGATIVE TEST CASES** (20 cases)

| Field                  | Test Case                     | Expected           |
| ---------------------- | ----------------------------- | ------------------ |
| **Dịch vụ**            | Không chọn dịch vụ            | ❌ Error           |
| **Thời gian bắt đầu**  | Không nhập                    | ❌ Error           |
|                        | < 1 tiếng từ hiện tại         | ❌ Error           |
|                        | Trong quá khứ                 | ❌ Error           |
| **Thời gian kết thúc** | Không nhập                    | ❌ Error           |
|                        | = Thời gian bắt đầu           | ❌ Error           |
|                        | < Thời gian bắt đầu           | ❌ Error           |
|                        | Tạo thời gian < 60% estimated | ❌ Error           |
| **Diện tích**          | Không nhập                    | ❌ Error           |
|                        | = 0                           | ❌ Error           |
|                        | Số âm                         | ❌ Error           |
|                        | Nhập text                     | ❌ Rejected        |
|                        | Ký tự đặc biệt                | ❌ Rejected        |
|                        | Nhiều dấu chấm                | ❌ Error           |
| **Ghi chú**            | 51 từ                         | ❌ Error           |
|                        | 100 từ                        | ❌ Error           |
| **Combined**           | Tất cả trống                  | ❌ Multiple errors |
|                        | Nhiều lỗi cùng lúc            | ❌ Multiple errors |
|                        | Button disabled khi invalid   | ❌ Disabled        |

### 🟢 **POSITIVE/BOUNDARY TEST CASES** (14 cases)

| Field                  | Test Case                   | Expected          |
| ---------------------- | --------------------------- | ----------------- |
| **Dịch vụ**            | Load list từ hệ thống       | ✅ List displayed |
| **Tiền**               | Auto-gen Regular Cleaning   | ✅ Calculated     |
|                        | Auto-gen Deep Cleaning      | ✅ Calculated     |
|                        | Tính với VAT 10%            | ✅ Correct total  |
|                        | Áp dụng hệ số phạt          | ✅ Factor applied |
| **Thời gian bắt đầu**  | Đúng 1 tiếng sau (boundary) | ✅ Valid          |
| **Thời gian kết thúc** | Start + 1 phút (boundary)   | ✅ Valid          |
| **Diện tích**          | 0.01 (min boundary)         | ✅ Valid          |
|                        | Số thập phân                | ✅ Valid          |
|                        | Số rất lớn                  | ⚠️ Check behavior |
| **Ghi chú**            | Không nhập (optional)       | ✅ Valid          |
|                        | Đúng 50 từ (boundary)       | ✅ Valid          |
|                        | Ký tự đặc biệt + emoji      | ✅ Valid          |
| **Combined**           | Happy path - tất cả hợp lệ  | ✅ Success        |

**TỔNG: 34 test cases**

## Xem kết quả

Sau khi chạy xong, mở file:

```
tests\robot\report.html
```

## Config

Sửa URL trong `resources\common.robot`:

```robot
${BASE_URL}    http://localhost:3000
```

Hoặc override khi chạy:

```powershell
robot --variable BASE_URL:http://localhost:3001 create_order\negative_test_cases.robot
```

## Tags Reference

| Tag           | Description               | Count |
| ------------- | ------------------------- | ----- |
| `negative`    | Negative test cases       | 20    |
| `positive`    | Positive test cases       | 11    |
| `required`    | Required field validation | 5     |
| `validation`  | Data validation           | 15    |
| `boundary`    | Boundary value tests      | 7     |
| `calculation` | Price/time calculations   | 4     |
| `service`     | Service type tests        | 2     |
| `price`       | Price tests               | 4     |
| `starttime`   | Start time tests          | 4     |
| `endtime`     | End time tests            | 5     |
| `area`        | Area tests                | 9     |
| `note`        | Note tests                | 6     |
| `combined`    | Combined field tests      | 4     |
