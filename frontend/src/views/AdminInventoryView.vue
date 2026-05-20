<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import axios from 'axios'

const inventory = ref([])
const q = ref('')
const selectedBranch = ref('')
const selectedStatus = ref('')
const branches = ref([])

const loadInventory = async () => {
  const [resInv, resBran] = await Promise.all([
    axios.get(`http://localhost:8000/store/api/inventory/?q=${q.value}&chi_nhanh=${selectedBranch.value}&trang_thai=${selectedStatus.value}`),
    axios.get('http://localhost:8000/store/api/branches/')
  ])
  inventory.value = resInv.data
  branches.value = resBran.data
}

onMounted(() => loadInventory())
watch([q, selectedBranch, selectedStatus], () => loadInventory())

// Thống kê nhanh ngoài hộp số liệu
const countTotal = computed(() => inventory.value.length)
const countHetHang = computed(() => inventory.value.filter(i => i.so_luong_ton <= 0).length)
const countSapHet = computed(() => inventory.value.filter(i => i.so_luong_ton > 0 && i.so_luong_ton <= i.muc_can_canh_bao).length)
const countConHang = computed(() => inventory.value.filter(i => i.so_luong_ton > i.muc_can_canh_bao).length)
</script>

<template>
  <div>
    <div class="stats-grid" style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 25px;">
      <div class="sc" style="background:#f1f5f9; padding:20px; border-radius:12px;"><span>Tổng mặt hàng</span><strong style="display:block; font-size:24px; margin-top:5px;">{{ countTotal }}</strong></div>
      <div class="sc" style="background:#dcfce7; padding:20px; border-radius:12px; color:#15803d;"><span>Còn hàng</span><strong style="display:block; font-size:24px; margin-top:5px;">{{ countConHang }}</strong></div>
      <div class="sc" style="background:#fef3c7; padding:20px; border-radius:12px; color:#b45309;"><span>Sắp hết</span><strong style="display:block; font-size:24px; margin-top:5px;">{{ countSapHet }}</strong></div>
      <div class="sc" style="background:#fee2e2; padding:20px; border-radius:12px; color:#b91c1c;"><span>Hết hàng</span><strong style="display:block; font-size:24px; margin-top:5px;">{{ countHetHang }}</strong></div>
    </div>

    <div class="toolbar" style="display: flex; gap: 10px; margin-bottom: 25px;">
      <input type="text" v-model="q" placeholder="Tìm sản phẩm / cửa hàng / loại..." style="padding: 10px; border-radius: 8px; border: 1px solid #ddd; min-width: 250px;" />
      <select v-model="selectedBranch" style="padding: 10px; border-radius: 8px; border: 1px solid #ddd;">
        <option value="">Tất cả cửa hàng</option>
        <option v-for="b in branches" :key="b.id" :value="b.id">{{ b.ten_chi_nhanh }}</option>
      </select>
    </div>

    <table style="width: 100%; border-collapse: collapse;">
      <thead>
        <tr style="background: #f8fafc; border-bottom: 2px solid #edf2f7; text-align: left; font-size: 14px;">
          <th style="padding:12px;">Chi nhánh</th><th>Tên sản phẩm</th><th>Loại</th><th>Số lượng tồn</th><th>Mức cảnh báo</th><th>Trạng thái</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="i in inventory" :key="i.id" :style="i.so_luong_ton <= 0 ? 'background:#fff1f2;' : (i.so_luong_ton <= i.muc_can_canh_bao ? 'background:#fff7ed;' : '')" style="border-bottom: 1px solid #f1f5f9; font-size:14px;">
          <td style="padding:12px;">{{ i.ten_chi_nhanh }}</td>
          <td><strong>{{ i.ten_san_pham }}</strong></td>
          <td>{{ i.ten_loai }}</td>
          <td><strong>{{ i.so_luong_ton }}</strong></td>
          <td>{{ i.muc_can_canh_bao }}</td>
          <td>
            <span v-if="i.so_luong_ton <= 0" style="background:#dc2626; color:white; padding:4px 10px; border-radius:20px; font-size:12px; font-weight:bold;">HẾT HÀNG</span>
            <span v-else-if="i.so_luong_ton <= i.muc_can_canh_bao" style="background:#f59e0b; color:white; padding:4px 10px; border-radius:20px; font-size:12px; font-weight:bold;">SẮP HẾT</span>
            <span v-else style="background:#16a34a; color:white; padding:4px 10px; border-radius:20px; font-size:12px; font-weight:bold;">CÒN HÀNG</span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>