<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { useCartStore } from '../stores/cart'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const cartStore = useCartStore()
const authStore = useAuthStore()

const product = ref(null)
const images = ref([])
const binhLuans = ref([])
const activeImageIndex = ref(0)

// Bình luận & Đánh giá state
const commentContent = ref('')
const selectedStars = ref(5)
const editingCommentId = ref(null)
const activeMenuId = ref(null)

const loadProductData = async () => {
  try {
    const id = route.params.id
    const resDetail = await axios.get(`http://localhost:8000/store/api/products/${id}/`)
    product.value = resDetail.data
    
    // Đồng bộ Gallery ảnh phụ theo cấu trúc mẫu
    images.value = resDetail.data.hinh_anh_url ? [{ image: { url: resDetail.data.hinh_anh_url } }] : []
    
    const resComments = await axios.get(`http://localhost:8000/store/api/products/${id}/comments/`)
    binhLuans.value = resComments.data
  } catch (error) {
    console.error('Lỗi tải dữ liệu chi tiết:', error)
  }
}

onMounted(() => {
  loadProductData()
})

const changeSlide = (step) => {
  if (images.value.length === 0) return
  activeImageIndex.value = (activeImageIndex.value + step + images.value.length) % images.value.length
}

const toggleCommentMenu = (event, commentId) => {
  event.stopPropagation()
  activeMenuId.value = activeMenuId.value === commentId ? null : commentId
}

const startEditComment = (bl) => {
  editingCommentId.value = bl.id
  commentContent.value = bl.noi_dung
  selectedStars.value = bl.so_sao
  activeMenuId.value = null
}

const cancelEditComment = () => {
  editingCommentId.value = null
  commentContent.value = ''
  selectedStars.value = 5
}

const submitComment = async () => {
  if (!commentContent.value.trim()) return alert('Vui lòng nhập nội dung bình luận.')
  const id = route.params.id
  try {
    if (editingCommentId.value) {
      await axios.post(`http://localhost:8000/store/api/products/comments/edit/${editingCommentId.value}/`, {
        noi_dung: commentContent.value,
        so_sao: selectedStars.value
      })
      alert('Đã cập nhật bình luận thành công!')
    } else {
      await axios.post(`http://localhost:8000/store/api/products/${id}/comments/add/`, {
        tai_khoan_id: authStore.user.id,
        noi_dung: commentContent.value,
        so_sao: selectedStars.value
      })
      alert('Đã gửi bình luận thành công!')
    }
    cancelEditComment()
    loadProductData()
  } catch (e) {
    alert('Thao tác thất bại!')
  }
}

const deleteComment = async (commentId) => {
  if (!confirm('Sếp có chắc muốn xóa bình luận này không?')) return
  try {
    await axios.delete(`http://localhost:8000/store/api/products/comments/delete/${commentId}/`)
    alert('Đã xóa bình luận thành công!')
    loadProductData()
  } catch (e) {
    alert('Lỗi hệ thống!')
  }
}

const formatVND = (tien) => Number(tien || 0).toLocaleString('vi-VN') + 'đ'
</script>

<template>
  <section class="detail-page" style="text-align: left; padding: 20px 0;" v-if="product">
    <div class="container">
      <div class="breadcrumb" style="font-size: 14px; color: #64748b; margin-bottom: 20px;">
        <router-link to="/" style="color: #008a37; text-decoration: none;">Trang chủ</router-link> <span>/</span>
        <router-link to="/san-pham" style="color: #008a37; text-decoration: none;">Sản phẩm</router-link> <span>/</span>
        <span>{{ product.ten_san_pham }}</span>
      </div>

      <div class="detail-wrapper" style="display: grid; grid-template-columns: 1fr 1fr; gap: 40px;">
        <div class="detail-gallery-card">
          <div class="detail-badge-wrap" style="margin-bottom: 12px; display: flex; gap: 8px;">
            <span v-if="product.is_khuyen_mai" class="detail-sale-badge" style="background: #ef4444; color: white; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 13px;">Khuyến mãi</span>
            <span class="detail-stock-badge in-stock" style="background: #dcfce7; color: #15803d; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 13px;">Còn hàng</span>
          </div>

          <div class="detail-image-box">
            <button v-if="images.length > 1" type="button" class="gallery-nav prev" @click="changeSlide(-1)">&#10094;</button>
            <img :src="images[activeImageIndex]?.image?.url || product.hinh_anh_url" :alt="product.ten_san_pham" class="detail-main-image" />
            <button v-if="images.length > 1" type="button" class="gallery-nav next" @click="changeSlide(1)">&#10095;</button>
          </div>
        </div>

        <div class="detail-info-card" style="background: #fff; padding: 30px; border-radius: 20px; border: 1px solid #e5e7eb; box-shadow: 0 4px 12px rgba(0,0,0,0.03);">
          <div class="detail-category-line" style="color: #64748b; font-size: 14px;">Danh mục: <strong style="color: #008a37;">{{ product.loai_ten || 'Rau củ quả' }}</strong></div>
          <h1 class="detail-title" style="font-size: 28px; color: #1e293b; margin: 10px 0 15px 0; font-weight: 800;">{{ product.ten_san_pham }}</h1>
          <p class="detail-desc" style="color: #475569; font-size: 15px; line-height: 1.6; margin-bottom: 25px;">{{ product.mo_ta || 'Sản phẩm chất lượng cao, an toàn vệ sinh thực phẩm.' }}</p>

          <div class="detail-price-box" style="background: #f8fafc; padding: 15px 20px; border-radius: 12px; margin-bottom: 25px;">
            <span class="detail-price-sale" style="font-size: 26px; color: #ef4444; font-weight: 900;">{{ formatVND(product.don_gia) }}</span>
          </div>

          <button type="button" @click="cartStore.themVaoGio(product)" class="btn-add-to-cart-vvip">
            🛒 THÊM VÀO GIỎ HÀNG NGAY
          </button>
        </div>
      </div>

      <section class="product-extra-section" style="margin-top: 40px;">
        <div class="product-extra-card" style="background: white; border-radius: 20px; padding: 30px; border: 1px solid #e5e7eb; box-shadow: 0 4px 12px rgba(0,0,0,0.03);">
          <h2 class="extra-title" style="margin-top:0; font-size: 20px; color: #1e293b; border-bottom: 2px solid #008a37; padding-bottom: 10px; margin-bottom: 20px;">Thông tin chi tiết sản phẩm</h2>
          <table class="extra-info-table" style="width: 100%; border-collapse: collapse;">
            <tbody>
              <tr style="border-bottom: 1px solid #f1f5f9;"><th style="padding: 12px; text-align: left; background: #f8fafc; width: 220px; font-weight: bold; color: #475569;">Thành phần</th><td style="padding: 12px; color: #334155;">{{ product.thanh_phan || '100% tự nhiên sạch sẽ' }}</td></tr>
              <tr style="border-bottom: 1px solid #f1f5f9;"><th style="padding: 12px; text-align: left; background: #f8fafc; font-weight: bold; color: #475569;">Bảo quản</th><td style="padding: 12px; color: #334155;">{{ product.bao_quan || 'Nơi khô ráo thoáng mát hoặc ngăn mát tủ lạnh' }}</td></tr>
              <tr style="border-bottom: 1px solid #f1f5f9;"><th style="padding: 12px; text-align: left; background: #f8fafc; font-weight: bold; color: #475569;">Quy cách đóng gói</th><td style="padding: 12px; color: #334155;">{{ product.quy_cach_dong_goi || 'Đóng khay túi màng co bọc bọc' }}</td></tr>
              <tr style="border-bottom: 1px solid #f1f5f9;"><th style="padding: 12px; text-align: left; background: #f8fafc; font-weight: bold; color: #475569;">Xuất xứ</th><td style="padding: 12px; color: #334155;">{{ product.xuat_xu || 'Việt Nam' }}</td></tr>
              <tr><th style="padding: 12px; text-align: left; background: #f8fafc; font-weight: bold; color: #475569;">Hạn sử dụng</th><td style="padding: 12px; color: #334155;">{{ product.han_su_dung || 'Xem trên bao bì sản phẩm' }}</td></tr>
            </tbody>
          </table>
        </div>
      </section>

      <section class="product-review-section" style="margin-top: 40px; background: white; border-radius: 20px; padding: 30px; border: 1px solid #e5e7eb;">
        <div class="review-comment-section" style="display: grid; grid-template-columns: 1fr; gap: 30px;">
          
          <div class="review-rating-box" style="background: #f8fafc; padding: 20px; border-radius: 12px;">
            <h2 style="margin-top:0; font-size: 18px; color: #1e293b;">Đánh giá sản phẩm này</h2>
            <div v-if="authStore.user" style="margin-top: 15px;">
              <div class="rating-stars" style="display: flex; gap: 5px; margin-bottom: 15px;">
                <span v-for="star in 5" :key="star" @click="selectedStars = star" style="font-size: 32px; cursor: pointer; color: #f59e0b;">
                  {{ star <= selectedStars ? '★' : '☆' }}
                </span>
              </div>
              <textarea v-model="commentContent" style="width:100%; padding:12px; border-radius:8px; border:1px solid #cbd5e1; outline:none; resize:none;" rows="3" placeholder="Mời sếp viết bình luận..."></textarea>
              <button @click="submitComment" style="margin-top:10px; background:#008a37; color:white; border:none; padding:10px 20px; font-weight:bold; border-radius:6px; cursor:pointer;">{{ editingCommentId ? 'Lưu chỉnh sửa' : 'Gửi đánh giá' }}</button>
            </div>
            <div v-else style="text-align: center; color: #64748b; font-size: 14px; padding: 10px 0;">🔒 Vui lòng đăng nhập để viết đánh giá.</div>
          </div>

          <div class="comment-list-box">
            <h3 style="margin-top:0; border-bottom: 1px solid #eee; padding-bottom: 10px;">Bình luận ({{ binhLuans.length }})</h3>
            <div v-for="item in binhLuans" :key="item.id" class="comment-item" style="padding: 15px 0; border-bottom: 1px solid #f1f5f9; position: relative;">
              <div class="comment-topbar" style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                  <span class="comment-author" style="font-weight: bold; color: #1e293b; margin-right: 10px;">🧔 {{ item.ten_nguoi_dung }}</span>
                  <span style="color: #f59e0b;">{{ '★'.repeat(item.so_sao) }}{{ '☆'.repeat(5 - item.so_sao) }}</span>
                </div>
                
                <div v-if="authStore.user && authStore.user.id === item.tai_khoan_id" style="position: relative;">
                  <button type="button" @click="toggleCommentMenu($event, item.id)" style="background: none; border: none; font-size: 18px; cursor: pointer; color: #94a3b8;">⋯</button>
                  <div v-if="activeMenuId === item.id" style="position: absolute; right: 0; top: 20px; background: white; border: 1px solid #e2e8f0; border-radius: 6px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); z-index: 10; width: 100px;">
                    <a href="#" @click.prevent="startEditComment(item)" style="display: block; padding: 8px 12px; color: #334155; text-decoration: none; font-size: 13px; font-weight: bold;">✏️ Sửa</a>
                    <button type="button" @click="deleteComment(item.id)" style="display: block; width: 100%; text-align: left; padding: 8px 12px; color: #ef4444; background: none; border: none; font-size: 13px; font-weight: bold; cursor: pointer; border-top: 1px solid #f1f5f9;">🗑️ Xóa</button>
                  </div>
                </div>
              </div>
              <p style="margin: 8px 0; color: #334155; font-size: 14px;">{{ item.noi_dung }}</p>
              <div style="font-size: 12px; color: #94a3b8;">📅 {{ item.ngay_binh_luan || 'Vừa xong' }}</div>
            </div>
          </div>

        </div>
      </section>
    </div>
  </section>
</template>

<style scoped>
/* STYLE PHÒNG TRƯNG BÀY KHỚP MẪU CHUẨN ĐÉT */
.detail-image-box { position: relative; border: 1px solid #e5e7eb; border-radius: 20px; background: #fff; padding: 24px; min-height: 420px; display: flex; align-items: center; justify-content: center; overflow: hidden; }
.detail-main-image { width: 100%; max-height: 460px; object-fit: contain; display: block; }
.gallery-nav { position: absolute; top: 50%; transform: translateY(-50%); width: 46px; height: 90px; border: none; background: rgba(148, 153, 165, 0.65); color: #fff; font-size: 28px; cursor: pointer; z-index: 2; border-radius: 10px; display: flex; align-items: center; justify-content: center; }
.gallery-nav.prev { left: 12px; }
.gallery-nav.next { right: 12px; }

/* THIẾT KẾ NÚT BẤM MUA HÀNG ĐỒ SỘ CỰC ĐẸP */
.btn-add-to-cart-vvip { width: 100%; background: linear-gradient(135deg, #8cc12e 0%, #7ab223 100%); color: white; border: none; padding: 15px; border-radius: 12px; font-size: 16px; font-weight: bold; cursor: pointer; box-shadow: 0 4px 15px rgba(140,193,46,0.35); transition: all 0.2s ease; }
.btn-add-to-cart-vvip:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(140,193,46,0.45); }
.btn-add-to-cart-vvip:active { transform: translateY(0); }
</style>