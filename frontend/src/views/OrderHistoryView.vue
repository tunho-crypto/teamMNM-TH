<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const rawOrders = ref([])
const branches = ref([])

// Bộ lọc trạng thái đơn hàng giống file gốc
const selectedBranch = ref('')
const dateFrom = ref('')
const dateTo = ref('')

// Quản lý trạng thái đóng/mở chi tiết của từng đơn hàng
const expandedOrders = ref({})

const taiLichSuGiaoDich = async () => {
  if (!authStore.user) return
  try {
    // 1. Tải danh sách đơn hàng từ DB
    const resOrders = await axios.get(`http://localhost:8000/store/api/orders/history/${authStore.user.khach_hang_id}/`)
    rawOrders.value = resOrders.data

    // 2. Tải danh sách chi nhánh phục vụ bộ lọc nâng cao
    const resBranches = await axios.get('http://localhost:8000/store/api/branches/')
    branches.value = resBranches.data
  } catch (error) {
    console.error('Lỗi kết nối dữ liệu lịch sử:', error)
  }
}

onMounted(() => {
  taiLichSuGiaoDich()
})

// Bộ điều khiển bật tắt xem chi tiết hóa đơn (Thay thế hàm toggleDetail cũ)
const handleToggleDetail = (orderId) => {
  expandedOrders.value[orderId] = !expandedOrders.value[orderId]
}

// HÀM LỌC VÀ NHÓM ĐƠN HÀNG THEO NGÀY (Map chuẩn logic nhóm ngày của Django Monolith)
const groupedOrdersByDate = computed(() => {
  let ketQua = [...rawOrders.value]

  // Lọc động theo ngày bắt đầu nếu sếp chọn
  if (dateFrom.value) {
    ketQua = ketQua.filter(o => {
      const ngayDon = o.ngay_lap.split(' ')[0].split('/').reverse().join('-') // Chuyển DD/MM/YYYY thành YYYY-MM-DD
      return ngayDon >= dateFrom.value
    })
  }

  // Lọc động theo ngày kết thúc
  if (dateTo.value) {
    ketQua = ketQua.filter(o => {
      const ngayDon = o.ngay_lap.split(' ')[0].split('/').reverse().join('-')
      return ngayDon <= dateTo.value
    })
  }

  // Tiến hành gom nhóm mảng phẳng thành cấu trúc nhóm theo Ngày đặt
  const groups = {}
  ketQua.forEach(order => {
    const ngayDuyet = order.ngay_lap.split(' ')[0] // Lấy cụm "DD/MM/YYYY"
    if (!groups[ngayDuyet]) {
      groups[ngayDuyet] = []
    }
    groups[ngayDuyet].push(order)
  })

  return groups
})

const formatVND = (tien) => Number(tien || 0).toLocaleString('vi-VN') + 'đ'
</script>

<template>
  <div class="page" style="text-align: left;">
    <div class="back-wrap">
        <router-link to="/" class="back-link">
            <span class="back-icon">←</span> Quay lại cửa hàng
        </router-link>
    </div>

    <div class="header-card">
        <div class="header-title">📋 Lịch sử giao dịch</div>
        <div class="header-subtitle">Xem lại danh sách đơn đặt hàng thiết yếu và lộ trình tích lũy điểm VIP của sếp.</div>
    </div>

    <div class="filter-card">
        <div class="filter-title">🔍 Bộ lọc tìm kiếm nhanh</div>
        <div class="filter-grid">
            <div class="filter-group">
                <label>Từ ngày</label>
                <input type="date" v-model="dateFrom" />
            </div>
            <div class="filter-group">
                <label>Đến ngày</label>
                <input type="date" v-model="dateTo" />
            </div>
            <div class="filter-group">
                <label>Chi nhánh phục vụ</label>
                <select v-model="selectedBranch">
                    <option value="">Tất cả siêu thị chi nhánh</option>
                    <option v-for="b in branches" :key="b.id" :value="b.id">{{ b.ten_chi_nhanh }}</option>
                </select>
            </div>
        </div>
    </div>

    <div v-if="Object.keys(groupedOrdersByDate).length > 0">
      <div v-for="(orders, date) in groupedOrdersByDate" :key="date" class="day-group">
          <div class="day-header">
              <span class="day-icon">📅</span> Ngày đặt hàng: {{ date }}
          </div>
          
          <div v-for="order in orders" :key="order.id" class="order-card">
              <div class="order-main-info">
                  <div class="order-meta">
                      <span class="order-id">Đơn hàng #{{ order.id }}</span>
                      <span class="order-time">⏰ Thời gian: {{ order.ngay_lap.split(' ')[1] }}</span>
                  </div>
                  <div style="display: flex; align-items: center; gap: 15px;">
                      <span :class="['status-badge', 'status-' + order.trang_thai]">
                          {{ order.trang_thai_hien_thi }}
                      </span>
                      <button @click="handleToggleDetail(order.id)" class="btn-toggle-detail">
                          {{ expandedOrders[order.id] ? 'Ẩn chi tiết' : 'Xem chi tiết' }}
                      </button>
                  </div>
              </div>

              <div class="order-details" :class="{ active: expandedOrders[order.id] }">
                  <div class="details-inner">
                      <div class="items-list-title">🛒 Mặt hàng đã chọn mua:</div>
                      <div class="items-grid">
                          <div v-for="(item, idx) in order.items" :key="idx" class="item-row">
                              <span class="item-name">🥦 {{ item.ten_san_pham }}</span>
                              <span class="item-qty">Số lượng: <b>{{ item.so_luong }}</b> bó/kg</span>
                              <span class="item-price">{{ formatVND(item.thanh_tien) }}</span>
                          </div>
                      </div>

                      <div class="invoice-summary-box">
                          <div class="invoice-summary-grid">
                              <span>Tiền hàng hóa:</span><strong>{{ formatVND(order.tong_tien) }}</strong>
                              <span>Phí giao hàng:</span><strong>0đ</strong>
                              <span>Tổng thanh toán:</span><strong style="color: #ef4444; font-size: 16px;">{{ formatVND(order.tong_tien) }}</strong>
                              <span>Đã nhận tiền:</span><strong style="color: #16a34a;">{{ order.trang_thai === 'DA_HUY' ? '0đ' : formatVND(order.tong_tien) }}</strong>
                          </div>
                      </div>
                  </div>
              </div>
          </div>
      </div>
    </div>

    <div v-else class="message-box empty-box" style="text-align: center; padding: 40px 20px;">
        <h3 style="margin: 0 0 10px 0; color: #1e293b;">Không có giao dịch phù hợp</h3>
        <p style="margin: 0; color: #64748b; font-size: 14px;">Hiện siêu thị chưa ghi nhận dữ liệu lịch sử nào khớp với bộ lọc sếp chọn.</p>
    </div>
  </div>
</template>

<style scoped>
/* ============================================================= */
/* KHÔI PHỤC TOÀN DIỆN BỘ CSS THẺ CAO CẤP TỪ FILE ORDER_HISTORY.HTML GỐC */
/* ============================================================= */
.page { max-width: 1200px; margin: 32px auto; padding: 0 16px 40px; font-family: Arial, sans-serif; }
.header-card, .filter-card, .day-group, .order-card, .message-box { background: #fff; border: 1px solid #e5e7eb; border-radius: 16px; box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06); margin-bottom: 24px; padding: 24px; }
.back-wrap { margin-bottom: 16px; }
.back-link { display: inline-flex; align-items: center; gap: 8px; text-decoration: none; color: #008a37; font-weight: bold; font-size: 15px; }

/* Header card style */
.header-title { font-size: 24px; font-weight: 800; color: #0f172a; }
.header-subtitle { font-size: 14px; color: #64748b; margin-top: 6px; }

/* Filter card style */
.filter-title { font-size: 16px; font-weight: 700; color: #1e293b; margin-bottom: 15px; }
.filter-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
.filter-group { display: flex; flex-direction: column; gap: 6px; }
.filter-group label { font-size: 13px; font-weight: 700; color: #475569; }
.filter-group input, .filter-group select { padding: 10px 12px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 14px; outline: none; background: #fff; }
.filter-group input:focus, .filter-group select:focus { border-color: #008a37; }

/* Day group style */
.day-group { padding: 0; overflow: hidden; border: none; background: transparent; box-shadow: none; }
.day-header { font-size: 16px; font-weight: 800; color: #1e293b; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }

/* Order card item styles */
.order-card { margin-bottom: 12px; padding: 18px 20px; transition: transform 0.2s; }
.order-card:hover { transform: translateY(-2px); }
.order-main-info { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; }
.order-id { font-size: 15px; font-weight: 700; color: #0f172a; margin-right: 15px; }
.order-time { font-size: 13px; color: #64748b; }
.btn-toggle-detail { background: #f1f5f9; border: 1px solid #cbd5e1; padding: 8px 16px; border-radius: 8px; font-size: 13px; font-weight: bold; color: #334155; cursor: pointer; transition: all 0.15s; }
.btn-toggle-detail:hover { background: #008a37; color: white; border-color: #008a37; }

/* Status Labels */
.status-badge { font-size: 12px; font-weight: 800; padding: 4px 10px; border-radius: 20px; text-transform: uppercase; }
.status-CHO_XU_LY { background: #fef3c7; color: #d97706; }
.status-HOAN_TAT { background: #dcfce7; color: #16a34a; }
.status-DA_HUY { background: #fee2e2; color: #dc2626; }

/* EFFECT SMOOTH SLIDE TOGGLE FOR DETAIL CONTENT (Chuẩn SPA cao cấp) */
.order-details { display: grid; grid-template-rows: 0fr; transition: grid-template-rows 0.3s ease-out; opacity: 0; visibility: hidden; }
.order-details.active { grid-template-rows: 1fr; opacity: 1; visibility: visible; padding-top: 15px; border-top: 1px dashed #e2e8f0; margin-top: 15px; }
.details-inner { overflow: hidden; }

.items-list-title { font-size: 14px; font-weight: 700; color: #475569; margin-bottom: 10px; }
.item-row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #f1f5f9; font-size: 14px; }
.item-name { font-weight: 600; flex: 2; }
.item-qty { color: #64748b; flex: 1; text-align: center; }
.item-price { font-weight: 700; color: #1f2937; flex: 1; text-align: right; }

/* Invoice breakdown card area */
.invoice-summary-box { margin-top: 20px; background: #f8fafc; padding: 15px; border-radius: 12px; width: 100%; max-width: 360px; margin-left: auto; border: 1px solid #edf2f7; }
.invoice-summary-grid { display: grid; grid-template-columns: 1fr auto; gap: 8px; font-size: 13px; color: #475569; }
.invoice-summary-grid strong { text-align: right; color: #0f172a; }
</style>