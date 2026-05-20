<script setup>
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const logout = () => {
  authStore.logout()
  router.push('/dang-nhap')
}
</script>

<template>
  <section class="admin-shell">
    <div class="container admin-layout">
      <aside class="admin-sidebar">
        <div class="admin-brand">
          <div class="admin-logo">BHX</div>
          <div>
            <h3>Quản trị hệ thống</h3>
            <p>Bách Hóa Xanh</p>
          </div>
        </div>

        <nav class="admin-menu">
          <div class="menu-section-title">Điều hướng</div>
          <router-link to="/admin/dashboard">Tổng quan</router-link>
          <router-link to="/admin/don-hang">Đơn hàng</router-link>
          <router-link to="/admin/san-pham">Sản phẩm</router-link>
          <router-link to="/admin/khach-hang">Khách hàng</router-link>
          <router-link to="/admin/ton-kho">Tồn kho cửa hàng</router-link>

          <div class="menu-section-title">Hệ thống</div>
          <template v-if="authStore.user && authStore.user.role === 'ADMIN'">
            <router-link to="/admin/nhan-vien">Nhân viên</router-link>
            <router-link to="/admin/tai-khoan">Tài khoản</router-link>
            <router-link to="/admin/chi-nhanh">Chi nhánh</router-link>
          </template>
          <template v-else>
            <span class="menu-disabled" title="Bạn không có quyền truy cập">Nhân viên</span>
            <span class="menu-disabled" title="Bạn không có quyền truy cập">Tài khoản</span>
            <span class="menu-disabled" title="Bạn không có quyền truy cập">Chi nhánh</span>
          </template>
          <div class="menu-section-title">Khác</div>
          <router-link to="/">Về trang chủ</router-link>
          <a href="#" @click.prevent="logout" class="menu-alert">Đăng xuất</a>
        </nav>
      </aside>

      <main class="admin-main">
        <div class="admin-topbar">
          <div>
            <h1>Hệ thống điều hành</h1>
            <p>Xin chào, <strong>{{ authStore.user?.ho_ten || 'Quản trị viên' }}</strong></p>
          </div>
        </div>

        <router-view></router-view>
      </main>
    </div>
  </section>
</template>

<style scoped>
/* Đồng bộ bộ mã CSS Core Admin Sidebar */
.admin-shell { background: #f8fafc; min-height: 100vh; padding: 20px 0; text-align: left; }
.admin-layout { display: grid; grid-template-columns: 260px 1fr; gap: 24px; max-width: 1400px; margin: 0 auto; }
.admin-sidebar { background: #1e293b; color: white; border-radius: 16px; padding: 24px; height: fit-content; box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06); }
.admin-brand { display: flex; align-items: center; gap: 12px; margin-bottom: 30px; border-bottom: 1px solid #334155; padding-bottom: 15px; }
.admin-logo { background: #16a34a; width: 42px; height: 42px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 18px; }
.admin-brand h3 { margin: 0; font-size: 15px; }
.admin-brand p { margin: 2px 0 0 0; font-size: 12px; color: #94a3b8; }
.menu-section-title { margin: 20px 0 8px; font-size: 11px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #64748b; }
.admin-menu a, .menu-disabled { display: block; padding: 10px 12px; color: #cbd5e1; text-decoration: none; font-size: 14px; font-weight: 600; border-radius: 8px; margin-bottom: 4px; }
.admin-menu a:hover, .admin-menu a.router-link-active { background: #334155; color: #fff; }
.menu-disabled { opacity: 0.4; cursor: not-allowed; }
.menu-alert { color: #f87171 !important; font-weight: 700; }
.admin-main { background: #fff; border: 1px solid #e5e7eb; border-radius: 16px; padding: 30px; box-shadow: 0 8px 24px rgba(15, 23, 42, 0.04); }
.admin-topbar { border-bottom: 1px solid #f1f5f9; padding-bottom: 20px; margin-bottom: 25px; }
.admin-topbar h1 { margin: 0; font-size: 24px; color: #0f172a; }
.admin-topbar p { margin: 5px 0 0 0; color: #64748b; font-size: 14px; }
</style>