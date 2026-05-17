<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const otpCode = ref('')
const newPassword = ref('')
const confirmPassword = ref('')

const showNewPass = ref(false)
const showConfPass = ref(false)

const xuLyDatLaiMatKhau = async () => {
  if (newPassword.value !== confirmPassword.value) {
    alert('Mật khẩu xác nhận không khớp nhau!')
    return
  }
  try {
    const res = await axios.post('http://localhost:8000/store/api/reset-password/', {
      otp_code: otpCode.value,
      new_password: newPassword.value
    })
    if (res.data.success) {
      alert('🔒 Đã cập nhật mật khẩu mã hóa mới thành công! Đăng nhập lại thôi sếp.')
      router.push('/dang-nhap')
    }
  } catch (error) {
    alert(error.response?.data?.error || 'Mã OTP không chính xác hoặc hết hạn!')
  }
}
</script>

<template>
  <section class="auth-page" style="text-align: left;">
    <div class="container">
      <div class="auth-box">
        <div class="auth-left">
          <span class="auth-tag">BHX Store</span>
          <h1>Tạo mật khẩu mới</h1>
        </div>
        <div class="auth-right">
          <h2>Bảo mật tài khoản</h2>
          <p class="auth-subtitle">Nhập mã OTP khôi phục được gửi kèm trong hòm thư để thiết lập lại mật khẩu.</p>

          <form @submit.prevent="xuLyDatLaiMatKhau" class="auth-form">
            <div class="form-group">
              <label>Mã OTP khôi phục (6 số)</label>
              <input type="text" v-model="otpCode" placeholder="------" maxlength="6" required style="letter-spacing: 5px; text-align: center; font-weight: bold; font-size: 18px; width: 100%; padding: 12px;" />
            </div>

            <div class="form-group">
              <label>Mật khẩu mới</label>
              <div style="position: relative; margin-top: 5px;">
                <input :type="showNewPass ? 'text' : 'password'" v-model="newPassword" required style="width: 100%; padding: 12px; padding-right: 45px; border-radius: 8px; border: 1px solid #ddd; box-sizing: border-box;" />
                <span @click="showNewPass = !showNewPass" style="position: absolute; right: 15px; top: 12px; cursor: pointer; font-size: 18px;">{{ showNewPass ? '🙈' : '👁️' }}</span>
              </div>
            </div>

            <div class="form-group">
              <label>Xác nhận mật khẩu mới</label>
              <div style="position: relative; margin-top: 5px;">
                <input :type="showConfPass ? 'text' : 'password'" v-model="confirmPassword" required style="width: 100%; padding: 12px; padding-right: 45px; border-radius: 8px; border: 1px solid #ddd; box-sizing: border-box;" />
                <span @click="showConfPass = !showConfPass" style="position: absolute; right: 15px; top: 12px; cursor: pointer; font-size: 18px;">{{ showConfPass ? '🙈' : '👁️' }}</span>
              </div>
            </div>

            <button type="submit" class="auth-btn" style="width: 100%; padding: 14px; background: #008a37; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; margin-top: 15px;">Xác nhận đặt lại mật khẩu</button>
          </form>
        </div>
      </div>
    </div>
  </section>
</template>