import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useCartStore = defineStore('cart', () => {
  const danhSachMua = ref([])

  const tongSoLuong = computed(() => {
    return danhSachMua.value.reduce((total, item) => total + item.so_luong, 0)
  })

  const tongTien = computed(() => {
    return danhSachMua.value.reduce((total, item) => total + (Number(item.don_gia) * item.so_luong), 0)
  })

  function themVaoGio(sanPham) {
    // Nếu sản phẩm đã có trong giỏ, tăng số lượng lên 1
    const itemTrung = danhSachMua.value.find(item => item.id === sanPham.id)
    if (itemTrung) {
      itemTrung.so_luong += 1
    } else {
      // Nếu chưa có, add mới và đặt số lượng mặc định là 1
      danhSachMua.value.push({ ...sanPham, so_luong: 1 })
    }
    alert(`Đã thêm "${sanPham.ten_san_pham}" vào giỏ!`)
  }

  function tangSoLuong(index) {
    // Kiểm tra tồn kho trước khi tăng để tránh lỗi vượt hạn mức chi nhánh
    if (danhSachMua.value[index].so_luong + 1 > danhSachMua.value[index].so_luong) {
      danhSachMua.value[index].so_luong++
    } else {
      alert("Sản phẩm đã đạt giới hạn tồn kho tại quầy sếp ơi!")
    }
  }

  function giamSoLuong(index) {
    if (danhSachMua.value[index].so_luong > 1) {
      danhSachMua.value[index].so_luong--
    } else {
      xoaKhoiGio(index) // Nếu giảm về 0 thì xóa luôn
    }
  }

  function xoaKhoiGio(index) {
    danhSachMua.value.splice(index, 1)
  }

  function xoaSachGio() {
    danhSachMua.value = []
  }

  return { danhSachMua, tongSoLuong, tongTien, themVaoGio, tangSoLuong, giamSoLuong, xoaKhoiGio, xoaSachGio }
})