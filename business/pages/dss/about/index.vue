<script setup lang="ts">
import { useRouter } from 'vue-router';
const router = useRouter();
const goToCreateOrder = () => router.push('/dss/orders/create');
const goContact = () => router.push('/dss/contact');
</script>

<template>
  <div class="about-page">

    <!-- HERO với background image như customer.css -->
    <section class="hero-section">
      <div class="hero-background">
        <img src="@/assets/images/bg.png" alt="Background" class="hero-bg-image" />
      </div>
      <div class="hero-overlay"></div>
      
      <div class="hero-content">
        <div class="hero-text">
          <p class="eyebrow">Về chúng tôi</p>
          <h1 class="title">Công Ty Dọn Dẹp – <span>tận tâm</span> & <span>chuẩn mực</span> từ năm 19xx</h1>
          <p class="sub">
            Chúng tôi bắt đầu từ một đội ngũ nhỏ với niềm tin: vệ sinh chất lượng không chỉ sạch
            mà còn mang lại sự an tâm. Hơn nhiều thập kỷ, giá trị ấy vẫn không đổi.
          </p>
          <div class="cta-row">
            <button class="btn" @click="goToCreateOrder">Đặt dịch vụ</button>
            <button class="btn ghost" @click="goContact">Liên hệ tư vấn</button>
          </div>

          <!-- Logos/Badges -->
          <ul class="badges">
            <li>ISO 9001</li>
            <li>ISO 14001</li>
            <li>Trusted Service</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- LỊCH SỬ (BE) -->
    <section class="stripe white">
      <div class="container">
        <h2>Lịch sử lâu đời</h2>
        <p class="section-subtitle">Những cột mốc đánh dấu hành trình lớn mạnh và chuyên nghiệp hóa.</p>

        <div class="timeline-grid">
          <div class="t-item">
            <div class="t-year">19xx</div>
            <div class="t-card">
              <h3>Khởi đầu</h3>
              <p>Thành lập tại TP. HCM, cung cấp dịch vụ vệ sinh nhà ở và văn phòng nhỏ.</p>
            </div>
          </div>
          <div class="t-item">
            <div class="t-year">200x</div>
            <div class="t-card">
              <h3>Mở rộng</h3>
              <p>Mở rộng quy mô, đầu tư máy móc hiện đại, chuẩn hóa quy trình vận hành.</p>
            </div>
          </div>
          <div class="t-item">
            <div class="t-year">201x</div>
            <div class="t-card">
              <h3>Chuyển đổi số</h3>
              <p>Đưa nền tảng đặt lịch trực tuyến, báo cáo chất lượng theo thời gian thực.</p>
            </div>
          </div>
          <div class="t-item">
            <div class="t-year">202x</div>
            <div class="t-card">
              <h3>Chuẩn quốc tế</h3>
              <p>Đạt các chứng nhận ISO, cam kết an toàn – môi trường – khách hàng là trung tâm.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- TẦM NHÌN | SỨ MỆNH | GIÁ TRỊ (TRẮNG) -->
    <section class="stripe beige">
      <div class="container vmv">
        <h2>Tầm nhìn · Sứ mệnh · Giá trị cốt lõi</h2>

        <div class="vmv-grid">
          <div class="card">
            <h3>Tầm nhìn</h3>
            <p>Trở thành đơn vị vệ sinh đáng tin cậy nhất tại Việt Nam, dẫn đầu về chất lượng và trải nghiệm.</p>
          </div>
          <div class="card">
            <h3>Sứ mệnh</h3>
            <p>Mang đến không gian sạch – gọn – an toàn, giúp khách hàng tập trung vào điều quan trọng hơn.</p>
          </div>
          <div class="card">
            <h3>Giá trị cốt lõi</h3>
            <ul class="bullets">
              <li>Tận tâm và trung thực</li>
              <li>Chuẩn hóa quy trình</li>
              <li>An toàn – Xanh – Bền vững</li>
              <li>Không ngừng cải tiến</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- NĂNG LỰC & SỐ LIỆU (BE) -->
    <section class="stripe white">
      <div class="container stats">
        <h2>Năng lực đã được chứng minh</h2>
        <p class="section-subtitle">Sự tin tưởng của khách hàng thể hiện qua những con số biết nói.</p>

        <div class="stats-grid">
          <div class="s-card">
            <div class="s-num">5000+</div>
            <div class="s-label">Công trình mỗi năm</div>
          </div>
          <div class="s-card">
            <div class="s-num">98.7%</div>
            <div class="s-label">Mức hài lòng</div>
          </div>
          <div class="s-card">
            <div class="s-num">24/7</div>
            <div class="s-label">Hỗ trợ</div>
          </div>
          <div class="s-card">
            <div class="s-num">30+</div>
            <div class="s-label">Tỉnh thành phục vụ</div>
          </div>
        </div>
      </div>
    </section>

    <!-- ĐỘI NGŨ LÃNH ĐẠO (TRẮNG) -->
    <section class="stripe beige">
      <div class="container team">
        <h2>Đội ngũ lãnh đạo</h2>
        <p class="section-subtitle">Những người dẫn dắt tầm nhìn và chất lượng dịch vụ.</p>

        <div class="team-grid">
          <div class="member">
            <img src="@/assets/images/a0.png" alt="CEO" />
            <h3>Nguyễn Văn A</h3>
            <p class="role">Tổng Giám Đốc</p>
          </div>
          <div class="member">
            <img src="@/assets/images/a0.png" alt="COO" />
            <h3>Trần Thị B</h3>
            <p class="role">Giám Đốc Vận Hành</p>
          </div>
          <div class="member">
            <img src="@/assets/images/a0.png" alt="QA" />
            <h3>Lê Văn C</h3>
            <p class="role">Giám Đốc Chất Lượng</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CHỨNG NHẬN | ĐỐI TÁC (BE) -->
    <section class="stripe white">
      <div class="container certs">
        <h2>Chứng nhận & Đối tác</h2>
        <div class="certs-row">
          <div class="cert">ISO 9001</div>
          <div class="cert">ISO 14001</div>
          <div class="cert">Green Cleaning</div>
          <div class="cert">Trusted Partner</div>
        </div>
      </div>
    </section>

    <!-- CTA CUỐI TRANG (TRẮNG) -->
    <section class="stripe beige">
      <div class="container final-cta">
        <h2>Bắt đầu với chúng tôi hôm nay</h2>
        <p>Hẹn lịch nhanh, báo giá minh bạch, đội ngũ chuyên nghiệp.</p>
        <div class="cta-row">
          <button class="btn" @click="goToCreateOrder">Đặt dịch vụ ngay</button>
          <button class="btn ghost" @click="goContact">Gặp chuyên gia</button>
        </div>
      </div>
    </section>

  </div>
</template>

<style scoped>
/* Styles đã được chuyển sang customer.css */
</style>
