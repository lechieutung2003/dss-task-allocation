# Payment WebSocket - Hướng dẫn Frontend Integration

## 🎯 Tổng quan

Hệ thống Payment WebSocket cho phép frontend nhận **real-time updates** về trạng thái thanh toán.

**Luồng thanh toán:**

1. User tạo đơn với `payment_method: "BANK_TRANSFER"` → Backend tự động tạo Payment + PayOS link
2. Frontend hiện màn hình thanh toán (QR code, thông tin chuyển khoản)
3. User chuyển khoản xong → Bấm "Đã chuyển khoản"
4. Frontend chuyển sang màn hình **Pending Checking** → **KẾT NỐI WEBSOCKET Ở ĐÂY**
5. WebSocket tự động nhận event `payment.success` khi thanh toán thành công
6. Tự động chuyển màn hình thành công

---

## 🖥️ Backend - Setup & Khởi động Server

### **Bước 1: Cài đặt thư viện (Lần đầu tiên)**

```powershell
# Di chuyển vào thư mục backend
cd D:\Cours\5\Android\cleanzy_app\erp\backend
# Cài đặt tất cả dependencies (bao gồm Django Channels, Redis, Daphne)
pip install -r requirements/base.txt
# Hoặc cài riêng từng package WebSocket:
pip install channels==4.0.0 channels-redis==4.2.0 redis==5.0.1 daphne==4.1.0
```

**✅ Thư viện WebSocket đã có sẵn trong `requirements/base.txt`:**

- `channels==4.0.0` - Django Channels (WebSocket support)
- `channels-redis==4.2.0` - Redis backend cho Channels
- `redis==5.0.1` - Python Redis client
- `daphne==4.1.0` - ASGI server (chạy WebSocket)

---

### **Bước 2: Khởi động Redis (Docker)**

```powershell
# Check Redis đang chạy chưa
docker ps | findstr redis
# Nếu chưa chạy, start Redis container
docker-compose up -d redis
```

**⚠️ LƯU Ý:** Backend đang dùng port **6382** (không phải 6379)

---

### **Bước 3: Chạy Server với Daphne**

**QUAN TRỌNG: Phải chạy bằng Daphne để có WebSocket!**

```powershell
# Di chuyển vào thư mục backend (nếu chưa)
cd D:\Cours\5\Android\cleanzy_app\erp\backend
# Chạy server bằng Daphne (ASGI server - support WebSocket)
daphne -b 0.0.0.0 -p 8008 core.asgi:application
# Hoặc dùng script ngắn gọn:
python -m daphne -b 0.0.0.0 -p 8008 core.asgi:application
```

**✅ Server đã sẵn sàng khi thấy:**

```
2025-11-13 10:00:00 INFO     Starting server at tcp:port=8008:interface=0.0.0.0
2025-11-13 10:00:00 INFO     HTTP/2 support enabled
2025-11-13 10:00:00 INFO     Configuring endpoint tcp:port=8008:interface=0.0.0.0
```

**⚠️ KHÔNG dùng `python manage.py runserver` - không support WebSocket đầy đủ!**

---

### **Bước 4: Test Redis Connection (Optional)**

```powershell
# Test Redis có hoạt động không
python test_redis.py
# Output nên thấy:
# ✅ Redis connection successful!
# ✅ Set test: True
# ✅ Get test: test_value
```

---

### **📦 Tóm Tắt Lệnh Setup Nhanh:**

```powershell
# 1. Cài đặt dependencies
cd D:\Cours\5\Android\cleanzy_app\erp\backend
pip install -r requirements/base.txt
# 2. Start Redis
docker start redis
# (Hoặc: docker run -d -p 6382:6379 --name redis redis:latest)
# 3. Chạy server
daphne -b 0.0.0.0 -p 8008 core.asgi:application
# ✅ Server ready at: http://127.0.0.1:8008
# ✅ WebSocket ready at: ws://127.0.0.1:8008/ws/payments/{order_id}/
```

---

## 📋 Backend Status (ĐÃ HOÀN THÀNH ✅)

- ✅ Django Channels, Redis, Daphne đã cài đặt
- ✅ WebSocket Consumer đã tạo (`payments/consumers.py`)
- ✅ Event Publisher đã tích hợp vào Payment Model
- ✅ API `GET /api/v1/payments/status/{order_code}/` tự động update DB khi check PayOS
- ✅ Payment.save() tự động gửi WebSocket events

**Backend endpoints:**

- `POST /api/v1/orders/` - Tạo đơn (tự động tạo Payment nếu BANK_TRANSFER)
- `GET /api/v1/payments/status/{order_code}/` - Check status từ PayOS
- `ws://YOUR_BACKEND/ws/payments/{order_id}/` - WebSocket endpoint

---

## � FRONTEND IMPLEMENTATION - HƯỚNG DẪN CHI TIẾT

### **🔴 QUAN TRỌNG: Khi nào cần WebSocket?**

**KHÔNG cần WebSocket:**

- ❌ Màn hình tạo đơn hàng
- ❌ Màn hình hiện QR code, thông tin chuyển khoản (PaymentScreen)

**CẦN WebSocket:**

- ✅ **Màn hình Pending Checking** (sau khi user bấm "Đã chuyển khoản")

---

## 🎬 LUỒNG THANH TOÁN HOÀN CHỈNH

### **Bước 1: Tạo Đơn Hàng**

```typescript
// Frontend gọi API tạo đơn
const response = await fetch("http://YOUR_BACKEND/api/v1/orders/", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    service_type: "service-uuid",
    area_m2: 50,
    requested_hours: 3,
    payment_method: "BANK_TRANSFER", // ← Quan trọng!
    // ...
  }),
});

const order = await response.json();

// Response example:
// {
//   "id": "order-uuid",
//   "status": "PENDING_PAYMENT",
//   "payment": {
//     "payment_id": "payment-uuid",
//     "payment_url": "https://pay.payos.vn/web/...",
//     "qr_code": "00020101021238590010...",
//     "order_code": 1763008300349,
//     "account_number": "V3CAS5601709898",
//     "account_name": "MAI LE HONG PHUC",
//     "amount": 10000.0,
//     "status": "PENDING",
//     "transfer_content": "DH1763008300349"
//   }
// }
```

---

### **Bước 2: Màn Hình Thanh Toán (PaymentScreen)**

```typescript
// PaymentScreen.tsx - Hiện QR code, thông tin chuyển khoản
import React from "react";
import { View, Text, Button, Linking } from "react-native";

function PaymentScreen({ route, navigation }) {
  const { order_id, payment } = route.params;
  const {
    payment_id,
    payment_url,
    qr_code,
    order_code,
    amount,
    account_number,
    account_name,
    transfer_content,
  } = payment;

  const handlePaymentConfirm = () => {
    // User bấm "Đã chuyển khoản"
    // → Chuyển qua màn hình Pending (CÓ WebSocket)
    navigation.navigate("PaymentPendingScreen", {
      order_id,
      payment_id,
      order_code,
      amount,
    });
  };

  return (
    <View style={{ padding: 20 }}>
      <Text style={{ fontSize: 24, fontWeight: "bold" }}>Thanh Toán</Text>

      {/* QR Code */}
      <QRCode value={qr_code} size={200} />

      {/* Thông tin chuyển khoản */}
      <View style={{ marginTop: 20 }}>
        <Text>Số tiền: {amount.toLocaleString()} VNĐ</Text>
        <Text>Số tài khoản: {account_number}</Text>
        <Text>Tên: {account_name}</Text>
        <Text>Nội dung: {transfer_content}</Text>
      </View>

      {/* Buttons */}
      <Button
        title="Mở Trang PayOS"
        onPress={() => Linking.openURL(payment_url)}
      />

      <Button
        title="Đã Chuyển Khoản"
        onPress={handlePaymentConfirm}
        color="green"
      />
    </View>
  );
}
```

---

### **Bước 3: Màn Hình Pending - KẾT NỐI WEBSOCKET ✅**

```typescript
// PaymentPendingScreen.tsx - ĐÂY LÀ MÀN HÌNH QUAN TRỌNG NHẤT
import React, { useEffect, useState, useRef } from "react";
import { View, Text, ActivityIndicator, StyleSheet } from "react-native";

function PaymentPendingScreen({ route, navigation }) {
  const { order_id, payment_id, order_code, amount } = route.params;

  const [status, setStatus] = useState("PENDING");
  const [message, setMessage] = useState("Đang kiểm tra thanh toán...");

  const wsRef = useRef(null);
  const pollingIntervalRef = useRef(null);

  useEffect(() => {
    // ============================================
    // 1. KẾT NỐI WEBSOCKET (Nhận event real-time)
    // ============================================
    const BACKEND_URL = "ws://127.0.0.1:8008"; // ← THAY ĐỔI URL NÀY
    const ws = new WebSocket(`${BACKEND_URL}/ws/payments/${order_id}/`);
    wsRef.current = ws;

    ws.onopen = () => {
      console.log("✅ WebSocket connected");
      setMessage("Đã kết nối, đang chờ xác nhận từ ngân hàng...");
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log("📨 WebSocket event:", data);

      // EVENT: payment.success - THANH TOÁN THÀNH CÔNG
      if (data.type === "payment.success") {
        console.log("🎉 Payment successful!");
        setStatus("PAID");
        setMessage("✅ Thanh toán thành công!");

        // Dừng polling
        if (pollingIntervalRef.current) {
          clearInterval(pollingIntervalRef.current);
        }

        // Tự động chuyển màn hình sau 2 giây
        setTimeout(() => {
          navigation.replace("OrderSuccess", {
            order_id,
            payment_data: data.data,
          });
        }, 2000);
      }

      // EVENT: payment.cancelled - THANH TOÁN BỊ HỦY
      if (data.type === "payment.cancelled") {
        console.log("❌ Payment cancelled");
        setStatus("CANCELLED");
        setMessage("❌ Thanh toán đã bị hủy");

        if (pollingIntervalRef.current) {
          clearInterval(pollingIntervalRef.current);
        }
      }
    };

    ws.onerror = (error) => {
      console.error("❌ WebSocket error:", error);
      setMessage("⚠️ Lỗi kết nối, vẫn đang kiểm tra...");
    };

    ws.onclose = () => {
      console.log("�🔌 WebSocket disconnected");
    };

    // ============================================
    // 2. POLLING TỰ ĐỘNG (Trigger backend check PayOS)
    // ============================================
    const BACKEND_API_URL = "http://127.0.0.1:8008"; // ← THAY ĐỔI URL NÀY

    const startPolling = () => {
      pollingIntervalRef.current = setInterval(async () => {
        try {
          console.log("🔄 Polling: Checking payment status...");

          // Gọi API check status (Backend sẽ tự động update DB)
          const response = await fetch(
            `${BACKEND_API_URL}/api/v1/payments/status/${order_code}/`
          );
          const data = await response.json();

          console.log("📊 Status:", data.status, "Updated:", data.updated);

          // Backend đã tự động update DB nếu status thay đổi
          // → WebSocket event sẽ được gửi tự động
          // → Không cần xử lý response ở đây

          // Dừng polling khi đã hoàn tất
          if (data.status === "PAID" || data.status === "CANCELLED") {
            if (pollingIntervalRef.current) {
              clearInterval(pollingIntervalRef.current);
              console.log("⏹️ Polling stopped");
            }
          }
        } catch (error) {
          console.error("❌ Polling error:", error);
        }
      }, 5000); // Mỗi 5 giây check 1 lần
    };

    startPolling();

    // ============================================
    // 3. CLEANUP KHI UNMOUNT
    // ============================================
    return () => {
      console.log("🧹 Cleanup: Closing WebSocket and polling");
      if (wsRef.current) {
        wsRef.current.close();
      }
      if (pollingIntervalRef.current) {
        clearInterval(pollingIntervalRef.current);
      }
    };
  }, [order_id, order_code, navigation]);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Đang Kiểm Tra Thanh Toán</Text>

      <View style={styles.amountContainer}>
        <Text style={styles.amountLabel}>Số tiền:</Text>
        <Text style={styles.amount}>{amount?.toLocaleString("vi-VN")} VNĐ</Text>
      </View>

      {status === "PENDING" && (
        <>
          <ActivityIndicator size="large" color="#0066FF" />
          <Text style={styles.message}>{message}</Text>
          <Text style={styles.info}>🔄 Tự động kiểm tra mỗi 5 giây</Text>
          <Text style={styles.info}>⚡ Cập nhật real-time qua WebSocket</Text>
        </>
      )}

      {status === "PAID" && (
        <View style={styles.successContainer}>
          <Text style={styles.successIcon}>✅</Text>
          <Text style={styles.successText}>Thanh toán thành công!</Text>
        </View>
      )}

      {status === "CANCELLED" && (
        <View style={styles.errorContainer}>
          <Text style={styles.errorIcon}>❌</Text>
          <Text style={styles.errorText}>Thanh toán đã hủy</Text>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: "#fff",
    justifyContent: "center",
    alignItems: "center",
  },
  title: {
    fontSize: 24,
    fontWeight: "bold",
    marginBottom: 30,
  },
  amountContainer: {
    marginBottom: 30,
    alignItems: "center",
  },
  amountLabel: {
    fontSize: 16,
    color: "#666",
  },
  amount: {
    fontSize: 32,
    fontWeight: "bold",
    color: "#0066FF",
    marginTop: 5,
  },
  message: {
    fontSize: 16,
    color: "#666",
    marginTop: 20,
    textAlign: "center",
  },
  info: {
    fontSize: 14,
    color: "#999",
    marginTop: 10,
  },
  successContainer: {
    alignItems: "center",
  },
  successIcon: {
    fontSize: 60,
  },
  successText: {
    fontSize: 20,
    color: "#00C851",
    fontWeight: "bold",
    marginTop: 10,
  },
  errorContainer: {
    alignItems: "center",
  },
  errorIcon: {
    fontSize: 60,
  },
  errorText: {
    fontSize: 20,
    color: "#FF4444",
    fontWeight: "bold",
    marginTop: 10,
  },
});

export default PaymentPendingScreen;
```
---
## 🔧 Configuration - Thay Đổi URL Backend
### **Development (Localhost):**
```typescript
const BACKEND_WS_URL = "ws://127.0.0.1:8008";
const BACKEND_API_URL = "http://127.0.0.1:8008";
```
### **Production:**
```typescript
const BACKEND_WS_URL = "wss://api.yourdomain.com"; // ← wss:// (secure)
const BACKEND_API_URL = "https://api.yourdomain.com";
```
### **React Native (Android Emulator):**
```typescript
const BACKEND_WS_URL = "ws://10.0.2.2:8008"; // 10.0.2.2 = localhost
const BACKEND_API_URL = "http://10.0.2.2:8008";
```
### **React Native (Real Device - Same WiFi):**
```typescript
const BACKEND_WS_URL = "ws://192.168.1.100:8008"; // ← IP máy backend
const BACKEND_API_URL = "http://192.168.1.100:8008";
```
---
## 📊 WebSocket Event Types
### **Frontend sẽ nhận được các event:**
#### **1. connection_established**
```json
{
  "type": "connection_established",
  "message": "You are now connected to payment updates for order xxx"
}
```
#### **2. payment.created** (Khi tạo payment mới)
```json
{
  "type": "payment.created",
  "data": {
    "order_id": "f2b1ff8a-834e-44af-ae1f-8be6ecb3756b",
    "payment_id": "0d0e1bdc-e691-4746-971c-6195bc450fea",
    "amount": 10000.0,
    "order_code": 1763008300349,
    "payment_url": "https://pay.payos.vn/web/...",
    "qr_code": "00020101021238590010...",
    "timestamp": "2025-11-13T04:31:40.341321Z"
  }
}
```
#### **3. payment.success** ✅ (Thanh toán thành công)
```json
{
  "type": "payment.success",
  "data": {
    "order_id": "f2b1ff8a-834e-44af-ae1f-8be6ecb3756b",
    "payment_id": "0d0e1bdc-e691-4746-971c-6195bc450fea",
    "amount": 10000.0,
    "transaction_id": "TXN987654321",
    "timestamp": "2025-11-13T04:35:20.123456Z"
  }
}
```
#### **4. payment.cancelled** (Thanh toán bị hủy)
```json
{
  "type": "payment.cancelled",
  "data": {
    "order_id": "f2b1ff8a-834e-44af-ae1f-8be6ecb3756b",
    "payment_id": "0d0e1bdc-e691-4746-971c-6195bc450fea",
    "timestamp": "2025-11-13T04:35:20.123456Z"
  }
}
```
---
## ⏱️ Timeline Ví Dụ
```
00:00s - User tạo đơn với BANK_TRANSFER
      → Backend: Tạo Order + Payment + gọi PayOS API
      → Response: payment_url, qr_code, order_code
      → WebSocket event: payment.created (tự động)

00:02s - Frontend: Chuyển qua PaymentScreen
      → Hiện QR code, thông tin chuyển khoản
      → User quét QR / copy thông tin

00:30s - User: Mở app ngân hàng
      → Chuyển khoản 10,000 VNĐ
      → PayOS nhận tiền ✅

01:00s - User: Bấm "Đã Chuyển Khoản"
      → Frontend: Chuyển qua PaymentPendingScreen
      → ✅ WebSocket connect
      → ✅ Polling start (mỗi 5s)

01:05s - Polling lần 1
      → Frontend: Gọi GET /api/v1/payments/status/{order_code}/
      → Backend: Gọi PayOS API → status = PAID
      → Backend: Update payment.status = PAID
      → Backend: payment.save() → 🚀 WebSocket event: payment.success

01:05s - Frontend: Nhận WebSocket event
      → Hiện "✅ Thanh toán thành công!"
      → Dừng polling
      → Sau 2s tự động chuyển OrderSuccess

01:07s - Màn hình OrderSuccess
      → Hiện thông tin đơn hàng đã thanh toán
```
---
## 🧪 Testing - Không Cần Thanh Toán Thật
### **Cách 1: Script Python (Backend)**
```python
# test_payment_events.py (Đã có sẵn)
# Chạy trong terminal backend:
cd D:\Cours\5\Android\cleanzy_app\erp\backend
python test_payment_events.py

# Chọn option "Mark payment as paid"
# → WebSocket event sẽ được gửi ngay lập tức
```
### **Cách 2: Django Shell**
```python
# Terminal backend:
python manage.py shell

# Trong shell:
from payments.models import Payment

# Tìm payment cần test
payment = Payment.objects.get(order_code=1763008300349)

# Mark as paid
payment.status = 'PAID'
payment.transaction_id = 'TEST_TXN_123'
payment.save()  # ← WebSocket event tự động gửi!

# Frontend sẽ nhận event payment.success ngay lập tức
```
---
## 🔍 Troubleshooting
### **Lỗi cài đặt thư viện:**
**Lỗi: `ERROR: Could not find a version that satisfies the requirement channels==4.0.0`**
```powershell
# Solution: Update pip trước
python -m pip install --upgrade pip

# Sau đó cài lại
pip install -r requirements/base.txt
```
**Lỗi: `ModuleNotFoundError: No module named 'channels'`**
```powershell
# Solution: Cài lại channels
pip install channels==4.0.0 channels-redis==4.2.0 redis==5.0.1 daphne==4.1.0
```
---
### **Lỗi Redis:**
**Lỗi: `redis.exceptions.ConnectionError: Error 10061`**
```powershell
# Redis chưa chạy, start Redis:
docker start redis

# Nếu chưa có container:
docker run -d -p 6382:6379 --name redis redis:latest

# Check Redis đang chạy:
docker ps | findstr redis

# Test connection:
python test_redis.py
```
**Lỗi: `ConnectionRefusedError: [WinError 10061]`**
```powershell
# Check port Redis trong settings
# File: core/settings/base.py
# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             "hosts": [('127.0.0.1', 6382)],  # ← Port 6382 (không phải 6379)
#         },
#     },
# }
```
---
### **WebSocket không connect:**
1. **Check Backend đang chạy với Daphne:**
   ```powershell
   # Phải thấy "Daphne" trong output
   daphne -b 0.0.0.0 -p 8008 core.asgi:application
   ```
2. **Check Redis đang chạy:**
   ```powershell
   docker ps | findstr redis
   ```
3. **Check URL:**
   - Development: `ws://127.0.0.1:8008` (không phải `wss://`)
   - Production: `wss://yourdomain.com` (phải có SSL)

### **Polling không hoạt động:**

1. **Check API endpoint:**

   ```bash
   curl http://127.0.0.1:8008/api/v1/payments/status/1763008300349/
   ```

2. **Check response có `updated: true` không:**
   ```json
   {
     "status": "PAID",
     "updated": true // ← Phải có field này
   }
   ```

### **WebSocket event không nhận được:**

1. **Check backend logs** (terminal chạy Daphne)
2. **Check console logs** trong frontend
3. **Test với script Python** để xem backend có gửi event không

---

## 📝 Checklist Frontend

- [ ] Tạo đơn với `payment_method: "BANK_TRANSFER"`
- [ ] Nhận response có `payment` object
- [ ] Màn hình PaymentScreen hiện QR code
- [ ] User bấm "Đã chuyển khoản" → Chuyển PaymentPendingScreen
- [ ] **PaymentPendingScreen kết nối WebSocket**
- [ ] **PaymentPendingScreen start polling mỗi 5s**
- [ ] Nhận event `payment.success` → Tự động chuyển màn hình
- [ ] Test với `test_payment_events.py` (không cần thanh toán thật)

---

## 🚀 Production Deployment

### **Backend:**

1. Cài SSL certificate
2. Dùng Nginx reverse proxy cho WebSocket
3. Cấu hình Redis Cluster (scaling)
4. Đổi `ws://` → `wss://`

### **Frontend:**

1. Đổi URL từ localhost → production domain
2. Đổi `ws://` → `wss://`
3. Handle network errors, reconnection

---

## 📞 Support

**Backend đã hoàn thành 100%!** Frontend chỉ cần:

1. Copy code `PaymentPendingScreen` từ guide này
2. Thay đổi URL backend
3. Test với `test_payment_events.py`

Hệ thống sẵn sàng! 🎉

---

## 📚 APPENDIX - Alternative Examples

### JavaScript/React Hook (Alternative Implementation)

constructor(orderId) {
this.orderId = orderId;
this.ws = null;
this.reconnectAttempts = 0;
this.maxReconnectAttempts = 5;
}

connect() {
const wsUrl = `ws://127.0.0.1:8008/ws/payments/${this.orderId}/`;

    console.log("🔌 Connecting to:", wsUrl);
    this.ws = new WebSocket(wsUrl);

    this.ws.onopen = () => {
      console.log("✅ WebSocket connected");
      this.reconnectAttempts = 0;
    };

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log("📨 Received:", data);

      this.handleMessage(data);
    };

    this.ws.onerror = (error) => {
      console.error("❌ WebSocket error:", error);
    };

    this.ws.onclose = (event) => {
      console.log("🔌 WebSocket closed:", event.code, event.reason);

      // Auto reconnect
      if (this.reconnectAttempts < this.maxReconnectAttempts) {
        this.reconnectAttempts++;
        const delay = Math.min(
          1000 * Math.pow(2, this.reconnectAttempts),
          10000
        );
        console.log(`🔄 Reconnecting in ${delay}ms...`);
        setTimeout(() => this.connect(), delay);
      }
    };

}

handleMessage(data) {
switch (data.type) {
case "connection_established":
console.log("🎉 Connected:", data.message);
break;

      case "payment_update":
        this.handlePaymentUpdate(data.event, data.data);
        break;

      case "pong":
        console.log("🏓 Pong received");
        break;

      default:
        console.log("Unknown message type:", data.type);
    }

}

handlePaymentUpdate(event, data) {
console.log(`💳 Payment Event: ${event}`, data);

    switch (event) {
      case "payment.pending":
        console.log("⏳ Payment pending...");
        // Show loading UI, QR code
        this.onPending(data);
        break;

      case "payment.success":
        console.log("🎉 Payment successful!");
        // Redirect to success page
        this.onSuccess(data);
        break;

      case "payment.failed":
        console.log("❌ Payment failed!");
        // Show error message
        this.onFailed(data);
        break;

      case "payment.cancelled":
        console.log("🚫 Payment cancelled");
        this.onCancelled(data);
        break;
    }

}

// Callback methods (override these)
onPending(data) {
// Show payment QR code
console.log("Show QR:", data.qr_code);
}

onSuccess(data) {
// Redirect to success page
window.location.href = `/orders/${data.order_id}/success`;
}

onFailed(data) {
// Show error alert
alert("Thanh toán thất bại: " + data.reason);
}

onCancelled(data) {
// Show cancelled message
alert("Thanh toán đã bị hủy");
}

// Send ping to keep connection alive
ping() {
if (this.ws && this.ws.readyState === WebSocket.OPEN) {
this.ws.send(
JSON.stringify({
type: "ping",
timestamp: new Date().toISOString(),
})
);
}
}

disconnect() {
if (this.ws) {
this.ws.close();
this.ws = null;
}
}
}

// Usage
const orderId = "your-order-uuid";
const paymentWS = new PaymentWebSocket(orderId);

// Connect
paymentWS.connect();

// Keep alive (ping every 30s)
setInterval(() => paymentWS.ping(), 30000);

// Cleanup on page unload
window.addEventListener("beforeunload", () => {
paymentWS.disconnect();
});

```
---
**⚠️ LƯU Ý:** Code trên chỉ là ví dụ tham khảo. **KHUYẾN NGHỊ sử dụng code `PaymentPendingScreen` ở phần chính** vì đã tối ưu cho React Native và có đầy đủ xử lý lỗi.
```