<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import '@/assets/css/customer.css'
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
  <div class="about-page">
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
      <div class="container">
        <div class="timeline-grid">
          <!-- LEFT: FORM -->
          <div class="t-card">
            <h2>Gửi yêu cầu</h2>
            <p style="color: var(--text-light); margin-bottom: 1rem;">Điền biểu mẫu dưới đây để được tư vấn nhanh.</p>

            <form @submit.prevent="handleSubmit" v-if="!sent">
              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
                <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                  <label style="font-weight: 600; font-size: 14px; color: var(--text-dark);">Họ và tên <span style="color: #ef4444;">*</span></label>
                  <input v-model="form.fullName" type="text" placeholder="Nguyễn Văn A" style="border: 1px solid #e5e7eb; border-radius: 8px; padding: 10px 12px; outline: none; font-size: 14px;" />
                </div>
                <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                  <label style="font-weight: 600; font-size: 14px; color: var(--text-dark);">Số điện thoại <span style="color: #ef4444;">*</span></label>
                  <input v-model="form.phone" type="tel" placeholder="090x xxx xxx" style="border: 1px solid #e5e7eb; border-radius: 8px; padding: 10px 12px; outline: none; font-size: 14px;" />
                </div>
              </div>

              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
                <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                  <label style="font-weight: 600; font-size: 14px; color: var(--text-dark);">Email</label>
                  <input v-model="form.email" type="email" placeholder="ban@congty.com" style="border: 1px solid #e5e7eb; border-radius: 8px; padding: 10px 12px; outline: none; font-size: 14px;" />
                </div>
                <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                  <label style="font-weight: 600; font-size: 14px; color: var(--text-dark);">Nhu cầu dịch vụ</label>
                  <select v-model="form.service" style="border: 1px solid #e5e7eb; border-radius: 8px; padding: 10px 12px; outline: none; font-size: 14px;">
                    <option value="">— Chọn —</option>
                    <option value="basic">Dọn dẹp cơ bản</option>
                    <option value="deep">Tổng vệ sinh</option>
                    <option value="office">Vệ sinh văn phòng</option>
                    <option value="post">Sau xây dựng</option>
                  </select>
                </div>
              </div>

              <div style="display: flex; flex-direction: column; gap: 0.5rem; margin-bottom: 1rem;">
                <label style="font-weight: 600; font-size: 14px; color: var(--text-dark);">Nội dung <span style="color: #ef4444;">*</span></label>
                <textarea v-model="form.message" rows="5" placeholder="Mô tả địa điểm, diện tích, thời gian mong muốn…" style="border: 1px solid #e5e7eb; border-radius: 8px; padding: 10px 12px; outline: none; font-size: 14px; resize: vertical;"></textarea>
              </div>

              <label style="display: flex; gap: 8px; align-items: flex-start; margin: 1rem 0; font-size: 14px; color: var(--text-dark);">
                <input type="checkbox" v-model="form.agree" />
                Tôi đồng ý để Công Ty liên hệ tư vấn theo thông tin đã cung cấp.
              </label>

              <p v-if="error" style="color: #ef4444; font-weight: 600; margin: 0.5rem 0;">{{ error }}</p>

              <button class="btn" style="width: 100%;" :disabled="sending">
                <span v-if="!sending">Gửi yêu cầu</span>
                <span v-else>Đang gửi…</span>
              </button>
            </form>

            <div v-else style="text-align: center; padding: 1.5rem;">
              <h3 style="margin: 0 0 0.5rem; font-size: 20px; font-weight: 700; color: var(--accent);">Đã nhận yêu cầu ✅</h3>
              <p style="margin-bottom: 1rem; color: var(--text-light);">Chúng tôi sẽ liên hệ lại trong thời gian sớm nhất. Cảm ơn bạn!</p>
              <button class="btn" @click="goToCreateOrder">Đặt dịch vụ ngay</button>
            </div>
          </div>

          <!-- RIGHT: INFO -->
          <div>
            <div class="t-card" style="margin-bottom: 1rem;">
              <h3 style="margin: 0 0 0.5rem; font-size: 1.25rem; font-weight: 700; color: var(--accent);">Hotline</h3>
              <a href="tel:19001234" style="font-weight: 700; color: var(--text-dark); text-decoration: none;">1900 1234</a>
              <p style="color: var(--text-light); margin: 0.25rem 0 0;">Giờ làm việc: 08:00–20:00 (T2–CN)</p>
            </div>
            
            <div class="t-card" style="margin-bottom: 1rem;">
              <h3 style="margin: 0 0 0.5rem; font-size: 1.25rem; font-weight: 700; color: var(--accent);">Email</h3>
              <a href="mailto:contact@congtydondep.vn" style="font-weight: 700; color: var(--text-dark); text-decoration: none;">contact@congtydondep.vn</a>
              <p style="color: var(--text-light); margin: 0.25rem 0 0;">Phản hồi trong vòng 24h</p>
            </div>
            
            <div class="t-card" style="margin-bottom: 1rem;">
              <h3 style="margin: 0 0 0.5rem; font-size: 1.25rem; font-weight: 700; color: var(--accent);">Zalo / WhatsApp</h3>
              <p style="color: var(--text-dark); font-weight: 600; margin: 0.25rem 0;">+84 90x xxx xxx</p>
              <p style="color: var(--text-light); margin: 0;">Kênh trao đổi nhanh, gửi hình hiện trạng</p>
            </div>
            
            <div class="t-card" style="margin-bottom: 1rem;">
              <h3 style="margin: 0 0 0.5rem; font-size: 1.25rem; font-weight: 700; color: var(--accent);">Văn phòng</h3>
              <p style="color: var(--text-dark); font-weight: 600; margin: 0.25rem 0;">123 Nguyễn Trãi, Q.1, TP.HCM</p>
              <p style="color: var(--text-light); margin: 0;">Chi nhánh: Hà Nội · Đà Nẵng</p>
            </div>
            
            <div class="t-card" style="background: var(--bg-light);">
              <h3 style="margin: 0 0 0.5rem; font-size: 1.25rem; font-weight: 700; color: var(--accent);">Giờ tiếp nhận</h3>
              <div style="margin-top: 0.5rem;">
                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px dashed #e5e5e5;">
                  <span style="color: var(--text-dark); font-weight: 500;">Thứ 2–Thứ 6</span>
                  <span style="color: var(--text-dark); font-weight: 600;">08:00–20:00</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0;">
                  <span style="color: var(--text-dark); font-weight: 500;">Thứ 7–Chủ nhật</span>
                  <span style="color: var(--text-dark); font-weight: 600;">09:00–18:00</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>    <!-- BẢN ĐỒ (BEIGE) -->
    <section class="stripe beige">
      <div class="container">
        <div style="text-align: center; margin-bottom: 2rem;">
          <h2 class="section-title">Bản đồ</h2>
          <p class="section-subtitle">Ghé văn phòng hoặc đặt lịch khảo sát tại chỗ.</p>
        </div>
        <!-- Thay src bằng Google Maps của bạn -->
        <div style="border-radius: 24px; overflow: hidden; box-shadow: var(--shadow);">
          <iframe
            title="Google Map"
            src="https://maps.google.com/maps?q=Ben%20Thanh%20Market&t=&z=13&ie=UTF8&iwloc=&output=embed"
            loading="lazy"
            referrerpolicy="no-referrer-when-downgrade"
            style="width: 100%; height: 400px; border: 0; display: block;"
          ></iframe>
        </div>
      </div>
    </section>

    <!-- CÂU HỎI THƯỜNG GẶP (TRẮNG) -->
    <section class="stripe white">
      <div class="container">
        <div style="text-align: center; margin-bottom: 2rem;">
          <h2 class="section-title">FAQ – Câu hỏi thường gặp</h2>
        </div>
        <div class="vmv-grid">
          <div class="vmv">
            <div class="card">
              <h3>Giá có bao gồm dụng cụ và hóa chất không?</h3>
              <p>Có. Chúng tôi chuẩn bị đầy đủ dụng cụ và hóa chất phù hợp từng hạng mục.</p>
            </div>
          </div>
          <div class="vmv">
            <div class="card">
              <h3>Đặt lịch gấp trong ngày được không?</h3>
              <p>Tùy tình trạng lịch. Vui lòng gọi hotline để được sắp xếp nhanh nhất.</p>
            </div>
          </div>
          <div class="vmv">
            <div class="card">
              <h3>Chính sách bảo hành chất lượng thế nào?</h3>
              <p>Nếu chưa hài lòng, chúng tôi sắp xếp xử lý lại miễn phí trong 24–48h.</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
