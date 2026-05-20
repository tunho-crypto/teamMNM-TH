<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const showPassword = ref(false) // Trạng thái bật/tắt mắt ẩn hiện mật khẩu

const authStore = useAuthStore()
const router = useRouter()

const xuLyDangNhap = async () => {
  if (!username.value || !password.value) {
    alert('Sếp nhập đầy đủ tài khoản và mật khẩu giùm nhé!')
    return
  }
  try {
    const response = await axios.post('http://localhost:8000/store/api/login/', {
      username: username.value,
      password: password.value
    })
    if (response.data.success) {
      authStore.login(response.data.user)
      alert(`🎉 Đăng nhập thành công! Chào mừng sếp ${response.data.user.ho_ten} quay trở lại!`)
      
      // Nếu là STAFF hoặc ADMIN thì đẩy thẳng vào Dashboard quản trị, ngược lại về trang chủ
      if (response.data.user.role !== 'USER') {
        router.push('/admin-dashboard')
      } else {
        router.push('/')
      }
    }
  } catch (error) {
    alert(error.response?.data?.error || 'Tài khoản hoặc mật khẩu không chính xác sếp ơi!')
  }
}
</script>

<template>
  <section class="auth-page" style="text-align: left;">
    <div class="container">
      <div class="auth-box">
        <div class="auth-left">
          <span class="auth-tag">BHX Store</span>
          <h1>Chào mừng sếp quay trở lại!</h1>
          <p style="color: white; margin-top: 15px; opacity: 0.9;">
            Đăng nhập hệ thống để quản lý giỏ hàng, theo dõi lịch sử giao dịch và tích lũy điểm thưởng thành viên VIP.
          </p>
        </div>
        
        <div class="auth-right">
          <h2>Đăng nhập hệ thống</h2>
          <p class="auth-subtitle">Nhập thông tin tài khoản của sếp để tiếp tục mua sắm.</p>

          <form @submit.prevent="xuLyDangNhap" class="auth-form">
            <div class="form-group">
              <label for="username">Số điện thoại hoặc Email</label>
              <input type="text" id="username" v-model="username" placeholder="Nhập số điện thoại hoặc email..." required autofocus />
            </div>

            <div class="form-group">
              <label for="password">Mật khẩu bảo mật</label>
              <div class="password-wrapper" style="position: relative;">
                <input :type="showPassword ? 'text' : 'password'" id="password" v-model="password" placeholder="Nhập mật khẩu của sếp..." required style="width: 100%; padding-right: 45px;" />
                <button type="button" class="toggle-password" @click="showPassword = !showPassword" style="position: absolute; right: 10px; top: 12px; background: none; border: none; cursor: pointer; font-size: 16px;">
                  {{ showPassword ? '🙈' : '👁️' }}
                </button>
              </div>
            </div>

            <div style="text-align: right; margin-bottom: 20px;">
              <router-link to="/quen-mat-khau" style="color: #64748b; font-size: 14px; text-decoration: none;">Quên mật khẩu sếp ơi?</router-link>
            </div>

            <button type="submit" class="auth-btn" style="width: 100%; padding: 14px; background: #008a37; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer;">Đăng nhập ngay</button>
          </form>

          <div class="auth-switch-links" style="margin-top: 25px;">
            <div class="auth-switch-card" style="padding: 14px 16px; border: 1px solid rgba(0, 0, 0, 0.08); border-radius: 14px; background: #f8fafc; text-align: center;">
                <p style="margin: 0 0 8px; color: #475569; font-size: 14px;">Sếp chưa có tài khoản thành viên?</p>
                <router-link to="/dang-ky" style="color: #15803d; font-weight: bold; text-decoration: none;">Đăng ký tài khoản mới tại đây</router-link>
            </div>
          </div>

        </div>
      </div>
    </div>
  </section>
</template>