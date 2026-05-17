<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useCartStore } from '../stores/cart'

const cartStore = useCartStore()
const danhSachSanPham = ref([])
const danhSachDanhMuc = ref([])
const toasts = ref([]) // Quản lý danh sách thông báo Toast

onMounted(async () => {
  try {
    const resProducts = await axios.get('http://localhost:8000/store/api/products/')
    danhSachSanPham.value = resProducts.data

    const resCategories = await axios.get('http://localhost:8000/store/api/categories/')
    danhSachDanhMuc.value = resCategories.data
  } catch (error) {
    console.error('Lỗi API:', error)
  }
})

const productsKM = computed(() => danhSachSanPham.value.filter(sp => sp.is_khuyen_mai).slice(0, 10))
const productsNew = computed(() => [...danhSachSanPham.value].reverse().slice(0, 10))
const formatVND = (tien) => Number(tien || 0).toLocaleString('vi-VN') + 'đ'

// Hàm hiển thị Toast thông báo xịn xò của sếp
const showToast = (message) => {
  const id = Date.now()
  toasts.value.push({ id, message })
  setTimeout(() => {
    toasts.value = toasts.value.filter(t => t.id !== id)
  }, 3000)
}

const handleAddToCart = (product) => {
  cartStore.themVaoGio(product)
  showToast(`Đã thêm ${product.ten_san_pham} vào giỏ hàng!`)
}
</script>

<template>
  <div style="text-align: left;">
    <section class="home-hero">
        <div class="container">
            <div class="home-hero-box modern-hero-box">
                <div class="hero-left">
                    <span class="hero-tag">Siêu thị online cho gia đình</span>
                    <h1 style="color:black">Mua sắm thực phẩm tươi ngon mỗi ngày</h1>
                    <p style="color:black">Đầy đủ rau củ, thịt cá, đồ uống, gia vị và các mặt hàng thiết yếu với giá hợp lý, dễ chọn, dễ mua và giao nhanh tận nơi.</p>

                    <div class="hero-actions">
                        <router-link to="/san-pham" class="hero-main-btn" style="color:black">Mua ngay</router-link>
                    </div>

                    <div style="color:black" class="hero-mini-stats">
                        <div class="hero-stat"><strong>Nhiều mặt hàng</strong><span>Thiết yếu gia đình</span></div>
                        <div class="hero-stat"><strong>Giá dễ mua</strong><span>Ưu đãi mỗi ngày</span></div>
                        <div class="hero-stat"><strong>Giao nhanh</strong><span>Tiết kiệm thời gian</span></div>
                    </div>
                </div>

                <div style="color:black" class="hero-right">
                    <div class="hero-highlight-card">
                        <span class="highlight-badge">Ưu đãi hôm nay</span>
                        <h3>Đi chợ online nhanh hơn</h3>
                        <p>Chọn món dễ hơn với danh mục rõ ràng, sản phẩm nổi bật và giá hiển thị dễ nhìn.</p>

                        <div class="hero-info-list">
                            <div class="hero-info-card"><strong>Rau củ tươi</strong><span>Phù hợp cho bữa cơm gia đình</span></div>
                            <div class="hero-info-card"><strong>Đồ uống & gia vị</strong><span>Dễ tìm, dễ chọn, đủ hàng</span></div>
                            <div class="hero-info-card"><strong>Khuyến mãi hấp dẫn</strong><span>Nhiều sản phẩm mức giá tốt</span></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section class="home-categories">
        <div class="container">
            <div class="section-head">
                <div><span class="section-label">Mua sắm nhanh</span><h2>Danh mục nổi bật</h2></div>
                <router-link to="/san-pham" class="section-link">Xem tất cả</router-link>
            </div>
            <div class="category-grid home-category-grid improved-category-grid">
                <router-link v-for="dm in danhSachDanhMuc" :key="dm.id" :to="'/san-pham?category=' + dm.id" class="category-card better-category-card">
                    <span class="category-icon">🛒</span><span class="category-name">{{ dm.ten_loai }}</span>
                </router-link>
            </div>
        </div>
    </section>

    <section class="featured-products home-product-section">
        <div class="container">
            <div class="section-head">
                <div><span class="section-label">Giá tốt hôm nay</span><h2>Sản phẩm khuyến mãi</h2></div>
                <router-link to="/san-pham" class="section-link">Xem thêm</router-link>
            </div>
            <div class="product-grid product-grid-4">
                <div v-for="product in productsKM" :key="product.id" class="product-card better-product-card">
                    <router-link :to="'/san-pham/' + product.id" class="product-image-wrap">
                        <img v-if="product.hinh_anh_url" :src="product.hinh_anh_url" class="product-image">
                        <div v-else class="product-image placeholder-image">Chưa có ảnh</div>
                        <span class="product-badge-sale">Sale</span>
                    </router-link>

                    <div class="product-info">
                        <div class="product-category">Khuyến mãi</div>
                        <h3 class="product-name"><router-link :to="'/san-pham/' + product.id">{{ product.ten_san_pham }}</router-link></h3>
                        <p class="product-desc">Sản phẩm đang có ưu đãi, phù hợp nhu cầu hàng ngày.</p>
                        
                        <div class="product-price-row">
                            <div class="price-group">
                                <span class="old-price" v-if="product.gia_goc">{{ formatVND(product.gia_goc) }}</span>
                                <span class="price">{{ formatVND(product.don_gia) }}</span>
                            </div>
                            <span class="sale-badge">Giá tốt</span>
                        </div>

                        <div style="margin-top: 8px; font-size: 13px; margin-bottom: 10px;">
                            <div v-if="product.so_luong > 0" style="color: #0b9445; font-weight: bold;">✓ Còn hàng ({{ product.so_luong }})</div>
                            <div v-else style="color: #d8232a; font-weight: bold;">✕ Tạm hết hàng</div>
                        </div>

                        <div class="product-actions">
                            <router-link :to="'/san-pham/' + product.id" class="btn-detail">Xem chi tiết</router-link>
                            <button @click="handleAddToCart(product)" class="btn-add">Thêm giỏ</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <div id="toast-container">
      <div v-for="toast in toasts" :key="toast.id" class="toast-msg show">
        🛒 <span>{{ toast.message }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.product-card { display: flex; flex-direction: column; height: 100%; }
.product-info { display: flex; flex-direction: column; flex-grow: 1; }
.product-actions { margin-top: auto; display: flex; justify-content: space-between; gap: 10px; padding-top: 15px; }
.product-actions .btn-detail, .product-actions .btn-add { flex: 1; text-align: center; padding: 8px 0; border: none; cursor: pointer; border-radius: 4px;}
.btn-add { background-color: #008848; color: white; font-weight: bold; }

/* CSS TOAST MESSAGE TỪ BẢN GỐC */
#toast-container { position: fixed; bottom: 30px; right: 30px; z-index: 9999; display: flex; flex-direction: column; gap: 10px; }
.toast-msg { background-color: #008a37; color: white; padding: 12px 24px; border-radius: 8px; box-shadow: 0 5px 15px rgba(0,0,0,0.2); font-weight: 600; font-size: 14px; display: flex; align-items: center; gap: 8px; animation: slideIn 0.3s ease forwards; }
@keyframes slideIn { from { opacity: 0; transform: translateX(100%); } to { opacity: 1; transform: translateX(0); } }
</style>