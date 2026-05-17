<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import axios from 'axios'

const route = useRoute()
const authStore = useAuthStore()
const store = ref(null)

// Form states
const noiDung = ref('')
const soSao = ref(5)
const fileAnhs = ref([])

// Lightbox states (Hệ thống phóng to ảnh trượt vòng lặp từ file gốc của sếp)
const lightboxVisible = ref(false)
const currentLightboxIndex = ref(0)
const galleryImages = ref([]) // Chứa danh sách ảnh để chạy slide

const taiChiTietCuaHang = async () => {
  try {
    const res = await axios.get(`http://localhost:8000/store/api/locations/${route.params.id}/`)
    store.value = res.data
  } catch (e) {
    console.error('Lỗi tải thông tin chi nhánh:', e)
  }
}

onMounted(() => {
  taiChiTietCuaHang()
  
  // Lắng nghe sự kiện bàn phím cứng cho Lightbox đúng bài mẫu gốc
  window.addEventListener('keydown', (event) => {
    if (!lightboxVisible.value) return
    if (event.key === "Escape") closeLightbox()
    if (event.key === "ArrowRight") changeLightboxImage(1)
    if (event.key === "ArrowLeft") changeLightboxImage(-1)
  })
})

const chonFileAnhs = (event) => {
  fileAnhs.value = Array.from(event.target.files)
}

const guiDanhGiaCuaHang = async () => {
  if (!noiDung.value.trim()) return alert('Sếp viết vài chữ đánh giá đã nhé!')
  
  const formData = new FormData()
  formData.append('tai_khoan_id', authStore.user.id)
  formData.append('noi_dung', noiDung.value)
  formData.append('so_sao', soSao.value)
  
  fileAnhs.value.forEach(file => {
    formData.append('hinh_anh_danh_gia', file)
  })

  try {
    await axios.post(`http://localhost:8000/store/api/locations/${store.value.id}/comment/add/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    alert('🎉 Đã gửi đánh giá đa phương tiện kèm ảnh thực tế thành công!')
    noiDung.value = ''
    fileAnhs.value = []
    taiChiTietCuaHang()
  } catch (e) {
    alert('Gửi đánh giá thất bại sếp ơi!')
  }
}

// BẬT LIGHTBOX PHÓNG TO ẢNH TRƯỢT VÒNG LẶP
const openLightbox = (commentImages, initialIndex) => {
  galleryImages.value = commentImages.map(url => ({ src: url }))
  currentLightboxIndex.value = initialIndex
  lightboxVisible.value = true
}

const closeLightbox = () => {
  lightboxVisible.value = false
}

const changeLightboxImage = (step) => {
  if (galleryImages.value.length === 0) return
  currentLightboxIndex.value = (currentLightboxIndex.value + step + galleryImages.value.length) % galleryImages.value.length
}
</script>

<template>
  <div v-if="store" class="store-detail-container" style="text-align: left;">
    <router-link to="/cua-hang" class="back-btn">← Quay lại danh sách</router-link>

    <div class="store-main-card">
      <div class="store-info-box">
        <h1 style="color: #008a37; font-size: 24px; font-weight: 800; margin-top: 0;">🏪 {{ store.ten_chi_nhanh }}</h1>
        <div style="margin: 15px 0; font-size: 15px; color: #475569; line-height: 1.8;">
          <p>📍 <strong>Địa chỉ:</strong> {{ store.dia_chi }}</p>
          <p>📞 <strong>Điện thoại liên hệ:</strong> {{ store.dien_thoai || '1900.1908' }}</p>
          <p>⏰ <strong>Thời gian phục vụ:</strong> Mở cửa từ 6:00 đến 22:00 (Kể cả CN và ngày lễ)</p>
        </div>
      </div>
      
      <div class="store-image-box" style="background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); display: flex; align-items: center; justify-content: center; border-radius: 18px; border: 1px solid #e5e7eb;">
        <div style="text-align: center; color: #16a34a; padding: 20px;">
          <span style="font-size: 48px;">🥦</span>
          <h3 style="margin: 10px 0 0 0;">Nông sản tươi xanh mỗi ngày</h3>
        </div>
      </div>
    </div>

    <div v-if="authStore.user" class="card-review-form" style="background: white; border-radius: 20px; padding: 25px; margin-top: 25px; border: 1px solid #e5e7eb; box-shadow: 0 4px 12px rgba(0,0,0,0.03);">
      <h3 style="margin-top:0; color: #1e293b;">✍️ Đăng đánh giá thực tế của sếp về siêu thị này</h3>
      <div style="margin-bottom: 15px;">
        <label style="font-weight: bold; font-size: 14px; margin-right: 10px;">Chọn mức độ hài lòng:</label>
        <select v-model="soSao" style="padding: 8px 12px; border-radius: 6px; border: 1px solid #cbd5e1; outline: none;">
          <option :value="5">⭐⭐⭐⭐⭐ 5 Sao (Tuyệt vời)</option>
          <option :value="4">⭐⭐⭐⭐ 4 Sao (Rất tốt)</option>
          <option :value="3">⭐⭐⭐ 3 Sao (Bình thường)</option>
        </select>
      </div>
      <textarea v-model="noiDung" style="width: 100%; padding: 12px; border-radius: 8px; border: 1px solid #cbd5e1; outline: none; resize: none;" rows="3" placeholder="Nhập cảm nhận mua sắm tại quầy, thái độ phục vụ của nhân viên thu ngân..."></textarea>
      
      <div style="margin-top: 15px; background: #f8fafc; padding: 15px; border-radius: 8px; border: 1px dashed #cbd5e1;">
        <label style="display: block; font-weight: bold; font-size: 14px; margin-bottom: 8px; color: #475569;">📸 Tải lên hình ảnh chụp thực tế tại quầy siêu thị (Chọn nhiều ảnh cùng lúc):</label>
        <input type="file" @change="chonFileAnhs" multiple accept="image/*" style="font-size: 14px;" />
      </div>

      <button @click="guiDanhGiaCuaHang" style="margin-top: 15px; background: #008a37; color: white; border: none; padding: 12px 24px; font-weight: bold; border-radius: 8px; cursor: pointer; box-shadow: 0 4px 10px rgba(0,138,55,0.2);">GỬI ĐÁNH GIÁ ĐA PHƯƠNG TIỆN</button>
    </div>

    <div class="comments-section-wrapper" style="background: white; border-radius: 20px; padding: 30px; margin-top: 25px; border: 1px solid #e5e7eb;">
      <h3 style="margin-top:0; border-bottom: 2px solid #008a37; padding-bottom: 10px; margin-bottom: 20px;">Ý kiến từ người mua sắm ({{ store.comments?.length || 0 }})</h3>
      <div v-if="store.comments?.length === 0" style="text-align: center; color: #94a3b8; padding: 20px;">Chưa có review hình ảnh nào cho chi nhánh này sếp ơi!</div>
      
      <div v-for="cm in store.comments" :key="cm.id" class="comment-item-box" style="padding: 20px 0; border-bottom: 1px solid #f1f5f9;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <strong style="font-size: 15px; color: #1e293b;">🧔 {{ cm.ten_nguoi_dung }}</strong>
          <span style="color: #f59e0b;">{{ '★'.repeat(cm.so_sao) }}{{ '☆'.repeat(5 - cm.so_sao) }}</span>
        </div>
        <p style="margin: 10px 0; color: #334155; font-size: 14px; line-height: 1.5;">{{ cm.noi_dung }}</p>
        
        <div v-if="cm.hinh_anhs && cm.hinh_anhs.length > 0" class="comment-photo-grid" style="display: flex; gap: 10px; flex-wrap: wrap; margin: 12px 0;">
          <img 
            v-for="(imgUrl, idx) in cm.hinh_anhs" 
            :key="idx" 
            :src="imgUrl" 
            @click="openLightbox(cm.hinh_anhs, idx)" 
            style="width: 90px; height: 90px; object-fit: cover; border-radius: 8px; border: 1px solid #e2e8f0; cursor: pointer; transition: transform 0.2s;"
            class="thumb-review-img"
          />
        </div>
        
        <div style="font-size: 12px; color: #94a3b8;">📅 Đăng tải lúc: {{ cm.created_at }}</div>
      </div>
    </div>

    <div v-if="lightboxVisible" class="custom-lightbox-overlay" @click="closeLightbox">
      <span class="close-lightbox-btn" @click="closeLightbox">×</span>
      <button class="lightbox-nav-btn prev-btn" @click.stopPropagation="changeLightboxImage(-1)">&#10094;</button>
      <div class="lightbox-content-box" @click.stopPropagation>
        <img :src="galleryImages[currentLightboxIndex]?.src" class="lightbox-main-img" id="lightbox-main-img" />
      </div>
      <button class="lightbox-nav-btn next-btn" @click.stopPropagation="changeLightboxImage(1)">&#10095;</button>
    </div>
  </div>
</template>

<style scoped>
/* CSS ĐẶC CHỦNG CHIA LƯỚI KHUNG GỐC ĐỒ ÁN */
.store-detail-container { max-width: 1100px; margin: 24px auto; padding: 0 16px 40px; line-height: 1.6; }
.back-btn { display: inline-block; margin-bottom: 18px; background: #f39c12; color: #fff; padding: 10px 14px; text-decoration: none; border-radius: 10px; font-weight: 600; box-shadow: 0 2px 6px rgba(243,156,18,0.3); }
.store-main-card { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; background: #fff; border: 1px solid #e5e7eb; border-radius: 20px; padding: 24px; box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06); }
.thumb-review-img:hover { transform: scale(1.05); box-shadow: 0 4px 10px rgba(0,0,0,0.1); }

/* BỘ CSS CHO LIGHTBOX OVERLAY PHÓNG TO ẢNH TRƯỢT VÒNG LẶP */
.custom-lightbox-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(15, 23, 42, 0.95); display: flex; align-items: center; justify-content: center; z-index: 99999; }
.lightbox-content-box { max-width: 85%; max-height: 85%; display: flex; align-items: center; justify-content: center; }
.lightbox-main-img { max-width: 100%; max-height: 80vh; object-fit: contain; border-radius: 8px; border: 3px solid white; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
.close-lightbox-btn { position: absolute; top: 25px; right: 35px; color: #fff; font-size: 48px; font-weight: bold; cursor: pointer; transition: 0.2s; user-select: none; }
.close-lightbox-btn:hover { color: #ef4444; }
.lightbox-nav-btn { position: absolute; top: 50%; transform: translateY(-50%); background: rgba(255, 255, 255, 0.15); border: none; color: white; font-size: 36px; padding: 16px 22px; cursor: pointer; border-radius: 12px; transition: 0.2s; user-select: none; }
.lightbox-nav-btn:hover { background: rgba(255, 255, 255, 0.3); color: #ffd400; }
.prev-btn { left: 40px; }
.next-btn { right: 40px; }
</style>