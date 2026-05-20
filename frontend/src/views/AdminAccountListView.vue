<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()
const accounts = ref([])
const searchQuery = ref('')

// Hàm kiểm tra quyền, nếu không phải Admin/Staff thì đá về trang chủ
onMounted(() => {
  if (!authStore.user || authStore.user.role === 'USER') {
    alert('Sếp không có quyền truy cập trang này!')
    router.push('/')
    return
  }
  fetchAccounts()
})

const fetchAccounts = async () => {
  try {
    const res = await axios.get(`http://localhost:8000/store/api/admin/accounts/?q=${searchQuery.value}`)
    accounts.value = res.data
  } catch (error) {
    console.error('Lỗi tải danh sách tài khoản', error)
  }
}

// Bắt sự kiện gõ phím để tìm kiếm Real-time
let timeout = null
const handleSearch = () => {
  clearTimeout(timeout)
  timeout = setTimeout(() => { fetchAccounts() }, 500)
}

const deleteAccount = async (id) => {
  if(confirm("Sếp có chắc chắn muốn xóa tài khoản này không?")) {
    // Giả lập Frontend xóa (Thực tế sếp viết thêm hàm gọi API DELETE nhé)
    accounts.value = accounts.value.filter(acc => acc.id !== id)
    alert("Đã xóa tài khoản thành công!")
  }
}
</script>

<template>
  <div class="admin-container">
    <div class="admin-header">
      <h2>👥 QUẢN LÝ TÀI KHOẢN HỆ THỐNG</h2>
      <button class="btn-add-new">+ Thêm Tài Khoản Mới</button>
    </div>

    <div class="admin-toolbar">
      <input type="text" v-model="searchQuery" @input="handleSearch" placeholder="🔍 Tìm kiếm theo tên, email, SĐT..." class="search-input" />
    </div>

    <div class="table-responsive">
      <table class="admin-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Họ và Tên</th>
            <th>Email</th>
            <th>Số Điện Thoại</th>
            <th>Phân Quyền</th>
            <th>Trạng Thái</th>
            <th>Hành Động</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="acc in accounts" :key="acc.id">
            <td>#{{ acc.id }}</td>
            <td style="font-weight: bold; color: #1e293b;">{{ acc.ho_ten }}</td>
            <td>{{ acc.email || '—' }}</td>
            <td>{{ acc.dien_thoai || '—' }}</td>
            <td>
              <span :class="['role-badge', acc.role.toLowerCase()]">{{ acc.role }}</span>
            </td>
            <td>
              <span :class="['status-badge', acc.trang_thai === 'ACTIVE' ? 'active' : 'locked']">
                {{ acc.trang_thai === 'ACTIVE' ? 'Hoạt động' : 'Đã Khóa' }}
              </span>
            </td>
            <td class="action-cell">
              <button class="btn-edit">✏️ Sửa</button>
              <button class="btn-delete" @click="deleteAccount(acc.id)">🗑️ Xóa</button>
            </td>
          </tr>
          <tr v-if="accounts.length === 0">
            <td colspan="7" style="text-align: center; padding: 30px; color: #64748b;">Không tìm thấy tài khoản nào khớp với từ khóa!</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
/* CSS Chuẩn Dashboard Quản Trị */
.admin-container { max-width: 1200px; margin: 30px auto; padding: 20px; background: #fff; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); text-align: left; }
.admin-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; border-bottom: 2px solid #f1f5f9; padding-bottom: 15px; }
.admin-header h2 { margin: 0; color: #008a37; font-size: 24px; }
.btn-add-new { background: #008a37; color: white; border: none; padding: 10px 20px; border-radius: 8px; font-weight: bold; cursor: pointer; transition: 0.2s; }
.btn-add-new:hover { background: #00732e; }

.admin-toolbar { margin-bottom: 20px; }
.search-input { width: 100%; max-width: 400px; padding: 12px 15px; border: 1px solid #cbd5e1; border-radius: 8px; outline: none; font-size: 14px; }
.search-input:focus { border-color: #008a37; box-shadow: 0 0 0 3px rgba(0,138,55,0.1); }

.table-responsive { overflow-x: auto; }
.admin-table { width: 100%; border-collapse: collapse; font-size: 14px; }
.admin-table th, .admin-table td { padding: 15px; border-bottom: 1px solid #e2e8f0; text-align: left; }
.admin-table th { background: #f8fafc; color: #475569; font-weight: bold; text-transform: uppercase; font-size: 13px; }
.admin-table tr:hover { background: #f0fdf4; }

/* Badges cho phân quyền và trạng thái */
.role-badge { padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; }
.role-badge.admin { background: #fee2e2; color: #b91c1c; }
.role-badge.staff { background: #fef08a; color: #b45309; }
.role-badge.user { background: #e0f2fe; color: #1d4ed8; }

.status-badge { padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; }
.status-badge.active { background: #dcfce7; color: #15803d; }
.status-badge.locked { background: #f3f4f6; color: #4b5563; }

/* Nút hành động */
.action-cell { display: flex; gap: 8px; }
.btn-edit, .btn-delete { border: none; padding: 6px 10px; border-radius: 6px; cursor: pointer; font-size: 13px; font-weight: bold; transition: 0.2s; }
.btn-edit { background: #e0f2fe; color: #0369a1; }
.btn-edit:hover { background: #bae6fd; }
.btn-delete { background: #fee2e2; color: #b91c1c; }
.btn-delete:hover { background: #fecaca; }
</style>