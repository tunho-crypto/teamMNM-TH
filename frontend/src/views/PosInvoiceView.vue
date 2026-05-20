<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const invoice = ref(null)

onMounted(() => {
  // Đọc dữ liệu hóa đơn bán tại quầy vừa lưu từ localStorage lên
  const dataInvoice = localStorage.getItem('pos_last_invoice')
  if (dataInvoice) {
    invoice.value = JSON.parse(dataInvoice)
    
    // Đợi giao diện render xong trong 500ms thì tự động gọi hộp thoại in nhiệt hóa đơn
    setTimeout(() => {
      window.print()
    }, 500)
  } else {
    alert('Không tìm thấy dữ liệu hóa đơn bán lẻ tại quầy!')
    router.push('/pos')
  }
})

const formatVND = (tien) => Number(tien || 0).toLocaleString('vi-VN') + ' đ'
</script>

<template>
  <div style="background: #f4f6f8; min-height: 100vh; padding: 20px; font-family: Arial, sans-serif; color: #111827; text-align: left;">
    <div class="topbar no-print" style="max-width: 820px; margin: 0 auto 16px auto; display: flex; align-items: center; justify-content: space-between;">
        <router-link to="/pos" class="back-home" style="display: inline-flex; align-items: center; text-decoration: none; color: #111827; font-size: 14px; padding: 8px 12px; border: 1px solid #d1d5db; border-radius: 10px; background: #fff;">← Quay lại Quầy POS</router-link>
        <button @click="window.print()" class="print-btn" style="border: none; background: #16a34a; color: white; border-radius: 10px; padding: 10px 14px; cursor: pointer; font-weight: bold;">🖨️ Tiến hành in lại</button>
    </div>

    <div v-if="invoice" class="invoice-box" style="max-width: 820px; margin: 0 auto; background: #fff; border: 1px solid #e5e7eb; border-radius: 16px; padding: 32px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
        <div class="receipt-head" style="text-align: center; margin-bottom: 24px; border-bottom: 1px dashed #d1d5db; padding-bottom: 16px;">
            <h1 style="margin: 0 0 6px 0; color: #16a34a; font-size: 26px; font-weight: 800;">BÁCH HÓA XANH</h1>
            <p style="margin: 0; color: #6b7280; font-size: 14px;">Hóa đơn bán lẻ tại quầy siêu thị chi nhánh</p>
        </div>

        <div class="meta-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 24px; font-size: 14px; line-height: 1.6;">
            <div><strong>Mã hóa đơn:</strong> #{{ invoice.hoa_don_id }}</div>
            <div><strong>Ngày lập:</strong> {{ invoice.ngay_gio }}</div>
            <div><strong>Thu ngân phụ trách:</strong> {{ invoice.thu_ngan }}</div>
            <div><strong>SĐT khách:</strong> {{ invoice.so_dien_thoai || '0000000000 (Khách lẻ)' }}</div>
        </div>

        <table style="width: 100%; border-collapse: collapse; margin-bottom: 24px;">
            <thead>
                <tr style="border-bottom: 2px solid #111827; text-align: left;">
                    <th style="padding: 10px 0;">Sản phẩm</th>
                    <th>SL</th>
                    <th>Đơn giá</th>
                    <th style="text-align: right;">Thành tiền</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(item, idx) in invoice.items" :key="idx" style="border-bottom: 1px solid #e5e7eb;">
                    <td style="padding: 12px 0; font-weight: bold;">{{ item.ten_san_pham }}</td>
                    <td>{{ item.so_luong_mua }} bó/kg</td>
                    <td>{{ formatVND(item.don_gia) }}</td>
                    <td style="text-align: right; font-weight: bold;">{{ formatVND(item.thanh_tien) }}</td>
                </tr>
            </tbody>
        </table>

        <div class="summary" style="border-top: 1px dashed #d1d5db; padding-top: 16px; width: 100%; max-width: 320px; margin-left: auto; font-size: 15px;">
            <div style="display: flex; justify-content: space-between; font-size: 18px; font-weight: 800; color: #16a34a; margin-bottom: 10px;">
                <span>Tổng tiền:</span><span>{{ formatVND(invoice.tong_tien) }}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 6px; color: #475569;">
                <span>Tiền khách đưa:</span><span>{{ formatVND(invoice.tien_khach_dua) }}</span>
            </div>
            <div style="display: flex; justify-content: space-between; font-weight: bold; border-top: 1px solid #eee; padding-top: 6px;">
                <span>Tiền hoàn lại:</span><span>{{ formatVND(invoice.tien_hoan_lai) }}</span>
            </div>
        </div>

        <div class="footer-note" style="text-align: center; margin-top: 40px; color: #6b7280; font-size: 13px; font-style: italic; border-top: 1px dashed #ccc; padding-top: 15px;">
            Cảm ơn quý khách đã mua hàng tại hệ thống Bách Hóa Xanh! 🙏
        </div>
    </div>
  </div>
</template>

<style>
/* CSS ĐẶC CHỦNG CHỐNG IN CÁC NÚT ĐIỀU HƯỚNG RA PHÔI GIẤY NHIỆT */
@media print {
  .no-print {
    display: none !important;
  }
  body {
    background: white !important;
    padding: 0 !important;
  }
  .invoice-box {
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
  }
}
</style>