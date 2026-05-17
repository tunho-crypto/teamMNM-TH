<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { useCartStore } from '../stores/cart'

const cartStore = useCartStore()
const route = useRoute()
const danhSachSanPham = ref([])
const danhSachDanhMuc = ref([])
const toasts = ref([]) // Mảng chứa các thông báo giỏ hàng

const tuKhoa = ref(route.query.q || '')
const selectedCategory = ref(route.query.category || '')
const selectedPrice = ref(route.query.price || '')

onMounted(async () => {
  const [resProd, resCat] = await Promise.all([
    axios.get('http://localhost:8000/store/api/products/'),
    axios.get('http://localhost:8000/store/api/categories/')
  ])
  danhSachSanPham.value = resProd.data
  danhSachDanhMuc.value = resCat.data
})

const sanPhamHienThi = computed(() => {
  return danhSachSanPham.value.filter(sp => {
    let matchTuKhoa = sp.ten_san_pham.toLowerCase().includes(tuKhoa.value.toLowerCase())
    let matchCategory = selectedCategory.value ? String(sp.loai) === String(selectedCategory.value) : true
    
    let matchPrice = true
    if (selectedPrice.value === 'under_50') matchPrice = Number(sp.don_gia) < 50000
    if (selectedPrice.value === '50_100') matchPrice = Number(sp.don_gia) >= 50000 && Number(sp.don_gia) <= 100000
    if (selectedPrice.value === 'over_100') matchPrice = Number(sp.don_gia) > 100000

    return matchTuKhoa && matchCategory && matchPrice
  })
})

const formatVND = (tien) => Number(tien || 0).toLocaleString('vi-VN') + 'đ'

// HÀM HIỂN THỊ THÔNG BÁO TOAST TRƯỢT GÓC MÀN HÌNH
const handleAddToCart = (product) => {
  cartStore.themVaoGio(product)
  const id = Date.now()
  toasts.value.push({ id, message: `Đã thêm ${product.ten_san_pham} vào giỏ!` })
  
  // Tự động xóa thông báo sau 3 giây
  setTimeout(() => {
    toasts.value = toasts.value.filter(t => t.id !== id)
  }, 3000)
}
</script>

<template>
  <section class="listing-page" style="text-align: left;">
    <div class="container">
        <div class="breadcrumb" style="margin-top: 20px; font-size: 14px; color: #64748b;">
            <router-link to="/" style="text-decoration: none; color: #008a37; font-weight: bold;">Trang chủ</router-link> <span>/</span> <span>Sản phẩm</span>
        </div>

        <div class="listing-header-box" style="display: flex; justify-content: space-between; align-items: center; margin-top: 15px; margin-bottom: 30px; border-bottom: 2px solid #e5e7eb; padding-bottom: 15px;">
            <div>
                <h1 class="listing-title" style="margin: 0; color: #1f2937; font-size: 28px;">Tất cả sản phẩm</h1>
                <p class="listing-subtitle" style="margin: 5px 0 0 0; color: #64748b;">Mua sắm tiện lợi với nhiều mặt hàng thiết yếu cho gia đình.</p>
            </div>
            <div class="listing-count" style="background: #e2e8f0; padding: 6px 12px; border-radius: 20px; font-weight: bold; color: #334155;">{{ sanPhamHienThi.length }} sản phẩm</div>
        </div>

        <div class="listing-layout" style="display: grid; grid-template-columns: 250px 1fr; gap: 30px;">
            <aside class="filter-sidebar" style="background: #fff; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0; height: fit-content; position: sticky; top: 80px;">
                <h3 style="margin-top: 0; color: #1e293b; border-bottom: 1px solid #eee; padding-bottom: 10px;">Danh mục</h3>
                <ul style="list-style: none; padding: 0; margin: 0;">
                    <li style="margin-bottom: 10px;"><a href="#" @click.prevent="selectedCategory = ''" :class="{ 'active-category': !selectedCategory }" style="text-decoration: none; color: #475569;">Tất cả</a></li>
                    <li v-for="dm in danhSachDanhMuc" :key="dm.id" style="margin-bottom: 10px;">
                        <a href="#" @click.prevent="selectedCategory = dm.id" :class="{ 'active-category': selectedCategory == dm.id }" style="text-decoration: none; color: #475569;">{{ dm.ten_loai }}</a>
                    </li>
                </ul>
                <div class="price-filter" style="margin-top: 30px;">
                    <h3 style="color: #1e293b; border-bottom: 1px solid #eee; padding-bottom: 10px;">Lọc theo giá</h3>
                    <ul style="list-style: none; padding: 0; margin: 0;">
                        <li style="margin-bottom: 10px;"><a href="#" @click.prevent="selectedPrice = 'under_50'" :class="{ 'active-category': selectedPrice === 'under_50' }" style="text-decoration: none; color: #475569;">Dưới 50.000đ</a></li>
                        <li style="margin-bottom: 10px;"><a href="#" @click.prevent="selectedPrice = '50_100'" :class="{ 'active-category': selectedPrice === '50_100' }" style="text-decoration: none; color: #475569;">50.000đ - 100.000đ</a></li>
                        <li style="margin-bottom: 10px;"><a href="#" @click.prevent="selectedPrice = 'over_100'" :class="{ 'active-category': selectedPrice === 'over_100' }" style="text-decoration: none; color: #475569;">Trên 100.000đ</a></li>
                        <li style="margin-bottom: 10px;"><a href="#" @click.prevent="selectedPrice = ''" :class="{ 'active-category': !selectedPrice }" style="text-decoration: none; color: #475569;">Tất cả mức giá</a></li>
                    </ul>
                </div>
            </aside>

            <div class="listing-content">
                <div v-if="tuKhoa" class="search-result-info" style="margin-bottom: 20px; background: #f0fdf4; padding: 12px 20px; border-radius: 8px; color: #16a34a; font-weight: bold;">Kết quả tìm kiếm cho: <strong>"{{ tuKhoa }}"</strong></div>

                <div class="product-grid" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;">
                    <div v-for="product in sanPhamHienThi" :key="product.id" class="product-card" style="display: flex; flex-direction: column; background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px; transition: box-shadow 0.2s;">
                        <router-link :to="'/san-pham/' + product.id" class="product-image-wrap" style="position: relative; text-align: center; display: block; height: 180px;">
                            <img v-if="product.hinh_anh_url" :src="product.hinh_anh_url" class="product-image" style="width: 100%; height: 100%; object-fit: contain;">
                            <div v-else class="product-image placeholder-image" style="width: 100%; height: 100%; background: #f1f5f9; display: flex; align-items: center; justify-content: center; color: #94a3b8; border-radius: 8px;">Chưa có ảnh</div>
                            <span v-if="product.is_khuyen_mai" class="product-badge-sale" style="position: absolute; top: 10px; left: 10px; background: #ef4444; color: white; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: bold;">Sale</span>
                        </router-link>

                        <div class="product-info" style="display: flex; flex-direction: column; flex-grow: 1; margin-top: 15px;">
                            <h3 class="product-name" style="margin: 0 0 8px 0; font-size: 16px; line-height: 1.4;">
                                <router-link :to="'/san-pham/' + product.id" style="text-decoration: none; color: #1e293b;">{{ product.ten_san_pham }}</router-link>
                            </h3>
                            <p class="product-desc" style="margin: 0; font-size: 13px; color: #64748b; line-height: 1.5; flex-grow: 1;">{{ product.mo_ta || 'Sản phẩm thiết yếu cho gia đình.' }}</p>
                            
                            <div class="product-price-row" style="margin-top: 15px;">
                                <span class="price" style="color: #d8232a; font-size: 18px; font-weight: 800;">{{ formatVND(product.don_gia) }}</span>
                            </div>

                            <div class="product-actions">
                                <router-link :to="'/san-pham/' + product.id" class="btn-detail">Chi tiết</router-link>
                                <button type="button" @click="handleAddToCart(product)" class="btn-add">🛒 Thêm</button>
                            </div>
                        </div>
                    </div>
                    
                    <div v-if="sanPhamHienThi.length === 0" class="empty-box" style="grid-column: 1 / -1; text-align: center; padding: 40px; background: #fff; border-radius: 12px; border: 1px dashed #cbd5e1;">
                        <h3 style="color: #64748b;">Không tìm thấy sản phẩm phù hợp</h3>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div id="toast-container">
      <div v-for="toast in toasts" :key="toast.id" class="toast-msg show">
        🛒 <span>{{ toast.message }}</span>
      </div>
    </div>
  </section>
</template>

<style scoped>
.active-category { color: #008a37 !important; font-weight: 800; }

/* ========================================================= */
/* CSS TÚT TÁT LẠI KHỐI 2 NÚT BẤM (Chi tiết & Thêm giỏ) */
/* ========================================================= */
.product-actions { margin-top: auto; display: flex; justify-content: space-between; gap: 10px; padding-top: 15px; }
.product-actions .btn-detail, .product-actions .btn-add { flex: 1; text-align: center; padding: 10px 0; border-radius: 8px; font-weight: bold; cursor: pointer; transition: all 0.2s ease; font-size: 14px; text-decoration: none; display: flex; align-items: center; justify-content: center; gap: 5px; }

/* Nút Xem chi tiết: Viền xanh, chữ xanh, nền trắng */
.btn-detail { background: #fff; color: #008a37; border: 1px solid #008a37; }
.btn-detail:hover { background: #f0fdf4; }

/* Nút Thêm giỏ: Nền xanh, chữ trắng */
.btn-add { background: #008a37; color: white; border: 1px solid #008a37; }
.btn-add:hover { background: #00732e; }

/* CSS TOAST MESSAGE TRƯỢT GÓC BẢN GỐC CỦA SẾP */
#toast-container { position: fixed; bottom: 30px; right: 30px; z-index: 9999; display: flex; flex-direction: column; gap: 10px; }
.toast-msg { background-color: #008a37; color: white; padding: 12px 24px; border-radius: 8px; box-shadow: 0 5px 15px rgba(0,0,0,0.2); font-weight: 600; font-size: 14px; display: flex; align-items: center; gap: 8px; animation: slideIn 0.3s ease forwards; }
@keyframes slideIn { from { opacity: 0; transform: translateX(100%); } to { opacity: 1; transform: translateX(0); } }
</style>