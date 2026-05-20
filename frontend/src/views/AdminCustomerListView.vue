<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import PaginationAdmin from '../components/PaginationAdmin.vue'

const customers = ref([])
const q = ref('')
const currentPage = ref(1)
const itemsPerPage = 10

const loadData = async () => {
  try {
    const res = await axios.get(`http://localhost:8000/store/api/admin/customers/?q=${q.value}`)
    customers.value = res.data
    currentPage.value = 1
  } catch (error) {
    console.error('Lỗi tải khách hàng:', error)
  }
}

onMounted(() => loadData())

// Bắt sự kiện gõ phím tìm kiếm delay 0.5s cho mượt
let timeout = null
const handleSearch = () => {
  clearTimeout(timeout)
  timeout = setTimeout(() => loadData(), 500)
}

const deleteCustomer = async (id) => {
  if (!confirm('Sếp có chắc muốn xóa khách hàng này không?')) return
  // Giả lập xóa UI (Sếp ráp API DELETE vào sau nhé)
  customers.value = customers.value.filter(c => c.id !== id)
  alert('Đã xóa khách hàng thành công!')
}

// Logic phân trang
const totalPages = computed(() => Math.ceil(customers.value.length / itemsPerPage))
const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return customers.value.slice(start, start + itemsPerPage)
})
</script>

<template>
  <div>
    <div class="admin-toolbar" style="display: flex; justify-content: space-between; margin-bottom: 20px;">
      <input type="text" v-model="q" @input="handleSearch" placeholder="🔍 Tìm tên khách hàng..." style="padding: 10px; border-radius: 8px; border: 1px solid #ddd; width: 300px;" />
      <button style="background: #16a34a; color: white; padding: 10px 16px; border-radius: 8px; border: none; font-weight: bold; cursor: pointer;">+ Thêm khách hàng</button>
    </div>

    <table style="width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
      <thead style="background: #f8fafc; border-bottom: 2px solid #edf2f7; text-align: left;">
        <tr><th style="padding: 15px;">ID</th><th>Họ tên</th><th>Điện thoại</th><th>Địa chỉ</th><th>Thao tác</th></tr>
      </thead>
      <tbody>
        <tr v-for="c in paginatedData" :key="c.id" style="border-bottom: 1px solid #f1f5f9;">
          <td style="padding: 15px; font-weight: bold; color: #64748b;">#{{ c.id }}</td>
          <td style="font-weight: bold; color: #1e293b;">{{ c.ten_khach_hang }}</td>
          <td>{{ c.dien_thoai || '—' }}</td>
          
          <td>{{ c.dia_chi || 'Chưa cập nhật' }}</td> 
          
          <td>
            <a href="#" style="color: #0288d1; font-weight: bold; text-decoration: none; margin-right: 15px;">Sửa</a>
            <a href="#" @click.prevent="deleteCustomer(c.id)" style="color: #ef4444; font-weight: bold; text-decoration: none;">Xóa</a>
          </td>
        </tr>
        <tr v-if="paginatedData.length === 0">
            <td colspan="5" style="text-align: center; padding: 30px; color: #94a3b8;">Không có dữ liệu khách hàng.</td>
        </tr>
      </tbody>
    </table>

    <PaginationAdmin :currentPage="currentPage" :totalPages="totalPages" @changePage="currentPage = $event" />
  </div>
</template>