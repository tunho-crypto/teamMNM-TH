<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import PaginationAdmin from '../components/PaginationAdmin.vue'

const employees = ref([])
const q = ref('')
const currentPage = ref(1)
const itemsPerPage = 10

const loadData = async () => {
  try {
    const res = await axios.get(`http://localhost:8000/store/api/admin/accounts/?q=${q.value}`)
    // Chỉ lấy những tài khoản có vai trò là Nhân viên hoặc Quản trị viên
    employees.value = res.data.filter(acc => acc.role === 'STAFF' || acc.role === 'ADMIN')
    currentPage.value = 1
  } catch (error) {
    console.error('Lỗi tải nhân viên:', error)
  }
}

onMounted(() => loadData())

let timeout = null
const handleSearch = () => {
  clearTimeout(timeout)
  timeout = setTimeout(() => loadData(), 500)
}

const totalPages = computed(() => Math.ceil(employees.value.length / itemsPerPage))
const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return employees.value.slice(start, start + itemsPerPage)
})
</script>

<template>
  <div>
    <div class="admin-toolbar" style="display: flex; justify-content: space-between; margin-bottom: 20px;">
      <input type="text" v-model="q" @input="handleSearch" placeholder="🔍 Tìm tên nhân sự..." style="padding: 10px; border-radius: 8px; border: 1px solid #ddd; width: 300px;" />
      <button style="background: #16a34a; color: white; padding: 10px 16px; border-radius: 8px; border: none; font-weight: bold; cursor: pointer;">+ Cấp tài khoản NV</button>
    </div>

    <table style="width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
      <thead style="background: #f8fafc; border-bottom: 2px solid #edf2f7; text-align: left;">
        <tr><th style="padding: 15px;">Mã NV</th><th>Họ tên</th><th>Liên hệ</th><th>Chức vụ</th><th>Trạng thái</th><th>Thao tác</th></tr>
      </thead>
      <tbody>
        <tr v-for="e in paginatedData" :key="e.id" style="border-bottom: 1px solid #f1f5f9;">
          <td style="padding: 15px; font-weight: bold; color: #64748b;">NV-{{ e.id }}</td>
          <td style="font-weight: bold; color: #1e293b;">{{ e.ho_ten }}</td>
          <td style="color: #475569;">
              <div>📧 {{ e.email || '—' }}</div>
              <div>📞 {{ e.dien_thoai || '—' }}</div>
          </td>
          <td>
            <span v-if="e.role === 'ADMIN'" style="background: #fee2e2; color: #b91c1c; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: bold;">Quản trị viên</span>
            <span v-else style="background: #fef08a; color: #b45309; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: bold;">Nhân viên (Staff)</span>
          </td>
          <td>
            <span :style="e.trang_thai === 'ACTIVE' ? 'background: #dcfce7; color: #15803d;' : 'background: #f3f4f6; color: #4b5563;'" style="padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: bold;">
                {{ e.trang_thai === 'ACTIVE' ? 'Đang làm việc' : 'Đã khóa' }}
            </span>
          </td>
          <td>
            <a href="#" style="color: #0288d1; font-weight: bold; text-decoration: none; margin-right: 15px;">Phân quyền</a>
          </td>
        </tr>
      </tbody>
    </table>

    <PaginationAdmin :currentPage="currentPage" :totalPages="totalPages" @changePage="currentPage = $event" />
  </div>
</template>