<script setup>
// ĐÃ BỔ SUNG LỆNH useRoute Ở ĐÂY CHỐNG LỖI TRẮNG TRANG
import { useRoute, useRouter } from 'vue-router'
import { useCartStore } from './stores/cart'
import { useAuthStore } from './stores/auth'

const route = useRoute()
const router = useRouter()
const cartStore = useCartStore()
const authStore = useAuthStore()

const logout = () => {
  authStore.logout()
  router.push('/dang-nhap')
}
</script>

<template>
  <div id="app-wrapper">
    <header class="site-header" v-if="!route.path.startsWith('/admin')">
      <div class="top-bar">
        <div class="top-bar-inner">
          <div v-if="authStore.user" class="user-logged-in">
            <span>🧔 Xin chào, <strong>{{ authStore.user.ho_ten }}</strong></span>
            <a href="#" @click.prevent="logout" class="logout-btn">Đăng xuất</a>
          </div>
          <div v-else class="user-guest">
            <router-link to="/dang-ky">Tạo tài khoản</router-link>
            <span> | </span>
            <router-link to="/dang-nhap">Đăng nhập hệ thống</router-link>
          </div>
        </div>
      </div>

      <div class="main-header" style="background-color: #ffd400; padding: 15px 0;">
        <div class="container" style="display: flex; justify-content: space-between; align-items: center; max-width: 1200px; margin: 0 auto; padding: 0 15px;">
          <router-link to="/" class="logo" style="text-decoration: none;">
            <h1 style="color: #008a37; margin: 0; font-size: 32px; font-weight: 900; letter-spacing: -1px;">BÁCH HÓA XANH</h1>
          </router-link>

          <div class="search-box" style="flex: 1; max-width: 500px; margin: 0 20px; display: flex;">
            <input type="text" placeholder="Giao hàng tận nhà, tìm gì cũng có..." style="flex: 1; padding: 12px; border: none; border-radius: 4px 0 0 4px; outline: none; font-size: 14px;" />
            <button style="background: white; border: none; padding: 0 15px; border-radius: 0 4px 4px 0; cursor: pointer;">🔍</button>
          </div>

          <router-link id="nut-gio-hang" to="/gio-hang" class="cart-btn" style="background: #008a37; color: white; text-decoration: none; padding: 10px 20px; border-radius: 8px; font-weight: bold; display: flex; align-items: center; gap: 8px;">
            🛒 Giỏ hàng
            <span class="cart-count" style="background: #ffd400; color: #d8232a; padding: 2px 8px; border-radius: 20px; font-size: 14px; font-weight: 800;">{{ cartStore.tongSoLuong }}</span>
          </router-link>
        </div>
      </div>
    </header>

    <nav class="navbar" v-if="!route.path.startsWith('/admin')">
      <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 15px;">
        <router-link to="/">🏠 TRANG CHỦ</router-link>
        <router-link to="/san-pham">🥬 SẢN PHẨM</router-link>
        <router-link to="/ban-do">🗺️ BẢN ĐỒ CHI NHÁNH</router-link>
        <router-link to="/cua-hang">📋 DANH SÁCH CỬA HÀNG</router-link>
        <router-link to="/gioi-thieu">ℹ️ GIỚI THIỆU</router-link>
        
        <router-link v-if="authStore.user" to="/lich-su">📦 LỊCH SỬ ĐƠN ĐẶT</router-link>
        <router-link v-if="authStore.user && authStore.user.role !== 'USER'" to="/admin" style="color: #ffd400;">📊 QUẢN TRỊ</router-link>
      </div>
    </nav>

    <main :style="!route.path.startsWith('/admin') ? 'background: #f6f7fb; min-height: 65vh; padding-bottom: 40px;' : ''">
      <router-view></router-view>
    </main>

    <footer class="site-footer" v-if="!route.path.startsWith('/admin')" style="background: #1f2937; color: #f3f4f6; padding: 40px 0 20px 0; font-family: Arial, sans-serif;">
      <div class="container" style="max-width: 1200px; margin: 0 auto; padding: 0 15px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 40px; text-align: left;">
        <div>
          <h3 style="color: #ffe100; font-size: 18px; margin-top: 0; margin-bottom: 15px;">🛒 BÁCH HÓA XANH ONLINE</h3>
          <p style="font-size: 14px; color: #9ca3af; line-height: 1.6; margin: 0;">Hệ thống đi chợ trực tuyến thiết yếu cho gia đình. Cung cấp sản phẩm tươi ngon sạch sẽ, giao nhanh tận cửa.</p>
        </div>
        <div>
          <h3 style="color: #ffe100; font-size: 18px; margin-top: 0; margin-bottom: 15px;">🔗 LIÊN KẾT HỆ THỐNG</h3>
          <ul style="list-style: none; padding: 0; margin: 0; font-size: 14px; line-height: 2;">
            <li><router-link to="/san-pham" style="color: #cbd5e1; text-decoration: none;">🥬 Danh sách sản phẩm mua sắm</router-link></li>
            <li><router-link to="/cua-hang" style="color: #cbd5e1; text-decoration: none;">🏪 Hệ thống chuỗi cửa hàng</router-link></li>
            <li><router-link to="/ban-do" style="color: #cbd5e1; text-decoration: none;">🗺️ Bản đồ số không gian GIS</router-link></li>
          </ul>
        </div>
        <div>
          <h3 style="color: #ffe100; font-size: 18px; margin-top: 0; margin-bottom: 15px;">📞 TỔNG ĐÀI HỖ TRỢ</h3>
          <p style="font-size: 14px; margin: 0 0 8px 0; color: #cbd5e1;">📞 Đặt hàng: <strong>1900.1908</strong></p>
          <p style="font-size: 14px; margin: 0 0 8px 0; color: #cbd5e1;">📧 Góp ý: <strong>support@bhx.local</strong></p>
        </div>
      </div>
      <div style="max-width: 1200px; margin: 30px auto 0 auto; padding: 20px 15px 0 15px; border-top: 1px solid #374151; font-size: 13px; color: #9ca3af; text-align: center;">
        <p style="margin: 0;">© 2026 Hệ thống siêu thị Bách Hóa Xanh (Bản nâng cấp SPA VueJS).</p>
      </div>
    </footer>
  </div>
</template>

<style>
/* CSS đồng bộ gốc */
body { margin: 0; font-family: 'Inter', Arial, sans-serif; background: #f6f7fb; }
.site-header { background-color: #ffd400; font-family: 'Inter', sans-serif; border-bottom: none; }
.top-bar { background-color: #f39c12; padding: 6px 0; }
.top-bar-inner { display: flex; justify-content: flex-end; align-items: center; gap: 15px; max-width: 1200px; margin: 0 auto; padding: 0 15px; font-size: 13px; }
.top-bar-inner a, .top-bar-inner span { color: white; text-decoration: none; font-weight: bold; }
.top-bar-inner a:hover { text-decoration: underline; }
.logout-btn { background: #d8232a; padding: 2px 8px; border-radius: 4px; margin-left: 10px; }
.navbar { background-color: #008a37; overflow: hidden; }
.navbar a { float: left; display: block; color: white; text-align: center; padding: 14px 16px; text-decoration: none; font-weight: bold; font-size: 15px; }
.navbar a:hover, .navbar a.router-link-active { background-color: #ffe100; color: #d8232a; }
.container { max-width: 1200px; margin: 0 auto; padding: 0 15px; }
</style>