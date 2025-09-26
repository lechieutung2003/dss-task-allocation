<template>
  <header :class="['user-topbar', { 'scrolled': isScrolled }]">
    <div class="user-topbar-wrapper">
      <!-- Tên công ty ở GIỮA -->
      <div class="company-name" @click="goHome">
        <h1>Công Ty Dọn Dẹp</h1>
      </div>
      <!-- Menu bên phải -->
      <nav class="nav-right">
        <span
          class="nav-link"
          :class="{ active: selected === 'about' }"
          @click="selectMenu('about', goAbout)"
        >Về chúng tôi</span>
        <span
          class="nav-link"
          :class="{ active: selected === 'services' }"
          @click="selectMenu('services', goServices)"
        >Dịch vụ</span>
        <span
          class="nav-link"
          :class="{ active: selected === 'contact' }"
          @click="selectMenu('contact', goContact)"
        >Liên hệ</span>
        <span
          class="pill-btn"
          :class="{ active: selected === 'create' }"
          @click="selectMenu('create', goCreateOrder)"
        >Tạo đơn</span>
        <!-- Avatar dropdown -->
        <div class="profile-wrapper">
          <el-avatar
            class="avatar"
            :size="36"
            @click="toggleMenu"
            style="cursor:pointer"
          >
            {{ initials }}
          </el-avatar>
          <div v-if="showMenu" class="dropdown-menu" @click.stop>
            <div class="dropdown-item" @click="goProfile">Trang cá nhân</div>
            <div class="dropdown-item" @click="logout">Đăng xuất</div>
          </div>
        </div>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { useOauthStore } from '@/stores/oauth'
import { useRouter } from 'vue-router'
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { ElAvatar } from 'element-plus'

const store = useOauthStore()
const router = useRouter()
const showMenu = ref(false)
const selected = ref('home')
const isScrolled = ref(false)

const fullName = computed(() =>
  store.user?.name || `${store.user?.first_name || ''} ${store.user?.last_name || ''}`.trim()
)
const initials = computed(() => {
  if (!fullName.value) return ''
  return fullName.value.split(' ').map(w => w[0]).join('').toUpperCase()
})

const selectMenu = (key, callback) => {
  selected.value = key
  callback()
}

const goHome = () => router.push('/dss/home')
const goAbout = () => router.push('/dss/about')
const goServices = () => router.push('/dss/services')
const goContact = () => router.push('/dss/contact')
const goCreateOrder = () => router.push('/dss/orders/create')
const goProfile = () => { showMenu.value = false; router.push('/dss/profile/client') }
const logout = () => { showMenu.value = false; store.$reset(); router.push('/') }

const handleClickOutside = (e) => { if (!e.target.closest('.profile-wrapper')) showMenu.value = false }
const toggleMenu = () => { showMenu.value = !showMenu.value }

const onScroll = () => {
  isScrolled.value = window.scrollY > 10
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  window.addEventListener('scroll', onScroll)
})
onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  window.removeEventListener('scroll', onScroll)
})
</script>

<style scoped>
:root{ --ink:#0f172a; --muted:#6b7280; --ring:#ecedec; }
.user-topbar{
  position: sticky; top: 0; z-index: 50;
  width: 100%; display: flex; justify-content: center;
  background: #fff;
  transition: background 0.3s, box-shadow 0.3s;
  box-shadow: 0 2px 8px rgba(0,0,0,0.03);
  backdrop-filter: none;
}
.user-topbar.scrolled {
  background: rgba(255,255,255,0.85);
  backdrop-filter: saturate(140%) blur(6px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
}

/* Wrapper chính */
.user-topbar-wrapper{
  width: 100%; max-width: 1100px;
  padding: 10px 20px;
  border-bottom: 1px solid #f0e7dc;
  display: flex; align-items: center; justify-content: flex-end;
  position: relative;
}

/* Logo/Company — ở CHÍNH GIỮA thanh */
.company-name{
  position: absolute; left: 10%; transform: translateX(-50%);
}
.company-name h1{
  margin: 0;
  font-size: 18px; font-weight: 800; letter-spacing:.2px;
  color: var(--ink); cursor: pointer;
}

/* Nav phải */
.nav-right{ display: flex; align-items: center; gap: 18px; color: var(--ink); }

.nav-link{
  cursor: pointer; font-size: 15px; font-weight: 600;
  padding: 6px 10px; border-radius: 8px; transition: .15s ease;
  color: var(--ink);
}
.nav-link:hover{ background: rgba(0,0,0,.05); }
.nav-link.active{ background:#111; color:#fff; }

.pill-btn{
  cursor:pointer; font-size:14px; font-weight:800;
  padding: 8px 14px; border-radius: 999px;
  background:#111; color:#fff; transition:.15s ease;
  border:1px solid #111;
}
.pill-btn:hover{ filter: brightness(.95); }
.pill-btn.active{ background:#000; color:#fff; }

.profile-wrapper{ position: relative; }
.avatar{
  background:#111; color:#fff; font-weight: 800; border:1px solid #000;
}

.dropdown-menu{
  position:absolute; top:48px; right:0;
  background:#fff; border:1.5px solid var(--ring);
  border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,.06);
  min-width: 180px; z-index: 100;
}
.dropdown-item{
  padding: 12px 16px; cursor:pointer; color:#222; font-size:14px;
  transition: background .15s; border-bottom:1px solid #f4f4f4;
}
.dropdown-item:last-child{ border-bottom: none; }
.dropdown-item:hover{ background:#f7f7f7; }

@media (max-width: 720px){
  .nav-right{ gap: 12px; }
  .company-name h1{ font-size: 16px; }
  .nav-link{ font-size:14px; padding:6px 8px; }
  .pill-btn{ padding:7px 12px; }
}
</style>