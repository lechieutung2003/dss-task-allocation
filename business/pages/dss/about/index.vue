<script setup lang="ts">
import { useRouter } from 'vue-router';
const router = useRouter();
const goToCreateOrder = () => router.push('/dss/orders/create');
const goContact = () => router.push('/dss/contact');
</script>

<template>
  <div class="about-page">

    <!-- HERO (TRẮNG) -->
    <section class="stripe beige">
      <div class="container hero">
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

        <!-- Logos/Badges (tùy) -->
        <ul class="badges">
          <li>ISO 9001</li>
          <li>ISO 14001</li>
          <li>Trusted Service</li>
        </ul>
      </div>
    </section>

    <!-- LỊCH SỬ (BE) -->
    <section class="stripe white">
      <div class="container timeline">
        <h2>Lịch sử lâu đời</h2>
        <p class="lead">Những cột mốc đánh dấu hành trình lớn mạnh và chuyên nghiệp hóa.</p>

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
        <p class="lead">Sự tin tưởng của khách hàng thể hiện qua những con số biết nói.</p>

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
        <p class="lead">Những người dẫn dắt tầm nhìn và chất lượng dịch vụ.</p>

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
:root{ --be:#fff7ee; --ink:#000; --muted:#6b7280; }

/* Stripes */
.about-page{ background:transparent; color:var(--ink); }
.stripe{ width:100%; }
.stripe.white{ background:#fff; }
.stripe.beige{ background:var(--be); }
.container{ max-width:1100px; margin:0 auto; padding:40px 20px; }

/* Hero */
.hero{ text-align:center; }
.eyebrow{ font:500 14px/1 ui-sans-serif,system-ui; letter-spacing:.06em; text-transform:uppercase; color:#444; margin:0 0 8px; }
.title{ font:800 40px/1.1 ui-sans-serif,system-ui; margin:0 0 12px; }
.title span{ font-weight:900; }
.sub{ max-width:720px; margin:0 auto 18px; color:var(--muted); }
.cta-row{ display:flex; gap:12px; justify-content:center; margin-top:8px; }
.btn{ background:#000; color:#fff; border:1px solid #000; border-radius:999px; padding:10px 16px; font-weight:800; cursor:pointer; }
.btn:hover{ filter:brightness(.92); }
.btn.ghost{ background:#fff; color:#000; border-color:#ddd; }

/* Badges */
.badges{ list-style:none; padding:0; margin:18px 0 0; display:flex; gap:16px; justify-content:center; color:#111; opacity:.8;}
.badges li{ background:#f2f2f2; border:1px solid #e9e9e9; padding:6px 10px; border-radius:999px; font-weight:700; font-size:12px;}

/* Timeline */
.timeline h2{ font-size:32px; font-weight:900; margin:0 0 6px; }
.timeline .lead{ color:var(--muted); margin:0 0 18px; }
.timeline-grid{ display:grid; grid-template-columns:repeat(2, minmax(0,1fr)); gap:18px; }
.t-item{ display:grid; grid-template-columns:100px 1fr; gap:14px; align-items:start; }
.t-year{ font-weight:900; font-size:28px; line-height:1; }
.t-card{ background:#fff; border:1px solid #eee; border-radius:14px; padding:14px; }
.t-card h3{ margin:0 0 6px; font-size:18px; font-weight:800; }

/* VMV */
.vmv h2{ font-size:32px; font-weight:900; margin:0 0 10px; text-align:center; }
.vmv-grid{ display:grid; grid-template-columns:repeat(3,1fr); gap:18px; }
.vmv .card{ background:#fff; border:1px solid #eee; border-radius:14px; padding:18px; }
.vmv .bullets{ margin:8px 0 0; padding-left:18px; }

/* Stats */
.stats h2{ font-size:32px; font-weight:900; margin:0 0 6px; }
.stats .lead{ color:var(--muted); margin:0 0 16px; }
.stats-grid{ display:grid; grid-template-columns:repeat(4,1fr); gap:18px; }
.s-card{ background:#fff; border:1px solid #eee; border-radius:14px; padding:18px; text-align:center; }
.s-num{ font-weight:900; font-size:32px; line-height:1; }
.s-label{ color:#333; }

/* Team */
.team h2{ font-size:32px; font-weight:900; margin:0 0 6px; }
.team .lead{ color:var(--muted); margin:0 0 16px; }
.team-grid{ display:grid; grid-template-columns:repeat(3,1fr); gap:18px; }
.member{ background:#fff; border:1px solid #eee; border-radius:14px; padding:14px; text-align:center; }
.member img{ width:100%; height:220px; object-fit:cover; border-radius:10px; margin-bottom:10px; }
.member h3{ margin:4px 0 2px; font-size:18px; font-weight:800; }
.member .role{ color:#444; font-size:14px; }

/* Certs */
.certs h2{ font-size:32px; font-weight:900; margin:0 0 10px; }
.certs-row{ display:flex; gap:12px; flex-wrap:wrap; }
.cert{ background:#fff; border:1px solid #eee; padding:10px 14px; border-radius:999px; font-weight:800; }

/* Final CTA */
.final-cta{ text-align:center; }
.final-cta h2{ font-size:32px; font-weight:900; margin:0 0 6px; }
.final-cta p{ color:var(--muted); margin:0 0 12px; }

/* Responsive */
@media (max-width:1024px){
  .timeline-grid{ grid-template-columns:1fr; }
  .vmv-grid{ grid-template-columns:1fr; }
  .stats-grid{ grid-template-columns:repeat(2,1fr); }
  .team-grid{ grid-template-columns:1fr 1fr; }
}
@media (max-width:640px){
  .title{ font-size:32px; }
  .member img{ height:200px; }
  .stats-grid{ grid-template-columns:1fr; }
  .team-grid{ grid-template-columns:1fr; }
}
</style>
