<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Form state
const form = ref({
  fullName: '',
  phone: '',
  email: '',
  service: '',
  message: '',
  agree: true
})
const sending = ref(false)
const sent = ref(false)
const error = ref('')

// Fake submit (thay bằng call API của bạn)
const handleSubmit = async () => {
  error.value = ''
  // validate nhẹ
  if (!form.value.fullName || !form.value.phone || !form.value.message) {
    error.value = 'Vui lòng điền Họ tên, Số điện thoại và Nội dung.'
    return
  }
  sending.value = true
  try {
    // TODO: gọi API của bạn ở đây
    await new Promise(r => setTimeout(r, 800))
    sent.value = true
  } catch (e) {
    error.value = 'Gửi thất bại, thử lại sau.'
  } finally {
    sending.value = false
  }
}

// Chuyển trang đặt dịch vụ
const goToCreateOrder = () => router.push('/dss/orders/create')
</script>

<template>
  <div class="contact-page">
    <!-- HERO (BEIGE) -->
    <section class="stripe beige">
      <div class="container hero">
        <p class="eyebrow">Liên hệ</p>
        <h1 class="title">Chúng tôi luôn sẵn sàng hỗ trợ</h1>
        <p class="sub">
          Hãy để lại thông tin, đội ngũ chăm sóc khách hàng sẽ phản hồi trong vòng <strong>15–30 phút (giờ hành chính)</strong>.
        </p>
        <div class="cta-row">
          <button class="btn" @click="goToCreateOrder">Đặt dịch vụ ngay</button>
          <a href="tel:19001234" class="btn ghost">Gọi hotline 1900 1234</a>
        </div>
        <ul class="badges">
          <li>Hỗ trợ 24/7</li>
          <li>Báo giá minh bạch</li>
          <li>Bảo hiểm trách nhiệm</li>
        </ul>
      </div>
    </section>

    <!-- FORM + THÔNG TIN (TRẮNG) -->
    <section class="stripe white">
      <div class="container two-col">
        <!-- LEFT: FORM -->
        <div class="card form-card">
          <h2>Gửi yêu cầu</h2>
          <p class="hint">Điền biểu mẫu dưới đây để được tư vấn nhanh.</p>

          <form @submit.prevent="handleSubmit" v-if="!sent">
            <div class="grid">
              <div class="field">
                <label>Họ và tên <span>*</span></label>
                <input v-model="form.fullName" type="text" placeholder="Nguyễn Văn A" />
              </div>
              <div class="field">
                <label>Số điện thoại <span>*</span></label>
                <input v-model="form.phone" type="tel" placeholder="090x xxx xxx" />
              </div>
            </div>

            <div class="grid">
              <div class="field">
                <label>Email</label>
                <input v-model="form.email" type="email" placeholder="ban@congty.com" />
              </div>
              <div class="field">
                <label>Nhu cầu dịch vụ</label>
                <select v-model="form.service">
                  <option value="">— Chọn —</option>
                  <option value="basic">Dọn dẹp cơ bản</option>
                  <option value="deep">Tổng vệ sinh</option>
                  <option value="office">Vệ sinh văn phòng</option>
                  <option value="post">Sau xây dựng</option>
                </select>
              </div>
            </div>

            <div class="field">
              <label>Nội dung <span>*</span></label>
              <textarea v-model="form.message" rows="5" placeholder="Mô tả địa điểm, diện tích, thời gian mong muốn…"></textarea>
            </div>

            <label class="agree">
              <input type="checkbox" v-model="form.agree" />
              Tôi đồng ý để Công Ty liên hệ tư vấn theo thông tin đã cung cấp.
            </label>

            <p v-if="error" class="error">{{ error }}</p>

            <button class="btn submit" :disabled="sending">
              <span v-if="!sending">Gửi yêu cầu</span>
              <span v-else>Đang gửi…</span>
            </button>
          </form>

          <div v-else class="sent">
            <h3>Đã nhận yêu cầu ✅</h3>
            <p>Chúng tôi sẽ liên hệ lại trong thời gian sớm nhất. Cảm ơn bạn!</p>
            <button class="btn" @click="goToCreateOrder">Đặt dịch vụ ngay</button>
          </div>
        </div>

        <!-- RIGHT: INFO -->
        <div class="info">
          <div class="i-card">
            <h3>Hotline</h3>
            <a href="tel:19001234" class="i-link">1900 1234</a>
            <p>Giờ làm việc: 08:00–20:00 (T2–CN)</p>
          </div>
          <div class="i-card">
            <h3>Email</h3>
            <a href="mailto:contact@congtydondep.vn" class="i-link">contact@congtydondep.vn</a>
            <p>Phản hồi trong vòng 24h</p>
          </div>
          <div class="i-card">
            <h3>Zalo / WhatsApp</h3>
            <p>+84 90x xxx xxx</p>
            <p>Kênh trao đổi nhanh, gửi hình hiện trạng</p>
          </div>
          <div class="i-card">
            <h3>Văn phòng</h3>
            <p>123 Nguyễn Trãi, Q.1, TP.HCM</p>
            <p>Chi nhánh: Hà Nội · Đà Nẵng</p>
          </div>
          <div class="i-card soft">
            <h3>Giờ tiếp nhận</h3>
            <ul class="hours">
              <li><span>Thứ 2–Thứ 6</span><span>08:00–20:00</span></li>
              <li><span>Thứ 7–Chủ nhật</span><span>09:00–18:00</span></li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- BẢN ĐỒ (BEIGE) -->
    <section class="stripe beige">
      <div class="container map">
        <h2>Bản đồ</h2>
        <p class="lead">Ghé văn phòng hoặc đặt lịch khảo sát tại chỗ.</p>
        <!-- Thay src bằng Google Maps của bạn -->
        <div class="map-frame">
          <iframe
            title="Google Map"
            src="https://maps.google.com/maps?q=Ben%20Thanh%20Market&t=&z=13&ie=UTF8&iwloc=&output=embed"
            loading="lazy"
            referrerpolicy="no-referrer-when-downgrade"
          ></iframe>
        </div>
      </div>
    </section>

    <!-- CÂU HỎI THƯỜNG GẶP (TRẮNG) -->
    <section class="stripe white">
      <div class="container faq">
        <h2>FAQ – Câu hỏi thường gặp</h2>
        <details>
          <summary>Giá có bao gồm dụng cụ và hóa chất không?</summary>
          <p>Có. Chúng tôi chuẩn bị đầy đủ dụng cụ và hóa chất phù hợp từng hạng mục.</p>
        </details>
        <details>
          <summary>Đặt lịch gấp trong ngày được không?</summary>
          <p>Tùy tình trạng lịch. Vui lòng gọi hotline để được sắp xếp nhanh nhất.</p>
        </details>
        <details>
          <summary>Chính sách bảo hành chất lượng thế nào?</summary>
          <p>Nếu chưa hài lòng, chúng tôi sắp xếp xử lý lại miễn phí trong 24–48h.</p>
        </details>
      </div>
    </section>
  </div>
</template>

<style scoped>
:root{ --be:#fff7ee; --ink:#000; --muted:#6b7280; --ring:#eae6dd; }

/* STRIPES */
.contact-page{ background:transparent; color:var(--ink); }
.stripe{ width:100%; }
.stripe.white{ background:#fff; }
.stripe.beige{ background:var(--be); }
.container{ max-width:1100px; margin:0 auto; padding:40px 20px; }

/* HERO */
.hero{ text-align:center; }
.eyebrow{ font:600 13px/1 ui-sans-serif,system-ui; letter-spacing:.1em; text-transform:uppercase; color:#555; margin:0 0 8px; }
.title{ font:800 40px/1.1 ui-sans-serif,system-ui; margin:0 0 10px; }
.sub{ max-width:720px; margin:0 auto 16px; color:var(--muted); }
.cta-row{ display:flex; gap:12px; justify-content:center; }
.btn{ background:#000; color:#fff; border:1px solid #000; border-radius:999px; padding:10px 16px; font-weight:800; cursor:pointer; }
.btn:hover{ filter:brightness(.92); }
.btn.ghost{ background:#fff; color:#000; border-color:#ddd; }
.badges{ list-style:none; padding:0; margin:16px 0 0; display:flex; gap:10px; justify-content:center; flex-wrap:wrap;}
.badges li{ background:#f5f5f5; border:1px solid #ededed; padding:6px 10px; border-radius:999px; font-weight:700; font-size:12px;}

/* TWO COL */
.two-col{ display:grid; grid-template-columns: 1.15fr .85fr; gap:24px; }

/* FORM CARD */
.card{ background:#fff; border:1px solid var(--ring); border-radius:16px; box-shadow:0 10px 30px rgba(0,0,0,.04); }
.form-card{ padding:20px; }
.form-card h2{ margin:0 0 6px; font-size:24px; font-weight:900; }
.hint{ color:var(--muted); margin:0 0 14px; }

.grid{ display:grid; grid-template-columns:1fr 1fr; gap:12px; }
.field{ display:flex; flex-direction:column; gap:6px; }
.field label{ font-weight:700; font-size:14px; }
.field label span{ color:#dc2626; }
.field input, .field select, .field textarea{
  border:1px solid #e6e6e6; border-radius:12px; padding:10px 12px;
  outline: none; font-size:14px;
}
.field textarea{ resize:vertical; }

.agree{ display:flex; gap:8px; align-items:flex-start; margin:8px 0 10px; font-size:14px; color:#222; }
.error{ color:#b91c1c; font-weight:700; margin:6px 0 10px; }
.submit{ width:100%; }

.sent{ text-align:center; padding:24px 10px; }
.sent h3{ margin:0 0 6px; font-size:20px; font-weight:900; }

/* INFO */
.info{ display:grid; gap:12px; }
.i-card{ background:#fff; border:1px solid var(--ring); border-radius:14px; padding:16px; }
.i-card.soft{ background:#f7f4ee; }
.i-card h3{ margin:0 0 6px; font-size:16px; font-weight:900; }
.i-link{ font-weight:900; color:#000; text-decoration:none; }

/* HOURS */
.hours{ list-style:none; margin:8px 0 0; padding:0; }
.hours li{ display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px dashed #e5e5e5; }
.hours li:last-child{ border-bottom:none; }

/* MAP */
.map h2{ font-size:28px; font-weight:900; margin:0 0 6px; }
.map .lead{ color:var(--muted); margin:0 0 14px; }
.map-frame{ border:1px solid var(--ring); border-radius:16px; overflow:hidden; }
.map-frame iframe{ width:100%; height:380px; border:0; display:block; }

/* FAQ */
.faq h2{ font-size:28px; font-weight:900; margin:0 0 12px; }
.faq details{ border:1px solid var(--ring); border-radius:12px; padding:12px 14px; background:#fff; margin-bottom:10px; }
.faq summary{ cursor:pointer; font-weight:800; }
.faq p{ margin:8px 0 0; color:#333; }

/* Responsive */
@media (max-width: 1024px){
  .two-col{ grid-template-columns:1fr; }
}
@media (max-width: 640px){
  .title{ font-size:32px; }
  .map-frame iframe{ height:300px; }
}
</style>
