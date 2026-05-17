<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()

// Bước hiện tại: 1 = nhập email, 2 = nhập OTP + mật khẩu mới
const buocHienTai = ref(1)
const dangTai = ref(false)

// Bước 1
const email = ref('')

// Bước 2
const otpCode = ref('')
const matKhauMoi = ref('')
const xacNhanMatKhau = ref('')
const showMatKhauMoi = ref(false)
const showXacNhan = ref(false)

// Gửi OTP về email
const guiOTP = async () => {
  if (!email.value) {
    alert('Sếp nhập email giúp nhé!')
    return
  }
  dangTai.value = true
  try {
    const res = await axios.post('http://localhost:8000/store/api/forgot-password/', {
      email: email.value
    })
    if (res.data.success) {
      buocHienTai.value = 2
    }
  } catch (error) {
    alert(error.response?.data?.error || 'Có lỗi xảy ra, sếp thử lại nhé!')
  } finally {
    dangTai.value = false
  }
}

// Đặt lại mật khẩu
const datLaiMatKhau = async () => {
  if (!otpCode.value || !matKhauMoi.value || !xacNhanMatKhau.value) {
    alert('Sếp nhập đầy đủ thông tin giúp nhé!')
    return
  }
  if (matKhauMoi.value !== xacNhanMatKhau.value) {
    alert('Mật khẩu xác nhận không khớp sếp ơi!')
    return
  }
  if (matKhauMoi.value.length < 6) {
    alert('Mật khẩu phải có ít nhất 6 ký tự nhé sếp!')
    return
  }
  dangTai.value = true
  try {
    const res = await axios.post('http://localhost:8000/store/api/reset-password/', {
      otp_code: otpCode.value,
      new_password: matKhauMoi.value
    })
    if (res.data.success) {
      alert('🎉 Đặt lại mật khẩu thành công! Sếp đăng nhập lại nhé!')
      router.push('/dang-nhap')
    }
  } catch (error) {
    alert(error.response?.data?.error || 'Mã OTP không hợp lệ hoặc đã hết hạn sếp ơi!')
  } finally {
    dangTai.value = false
  }
}

// Gửi lại OTP
const guiLaiOTP = async () => {
  otpCode.value = ''
  dangTai.value = true
  try {
    await axios.post('http://localhost:8000/store/api/forgot-password/', {
      email: email.value
    })
    alert('Đã gửi lại mã OTP vào email của sếp!')
  } catch (error) {
    alert('Không thể gửi lại OTP, sếp thử lại sau nhé!')
  } finally {
    dangTai.value = false
  }
}
</script>

<template>
  <section class="auth-page" style="text-align: left;">
    <div class="container">
      <div class="auth-box">

        <!-- CỘT TRÁI: Mô tả -->
        <div class="auth-left">
          <span class="auth-tag">BHX Store</span>
          <h1>
            <template v-if="buocHienTai === 1">Quên mật khẩu?</template>
            <template v-else>Kiểm tra email của sếp!</template>
          </h1>
          <p style="color: white; margin-top: 15px; opacity: 0.9;">
            <template v-if="buocHienTai === 1">
              Đừng lo sếp ơi! Nhập email đã đăng ký, chúng tôi sẽ gửi mã OTP để đặt lại mật khẩu ngay.
            </template>
            <template v-else>
              Mã OTP gồm 6 chữ số đã được gửi đến <strong>{{ email }}</strong>. Mã có hiệu lực trong 15 phút.
            </template>
          </p>

          <!-- Thanh tiến trình -->
          <div style="margin-top: 35px;">
            <div style="display: flex; align-items: center; gap: 10px;">
              <!-- Bước 1 -->
              <div style="display: flex; flex-direction: column; align-items: center; gap: 6px;">
                <div :style="{
                  width: '36px', height: '36px', borderRadius: '50%',
                  background: buocHienTai >= 1 ? '#fff' : 'rgba(255,255,255,0.3)',
                  color: buocHienTai >= 1 ? '#008a37' : '#fff',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  fontWeight: 'bold', fontSize: '15px'
                }">1</div>
                <span style="font-size: 11px; color: rgba(255,255,255,0.85);">Nhập email</span>
              </div>
              <div style="flex: 1; height: 2px; background: rgba(255,255,255,0.3); border-radius: 2px; margin-bottom: 20px;">
                <div :style="{ width: buocHienTai >= 2 ? '100%' : '0%', height: '100%', background: '#fff', borderRadius: '2px', transition: 'width 0.5s ease' }"></div>
              </div>
              <!-- Bước 2 -->
              <div style="display: flex; flex-direction: column; align-items: center; gap: 6px;">
                <div :style="{
                  width: '36px', height: '36px', borderRadius: '50%',
                  background: buocHienTai >= 2 ? '#fff' : 'rgba(255,255,255,0.3)',
                  color: buocHienTai >= 2 ? '#008a37' : '#fff',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  fontWeight: 'bold', fontSize: '15px'
                }">2</div>
                <span style="font-size: 11px; color: rgba(255,255,255,0.85);">Đặt lại MK</span>
              </div>
            </div>
          </div>
        </div>

        <!-- CỘT PHẢI: Form -->
        <div class="auth-right">

          <!-- BƯỚC 1: Nhập email -->
          <template v-if="buocHienTai === 1">
            <h2>Khôi phục mật khẩu</h2>
            <p class="auth-subtitle">Nhập email đã đăng ký, hệ thống sẽ gửi mã OTP về cho sếp.</p>

            <form @submit.prevent="guiOTP" class="auth-form">
              <div class="form-group">
                <label for="email">Địa chỉ Email đã đăng ký</label>
                <input
                  type="email"
                  id="email"
                  v-model="email"
                  placeholder="Nhập email của sếp..."
                  required
                  autofocus
                />
              </div>

              <button
                type="submit"
                class="auth-btn"
                :disabled="dangTai"
                style="width: 100%; padding: 14px; background: #008a37; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; margin-top: 8px; opacity: 1;"
              >
                <span v-if="dangTai">⏳ Đang gửi mã OTP...</span>
                <span v-else>Gửi mã OTP về Email</span>
              </button>
            </form>
          </template>

          <!-- BƯỚC 2: Nhập OTP + mật khẩu mới -->
          <template v-else>
            <h2>Đặt lại mật khẩu</h2>
            <p class="auth-subtitle">Nhập mã OTP từ email và mật khẩu mới của sếp.</p>

            <form @submit.prevent="datLaiMatKhau" class="auth-form">

              <!-- OTP -->
              <div class="form-group">
                <label for="otp">Mã OTP (6 chữ số)</label>
                <input
                  type="text"
                  id="otp"
                  v-model="otpCode"
                  placeholder="Nhập mã 6 số từ email..."
                  maxlength="6"
                  inputmode="numeric"
                  required
                  autofocus
                  style="letter-spacing: 6px; font-size: 20px; font-weight: bold; text-align: center;"
                />
              </div>

              <!-- Mật khẩu mới -->
              <div class="form-group">
                <label for="mat-khau-moi">Mật khẩu mới</label>
                <div class="password-wrapper" style="position: relative;">
                  <input
                    :type="showMatKhauMoi ? 'text' : 'password'"
                    id="mat-khau-moi"
                    v-model="matKhauMoi"
                    placeholder="Nhập mật khẩu mới (ít nhất 6 ký tự)..."
                    required
                    style="width: 100%; padding-right: 45px;"
                  />
                  <button type="button" @click="showMatKhauMoi = !showMatKhauMoi"
                    style="position: absolute; right: 10px; top: 12px; background: none; border: none; cursor: pointer; font-size: 16px;">
                    {{ showMatKhauMoi ? '🙈' : '👁️' }}
                  </button>
                </div>
              </div>

              <!-- Xác nhận mật khẩu -->
              <div class="form-group">
                <label for="xac-nhan">Xác nhận mật khẩu mới</label>
                <div class="password-wrapper" style="position: relative;">
                  <input
                    :type="showXacNhan ? 'text' : 'password'"
                    id="xac-nhan"
                    v-model="xacNhanMatKhau"
                    placeholder="Nhập lại mật khẩu mới..."
                    required
                    style="width: 100%; padding-right: 45px;"
                    :style="xacNhanMatKhau && matKhauMoi !== xacNhanMatKhau ? { borderColor: '#dc2626' } : {}"
                  />
                  <button type="button" @click="showXacNhan = !showXacNhan"
                    style="position: absolute; right: 10px; top: 12px; background: none; border: none; cursor: pointer; font-size: 16px;">
                    {{ showXacNhan ? '🙈' : '👁️' }}
                  </button>
                </div>
                <p v-if="xacNhanMatKhau && matKhauMoi !== xacNhanMatKhau"
                  style="color: #dc2626; font-size: 12px; margin-top: 4px;">
                  ❌ Mật khẩu xác nhận chưa khớp
                </p>
                <p v-else-if="xacNhanMatKhau && matKhauMoi === xacNhanMatKhau"
                  style="color: #16a34a; font-size: 12px; margin-top: 4px;">
                  ✅ Mật khẩu khớp rồi
                </p>
              </div>

              <button
                type="submit"
                class="auth-btn"
                :disabled="dangTai"
                style="width: 100%; padding: 14px; background: #008a37; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; margin-top: 8px;"
              >
                <span v-if="dangTai">⏳ Đang xử lý...</span>
                <span v-else>Đặt lại mật khẩu ngay</span>
              </button>
            </form>

            <!-- Gửi lại OTP -->
            <div style="margin-top: 20px; text-align: center; color: #64748b; font-size: 14px;">
              Không nhận được mã?
              <button
                type="button"
                @click="guiLaiOTP"
                :disabled="dangTai"
                style="background: none; border: none; color: #008a37; font-weight: bold; cursor: pointer; text-decoration: underline; font-size: 14px;">
                Gửi lại OTP
              </button>
            </div>
          </template>

          <!-- Link quay lại đăng nhập -->
          <div class="auth-switch-links" style="margin-top: 25px;">
            <div class="auth-switch-card" style="padding: 14px 16px; border: 1px solid rgba(0,0,0,0.08); border-radius: 14px; background: #f8fafc; text-align: center;">
              <p style="margin: 0; color: #475569; font-size: 14px;">
                Nhớ mật khẩu rồi?
                <router-link to="/dang-nhap" style="color: #15803d; font-weight: bold; text-decoration: none;">Đăng nhập tại đây</router-link>
              </p>
            </div>
          </div>

        </div>
      </div>
    </div>
  </section>
</template>
