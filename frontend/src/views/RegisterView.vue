<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const registerMethod = ref('email') // 'email' hoặc 'phone'

// Form fields
const hoTen = ref('')
const email = ref('')
const dienThoai = ref('')
const password = ref('')
const confirmPassword = ref('')

// Trạng thái ẩn hiện mật khẩu
const showPassword = ref(false)
const showConfirmPassword = ref(false)

const xuLyDangKy = async () => {
  if (password.value !== confirmPassword.value) {
    alert('Mật khẩu nhập lại không khớp sếp ơi!')
    return
  }

  try {
    const payload = {
      ho_ten: hoTen.value,
      password: password.value,
      email: registerMethod.value === 'email' ? email.value : null,
      dien_thoai: registerMethod.value === 'phone' ? dienThoai.value : null
    }

    const res = await axios.post('http://localhost:8000/store/api/register/', payload)
    
    if (res.data.success) {
      if (registerMethod.value === 'email') {
        // Nếu chọn đăng ký email thì chuyển sang trang nhập mã OTP
        alert('Mã OTP xác thực đã gửi vào hòm thư của sếp!')
        // Lưu tạm email vào sessionStorage để trang OTP lấy hiển thị
        sessionStorage.setItem('pending_email', email.value)
        router.push('/xac-thuc-otp')
      } else {
        // Đăng ký số điện thoại thì cho qua thẳng trang đăng nhập luôn
        alert('Đăng ký thành công! Tiến hành đăng nhập thôi sếp.')
        router.push('/dang-nhap')
      }
    }
  } catch (error) {
    alert(error.response?.data?.error || 'Đăng ký không thành công!')
  }
}
</script>

<template>
  <section class="auth-page" style="text-align: left;">
    <div class="container">
      <div class="auth-box">
        <div class="auth-left">
          <span class="auth-tag">BHX Store</span>
          <h1>Tạo tài khoản mới</h1>
          <p style="color: white; margin-top: 15px; opacity: 0.9;">
            Tham gia mua sắm nhu yếu phẩm tươi ngon tiện lợi cùng ngàn ưu đãi tích điểm VIP tích lũy mỗi ngày.
          </p>
        </div>
        
        <div class="auth-right">
          <h2>Đăng ký hệ thống</h2>
          <p class="auth-subtitle">Chọn phương thức thuận tiện nhất để kích hoạt thành viên.</p>

          <div class="auth-switch-links" style="margin-bottom: 20px;">
            <div class="auth-switch-card" style="display: flex; gap: 10px; justify-content: center;">
              <button type="button" @click="registerMethod = 'email'" :style="registerMethod === 'email' ? 'background:#008a37; color:white; border:none; padding:8px 12px; border-radius:6px; font-weight:bold;' : 'padding:8px 12px; border:1px solid #ccc; background:none; border-radius:6px; cursor:pointer;'">📧 Qua Email</button>
              <button type="button" @click="registerMethod = 'phone'" :style="registerMethod === 'phone' ? 'background:#008a37; color:white; border:none; padding:8px 12px; border-radius:6px; font-weight:bold;' : 'padding:8px 12px; border:1px solid #ccc; background:none; border-radius:6px; cursor:pointer;'">📱 Qua Số điện thoại</button>
            </div>
          </div>

          <form @submit.prevent="xuLyDangKy" class="auth-form">
            <div class="form-group">
              <label>Họ và tên sếp</label>
              <input type="text" v-model="hoTen" placeholder="Nhập họ và tên..." required />
            </div>

            <div class="form-group" v-if="registerMethod === 'email'">
              <label>Địa chỉ Email</label>
              <input type="email" v-model="email" placeholder="example@gmail.com..." required />
            </div>

            <div class="form-group" v-else>
              <label>Số điện thoại</label>
              <input type="text" v-model="dienThoai" placeholder="Nhập số điện thoại..." required />
            </div>

            <div class="form-group">
              <label>Mật khẩu</label>
              <div class="password-wrapper" style="position: relative;">
                <input :type="showPassword ? 'text' : 'password'" v-model="password" placeholder="Nhập mật khẩu an toàn..." required style="width: 100%; padding-right: 40px;" />
                <button type="button" class="toggle-password" @click="showPassword = !showPassword" style="position: absolute; right: 10px; top: 12px; background: none; border: none; cursor: pointer;">{{ showPassword ? '🙈' : '👁' }}</button>
              </div>
            </div>

            <div class="form-group">
              <label>Xác nhận mật khẩu</label>
              <div class="password-wrapper" style="position: relative;">
                <input :type="showConfirmPassword ? 'text' : 'password'" v-model="confirmPassword" placeholder="Nhập lại mật khẩu..." required style="width: 100%; padding-right: 40px;" />
                <button type="button" class="toggle-password" @click="showConfirmPassword = !showConfirmPassword" style="position: absolute; right: 10px; top: 12px; background: none; border: none; cursor: pointer;">{{ showConfirmPassword ? '🙈' : '👁' }}</button>
              </div>
            </div>

            <button type="submit" class="auth-btn" style="width: 100%; padding: 14px; background: #008a37; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; margin-top: 15px;">Đăng ký thành viên</button>
          </form>

          <div style="text-align: center; margin-top: 20px;">
            <router-link to="/dang-nhap" style="color: #008a37; font-weight: bold; text-decoration: none;">← Quay lại đăng nhập</router-link>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>