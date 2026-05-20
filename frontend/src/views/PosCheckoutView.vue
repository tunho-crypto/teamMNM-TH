<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

// Giả lập state dùng Pinia hoặc biến cục bộ cho đơn POS
const posCart = ref([])
const tienKhachDua = ref(0)

const totalValue = computed(() => {
  return posCart.value.reduce((sum, item) => sum + (item.don_gia * item.so_luong_mua), 0)
})

const changeDue = computed(() => {
  const change = tienKhachDua.value - totalValue.value
  return change > 0 ? change : 0
})

const submitPosCheckout = async () => {
  if (posCart.value.length === 0) return alert('Đơn tại quầy đang trống!')
  if (tienKhachDua.value < totalValue.value) {
    return alert('Tiền khách đưa phải lớn hơn hoặc bằng tổng tiền.')
  }

  try {
    const res = await axios.post('http://localhost:8000/store/api/pos/checkout/', {
      tien_khach_dua: tienKhachDua.value,
      items: posCart.value
    })
    if (res.data.success) {
      // Lưu hóa đơn tạm vào localStorage để trang In Biên Lai lấy dữ liệu
      localStorage.setItem('pos_last_invoice', JSON.stringify(res.data.invoice_data))
      router.push('/pos/hoa-don')
    }
  } catch (error) {
    alert(error.response?.data?.error || 'Lỗi thanh toán POS!')
  }
}

const formatVND = (tien) => Number(tien || 0).toLocaleString('vi-VN') + 'đ'
</script>

<template>
  <div style="background: #f5f7fb; min-height: 100vh; padding: 18px; text-align: left;">
    <div class="topbar" style="max-width: 1400px; margin: 0 auto; display: flex; justify-content: space-between; margin-bottom: 16px;">
      <router-link to="/" class="back-home" style="padding: 8px 12px; background: #fff; border-radius: 10px; border: 1px solid #e5e7eb; text-decoration: none; color: #1f2937;">← Về trang chủ</router-link>
      <h2 style="margin: 0; font-size: 20px; font-weight: 800;">🛒 HỆ THỐNG THU NGÂN TẠI QUẦY</h2>
    </div>

    <div style="max-width: 1400px; margin: 0 auto; display: grid; grid-template-columns: 2fr 1fr; gap: 20px;">
      
      <div style="background: #fff; border-radius: 16px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.02);">
        <input type="text" placeholder="🔍 Quét mã vạch hoặc tìm tên sản phẩm..." style="width: 100%; padding: 12px; border-radius: 8px; border: 1px solid #ddd; margin-bottom: 20px;" />
        <div style="padding: 20px; text-align: center; color: #6b7280;">Khu vực hiển thị sản phẩm...</div>
      </div>

      <div style="background: #fff; border-radius: 16px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.02);">
        <h3 style="margin-top: 0; border-bottom: 1px solid #eee; padding-bottom: 10px;">Chi tiết hóa đơn</h3>
        
        <div style="min-height: 200px;">
          <div v-if="posCart.length === 0" style="text-align: center; color: #9ca3af; margin-top: 50px;">Đơn hàng trống</div>
          </div>

        <form @submit.prevent="submitPosCheckout" style="border-top: 1px dashed #ccc; padding-top: 15px; margin-top: 15px;">
          <div style="display: flex; justify-content: space-between; margin-bottom: 10px; font-weight: bold;">
            <span>Tổng tiền:</span>
            <span style="color: red; font-size: 18px;">{{ formatVND(totalValue) }}</span>
          </div>

          <div style="margin-bottom: 10px;">
            <label style="display: block; margin-bottom: 5px; color: #4b5563;">Tiền khách đưa (VNĐ):</label>
            <input type="number" v-model="tienKhachDua" style="width: 100%; padding: 10px; border-radius: 6px; border: 1px solid #ccc;" required />
          </div>

          <div style="display: flex; justify-content: space-between; margin-bottom: 15px; color: #059669; font-weight: bold;">
            <span>Tiền hoàn lại:</span>
            <span>{{ formatVND(changeDue) }}</span>
          </div>

          <button type="submit" style="width: 100%; padding: 12px; background: #008a37; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer;">
            XÁC NHẬN THANH TOÁN
          </button>
        </form>
      </div>
    </div>
  </div>
</template>