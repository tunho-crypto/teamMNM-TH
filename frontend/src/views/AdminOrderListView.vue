<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'

const orders = ref([])
const q = ref('')
const statusFilter = ref('')

const loadOrders = async () => {
  const res = await axios.get(`http://localhost:8000/store/api/admin/orders/?q=${q.value}&trang_thai=${statusFilter.value}`)
  orders.value = res.data
}

onMounted(() => loadOrders())
watch([q, statusFilter], () => loadOrders())

const changeStatus = async (orderId, newStatus) => {
  await axios.post(`http://localhost:8000/store/api/admin/orders/update-status/${orderId}/`, { trang_thai: newStatus })
  alert('Đã cập nhật trạng thái đơn hàng!')
  loadOrders()
}
</script>

<template>
  <div>
    <div class="toolbar" style="display: flex; gap: 15px; margin-bottom: 25px;">
      <input type="text" v-model="q" placeholder="Tìm tên người nhận..." style="padding: 10px; border-radius: 8px; border: 1px solid #ddd; min-width: 240px;" />
      <select v-model="statusFilter" style="padding: 10px; border-radius: 8px; border: 1px solid #ddd;">
        <option value="">Tất cả trạng thái</option>
        <option value="CHO_XU_LY">Chờ xử lý</option>
        <option value="DA_XAC_NHAN">Đã xác nhận</option>
        <option value="HOAN_TAT">Hoàn tất</option>
        <option value="DA_HUY">Đã hủy</option>
      </select>
    </div>

    <table style="width: 100%; border-collapse: collapse;">
      <thead>
        <tr style="background: #f8fafc; border-bottom: 2px solid #edf2f7; text-align: left; font-size: 14px;">
          <th style="padding:12px;">Mã</th><th>Người nhận</th><th>SĐT</th><th>Ngày đặt</th><th>Trạng thái</th><th>Thao tác xử lý</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="o in orders" :key="o.id" style="border-bottom: 1px solid #f1f5f9; font-size: 14px;">
          <td style="padding: 12px; font-weight: bold;">#{{ o.id }}</td>
          <td>{{ o.ten_nguoi_nhan }}</td>
          <td>{{ o.sdt_nguoi_nhan }}</td>
          <td>{{ o.ngay_lap }}</td>
          <td><strong style="color: #f59e0b;">{{ o.trang_thai }}</strong></td>
          <td>
            <select :value="o.trang_thai" @change="changeStatus(o.id, $event.target.value)" style="padding: 4px 8px; border-radius: 4px;">
              <option value="CHO_XU_LY">Chờ xử lý</option><option value="DA_XAC_NHAN">Đã xác nhận</option>
              <option value="HOAN_TAT">Hoàn tất</option><option value="DA_HUY">Hủy đơn</option>
            </select>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>