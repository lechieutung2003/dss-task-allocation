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
            <button class="hero-cta" @click="goToCreateOrder">
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

<style scoped>
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

.home-page {
  min-height: 100vh;
  /* Nền với hình ảnh */
  background: 
    linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(13, 148, 136, 0.1) 100%),
    url('@/assets/images/bg.png') center/cover no-repeat fixed;
  
  /* Hoặc chỉ dùng hình ảnh đơn giản:
     background: url('@/assets/images/a0.png') center/cover no-repeat fixed;
  */
  
  /* Hoặc dùng pattern/texture:
     background: 
       radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
       radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
       url('@/assets/images/a0.png') center/cover no-repeat;
  */
}

/* Hero Section */
.hero-section {
  position: relative;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.hero-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
}

.hero-bg-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: brightness(0.7);
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.8) 0%, rgba(13, 148, 136, 0.6) 100%);
  backdrop-filter: blur(1px);
}

.hero-content {
  position: relative;
  z-index: 2;
  max-width: 1200px;
  width: 100%;
  padding: 0 2rem;
  color: white;
  text-align: center;
}

.hero-text {
  margin-bottom: 4rem;
}

.hero-title {
  font-size: 6rem;
  font-weight: 500;
  margin: 0 0 1rem;
  letter-spacing: -1px;
  text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.hero-subtitle {
  font-size: 2.5rem;
  font-weight: 600;
  margin: 0 0 1.5rem;
  letter-spacing: -0.5px;
  text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.hero-description {
  font-size: 1.2rem;
  opacity: 0.9;
  max-width: 600px;
  margin: 0 auto 2rem;
  line-height: 1.6;
}

.hero-cta {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 16px 32px;
  border-radius: 50px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.hero-cta:hover {
  background: rgba(255, 255, 255, 0.35); /* sáng hơn nhưng vẫn trong suốt */
  backdrop-filter: blur(70px); /* tăng blur một chút để nhìn lung linh hơn */
  color: #ffffff; /* giữ chữ trắng cho cảm giác sáng */
  transform: translateY(-2px);
  border-color: rgba(255, 255, 255, 0.5); /* viền sáng hơn một chút */
  
  transition: background 0.3s ease, box-shadow 0.3s ease, transform 0.2s ease;
}



.cta-icon {
  width: 24px;
  height: 24px;
}

/* Quick Services */
.quick-services {
  display: flex;
  gap: 1.5rem;
  justify-content: center;
  margin-top: 3rem;
}

.service-card {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  padding: 1.5rem;
  width: 200px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.service-card.active {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.4);
  transform: translateY(-5px);
}

.service-card:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
}

.service-image {
  width: 100%;
  height: 120px;
  border-radius: 16px;
  overflow: hidden;
  margin-bottom: 1rem;
}

.service-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.service-info h4 {
  color: white;
  margin: 0 0 0.5rem;
  font-size: 1.1rem;
  font-weight: 600;
}

.service-info p {
  color: rgba(255, 255, 255, 0.8);
  margin: 0;
  font-size: 0.9rem;
}

/* Container */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

/* Hot Services Section */
.hot-services {
  padding: 5rem 0;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  /* Hoặc thay bằng:
     background: transparent; // Trong suốt
     background: rgba(255, 255, 255, 0.1); // Trắng mờ
  */
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--text-dark);
  text-align: center;
  margin: 0 0 1rem;
}

.section-subtitle {
  color: var(--text-light);
  text-align: center;
  font-size: 1.1rem;
  margin: 0 0 3rem;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.services-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.service-tile {
  position: relative;
  border-radius: 24px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: var(--shadow);
}

.service-tile.large {
  grid-row: 1 / -1;
}

.service-tile:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-hover);
}

.service-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.service-bg img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.service-tile:hover .service-bg img {
  transform: scale(1.05);
}

.service-overlay {
  position: relative;
  height: 300px;
  background: linear-gradient(45deg, rgba(0, 0, 0, 0.7) 0%, rgba(0, 0, 0, 0.3) 100%);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 1.5rem;
  color: white;
}

.service-tile.large .service-overlay {
  height: 100%;
  min-height: 400px;
}

.service-tag {
  align-self: flex-start;
  background: var(--clean-gradient);
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.service-content {
  margin-top: auto;
}

.service-content h3 {
  font-size: 1.3rem;
  font-weight: 600;
  margin: 0 0 0.5rem;
}

.service-content p {
  color: rgba(255, 255, 255, 0.8);
  margin: 0;
  font-size: 1rem;
}

/* Navigation Dots */
.navigation-dots {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
}

.nav-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: none;
  background: #e5e7eb;
  cursor: pointer;
  transition: all 0.3s ease;
}

.nav-dot.active {
  background: var(--primary);
  transform: scale(1.2);
}

/* Featured Section */
.featured-section {
  padding: 5rem 0;
  background: rgba(248, 250, 252, 0.5);
  /* Hoặc thay bằng:
     background: transparent; // Trong suốt
     background: rgba(255, 255, 255, 0.3); // Trắng mờ hơn
  */
}

.featured-card {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  align-items: center;
  background: var(--bg-card);
  border-radius: 32px;
  padding: 3rem;
  box-shadow: var(--shadow);
}

.featured-image {
  position: relative;
  border-radius: 24px;
  overflow: hidden;
  height: 400px;
}

.featured-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.featured-badge {
  position: absolute;
  top: 1.5rem;
  left: 1.5rem;
  background: var(--clean-gradient);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
}

.featured-content h2 {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--text-dark);
  margin: 0 0 1.5rem;
}

.featured-content p {
  color: var(--text-light);
  font-size: 1.1rem;
  line-height: 1.7;
  margin: 0 0 2rem;
}

.featured-tags {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 2rem;
}

.tag {
  background: var(--bg-light);
  color: var(--text-light);
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
}

.featured-cta {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  background: var(--clean-gradient);
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 50px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.featured-cta:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-hover);
}

.arrow-icon {
  width: 20px;
  height: 20px;
  transition: transform 0.3s ease;
}

.featured-cta:hover .arrow-icon {
  transform: translateX(4px);
}

/* Responsive */
@media (max-width: 1024px) {
  .services-grid {
    grid-template-columns: 1fr 1fr;
    grid-template-rows: auto;
  }
  
  .service-tile.large {
    grid-row: auto;
    grid-column: 1 / -1;
  }
  
  .featured-card {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  
  .quick-services {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }
  
  .hero-subtitle {
    font-size: 2rem;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .quick-services {
    flex-direction: column;
    align-items: center;
  }
  
  .service-card {
    width: 280px;
  }
  
  .services-grid {
    grid-template-columns: 1fr;
  }
  
  .featured-card {
    padding: 2rem;
  }
  
  .featured-content h2 {
    font-size: 2rem;
  }
}
</style>
