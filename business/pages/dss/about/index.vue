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
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root { 
  --primary: #3b82f6;
  --secondary: #0d9488; 
  --accent: #059669;
  --text-dark: #1e293b;
  --text-light: #64748b;
  --bg-light: #f8fafc;
  --bg-card: #ffffff;
  --shadow: 0 10px 25px -3px rgba(0, 0, 0, 0.1);
  --shadow-hover: 0 20px 40px -4px rgba(0, 0, 0, 0.15);
  --gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --clean-gradient: linear-gradient(135deg, #3b82f6 0%, #0d9488 100%);
}

.about-page {
  min-height: 100vh;
  margin: 0;
  padding: 0;
  margin-top: -1px; /* Loại bỏ khoảng trắng do border */
  background: 
    linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.9) 100%),
    url('@/assets/images/bg.png') center/cover no-repeat fixed;
  color: var(--text-dark);
}

/* Stripes */
.stripe { 
  width: 100%; 
  margin-top: 0; /* Loại bỏ margin để liền mạch */
  padding-top: 0; /* Loại bỏ padding phân tách */
}
.stripe:first-child {
  margin-top: -80px; /* Chỉ section đầu tiên che topbar */
  padding-top: 80px;
}
.stripe.white { 
  background: rgba(255, 255, 255, 0.95); /* Đậm hơn để ít trong suốt */
  backdrop-filter: blur(10px);
  color: var(--text-dark);
}
.stripe.beige { 
  background: rgba(248, 250, 252, 0.95); /* Đậm hơn để ít trong suốt */
  backdrop-filter: blur(15px);
  color: var(--text-dark);
}

.container { 
  max-width: 1200px; 
  margin: 0 auto; 
  padding: 3rem 2rem; /* Giảm padding để sections gần nhau hơn */
}

/* Hero */
.hero { 
  text-align: center; 
}
.eyebrow { 
  font: 600 14px/1 ui-sans-serif,system-ui; 
  letter-spacing: 0.1em; 
  text-transform: uppercase; 
  color: var(--accent); 
  margin: 0 0 1rem; 
}
.title { 
  font: 800 3rem/1.1 ui-sans-serif,system-ui; 
  margin: 0 0 1.5rem;
  color: var(--text-dark);
}
.title span { 
  font-weight: 900;
  color: var(--accent); /* Xanh đậm thay vì gradient trong suốt */
}
.sub { 
  max-width: 720px; 
  margin: 0 auto 2rem; 
  color: var(--text-light);
  font-size: 1.1rem;
  line-height: 1.7;
}
.cta-row { 
  display: flex; 
  gap: 1rem; 
  justify-content: center; 
  margin-top: 2rem; 
}
.btn { 
  background: var(--clean-gradient); 
  color: white; 
  border: 2px solid transparent; 
  border-radius: 50px; 
  padding: 14px 28px; 
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: var(--shadow);
}
.btn:hover { 
  transform: translateY(-2px);
  box-shadow: var(--shadow-hover);
}
.btn.ghost { 
  background: rgba(255, 255, 255, 0.9); 
  color: var(--text-dark); 
  border-color: rgba(59, 130, 246, 0.3);
}
.btn.ghost:hover {
  background: rgba(255, 255, 255, 1);
  border-color: var(--primary);
}

/* Badges */
.badges { 
  list-style: none; 
  padding: 0; 
  margin: 2rem 0 0; 
  display: flex; 
  gap: 1rem; 
  justify-content: center; 
  flex-wrap: wrap;
}
.badges li { 
  background: rgba(255, 255, 255, 0.9); 
  border: 1px solid rgba(59, 130, 246, 0.2); 
  padding: 8px 16px; 
  border-radius: 25px; 
  font-weight: 700; 
  font-size: 0.8rem;
  color: var(--text-dark);
  box-shadow: var(--shadow);
}

/* Timeline */
.timeline h2 { 
  font-size: 2.5rem; 
  font-weight: 800; 
  margin: 0 0 1rem;
  color: var(--text-dark); /* Đảm bảo chữ đen */
}
.timeline .lead { 
  color: var(--text-light); /* Màu xám nhạt để dễ đọc */
  margin: 0 0 3rem;
  font-size: 1.1rem;
}
.timeline-grid { 
  display: grid; 
  grid-template-columns: repeat(2, minmax(0,1fr)); 
  gap: 2rem; 
}
.t-item { 
  display: grid; 
  grid-template-columns: 120px 1fr; 
  gap: 1.5rem; 
  align-items: start; 
}
.t-year { 
  font-weight: 900; 
  font-size: 2rem; 
  line-height: 1;
  color: var(--accent); /* Xanh đậm cho năm timeline */
}
.t-card { 
  background: rgba(255, 255, 255, 0.9); 
  border: 1px solid rgba(59, 130, 246, 0.1); 
  border-radius: 20px; 
  padding: 1.5rem;
  box-shadow: var(--shadow);
  transition: all 0.3s ease;
}
.t-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-hover);
}
.t-card h3 { 
  margin: 0 0 0.75rem; 
  font-size: 1.25rem; 
  font-weight: 700;
  color: var(--text-dark);
}
.t-card p {
  color: var(--text-light);
  line-height: 1.6;
}

/* VMV */
.vmv h2 { 
  font-size: 2.5rem; 
  font-weight: 800; 
  margin: 0 0 1rem; 
  text-align: center;
  color: var(--text-dark);
}
.vmv-grid { 
  display: grid; 
  grid-template-columns: repeat(3,1fr); 
  gap: 2rem; 
}
.vmv .card { 
  background: rgba(255, 255, 255, 0.9); 
  border: 1px solid rgba(59, 130, 246, 0.1); 
  border-radius: 24px; 
  padding: 2rem;
  box-shadow: var(--shadow);
  transition: all 0.3s ease;
}
.vmv .card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-hover);
}
.vmv .card h3 {
  color: var(--accent); /* Xanh đậm cho tiêu đề */
  margin-bottom: 1rem;
  font-size: 1.25rem;
  font-weight: 700;
}
.vmv .card p {
  color: var(--text-light);
  line-height: 1.6;
}
.vmv .bullets { 
  margin: 1rem 0 0; 
  padding-left: 1.5rem;
  color: var(--text-light);
}
.vmv .bullets li {
  margin-bottom: 0.5rem;
}

/* Stats */
.stats h2 { 
  font-size: 2.5rem; 
  font-weight: 800; 
  margin: 0 0 1rem;
  color: var(--text-dark); /* Chữ đen rõ ràng */
}
.stats .lead { 
  color: var(--text-light); /* Xám đậm để dễ đọc */
  margin: 0 0 3rem;
  font-size: 1.1rem;
}
.stats-grid { 
  display: grid; 
  grid-template-columns: repeat(4,1fr); 
  gap: 2rem; 
}
.s-card { 
  background: rgba(255, 255, 255, 0.9); 
  border: 1px solid rgba(59, 130, 246, 0.1); 
  border-radius: 20px; 
  padding: 2rem; 
  text-align: center;
  box-shadow: var(--shadow);
  transition: all 0.3s ease;
}
.s-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-hover);
}
.s-num { 
  font-weight: 900; 
  font-size: 2.5rem; 
  line-height: 1;
  color: var(--accent); /* Xanh đậm thay vì gradient trong suốt */
  margin-bottom: 0.5rem;
}
.s-label { 
  color: var(--text-dark);
  font-weight: 600;
}

/* Team */
.team h2 { 
  font-size: 2.5rem; 
  font-weight: 800; 
  margin: 0 0 1rem;
  color: var(--text-dark); /* Chữ đen rõ ràng */
}
.team .lead { 
  color: var(--text-light); /* Xám đậm để dễ đọc */
  margin: 0 0 3rem;
  font-size: 1.1rem;
}
.team-grid { 
  display: grid; 
  grid-template-columns: repeat(3,1fr); 
  gap: 2rem; 
}
.member { 
  background: rgba(255, 255, 255, 0.9); 
  border: 1px solid rgba(59, 130, 246, 0.1); 
  border-radius: 24px; 
  padding: 1.5rem; 
  text-align: center;
  box-shadow: var(--shadow);
  transition: all 0.3s ease;
}
.member:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-hover);
}
.member img { 
  width: 100%; 
  height: 220px; 
  object-fit: cover; 
  border-radius: 16px; 
  margin-bottom: 1rem; 
}
.member h3 { 
  margin: 0.5rem 0 0.25rem; 
  font-size: 1.25rem; 
  font-weight: 700;
  color: var(--accent); /* Xanh đậm cho tên thành viên */
}
.member .role { 
  color: var(--text-light); 
  font-size: 1rem;
  font-weight: 500;
}

/* Certs */
.certs h2 { 
  font-size: 2.5rem; 
  font-weight: 800; 
  margin: 0 0 2rem;
  color: var(--text-dark); /* Chữ đen rõ ràng */
}
.certs-row { 
  display: flex; 
  gap: 1rem; 
  flex-wrap: wrap;
  justify-content: center;
}
.cert { 
  background: rgba(255, 255, 255, 0.9); 
  border: 1px solid rgba(59, 130, 246, 0.2); 
  padding: 12px 20px; 
  border-radius: 25px; 
  font-weight: 700;
  color: var(--text-dark);
  box-shadow: var(--shadow);
  transition: all 0.3s ease;
}
.cert:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-hover);
  border-color: var(--primary);
}

/* Final CTA */
.final-cta { 
  text-align: center; 
}
.final-cta h2 { 
  font-size: 2.5rem; 
  font-weight: 800; 
  margin: 0 0 1rem;
  color: var(--text-dark);
}
.final-cta p { 
  color: var(--text-light); 
  margin: 0 0 2rem;
  font-size: 1.1rem;
}

/* Responsive */
@media (max-width: 1024px) {
  .timeline-grid { grid-template-columns: 1fr; }
  .vmv-grid { grid-template-columns: 1fr; }
  .stats-grid { grid-template-columns: repeat(2,1fr); }
  .team-grid { grid-template-columns: 1fr 1fr; }
  .container { padding: 3rem 2rem; }
}

@media (max-width: 768px) {
  .title { font-size: 2rem; }
  .member img { height: 200px; }
  .stats-grid { grid-template-columns: 1fr; }
  .team-grid { grid-template-columns: 1fr; }
  .cta-row { flex-direction: column; align-items: center; }
  .btn { width: 100%; max-width: 300px; }
  .container { padding: 2rem 1rem; }
}
</style>
