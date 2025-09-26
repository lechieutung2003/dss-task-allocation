<script setup lang="ts">
import { useOauthStore } from '@/stores/oauth';
import { useRouter } from 'vue-router';

const store = useOauthStore();
const router = useRouter();

const goToCreateOrder = () => {
  router.push('/dss/orders/create');
};
</script>

<template>
  <div class="service-page">
    <div class="top-spacer"></div>

    <!-- HERO stripe BEIGE -->
    <section class="stripe beige">
      <div class="container hero">
        <h2 class="eyebrow">Làm gọn đội ngũ –</h2>
        <h1 class="title"><span>Siêu tăng tốc</span> quy trình vệ sinh của bạn</h1>
        <p class="sub">
          Nền tảng all-in-one để đặt lịch, theo dõi và bàn giao chất lượng — nhanh và thông minh hơn.
        </p>
        <button class="cta" @click="goToCreateOrder">
          Đặt dịch vụ miễn phí
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
            <path d="M5 12h14M13 5l7 7-7 7"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"/>
          </svg>
        </button>

        <!-- Avatars cong -->
        <div class="portrait-row">
          <div class="portrait p1"><img src="@/assets/images/a0.png" alt="Cleaner"/></div>
          <div class="portrait p2"><img src="@/assets/images/a0.png" alt="Cleaner"/></div>
          <div class="portrait p3"><img src="@/assets/images/a0.png" alt="Cleaner"/></div>
          <div class="portrait p4"><img src="@/assets/images/a0.png" alt="Cleaner"/></div>
          <div class="portrait p5"><img src="@/assets/images/a0.png" alt="Cleaner"/></div>
          <div class="portrait p6"><img src="@/assets/images/a0.png" alt="Cleaner"/></div>
          <div class="portrait p7"><img src="@/assets/images/a0.png" alt="Cleaner"/></div>
        </div>

        <div class="features3">
          <div class="f">
            <h3>Hỗ trợ theo thời gian thực</h3>
            <p>Chat, chia sẻ hình hiện trường, cập nhật ngay trong buổi vệ sinh.</p>
          </div>
          <div class="f">
            <h3>Giao việc & theo dõi</h3>
            <p>Tạo checklist, deadline và tiến độ rõ ràng cho từng căn hộ/công trình.</p>
          </div>
          <div class="f">
            <h3>Báo cáo hiệu suất</h3>
            <p>Dashboard minh bạch: thời lượng, điểm chất lượng, nút thắt cần cải thiện.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION 2 stripe WHITE -->
    <section class="stripe white">
      <div class="container everything">
        <h2>Mọi thứ bạn cần để làm việc thông minh hơn</h2>
        <p class="lead">
          Từ giao việc đến cập nhật theo thời gian thực, các tính năng giữ đội ngũ luôn kết nối, gọn gàng và tiến lên cùng nhau.
        </p>

        <div class="grid-tiles">
          <div class="tile photo">
            <img src="@/assets/images/a0.png" alt="Đội vệ sinh đang làm việc"/>
            <div class="label">Chat đội ngũ tích hợp</div>
          </div>
          <div class="tile card">
            <h3>Phân công tác vụ</h3>
            <p>Dễ tạo – dễ giao – dễ kiểm tra. Giữ mọi người thẳng hàng với checklist rõ ràng.</p>
            <button class="link" @click="goToCreateOrder">Bắt đầu ngay →</button>
          </div>
          <div class="tile card soft-sand">
            <h3>Lịch theo thời gian thực</h3>
            <p>Đặt lịch, đặt deadline, đồng bộ lịch để cả đội cùng một nhịp.</p>
          </div>
          <div class="tile photo green">
            <img src="@/assets/images/a0.png" alt="Báo cáo tiến độ"/>
            <div class="label">Theo dõi tiến độ</div>
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION 3 stripe BEIGE -->
    <section class="stripe beige">
      <div class="container results">
        <h2>Kết quả đã được chứng minh</h2>
        <p>Khách hàng báo cáo quy trình nhanh hơn, giao tiếp tốt hơn và chất lượng ổn định hơn sau khi dùng dịch vụ.</p>
        <button class="cta ghost" @click="goToCreateOrder">Tạo đơn ngay</button>
      </div>
    </section>
  </div>
</template>

<style scoped>
:root { --be:#fff7ee; --ink:#0f172a; --muted:#6b7280; }

/* Tổng thể */
.service-page{ background:transparent; color:var(--ink); }

/* STRIPES */
.stripe{ width:100%; }
.stripe.white{ background:#fff; }
.stripe.beige{ background:var(--be); }
.stripe + .stripe{ margin-top:0; }

/* Container */
.container{ max-width:1100px; margin:0 auto; padding:40px 20px; }

/* Hero */
.hero{ text-align:center; }
.eyebrow{ font-family:"Georgia",ui-serif,serif; font-weight:500; font-size:28px; color:#3b3b3b; margin:0 0 6px; }
.title{ font-family:ui-sans-serif,system-ui; font-weight:800; line-height:1.05; font-size:48px; margin:0 0 12px; }
.title span{ font-weight:900; }
.sub{ max-width:720px; margin:0 auto 18px; color:var(--muted); font-size:16px; }

/* CTA */
.cta{ display:inline-flex; align-items:center; gap:10px;
  background:#111; color:#fff; border:none; border-radius:999px;
  padding:12px 20px; font-weight:700; cursor:pointer; box-shadow:0 2px 0 rgba(0,0,0,.2);
}
.cta.ghost{ background:#fff; color:#111; border:1px solid #ddd; }
.cta:hover{ filter:brightness(0.95); }

/* Portraits */
.portrait-row{ margin:40px auto 18px; display:flex; justify-content:space-between; gap:18px; perspective:1000px; }
.portrait{ flex:1 1 0; min-width:110px; max-width:170px; background:#fff; border-radius:18px; overflow:hidden; box-shadow:0 10px 30px rgba(0,0,0,.08); transform-origin:bottom center; }
.portrait img{ width:100%; height:190px; object-fit:cover; }
.p1{ transform:rotate(-8deg) translateY(16px); opacity:.6;} .p2{ transform:rotate(-5deg) translateY(8px);} .p3{ transform:rotate(-2deg) translateY(2px);} .p4{ transform:rotate(0deg);} .p5{ transform:rotate(2deg) translateY(2px);} .p6{ transform:rotate(5deg) translateY(8px);} .p7{ transform:rotate(8deg) translateY(16px); opacity:.6;}

/* Features */
.features3{ display:grid; grid-template-columns:repeat(3,1fr); gap:28px; margin:26px auto 0; }
.features3 h3{ margin:0 0 6px; font-size:18px; font-weight:800;}
.features3 p{ margin:0; color:var(--muted); font-size:14px; line-height:1.5;}

/* Everything / Tiles */
.everything h2{ font-size:32px; margin:0 0 8px; font-weight:900; }
.everything .lead{ color:var(--muted); max-width:760px; margin:0 auto 24px; }
.grid-tiles{ margin-top:8px; display:grid; grid-template-columns:1.2fr .8fr; grid-auto-rows:260px; gap:24px; }
.tile{ border-radius:18px; overflow:hidden; background:#fff; box-shadow:0 10px 30px rgba(0,0,0,.06);}
.tile.photo{ position:relative;}
.tile.photo img{ width:100%; height:100%; object-fit:cover; }
.tile.photo .label{ position:absolute; left:16px; bottom:16px; background:rgba(0,0,0,.65); color:#fff; padding:8px 12px; border-radius:12px; font-weight:700; font-size:14px;}
.tile.card{ padding:22px; display:flex; flex-direction:column; justify-content:center; }
.tile.card h3{ margin:0 0 8px; font-size:20px; font-weight:900;}
.tile.card p{ margin:0 0 12px; color:var(--muted);}
.tile.card.soft-sand{ background:#efe5d6; }
.tile.photo.green{ background:#e4efe5; }
.link{ align-self:flex-start; border:none; background:transparent; color:#111; font-weight:800; cursor:pointer; }

/* Results */
.results{ text-align:center; }
.results h2{ font-size:32px; margin:0 0 8px; font-weight:900; }
.results p{ color:var(--muted); margin:0 0 16px; }

/* Responsive */
@media (max-width:1024px){
  .portrait img{ height:170px; }
  .grid-tiles{ grid-template-columns:1fr; grid-auto-rows:220px; }
}
@media (max-width:640px){
  .title{ font-size:36px; }
  .features3{ grid-template-columns:1fr; }
  .portrait-row{ gap:12px; }
  .portrait{ min-width:90px; }
}
</style>
