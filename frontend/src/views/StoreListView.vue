<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'

const stores = ref([])
const quanChon = ref('all')
const tuKhoa = ref('')

const danhSachQuan = ['Quận 1', 'Quận 3', 'Quận 4', 'Quận 5', 'Quận 7', 'Quận 10', 'Bình Thạnh', 'Thủ Đức', 'Tân Bình', 'Gò Vấp']

const taiCuaHang = async () => {
  const res = await axios.get(`http://localhost:8000/store/api/locations/?quan=${quanChon.value}&q=${tuKhoa.value}`)
  stores.value = res.data
}

onMounted(() => taiCuaHang())
watch([quanChon, tuKhoa], () => taiCuaHang())
</script>

<template>
  <div class="store-page">
    <h2>🏪 DANH SÁCH SIÊU THỊ BÁCH HÓA XANH</h2>
    
    <div class="filter-box">
      <select v-model="quanChon" class="select-quan">
        <option value="all">📍 Tất cả Quận/Huyện</option>
        <option v-for="q in danhSachQuan" :key="q" :value="q">{{ q }}</option>
      </select>
      <input v-model="tuKhoa" type="text" placeholder="Gõ tên đường hoặc khu vực để tìm nhanh..." class="input-search" />
    </div>

    <div class="store-grid">
      <div v-for="st in stores" :key="st.id" class="store-card">
        <h3>🟢 {{ st.ten_chi_nhanh }}</h3>
        <p>🗺️ <strong>Địa chỉ:</strong> {{ st.dia_chi }}</p>
        <p>📞 <strong>Hotline:</strong> {{ st.dien_thoai }}</p>
        <router-link :to="'/cua-hang/' + st.id" class="btn-view">Xem đánh giá cửa hàng</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.store-page { text-align: left; }
.filter-box { display: flex; gap: 15px; margin-bottom: 25px; }
.select-quan, .input-search { padding: 10px 15px; border-radius: 6px; border: 1px solid #ccc; outline: none; }
.input-search { flex: 1; }
.store-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
.store-card { background: #fff; padding: 20px; border-radius: 8px; border: 1px solid #eee; box-shadow: 0 2px 6px rgba(0,0,0,0.05); }
.btn-view { display: inline-block; margin-top: 10px; color: #008848; font-weight: bold; text-decoration: none; }
</style>