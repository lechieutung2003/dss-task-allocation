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
          <RouterLink to="/dss/customer-orders" class="btn-back">
            {{ t("back_to_orders") }}
          </RouterLink>
        </div>

        <!-- Payment info -->
        <div v-else-if="orderData" class="payment-content">
          <div class="payment-header">
            <div class="header-icon">💳</div>
            <h1>{{ t("payment_title") }}</h1>
            <p class="subtitle">{{ t("payment_subtitle") }}</p>
          </div>

          <!-- Order Summary -->
          <div class="order-summary">
            <h3>{{ t("payment_order_summary") }}</h3>
            <div class="summary-grid">
              <div class="summary-item">
                <span class="label">{{ t("payment_service") }}</span>
                <span class="value">{{ orderData.service_details?.name }}</span>
              </div>
              <div class="summary-item">
                <span class="label">{{ t("payment_area") }}</span>
                <span class="value">{{ orderData.area_m2 }} m²</span>
              </div>
              <div class="summary-item">
                <span class="label">{{ t("payment_start_time") }}</span>
                <span class="value">{{
                  formatDateTime(orderData.preferred_start_time)
                }}</span>
              </div>
              <div class="summary-item highlight">
                <span class="label">{{ t("payment_total_amount") }}</span>
                <span class="value amount">{{
                  formatPrice(orderData.cost_confirm)
                }}</span>
              </div>
            </div>
          </div>

          <!-- Payment method: Bank Transfer -->
          <div v-if="orderData.payment" class="payment-section">
            <h3>{{ t("payment_bank_transfer_title") }}</h3>

            <div class="payment-grid">
              <!-- QR Code -->
              <div class="qr-section">
                <div class="qr-wrapper">
                  <img
                    v-if="qrCodeDataUrl"
                    :src="qrCodeDataUrl"
                    alt="QR Code"
                    class="qr-code"
                  />
                  <div v-else class="qr-placeholder">
                    <div class="loading-spinner small"></div>
                    <p>{{ t("payment_qr_loading") }}</p>
                  </div>
                </div>
                <p class="qr-instruction">{{ t("payment_qr_instruction") }}</p>
              </div>

              <!-- Bank Details -->
              <div class="bank-details">
                <h4>{{ t("payment_bank_info") }}</h4>
                <div class="detail-item">
                  <span class="detail-label">{{ t("payment_bank_name") }}</span>
                  <div class="detail-value">
                    <span>{{ orderData.payment.bank_name }}</span>
                  </div>
                </div>
                <div class="detail-item">
                  <span class="detail-label">{{
                    t("payment_account_number")
                  }}</span>
                  <div class="detail-value">
                    <span class="account-number">{{
                      orderData.payment.account_number
                    }}</span>
                    <button
                      @click="copyToClipboard(orderData.payment.account_number)"
                      class="copy-btn"
                    >
                      📋
                    </button>
                  </div>
                </div>
                <div class="detail-item">
                  <span class="detail-label">{{
                    t("payment_account_name")
                  }}</span>
                  <div class="detail-value">
                    <span>{{ orderData.payment.account_name }}</span>
                  </div>
                </div>
                <div class="detail-item highlight-detail">
                  <span class="detail-label">{{ t("payment_amount") }}</span>
                  <div class="detail-value">
                    <span class="amount-value">{{
                      formatPrice(orderData.payment.amount)
                    }}</span>
                    <button
                      @click="copyToClipboard(orderData.payment.amount)"
                      class="copy-btn"
                    >
                      📋
                    </button>
                  </div>
                </div>
                <div class="detail-item highlight-detail">
                  <span class="detail-label">{{
                    t("payment_transfer_content")
                  }}</span>
                  <div class="detail-value">
                    <span class="transfer-content">{{
                      orderData.payment.transfer_content
                    }}</span>
                    <button
                      @click="
                        copyToClipboard(orderData.payment.transfer_content)
                      "
                      class="copy-btn"
                    >
                      📋
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Important Notice -->
            <div class="payment-notice">
              <div class="notice-icon">⚠️</div>
              <div class="notice-content">
                <h4>{{ t("payment_important_notice") }}</h4>
                <ul>
                  <li>{{ t("payment_notice_1") }}</li>
                  <li>{{ t("payment_notice_2") }}</li>
                  <li>{{ t("payment_notice_3") }}</li>
                </ul>
              </div>
            </div>

            <!-- Payment Status -->
            <div class="payment-status">
              <div v-if="checkingPayment" class="status-checking">
                <div class="loading-spinner small"></div>
                <span>{{ t("payment_checking_status") }}</span>
              </div>
              <div v-else-if="paymentConfirmed" class="status-confirmed">
                <div class="status-icon">✅</div>
                <span>{{ t("payment_confirmed") }}</span>
              </div>
              <div v-else class="status-pending">
                <div class="status-icon">⏳</div>
                <span>{{ t("payment_pending") }}</span>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="action-buttons">
              <button
                @click="checkPaymentStatus"
                :disabled="checkingPayment || paymentConfirmed"
                class="btn-check-payment"
              >
                <span v-if="checkingPayment">{{ t("payment_checking") }}</span>
                <span v-else-if="paymentConfirmed">{{
                  t("payment_confirmed_button")
                }}</span>
                <span v-else>{{ t("payment_check_button") }}</span>
              </button>

              <button
                v-if="paymentConfirmed"
                @click="viewInvoice"
                class="btn-view-invoice"
              >
                {{ t("payment_view_invoice") }}
              </button>

              <RouterLink to="/dss/customer-orders" class="btn-back-orders">
                {{ t("payment_back_orders") }}
              </RouterLink>
            </div>
          </div>

          <!-- Payment method: Cash -->
          <div v-else class="cash-payment-section">
            <div class="cash-icon">💵</div>
            <h3>{{ t("payment_cash_title") }}</h3>
            <p>{{ t("payment_cash_description") }}</p>
            <RouterLink to="/dss/customer-orders" class="btn-back">
              {{ t("back_to_orders") }}
            </RouterLink>
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
                <span
                  >{{
                    selectedInvoice.pricing.subtotal.toLocaleString("vi-VN")
                  }}
                  VNĐ</span
                >
              </div>
              <div class="info-row">
                <span>{{ t("invoice_tax") }}</span>
                <span
                  >{{
                    selectedInvoice.pricing.tax.toLocaleString("vi-VN")
                  }}
                  VNĐ</span
                >
              </div>
              <div class="total-amount">
                <span
                  ><strong>{{ t("invoice_total") }}</strong></span
                >
                <span class="total-price">
                  <strong
                    >{{
                      selectedInvoice.pricing.total.toLocaleString("vi-VN")
                    }}
                    VNĐ</strong
                  >
                </span>
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
      error.value = t("payment_no_info_error");
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
      
      // Show invoice
      viewInvoice();
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
});
</script>

<style scoped>
.payment-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

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

.btn-check-payment {
  background: var(--primary);
  color: white;
}

.btn-check-payment:hover:not(:disabled) {
  background: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.btn-check-payment:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background: #6c757d;
}

.btn-view-invoice {
  background: #28a745;
  color: white;
}

.btn-view-invoice:hover {
  background: #218838;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(40, 167, 69, 0.3);
}

.btn-back-orders,
.btn-back {
  background: #6c757d;
  color: white;
}

.btn-back-orders:hover,
.btn-back:hover {
  background: #5a6268;
  color: white;
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
