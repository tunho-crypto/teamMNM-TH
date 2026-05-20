<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const pendingEmail = ref('')
const otpCode = ref('')

onMounted(() => {
  // Lấy email đang chờ kích hoạt từ bộ nhớ sessionStorage lên
  pendingEmail.value = sessionStorage.getItem('pending_email') || 'email_cua_sep@gmail.com'
})

const xuLyXacThucOTP = async () => {
  if (otpCode.value.length < 6) return alert('Vui lòng điền đủ 6 số mã OTP!')
  try {
    const res = await axios.post('http://localhost:8000/store/api/verify-otp/', {
      email: pendingEmail.value,
      otp_code: otpCode.value
    })
    if (res.data.success) {
      alert('🎉 Tài khoản của sếp đã kích hoạt trạng thái ACTIVE thành công!')
      sessionStorage.removeItem('pending_email')
      router.push('/dang-nhap')
    }
  } catch (error) {
    alert(error.response?.data?.error || 'Mã xác thực OTP không chính xác!')
  }
}

const guiLaiMaOTP = async () => {
  try {
    await axios.post('http://localhost:8000/store/api/resend-otp/', { email: pendingEmail.value })
    alert('🔄 Hệ thống đã làm mới và gửi lại mã OTP 6 số vào Email của sếp!')
  } catch (e) {
    alert('Không thể gửi lại mã vào lúc này!')
  }
}
</script>

<template>
  <section class="auth-page" style="text-align: left;">
    <div class="container">
      <div class="auth-box">
        <div class="auth-left">
          <span class="auth-tag">Xác thực OTP</span>
          <h1>Kích hoạt bảo mật</h1>
        </div>
        <div class="auth-right">
          <h2>Xác nhận mã OTP</h2>
          <p class="auth-subtitle">Mã gồm 6 chữ số đã được gửi tới:<br><strong style="color: #008a37;">{{ pendingEmail }}</strong></p>

          <form @submit.prevent="xuLyXacThucOTP" class="auth-form">
            <div class="form-group" style="text-align: center;">
              <label for="otp_code" style="text-align: left; display: block;">Mã OTP (6 số)</label>
              <input type="text" v-model="otpCode" maxlength="6" placeholder="------" required style="letter-spacing: 5px; text-align: center; font-weight: bold; font-size: 18px; width: 100%; padding: 12px; margin-top: 5px;" />
            </div>

            <button type="submit" class="auth-btn" style="width: 100%; padding: 14px; background: #008a37; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; margin-top: 10px;">Xác nhận mã OTP</button>
          </form>

          <div class="auth-switch-links" style="margin-top: 20px;">
            <div class="auth-switch-card" style="padding: 14px 16px; border: 1px solid rgba(0, 0, 0, 0.08); border-radius: 14px; background: #f8fafc; text-align: center;">
              <p style="margin: 0 0 8px; color: #475569; font-size: 14px;">Chưa nhận được mã sếp ơi?</p>
              <button type="button" @click="guiLaiMaOTP" style="background: none; border: none; color: #008a37; font-weight: bold; cursor: pointer; text-decoration: underline;">Gửi lại mã OTP ngay</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>