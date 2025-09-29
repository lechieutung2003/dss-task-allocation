<script setup lang="ts">
import { useOauthStore } from '@/stores/oauth';
import { useRouter } from 'vue-router';
import '@/assets/css/customer.css'
const store = useOauthStore();
const router = useRouter();

const goToCreateOrder = () => {
  router.push('/dss/orders/create');
};
</script>

<template>
  <div class="home-page">
    <!-- Hero Section with Background -->
    <section class="hero-section">
      <div class="hero-background">
        <div class="hero-overlay"></div>
        <img src="@/assets/images/a0.png" alt="Clean Home" class="hero-bg-image" />
      </div>
      
      <div class="hero-content">
        <div class="hero-text">
          <h1 class="hero-title">Khám phá và trải nghiệm</h1>
          <h2 class="hero-subtitle">Dịch vụ dọn dẹp chuyên nghiệp</h2>
          <p class="hero-description">
            Nền tảng all-in-one để đặt lịch, theo dõi và bàn giao chất lượng — nhanh và thông minh hơn.
          </p>
          
          <button class="hero-cta" @click="goToCreateOrder">
            <svg class="cta-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              <path d="M9 12l2 2 4-4"></path>
            </svg>
            Chọn dịch vụ
          </button>
        </div>
        
        <!-- Service Quick Access Cards -->
        <div class="quick-services">

          <div class="service-card" @click="goToCreateOrder">
            <div class="service-image">
              <img src="@/assets/images/regular.jpg" alt="Vệ sinh văn phòng" />
            </div>
            <div class="service-info">
              <h4>Vệ sinh cơ bản</h4>
              <p>Đảm bảo sạch sẽ</p>
            </div>
          </div>
          
          <div class="service-card" @click="goToCreateOrder">
            <div class="service-image">
              <img src="@/assets/images/deep.jpg" alt="Vệ sinh văn phòng" />
            </div>
            <div class="service-info">
              <h4>Vệ sinh nâng cao</h4>
              <p>Hiệu quả cao</p>
            </div>
          </div>
          
          
          <div class="service-card" @click="goToCreateOrder">
            <div class="service-image">
              <img src="@/assets/images/clock.jpg" alt="Dọn theo giờ" />
            </div>
            <div class="service-info">
              <h4>Dọn theo giờ</h4>
              <p>Linh hoạt</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Hot Services Section -->
    <section class="hot-services">
      <div class="container">
        <h2 class="section-title">Dịch vụ được yêu thích</h2>
        <p class="section-subtitle">
          Phổ biến nhất dành cho gia đình và doanh nghiệp hiện đại
        </p>
        
        <div class="services-grid">
          <div class="service-tile large" @click="goToCreateOrder">
            <div class="service-bg">
              <img src="@/assets/images/all.jpg" alt="Dọn dẹp tổng thể" />
            </div>
            <div class="service-overlay">
              <span class="service-tag">TOP</span>
              <div class="service-content">
                <h3>Dọn dẹp tổng thể</h3>
                <p>từ 500.000đ</p>
              </div>
            </div>
          </div>
          
          <div class="service-tile" @click="goToCreateOrder">
            <div class="service-bg">
              <img src="@/assets/images/glass.jpeg" alt="Vệ sinh kính" />
            </div>
            <div class="service-overlay">
              <div class="service-content">
                <h3>Vệ sinh kính</h3>
                <p>từ 180.000đ</p>
              </div>
            </div>
          </div>
          
          <div class="service-tile" @click="goToCreateOrder">
            <div class="service-bg">
              <img src="@/assets/images/construct.jpeg" alt="Dọn sau xây dựng" />
            </div>
            <div class="service-overlay">
              <div class="service-content">
                <h3>Dọn sau xây dựng</h3>
                <p>từ 800.000đ</p>
              </div>
            </div>
          </div>
          
          <div class="service-tile" @click="goToCreateOrder">
            <div class="service-bg">
              <img src="@/assets/images/carpet.jpeg" alt="Vệ sinh thảm" />
            </div>
            <div class="service-overlay">
              <div class="service-content">
                <h3>Vệ sinh thảm</h3>
                <p>từ 120.000đ</p>
              </div>
            </div>
          </div>
        </div>
        
        <div class="navigation-dots">
          <button class="nav-dot"></button>
          <button class="nav-dot active"></button>
        </div>
      </div>
    </section>

    <!-- Featured Section -->
    <section class="featured-section">
      <div class="container">
        <div class="featured-card">
          <div class="featured-image">
            <img src="@/assets/images/luxury.jpg" alt="Dịch vụ cao cấp" />
            <div class="featured-badge">Cinnamon Clean Service</div>
          </div>
          <div class="featured-content">
            <h2>Dịch vụ cao cấp</h2>
            <p>Trải nghiệm dịch vụ dọn dẹp đẳng cấp 5 sao với đội ngũ chuyên nghiệp và trang thiết bị hiện đại nhất.</p>
            <div class="featured-tags">
              <span class="tag">#DanhGiaCao</span>
              <span class="tag">#ChuyenNghiep</span>
            </div>
            <button class="hero-cta1" @click="goToCreateOrder">
              Chọn dịch vụ
              <svg class="arrow-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M7 17l10-10M7 7h10v10"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
