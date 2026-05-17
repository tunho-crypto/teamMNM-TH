<script setup>
import { ref, computed } from 'vue'
import { useCartStore } from '../stores/cart'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import axios from 'axios'

const cartStore = useCartStore()
const authStore = useAuthStore()
const router = useRouter()

// Cấu hình trạng thái đơn đặt hàng khớp 100% nghiệp vụ gốc
const deliveryMethod = ref('delivery')
const paymentMethod = ref('BANK')
const deliveryTimeSlot = ref('7H-8H')
const tenNguoiNhan = ref(authStore.user ? authStore.user.ho_ten : '')
const sdtNguoiNhan = ref('')
const diaChiGiaoHang = ref('')
const selectStoreId = ref('')

// Danh sách chi nhánh siêu thị mẫu
const branches = ref([
  { id: 1, ten_chi_nhanh: 'Bách Hóa Xanh Trường Chinh', dia_chi: 'Tân Bình, TP.HCM' },
  { id: 2, ten_chi_nhanh: 'Bách Hóa Xanh Lê Trọng Tấn', dia_chi: 'Tân Phú, TP.HCM' }
])

const timeSlots = ['7H-8H', '8H-9H', '9H-10H', '14H-15H', '16H-17H']

// Phí giao hàng dựa trên tổng tiền
const phiShip = computed(() => {
  if (deliveryMethod.value === 'pickup') return 0
  return cartStore.tongTien >= 150000 ? 0 : 1500
})

const tongThanhToan = computed(() => cartStore.tongTien + phiShip.value)
const diemVip = computed(() => Math.floor(cartStore.tongTien / 100))

const submitCheckout = async () => {
  if (cartStore.danhSachMua.length === 0) return alert('Giỏ hàng trống sếp ơi!')
  if (!tenNguoiNhan.value || !sdtNguoiNhan.value) return alert('Sếp điền tên và số điện thoại người nhận nhé.')
  if (deliveryMethod.value === 'delivery' && !diaChiGiaoHang.value) return alert('Sếp điền địa chỉ giao hàng giùm em.')

  try {
    const dataCheckout = {
      ten_nguoi_nhan: tenNguoiNhan.value,
      sdt_nguoi_nhan: sdtNguoiNhan.value,
      dia_chi_giao_hang: deliveryMethod.value === 'pickup' ? 'Nhận tại quầy chi nhánh' : diaChiGiaoHang.value,
      delivery_method: deliveryMethod.value,
      payment_method: paymentMethod.value,
      delivery_time_slot: deliveryTimeSlot.value,
      khach_hang_id: authStore.user ? authStore.user.khach_hang_id : null,
      items: cartStore.danhSachMua
    }

    const res = await axios.post('http://localhost:8000/store/api/checkout/', dataCheckout)
    if (res.data.success) {
      alert('🎉 Đặt hàng thành công! Đơn hàng đã được lưu xuống Database và gửi Mail.')
      cartStore.xoaSachGio()
      router.push('/dat-hang-thanh-cong')
    }
  } catch (error) {
    alert('Có lỗi xảy ra khi chốt đơn sếp ơi!')
  }
}

const formatVND = (tien) => Number(tien || 0).toLocaleString('vi-VN') + 'đ'
</script>

<template>
  <div class="app-shell">
    <div class="card" style="padding: 10px; margin-bottom: 15px;">
        <div class="delivery-tabs">
            <button type="button" class="delivery-tab" :class="{ active: deliveryMethod === 'delivery' }" @click="deliveryMethod = 'delivery'">Giao hàng tận nhà</button>
            <button type="button" class="delivery-tab" :class="{ active: deliveryMethod === 'pickup' }" @click="deliveryMethod = 'pickup'">Nhận tại cửa hàng</button>
            <span class="free-ship">Không phí SHIP</span>
        </div>
    </div>

    <div class="card">
        <div class="section-title">
            {{ deliveryMethod === 'pickup' ? 'Chọn cửa hàng bạn sẽ đến nhận' : 'Cửa hàng phục vụ (Sẽ giao đến nhà bạn)' }}
        </div>
        <select class="field" v-model="selectStoreId" style="width: 100%; margin-top: 10px;">
            <option value="">-- Chọn cửa hàng gần sếp --</option>
            <option v-for="st in branches" :key="st.id" :value="st.id">{{ st.ten_chi_nhanh }} - {{ st.dia_chi }}</option>
        </select>
    </div>

    <div v-if="deliveryMethod === 'delivery'">
        <div class="card">
            <div class="section-title">Thông tin người nhận</div>
            <div class="input-grid-2">
                <input class="field" type="text" v-model="tenNguoiNhan" placeholder="Tên người nhận *" />
                <input class="field" type="text" v-model="sdtNguoiNhan" placeholder="Số điện thoại *" />
            </div>
        </div>

        <div class="card">
            <div class="section-title">Địa chỉ nhận hàng</div>
            <textarea class="textarea" v-model="diaChiGiaoHang" placeholder="Nhập số nhà, tên đường, khu vực..."></textarea>
        </div>

        <div class="card">
            <div class="section-title">Chọn khung giờ nhận hàng</div>
            <div class="option-grid">
                <label v-for="slot in timeSlots" :key="slot" class="radio-line" :class="{ active: deliveryTimeSlot === slot }">
                    <input type="radio" name="time_slot" :value="slot" v-model="deliveryTimeSlot" />
                    <span>Từ {{ slot }}</span>
                </label>
            </div>
        </div>
    </div>

    <div v-else class="card">
        <div class="section-title">Thông tin người nhận tại cửa hàng</div>
        <div class="input-grid-2">
            <input class="field" type="text" v-model="tenNguoiNhan" placeholder="Tên người nhận *" />
            <input class="field" type="text" v-model="sdtNguoiNhan" placeholder="Số điện thoại *" />
        </div>
    </div>

    <div class="card">
        <div class="section-title">Sản phẩm đã chọn</div>
        <div class="cart-list" v-if="cartStore.danhSachMua.length > 0" style="margin-top: 10px;">
            <div v-for="(item, index) in cartStore.danhSachMua" :key="index" class="product-row">
                <div>
                    <div class="product-name">📌 {{ item.ten_san_pham }}</div>
                    <div class="unit-line">Đơn giá: {{ formatVND(item.don_gia) }}</div>
                </div>
                <div class="price-col">
                    <div class="sale-price">{{ formatVND(item.don_gia * item.so_luong) }}</div>
                    <div class="qty-row">
                        <div class="qty-box">
                            <button type="button" @click="cartStore.giamSoLuong(index)">−</button>
                            <span class="js-qty">{{ item.so_luong }}</span>
                            <button type="button" @click="cartStore.tangSoLuong(index)">+</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div v-else style="text-align: center; padding: 30px 0; color: #64748b;">Giỏ hàng trống trơn sếp ơi!</div>
    </div>

    <div class="card" v-if="cartStore.danhSachMua.length > 0">
        <div class="summary-card">
            <div class="summary-row">
                <div>Tiền hàng</div><div><strong>{{ formatVND(cartStore.tongTien) }}</strong></div>
            </div>
            <div class="summary-row">
                <div>Phí giao hàng</div><div><strong>{{ phiShip === 0 ? 'Miễn phí' : formatVND(phiShip) }}</strong></div>
            </div>
            <div class="summary-row total">
                <div>Tổng tiền</div><div style="color: #d8232a;">{{ formatVND(tongThanhToan) }}</div>
            </div>
            <div class="summary-sub">
                <div>Điểm VIP tạm tính</div><div>✨ +{{ diemVip }} điểm</div>
            </div>
        </div>
    </div>

    <div class="card" v-if="cartStore.danhSachMua.length > 0">
        <div class="section-title">Hình thức thanh toán</div>
        <div class="option-grid">
            <label class="radio-line" :class="{ active: paymentMethod === 'BANK' }">
                <input type="radio" name="payment" value="BANK" v-model="paymentMethod" />
                <span>🏦 Chuyển khoản ngân hàng (x2 điểm VIP)</span>
            </label>
            <label class="radio-line" :class="{ active: paymentMethod === 'CASH' }">
                <input type="radio" name="payment" value="CASH" v-model="paymentMethod" />
                <span>💵 Thanh toán tiền mặt khi nhận hàng (COD)</span>
            </label>
        </div>
    </div>

    <div class="bottom-bar-wrap" v-if="cartStore.danhSachMua.length > 0">
        <div class="bottom-bar">
            <button class="order-btn" type="button" @click="submitCheckout">
                <span>Đặt hàng tức thì {{ formatVND(tongThanhToan) }}</span>
            </button>
        </div>
    </div>
  </div>
</template>

<style scoped>
/* ======================================================= */
/* BÊ NGUYÊN XI BỘ CSS PHOM MOBILE APP TỪ FILE CART.HTML GỐC */
/* ======================================================= */
.app-shell { max-width: 760px; margin: 24px auto; min-height: 100vh; padding: 0 12px 120px 12px; font-family: Arial, sans-serif; text-align: left; }
.card { background: #fff; border-radius: 12px; padding: 16px; margin-bottom: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.04); border: 1px solid #e2e8f0; }
.section-title { font-size: 15px; font-weight: 700; color: #1e293b; margin-bottom: 8px; }

/* CSS Tabs chọn hình thức nhận hàng */
.delivery-tabs { display: flex; background: #f1f5f9; padding: 4px; border-radius: 8px; align-items: center; position: relative; }
.delivery-tab { flex: 1; padding: 10px; border: none; background: transparent; font-weight: 700; font-size: 14px; color: #64748b; cursor: pointer; border-radius: 6px; transition: all 0.2s; }
.delivery-tab.active { background: #fff; color: #008a37; box-shadow: 0 2px 6px rgba(0,0,0,0.08); }
.free-ship { position: absolute; right: -5px; top: -15px; background: #ef4444; color: white; font-size: 10px; font-weight: 800; padding: 2px 6px; border-radius: 10px; text-transform: uppercase; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }

/* CSS Ô nhập liệu nâng cao */
.field { width: 100%; padding: 11px 14px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 14px; outline: none; transition: border-color 0.2s; background: #fff; }
.field:focus { border-color: #008a37; box-shadow: 0 0 0 3px rgba(0,138,55,0.1); }
.textarea { width: 100%; height: 75px; padding: 11px 14px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 14px; outline: none; resize: none; margin-top: 10px; font-family: inherit; }
.textarea:focus { border-color: #008a37; }
.input-grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 10px; }

/* CSS Radio chọn khung giờ & hình thức thanh toán */
.option-grid { display: grid; gap: 8px; margin-top: 10px; }
.radio-line { display: flex; align-items: center; gap: 10px; padding: 12px 14px; border: 1px solid #cbd5e1; border-radius: 8px; cursor: pointer; font-size: 14px; font-weight: 600; color: #334155; transition: all 0.2s; background: #fff; }
.radio-line input { accent-color: #008a37; width: 16px; height: 16px; }
.radio-line.active { border-color: #008a37; background: #f0fdf4; color: #008a37; }

/* CSS Danh sách giỏ hàng */
.product-row { display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid #f1f5f9; }
.product-row:last-child { border-bottom: none; }
.product-name { font-size: 14px; font-weight: 700; color: #1e293b; }
.unit-line { font-size: 12px; color: #64748b; margin-top: 2px; }
.price-col { text-align: right; }
.sale-price { color: #d8232a; font-weight: 700; font-size: 14px; }

/* Bộ nút tăng giảm số lượng (+ / -) chuẩn đét */
.qty-row { margin-top: 6px; }
.qty-box { display: inline-flex; align-items: center; border: 1px solid #cbd5e1; border-radius: 6px; background: #fff; overflow: hidden; }
.qty-box button { width: 28px; height: 28px; border: none; background: #f8fafc; font-size: 16px; font-weight: bold; cursor: pointer; color: #475569; transition: background 0.1s; }
.qty-box button:hover { background: #e2e8f0; }
.js-qty { min-width: 32px; text-align: center; font-size: 13px; font-weight: 700; color: #1e293b; }

/* Bảng tính tiền */
.summary-card { font-size: 14px; color: #475569; }
.summary-row { display: flex; justify-content: space-between; margin-bottom: 8px; }
.summary-row.total { border-top: 1px dashed #cbd5e1; padding-top: 8px; font-weight: 700; font-size: 16px; }
.summary-sub { display: flex; justify-content: space-between; margin-top: 8px; font-size: 12px; color: #16a34a; font-weight: 600; }

/* Thanh chốt đơn dính chặt đáy màn hình (Bottom Floating Bar) */
.bottom-bar-wrap { position: fixed; bottom: 0; left: 0; right: 0; background: #fff; box-shadow: 0 -4px 16px rgba(0,0,0,0.08); padding: 12px 16px; z-index: 999; border-top: 1px solid #e2e8f0; }
.bottom-bar { max-width: 736px; margin: 0 auto; }
.order-btn { width: 100%; background: #8cc12e; color: #fff; border: none; padding: 14px; border-radius: 10px; font-size: 16px; font-weight: 700; cursor: pointer; text-align: center; box-shadow: 0 4px 12px rgba(140,193,46,0.3); transition: background 0.2s; }
.order-btn:hover { background: #7ab223; }
</style>