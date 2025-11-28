<template>
  <div class="about-page">
    <section class="stripe white">
      <div class="container payment-container">
        <!-- Loading state -->
        <div v-if="loading" class="loading-state">
          <div class="loading-spinner"></div>
          <p>{{ t("payment_loading") }}</p>
        </div>

        <!-- Error state -->
          <div v-else-if="error" class="error-state">
          <div class="error-icon">❌</div>
          <h2>{{ t("payment_error_title") }}</h2>
          <p class="error-message">{{ error }}</p>
          <router-link to="/dss/customer-orders" class="btn-back">
            {{ t("back_to_orders") }}
          </router-link>
        </div>

        <!-- Payment info -->
        <div v-else-if="orderData" class="payment-content">
          <div class="ticket-layout">
            <!-- LEFT: Ticket details (pink card) -->
            <div class="ticket-left">
              <div class="ticket-header">
                <h1 class="ticket-title">{{ t("payment_title") }}</h1>
                <p class="ticket-subtitle">{{ t("payment_subtitle") }}</p>
                <div class="price-tag">{{ formatPrice(orderData.cost_confirm) }}</div>
              </div>

              <div v-if="orderData.payment" class="ticket-body">
                <div class="info-section">
                  <div class="info-icon">📅</div>
                  <div class="info-text">
                    <span class="info-label">{{ formatDateTime(orderData.preferred_start_time) }}</span>
                  </div>
                </div>

                <div class="info-section">
                  <div class="info-icon">📍</div>
                  <div class="info-text">
                    <span class="info-label">{{ orderData.service_details?.name || '' }}</span>
                  </div>
                </div>

                <div class="bank-info-section">
                  <div class="bank-detail">
                    <span class="bank-label">{{ t("payment_bank_name") }}</span>
                    <span class="bank-value">{{ orderData.payment.bank_name }}</span>
                  </div>
                  <div class="bank-detail">
                    <span class="bank-label">{{ t("payment_account_number") }}</span>
                    <div class="bank-value-row">
                      <span class="bank-value mono">{{ orderData.payment.account_number }}</span>
                      <button @click="copyToClipboard(orderData.payment.account_number)" class="copy-btn-mini">📋</button>
                    </div>
                  </div>
                  <div class="bank-detail">
                    <span class="bank-label">{{ t("payment_account_name") }}</span>
                    <span class="bank-value">{{ orderData.payment.account_name }}</span>
                  </div>
                </div>

                <div class="transfer-info-section">
                  <div class="transfer-content-box">
                    <span class="transfer-label">{{ t("payment_transfer_content") }}</span>
                    <div class="transfer-value-row">
                      <span class="transfer-value mono">{{ orderData.payment.transfer_content }}</span>
                      <button @click="copyToClipboard(orderData.payment.transfer_content)" class="copy-btn-mini">📋</button>
                    </div>
                  </div>
                </div>

                <div class="action-buttons-row">
                  <button @click="checkPaymentStatus" :disabled="checkingPayment || paymentConfirmed" class="btn-action primary">
                    <span v-if="checkingPayment">{{ t("payment_checking") }}</span>
                    <span v-else-if="paymentConfirmed">{{ t("payment_confirmed_button") }}</span>
                    <span v-else>{{ t("payment_check_button") }}</span>
                  </button>
                  <button v-if="paymentConfirmed" @click="viewInvoice" class="btn-action secondary">{{ t("payment_view_invoice") }}</button>
                </div>

                <div class="bottom-info">
                  <div class="area-info">{{ t("payment_area") }}: {{ orderData.area_m2 }} m²</div>
                </div>
              </div>
            </div>

            <!-- RIGHT: QR card (coral gradient) -->
            <div class="ticket-right">
              <div class="qr-card-coral">
                <div class="qr-wrapper-white">
                  <img v-if="qrCodeDataUrl" :src="qrCodeDataUrl" alt="QR Code" class="qr-image" />
                  <div v-else class="qr-placeholder">
                    <div class="loading-spinner small"></div>
                    <p>{{ t("payment_qr_loading") }}</p>
                  </div>
                </div>

                <div class="qr-footer">
                  <div class="qr-name-white">{{ orderData?.service_details?.name || 'Your name here' }}</div>
                  <div class="qr-meta-row">
                    <span>Gate 05</span>
                    <span>Row 02</span>
                    <span>Seat 13</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Toast Notification -->
    <div v-if="showToast" :class="['toast-notification', toastType]">
      {{ toastMessage }}
    </div>

    <!-- Invoice Modal -->
    <div
      v-if="showInvoiceModal && selectedInvoice"
      class="modal-overlay"
      @click="closeInvoiceModal"
    >
      <div class="modal-content invoice-modal" @click.stop>
        <div class="modal-header">
          <h2>{{ t("invoice_title") }}</h2>
          <button class="close-btn" @click="closeInvoiceModal">×</button>
        </div>

        <div class="modal-body">
          <div class="invoice-header">
            <div class="invoice-title">{{ t("invoice_header_title") }}</div>
            <div class="invoice-number">
              {{
                t("invoice_number", { number: selectedInvoice.invoiceNumber })
              }}
            </div>
          </div>

          <div class="invoice-section">
            <h4>{{ t("invoice_service_details") }}</h4>
            <div class="service-details">
              <div class="info-row">
                <span>{{ t("invoice_service") }}</span>
                <span>{{ selectedInvoice.orderInfo.serviceName }}</span>
              </div>
              <div class="info-row">
                <span>{{ t("invoice_area") }}</span>
                <span>{{ selectedInvoice.orderInfo.area }} m²</span>
              </div>
              <div class="info-row">
                <span>{{ t("invoice_start_time") }}</span>
                <span>{{
                  formatDateTime(selectedInvoice.orderInfo.startTime)
                }}</span>
              </div>
              <div class="info-row">
                <span>{{ t("invoice_end_time") }}</span>
                <span>{{
                  formatDateTime(selectedInvoice.orderInfo.endTime)
                }}</span>
              </div>
              <div class="info-row">
                <span>{{ t("invoice_payment_method") }}</span>
                <span>{{ selectedInvoice.orderInfo.paymentMethod }}</span>
              </div>
            </div>
          </div>

          <div class="invoice-section">
            <h4>{{ t("invoice_payment_title") }}</h4>
            <div class="pricing-details">
              <div class="info-row">
                <span>{{ t("invoice_subtotal") }}</span>
                <span>{{ selectedInvoice.pricing.subtotal.toLocaleString("vi-VN") }} VNĐ</span>
              </div>
              <div class="info-row">
                <span>{{ t("invoice_tax") }}</span>
                <span>{{ selectedInvoice.pricing.tax.toLocaleString("vi-VN") }} VNĐ</span>
              </div>
              <div class="total-amount">
                <span><strong>{{ t("invoice_total") }}</strong></span>
                <span class="total-price"><strong>{{ selectedInvoice.pricing.total.toLocaleString("vi-VN") }} VNĐ</strong></span>
              </div>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn-download" @click="downloadInvoice">
            {{ t("invoice_download") }}
          </button>
          <button class="btn-close-modal" @click="closeInvoiceModal">
            {{ t("invoice_close") }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import CustomerOrderService from "@/services/dss/users/customer";
import QRCode from "qrcode";
import "@/assets/css/customer.css";

// Apply role-based middleware
definePageMeta({
  middleware: "role-based",
});

const { t } = useI18n();
const route = useRoute();
const router = useRouter();

const orderId = route.params.id;
const loading = ref(true);
const error = ref("");
const orderData = ref(null);
const qrCodeDataUrl = ref("");
const checkingPayment = ref(false);
const paymentConfirmed = ref(false);

// Toast notification
const showToast = ref(false);
const toastMessage = ref("");
const toastType = ref("success");

// Invoice modal
const showInvoiceModal = ref(false);
const selectedInvoice = ref(null);

// Load order data
const loadOrderData = async () => {
  try {
    loading.value = true;
    error.value = "";

    const response = await CustomerOrderService.getOrder(orderId);
    console.log("=== PAYMENT PAGE - Order data ===");
    console.log("Full response:", response);
    console.log("Response.payment:", response?.payment);

    orderData.value = response;

    // Thử lấy payment info từ sessionStorage trước
    const storedPayment = sessionStorage.getItem(`payment_${orderId}`);
    if (storedPayment) {
      console.log("💾 Found payment info in sessionStorage");
      orderData.value.payment = JSON.parse(storedPayment);
      // Xóa sau khi đã lấy
      sessionStorage.removeItem(`payment_${orderId}`);
    }

    // Check if payment info exists
    if (!orderData.value || !orderData.value.payment) {
      console.error("No payment info found in response or sessionStorage");
      // show an error toast and redirect back to orders list
      showToastMessage(t("payment_no_info_error"), "error");
      try {
        await router.replace({ path: "/dss/customer-orders" });
      } catch (e) {
        // ignore
      }
      return;
    }

    console.log("Payment info:", orderData.value.payment);
    console.log("QR code string:", orderData.value.payment.qr_code);

    // Generate QR code từ string
    if (orderData.value.payment.qr_code) {
      try {
        qrCodeDataUrl.value = await QRCode.toDataURL(
          orderData.value.payment.qr_code,
          {
            width: 300,
            margin: 1,
            color: {
              dark: "#000000",
              light: "#FFFFFF",
            },
          }
        );
        console.log("QR code generated successfully");
      } catch (qrError) {
        console.error("Error generating QR code:", qrError);
        showToastMessage(t("payment_qr_error"), "error");
      }
    } else {
      console.warn("No QR code in payment info");
    }

    // Check if payment is already confirmed
    if (
      orderData.value.payment.status === "PAID" ||
      orderData.value.status === "confirmed"
    ) {
      paymentConfirmed.value = true;
      console.log("Payment already confirmed");
    }
  } catch (e) {
    console.error("Error loading order data:", e);
    error.value = t("payment_load_error") + ": " + e.message;
  } finally {
    loading.value = false;
  }
};

// Check payment status
const checkPaymentStatus = async () => {
  if (!orderData.value?.payment?.order_code) {
    console.error("❌ No order_code found!");
    console.log("orderData.value:", orderData.value);
    console.log("payment:", orderData.value?.payment);
    showToastMessage(t("payment_no_order_code"), "error");
    return;
  }

  try {
    checkingPayment.value = true;
    
    console.log("=== CHECKING PAYMENT STATUS ===");
    console.log("Order code:", orderData.value.payment.order_code);

    const response = await CustomerOrderService.checkPaymentStatus(
      orderData.value.payment.order_code
    );
    
    console.log("=== PAYMENT STATUS RESPONSE ===");
    console.log("Full response:", response);
    console.log("response.status:", response.status);
    console.log("response.data:", response.data);
    console.log("response.data?.status:", response.data?.status);

    if (response.status === "PAID" || response.data?.status === "PAID") {
      console.log("✅ Payment confirmed!");
      paymentConfirmed.value = true;
      showToastMessage(t("payment_success"), "success");

      // Reload order data to get updated status
      await loadOrderData();
      
      // Redirect to orders index (pending tab) instead of staying on payment page
      try {
        await router.replace({ path: "/dss/customer-orders", query: { paid: "1" } });
      } catch (e) {
        // fallback
        window.location.href = "/dss/customer-orders";
      }
    } else {
      console.log("⏳ Payment still pending");
      console.log("Current status:", response.status || response.data?.status);
      showToastMessage(t("payment_still_pending"), "info");
    }
  } catch (e) {
    console.error("❌ Error checking payment status:", e);
    console.error("Error details:", e.response?.data || e.message);
    showToastMessage(t("payment_check_error"), "error");
  } finally {
    checkingPayment.value = false;
  }
};

// View invoice
const viewInvoice = () => {
  if (!orderData.value) return;

  console.log("=== GENERATING INVOICE ===");
  console.log("orderData.value.payment_method:", orderData.value.payment_method);
  console.log("Full orderData:", orderData.value);

  const totalPrice = parseInt(orderData.value.cost_confirm) || 0;
  const subtotal = Math.round(totalPrice / 1.1);
  const tax = totalPrice - subtotal;

  // Xác định phương thức thanh toán
  let paymentMethodText;
  if (orderData.value.payment_method === "BANK_TRANSFER") {
    paymentMethodText = t("payment_bank_transfer");
  } else if (orderData.value.payment_method === "CASH") {
    paymentMethodText = t("payment_cash");
  } else {
    // Fallback: nếu có payment info thì là chuyển khoản
    paymentMethodText = orderData.value.payment 
      ? t("payment_bank_transfer") 
      : t("payment_cash");
  }

  console.log("Payment method text:", paymentMethodText);

  selectedInvoice.value = {
    invoiceNumber: orderData.value.id,
    orderInfo: {
      serviceName: orderData.value.service_details?.name || "N/A",
      area: orderData.value.area_m2,
      startTime: orderData.value.preferred_start_time,
      endTime: orderData.value.preferred_end_time,
      paymentMethod: paymentMethodText,
    },
    pricing: {
      subtotal: subtotal,
      tax: tax,
      total: totalPrice,
    },
  };

  showInvoiceModal.value = true;
};

const closeInvoiceModal = () => {
  showInvoiceModal.value = false;
  selectedInvoice.value = null;
};

const downloadInvoice = () => {
  if (!selectedInvoice.value) return;

  const invoice = selectedInvoice.value;
  const htmlContent = `
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>${t("invoice_title")} ${invoice.invoiceNumber}</title>
      <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { text-align: center; margin-bottom: 30px; background: #f8f9fa; padding: 20px; }
        .title { font-size: 24px; font-weight: bold; color: #333; }
        .invoice-number { font-size: 18px; margin: 10px 0; }
        .section { margin: 20px 0; padding: 15px; border: 1px solid #ddd; }
        .section h3 { margin: 0 0 15px 0; color: #555; }
        .row { display: flex; justify-content: space-between; margin: 8px 0; }
        .total { background: #e3f2fd; padding: 15px; font-weight: bold; font-size: 18px; }
      </style>
    </head>
    <body>
      <div class="header">
        <div class="title">${t("invoice_header_title")}</div>
        <div class="invoice-number">${t("invoice_number", {
          number: invoice.invoiceNumber,
        })}</div>
      </div>
      
      <div class="section">
        <h3>${t("invoice_service_details")}</h3>
        <div class="row"><span>${t("invoice_service")}</span><span>${
    invoice.orderInfo.serviceName
  }</span></div>
        <div class="row"><span>${t("invoice_area")}</span><span>${
    invoice.orderInfo.area
  } m²</span></div>
        <div class="row"><span>${t(
          "invoice_start_time"
        )}</span><span>${formatDateTime(
    invoice.orderInfo.startTime
  )}</span></div>
        <div class="row"><span>${t(
          "invoice_end_time"
        )}</span><span>${formatDateTime(invoice.orderInfo.endTime)}</span></div>
        <div class="row"><span>${t("invoice_payment_method")}</span><span>${
    invoice.orderInfo.paymentMethod
  }</span></div>
      </div>
      
      <div class="section">
        <h3>${t("invoice_payment_title")}</h3>
        <div class="row"><span>${t(
          "invoice_subtotal"
        )}</span><span>${invoice.pricing.subtotal.toLocaleString(
    "vi-VN"
  )} VNĐ</span></div>
        <div class="row"><span>${t(
          "invoice_tax"
        )}</span><span>${invoice.pricing.tax.toLocaleString(
    "vi-VN"
  )} VNĐ</span></div>
        <div class="total"><span>${t(
          "invoice_total"
        )}</span><span>${invoice.pricing.total.toLocaleString(
    "vi-VN"
  )} VNĐ</span></div>
      </div>
      
      <div style="text-align: center; margin-top: 30px; color: #666;">
        Cảm ơn bạn đã sử dụng dịch vụ!
      </div>
    </body>
    </html>
  `;

  const printWindow = window.open("", "_blank");
  if (printWindow) {
    printWindow.document.write(htmlContent);
    printWindow.document.close();
    printWindow.focus();
    printWindow.print();
    printWindow.onafterprint = () => printWindow.close();
  }
};

// Copy to clipboard
const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text.toString());
    showToastMessage(t("copy_success"), "success");
  } catch (error) {
    console.error("Failed to copy:", error);
    showToastMessage(t("copy_error"), "error");
  }
};

// Utility functions
const formatPrice = (price) => {
  if (!price) return "0 VNĐ";
  return new Intl.NumberFormat("vi-VN", {
    style: "currency",
    currency: "VND",
  }).format(price);
};

const formatDateTime = (datetime) => {
  return datetime ? new Date(datetime).toLocaleString("vi-VN") : "";
};

// Show toast message
const showToastMessage = (message, type = "success") => {
  toastMessage.value = message;
  toastType.value = type;
  showToast.value = true;

  setTimeout(() => {
    showToast.value = false;
  }, 3000);
};

onMounted(async () => {
  await loadOrderData();
  // If payment was already confirmed on load, redirect back to orders index
  if (paymentConfirmed.value) {
    showToastMessage(t("payment_success"), "success");
    try {
      await router.replace({ path: "/dss/customer-orders", query: { paid: "1" } });
    } catch (e) {
      window.location.href = "/dss/customer-orders";
    }
  }
});
</script>

<style scoped>
.payment-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

/* Reuse modal/create styles to align payment page appearance */
.t-card {
  background: var(--bg-card, #fff);
  border: 1px solid rgba(59, 130, 246, 0.06);
  border-radius: 12px;
  padding: 1.25rem;
  box-shadow: var(--shadow, 0 6px 18px rgba(14,30,37,0.06));
  margin-bottom: 1rem;
}

.t-card h3 {
  margin: 0 0 0.75rem;
  font-size: 1.125rem;
  color: var(--text-dark);
}

.summary-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(229,231,235,0.9);
}

.summary-item:last-child {
  border-bottom: none;
}

.payment-methods h3 {
  margin: 0 0 1rem;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-dark);
}

.radio-container {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 0.75rem;
  border: 1.5px solid #ecedec;
  border-radius: 10px;
  transition: all 0.15s;
  margin-bottom: 0.75rem;
}

.radio-container input[type="radio"] { display:none; }

.checkmark {
  width: 18px;
  height: 18px;
  border: 2px solid #d1d5db;
  border-radius: 50%;
  margin-right: 12px;
  position: relative;
}

.radio-container input[type="radio"]:checked + .checkmark {
  border-color: var(--primary, #3b82f6);
  background-color: var(--primary, #3b82f6);
}

.radio-container input[type="radio"]:checked + .checkmark::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 8px;
  height: 8px;
  background: white;
  border-radius: 50%;
}

.payment-info { flex: 1; }
.payment-title { font-weight: 600; display:flex; align-items:center; gap:0.5rem; }
.payment-desc { color: var(--text-light); font-size:0.9rem }

/* Ticket-style layout matching reference image */
.ticket-layout {
  display: flex;
  gap: 1.5rem;
  align-items: stretch;
  width: 100%;
  max-width: 1100px;
  margin: 0 auto;
  box-sizing: border-box;
}

.ticket-left {
  flex: 1 1 auto;
  background: #ccf6dc;
  border-radius: 24px;
  padding: 2rem;
  box-shadow: 0 8px 24px rgba(6,95,70,0.06);
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  color: #064e3b;
}
.ticket-header {
  border-bottom: 1px solid rgba(90, 26, 26, 0.15);
  padding-bottom: 1rem;
}

.ticket-title {
  font-size: 2.5rem;
  font-weight: 400;
  margin: 0 0 0.25rem;
  color: #000000;
  letter-spacing: -0.5px;
}

.ticket-subtitle {
  font-size: 0.9rem;
  margin: 0 0 0.75rem;
  color: rgba(90, 26, 26, 0.7);
}

.price-tag {
  font-size: 1.1rem;
  font-weight: 600;
  color: #38c348;
}

.ticket-body {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  flex: 1;
}

.info-section {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(90, 26, 26, 0.1);
}

.info-icon {
  font-size: 1.25rem;
}

.info-label {
  font-size: 0.95rem;
  color: rgba(90, 26, 26, 0.85);
}

.bank-info-section {
  background: rgba(255, 255, 255, 0.4);
  border-radius: 12px;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.bank-detail {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.bank-label {
  font-size: 0.85rem;
  color: rgba(90, 26, 26, 0.7);
  font-weight: 500;
}

.bank-value {
  font-size: 0.95rem;
  color: #5a1a1a;
  font-weight: 600;
}

.bank-value-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.mono {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, "Roboto Mono", monospace;
}

.copy-btn-mini {
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  padding: 0.25rem;
  opacity: 0.7;
  transition: opacity 0.2s;
}

.copy-btn-mini:hover {
  opacity: 1;
}

.transfer-info-section {
  background: rgba(255, 255, 255, 0.4);
  border-radius: 12px;
  padding: 1rem;
}

.transfer-content-box {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.transfer-label {
  font-size: 0.85rem;
  color: rgba(90, 26, 26, 0.7);
  font-weight: 500;
}

.transfer-value-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.transfer-value {
  font-size: 0.95rem;
  color: #5a1a1a;
  font-weight: 600;
}

.action-buttons-row {
  display: flex;
  gap: 0.75rem;
  margin-top: auto;
}

.btn-action {
  flex: 1;
  padding: 0.75rem 1.5rem;
  border-radius: 50px;
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.95rem;
}

.btn-action.primary {
  background: linear-gradient(135deg, var(--primary, #3b82f6) 0%, #2563eb 100%);
  color: white;
}

.btn-action.primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.btn-action.primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-action.secondary {
  background: rgba(255, 255, 255, 0.6);
  color: #5a1a1a;
  border: 2px solid rgba(90, 26, 26, 0.2);
}

.btn-action.secondary:hover {
  background: rgba(255, 255, 255, 0.8);
}

.bottom-info {
  padding-top: 0.75rem;
  border-top: 1px solid rgba(90, 26, 26, 0.15);
}

.area-info {
  font-size: 0.9rem;
  color: rgba(90, 26, 26, 0.7);
}

/* RIGHT: Coral gradient QR card */
.ticket-right {
  flex: 0 0 380px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.qr-card-coral {
  width: 100%;
  max-width: 360px;
  background: linear-gradient(180deg, #bff3d7 0%, #7de3b0 50%, #34d399 100%);
  border-radius: 24px;
  padding: 1.5rem;
  box-shadow: 0 12px 40px rgba(16,185,129,0.12);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  color: white;
  position: relative;
  overflow: hidden;
}

/* Subtle pattern overlay for texture */
.qr-card-coral::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: repeating-linear-gradient(
    45deg,
    transparent,
    transparent 10px,
    rgba(255, 255, 255, 0.02) 10px,
    rgba(255, 255, 255, 0.02) 20px
  );
  pointer-events: none;
}

.qr-wrapper-white {
  background: white;
  padding: 1rem;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 1;
}

.qr-image {
  width: 240px;
  height: 240px;
  display: block;
}

.qr-placeholder {
  width: 240px;
  height: 240px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  gap: 0.5rem;
}

.qr-footer {
  text-align: center;
  width: 100%;
  position: relative;
  z-index: 1;
}

.qr-name-white {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
  color: white;
}

.qr-meta-row {
  display: flex;
  justify-content: space-around;
  gap: 1rem;
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.95);
}

.qr-meta-row span {
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* Responsive */
@media (max-width: 1000px) {
  .ticket-layout {
    flex-direction: column;
    gap: 1rem;
  }
  
  .ticket-right {
    order: -1;
    width: 100%;
    flex: 0 0 auto;
  }
  
  .qr-card-coral {
    max-width: 100%;
  }
  
  .qr-image,
  .qr-placeholder {
    width: 200px;
    height: 200px;
  }
}

/* Further compress text and spacing to fit short viewports */
.payment-header.compact h1 { font-size: 1.4rem; margin: 0.25rem 0; }
.payment-header.compact .subtitle { font-size: 0.85rem; margin-bottom: 0.25rem; }
.t-card { padding: 0.75rem; }
.summary-item { padding: 0.35rem 0; }
.summary-item .label { font-size: 0.82rem; }
.summary-item .value { font-size: 0.95rem; }
.qr-instruction { font-size: 0.85rem; }
.detail-label { font-size: 0.82rem; }
.detail-value span { font-size: 0.95rem; }
.action-buttons { gap: 0.6rem; }
.btn-check-payment, .btn-view-invoice, .btn-back-orders, .btn-back { padding: 0.6rem 1rem; font-size: 0.92rem; }

/* Loading state */
.loading-state {
  text-align: center;
  padding: 60px 20px;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid var(--primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

.loading-spinner.small {
  width: 24px;
  height: 24px;
  border-width: 3px;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* Error state */
.error-state {
  text-align: center;
  padding: 60px 20px;
}

.error-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.error-state h2 {
  color: #dc3545;
  margin-bottom: 15px;
}

.error-message {
  color: #666;
  margin-bottom: 30px;
}

/* Payment Header */
.payment-header {
  text-align: center;
  margin-bottom: 2rem;
}

.header-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.payment-header h1 {
  font-size: 2rem;
  color: var(--text-dark);
  margin-bottom: 0.5rem;
}

.subtitle {
  color: var(--text-light);
  font-size: 1rem;
}

/* Order Summary */
.order-summary {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 12px;
  margin-bottom: 2rem;
  border: 1px solid #e9ecef;
}

.order-summary h3 {
  margin: 0 0 1rem;
  color: var(--text-dark);
  font-size: 1.25rem;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.summary-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.summary-item.highlight {
  grid-column: 1 / -1;
  padding-top: 1rem;
  border-top: 2px solid #dee2e6;
}

.summary-item .label {
  font-size: 0.875rem;
  color: var(--text-light);
  font-weight: 500;
}

.summary-item .value {
  font-size: 1rem;
  color: var(--text-dark);
  font-weight: 600;
}

.summary-item .amount {
  font-size: 1.5rem;
  color: var(--primary);
}

/* Payment Section */
.payment-section {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  border: 1px solid #e9ecef;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.payment-section h3 {
  margin: 0 0 1.5rem;
  color: var(--text-dark);
  font-size: 1.5rem;
  text-align: center;
}

/* Payment Grid */
.payment-grid {
  display: grid;
  grid-template-columns: 1fr 1.5fr;
  gap: 2rem;
  margin-bottom: 2rem;
}

/* QR Section */
.qr-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.qr-wrapper {
  width: 300px;
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border: 2px solid #e9ecef;
  border-radius: 12px;
  padding: 1rem;
}

.qr-code {
  max-width: 100%;
  height: auto;
}

.qr-placeholder {
  text-align: center;
  color: var(--text-light);
}

.qr-instruction {
  text-align: center;
  color: var(--text-light);
  font-size: 0.875rem;
}

/* Bank Details */
.bank-details {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.bank-details h4 {
  margin: 0 0 0.5rem;
  color: var(--text-dark);
  font-size: 1.125rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.detail-item.highlight-detail {
  background: #fff3cd;
  border-color: #ffc107;
}

.detail-label {
  font-size: 0.875rem;
  color: var(--text-light);
  font-weight: 500;
}

.detail-value {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.detail-value span {
  font-size: 1rem;
  color: var(--text-dark);
  font-weight: 600;
}

.account-number,
.transfer-content {
  font-family: "Courier New", monospace;
  font-size: 1.125rem;
  color: var(--primary);
}

.amount-value {
  font-size: 1.25rem;
  color: #dc3545;
}

.copy-btn {
  background: white;
  border: 1px solid #dee2e6;
  border-radius: 6px;
  padding: 0.5rem 0.75rem;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.copy-btn:hover {
  background: #e9ecef;
  border-color: #adb5bd;
}

/* Payment Notice */
.payment-notice {
  background: #fff3cd;
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid #ffc107;
  margin-bottom: 2rem;
  display: flex;
  gap: 1rem;
}

.notice-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.notice-content h4 {
  margin: 0 0 0.75rem;
  color: #856404;
  font-size: 1rem;
}

.notice-content ul {
  margin: 0;
  padding-left: 1.25rem;
  color: #856404;
}

.notice-content li {
  margin-bottom: 0.5rem;
  line-height: 1.5;
}

/* Payment Status */
.payment-status {
  text-align: center;
  padding: 1.5rem;
  margin-bottom: 2rem;
  border-radius: 8px;
}

.status-checking,
.status-pending,
.status-confirmed {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  font-size: 1.125rem;
  font-weight: 600;
}

.status-checking {
  color: #0d6efd;
}

.status-pending {
  color: #ffc107;
}

.status-confirmed {
  color: #28a745;
}

.status-icon {
  font-size: 2rem;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.btn-check-payment,
.btn-view-invoice,
.btn-back-orders,
.btn-back {
  padding: 0.875rem 2rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.btn-check-payment,
.btn-view-invoice,
.btn-back-orders,
.btn-back {
  background: #000; /* black buttons requested */
  color: #fff;
  border: none;
  padding: 0.9rem 1.6rem;
  border-radius: 10px;
  font-weight: 700;
  letter-spacing: 0.2px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.12);
  transition: transform 120ms ease, box-shadow 120ms ease, background-color 120ms ease;
}

.btn-check-payment:hover:not(:disabled),
.btn-view-invoice:hover,
.btn-back-orders:hover,
.btn-back:hover {
  transform: translateY(-3px);
  box-shadow: 0 14px 30px rgba(0,0,0,0.16);
  background-color: #111;
}

.btn-check-payment:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  box-shadow: none;
}

/* Make primary action visually stronger */
.btn-check-payment {
  padding: 0.95rem 1.8rem;
  border-radius: 12px;
}

/* Secondary button style (if you want lighter look later) */
.btn-back,
.btn-back-orders {
  background: #0d0d0d;
  opacity: 0.95;
}

/* Improve card/detail appearance */
.bank-details .detail-item {
  background: #ffffff;
  border: 1px solid rgba(16,24,40,0.04);
  box-shadow: 0 6px 18px rgba(14,30,37,0.04);
}

.payment-section {
  background: linear-gradient(180deg, #ffffff 0%, #fbfbfb 100%);
  padding: 2rem;
  border-radius: 14px;
  border: 1px solid rgba(16,24,40,0.04);
}

.qr-wrapper {
  width: 320px;
  height: 320px;
  padding: 1.25rem;
  border-radius: 14px;
  background: #ffffff;
  box-shadow: 0 10px 30px rgba(2,6,23,0.06);
  display: flex;
  align-items: center;
  justify-content: center;
}

.qr-instruction {
  color: #334155;
  font-size: 0.95rem;
  margin-top: 0.6rem;
}

/* Improve headings and spacing for a more professional look */
.payment-header h1 {
  font-size: 2.1rem;
  letter-spacing: -0.2px;
}

.order-summary.t-card {
  padding: 1.5rem 1.25rem;
}

.summary-item .label {
  color: #6b7280;
  font-weight: 600;
}

.summary-item .value {
  color: #0f172a;
  font-weight: 700;
}

/* Cash Payment Section */
.cash-payment-section {
  text-align: center;
  padding: 3rem 2rem;
  background: #f8f9fa;
  border-radius: 12px;
  border: 1px solid #e9ecef;
}

.cash-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.cash-payment-section h3 {
  font-size: 1.5rem;
  color: var(--text-dark);
  margin-bottom: 1rem;
}

.cash-payment-section p {
  color: var(--text-light);
  margin-bottom: 2rem;
  line-height: 1.6;
}

/* Toast Notification */
.toast-notification {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 15px 25px;
  border-radius: 8px;
  color: white;
  font-weight: 500;
  z-index: 1000;
  animation: slideIn 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.toast-notification.success {
  background: #28a745;
}

.toast-notification.error {
  background: #dc3545;
}

.toast-notification.info {
  background: #17a2b8;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

/* Invoice Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  max-width: 600px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e9ecef;
}

.modal-header h2 {
  margin: 0;
  color: var(--text-dark);
  font-size: 1.5rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 2rem;
  cursor: pointer;
  color: #6c757d;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  line-height: 1;
}

.close-btn:hover {
  color: #333;
}

.modal-body {
  padding: 1.5rem;
}

.invoice-header {
  text-align: center;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid #e9ecef;
}

.invoice-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--primary);
  margin-bottom: 0.5rem;
}

.invoice-number {
  font-size: 1rem;
  color: var(--text-light);
}

.invoice-section {
  margin-bottom: 2rem;
}

.invoice-section h4 {
  margin: 0 0 1rem;
  color: var(--text-dark);
  font-size: 1.125rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #e9ecef;
}

.service-details,
.pricing-details {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  gap: 1rem;
  flex-wrap: wrap;
}

.info-row span:first-child {
  color: var(--text-light);
  font-size: 0.9rem;
  min-width: 140px;
  flex-shrink: 0;
}

.info-row span:last-child {
  color: var(--text-dark);
  font-weight: 600;
  text-align: right;
  flex: 1;
  word-break: break-word;
}

.total-amount {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #f0f9ff;
  border-radius: 8px;
  margin-top: 0.5rem;
}

.total-price {
  font-size: 1.25rem;
  color: var(--primary);
}

.modal-footer {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  padding: 1.5rem;
  border-top: 1px solid #e9ecef;
}

.btn-download,
.btn-close-modal {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-download {
  background: var(--primary);
  color: white;
}

.btn-download:hover {
  background: var(--primary-dark);
}

.btn-close-modal {
  background: #6c757d;
  color: white;
}

.btn-close-modal:hover {
  background: #5a6268;
}

/* Responsive */
@media (max-width: 768px) {
  .payment-grid {
    grid-template-columns: 1fr;
  }

  .qr-wrapper {
    width: 100%;
    max-width: 300px;
  }

  .action-buttons {
    flex-direction: column;
  }

  .btn-check-payment,
  .btn-view-invoice,
  .btn-back-orders,
  .btn-back {
    width: 100%;
  }

  .summary-grid {
    grid-template-columns: 1fr;
  }

  .modal-content {
    width: 95%;
    margin: 1rem;
  }

  .modal-footer {
    flex-direction: column;
  }

  .btn-download,
  .btn-close-modal {
    width: 100%;
  }
}
</style>