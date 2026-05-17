<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import PaginationAdmin from '../components/PaginationAdmin.vue'

const branches = ref([])
const q = ref('')
const currentPage = ref(1)
const itemsPerPage = 10

const loadData = async () => {
  try {
    const res = await axios.get(`http://localhost:8000/store/api/admin/branches/?q=${q.value}`)
    branches.value = res.data
    currentPage.value = 1
  } catch (error) {
    console.error('Lỗi tải chi nhánh:', error)
  }
}

onMounted(() => loadData())

let timeout = null
const handleSearch = () => {
  clearTimeout(timeout)
  timeout = setTimeout(() => loadData(), 500)
}

const deleteBranch = async (id) => {
  if (!confirm('Xóa chi nhánh này sẽ ảnh hưởng đến kho hàng. Tiếp tục?')) return
  branches.value = branches.value.filter(b => b.id !== id)
  alert('Đã xóa chi nhánh!')
}

const totalPages = computed(() => Math.ceil(branches.value.length / itemsPerPage))
const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return branches.value.slice(start, start + itemsPerPage)
})
</script>

<template>
  <div>
    <div class="admin-toolbar" style="display: flex; justify-content: space-between; margin-bottom: 20px;">
      <input type="text" v-model="q" @input="handleSearch" placeholder="🔍 Tìm tên chi nhánh..." style="padding: 10px; border-radius: 8px; border: 1px solid #ddd; width: 300px;" />
      <button style="background: #16a34a; color: white; padding: 10px 16px; border-radius: 8px; border: none; font-weight: bold; cursor: pointer;">+ Thêm chi nhánh</button>
    </div>

    <table style="width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
      <thead style="background: #f8fafc; border-bottom: 2px solid #edf2f7; text-align: left;">
        <tr><th style="padding: 15px;">ID</th><th>Tên chi nhánh</th><th>Địa chỉ</th><th>Điện thoại</th><th>Thao tác</th></tr>
      </thead>
      <tbody>
        <tr v-for="b in paginatedData" :key="b.id" style="border-bottom: 1px solid #f1f5f9;">
          <td style="padding: 15px; font-weight: bold; color: #64748b;">#{{ b.id }}</td>
          <td style="font-weight: bold; color: #008a37;">{{ b.ten_chi_nhanh }}</td>
          <td style="color: #475569;">{{ b.dia_chi }}</td>
          <td style="font-weight: bold;">{{ b.dien_thoai || '1900.1908' }}</td>
          <td>
            <a href="#" style="color: #0288d1; font-weight: bold; text-decoration: none; margin-right: 15px;">Sửa</a>
            <a href="#" @click.prevent="deleteBranch(b.id)" style="color: #ef4444; font-weight: bold; text-decoration: none;">Xóa</a>
          </td>
        </tr>
        <tr v-if="paginatedData.length === 0">
            <td colspan="5" style="text-align: center; padding: 30px; color: #94a3b8;">Không có dữ liệu chi nhánh.</td>
        </tr>
      </tbody>
    </table>

    <PaginationAdmin :currentPage="currentPage" :totalPages="totalPages" @changePage="currentPage = $event" />
  </div>
</template>