<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import axios from 'axios'
import PaginationAdmin from '../components/PaginationAdmin.vue'

const products = ref([])
const categories = ref([])
const q = ref('')
const selectedCate = ref('')
const brokenImages = ref(new Set()) // Lưu id sản phẩm bị lỗi ảnh

const currentPage = ref(1)
const itemsPerPage = 10

const loadData = async () => {
  brokenImages.value = new Set() // Reset ảnh lỗi mỗi lần tải lại
  // 1. Tải danh sách sản phẩm (Tách riêng try/catch chống sập dây chuyền)
  try {
    const resProd = await axios.get(`http://localhost:8000/store/api/admin/products/?q=${q.value}&loai=${selectedCate.value}`)
    products.value = resProd.data
  } catch (error) {
    console.error('Lỗi tải sản phẩm:', error)
  }

  // 2. Tải danh mục phân loại
  try {
    const resCat = await axios.get('http://localhost:8000/store/api/categories/')
    categories.value = resCat.data
  } catch (error) {
    console.error('Lỗi tải danh mục:', error)
  }
  
  currentPage.value = 1
}

onMounted(() => loadData())

// Delay search để không bị giật lag
let timeout = null
const handleSearch = () => {
  clearTimeout(timeout)
  timeout = setTimeout(() => loadData(), 500)
}

watch([selectedCate], () => loadData())

const deleteProduct = async (id) => {
  if (!confirm('Sếp có chắc chắn muốn xóa sản phẩm này không?')) return
  try {
    await axios.delete(`http://localhost:8000/store/api/admin/products/delete/${id}/`)
    alert('Đã xóa thành công!')
    loadData()
  } catch (error) {
    alert('Không thể xóa sản phẩm này!')
  }
}

// Tính toán Phân trang
const totalPages = computed(() => Math.ceil(products.value.length / itemsPerPage))
const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return products.value.slice(start, start + itemsPerPage)
})
</script>

<template>
  <div>
    <div class="admin-toolbar" style="display: flex; justify-content: space-between; margin-bottom: 20px;">
      <div style="display: flex; gap: 10px;">
        <input type="text" v-model="q" @input="handleSearch" placeholder="🔍 Tìm tên sản phẩm..." style="padding: 10px; border-radius: 8px; border: 1px solid #ddd; width: 250px;" />
        <select v-model="selectedCate" style="padding: 10px; border-radius: 8px; border: 1px solid #ddd;">
          <option value="">Tất cả loại hàng</option>
          <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.ten_loai }}</option>
        </select>
      </div>
      <router-link to="/admin/san-pham/them" style="background: #16a34a; color: white; padding: 10px 16px; border-radius: 8px; text-decoration: none; font-weight: bold;">+ Thêm sản phẩm</router-link>
    </div>

    <table style="width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
      <thead style="background: #f8fafc; border-bottom: 2px solid #edf2f7; text-align: left;">
        <tr><th style="padding: 15px;">Ảnh</th><th>Tên sản phẩm</th><th>Loại</th><th>Đơn giá</th><th>SL Tồn</th><th>Thao tác</th></tr>
      </thead>
      <tbody>
        <tr v-for="p in paginatedProducts" :key="p.id" style="border-bottom: 1px solid #f1f5f9;">
          <td style="padding: 15px;">
            <img
              v-if="p.hinh_anh_url && !brokenImages.has(p.id)"
              :src="p.hinh_anh_url"
              @error="brokenImages.add(p.id)"
              style="width: 50px; height: 50px; object-fit: cover; border-radius: 6px; border: 1px solid #e2e8f0;"
            />
            <div v-else style="width: 50px; height: 50px; background: #f1f5f9; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 10px; color: #94a3b8; font-weight: bold; text-align: center; border: 1px dashed #cbd5e1;">No Image</div>
          </td>
          <td style="font-weight: bold; color: #1e293b;">{{ p.ten_san_pham }}</td>
          <td>
            <span style="background: #f1f5f9; padding: 4px 10px; border-radius: 6px; font-size: 13px;">{{ p.loai_ten }}</span>
          </td>
          <td style="font-size: 15px; font-weight: bold;">
            <template v-if="p.is_khuyen_mai">
              <span style="color: #d8232a;">{{ Number(p.gia_hien_thi).toLocaleString() }}đ</span>
              <span style="text-decoration: line-through; color: #94a3b8; font-size: 12px; margin-left: 4px;">{{ Number(p.don_gia).toLocaleString() }}đ</span>
              <span style="background: #fef2f2; color: #dc2626; font-size: 11px; padding: 2px 6px; border-radius: 4px; margin-left: 4px;">KM</span>
            </template>
            <span v-else style="color: #d8232a;">{{ Number(p.don_gia).toLocaleString() }}đ</span>
          </td>
          <td><strong style="color: #008a37;">{{ p.so_luong }}</strong></td>
          <td>
            <router-link :to="'/admin/san-pham/sua/' + p.id" style="color: #0288d1; font-weight: bold; text-decoration: none; margin-right: 15px;">Sửa</router-link>
            <a href="#" @click.prevent="deleteProduct(p.id)" style="color: #ef4444; font-weight: bold; text-decoration: none;">Xóa</a>
          </td>
        </tr>
        
        <tr v-if="paginatedProducts.length === 0">
            <td colspan="6" style="text-align: center; padding: 40px; color: #64748b;">
                <div style="font-size: 40px; margin-bottom: 10px;">📦</div>
                Không có dữ liệu sản phẩm!
            </td>
        </tr>
      </tbody>
    </table>

    <PaginationAdmin :currentPage="currentPage" :totalPages="totalPages" @changePage="currentPage = $event" />
  </div>
</template>