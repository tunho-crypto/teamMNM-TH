from django.contrib import admin
from .models import (
    NhanVien, KhachHang, LoaiSanPham, SanPham,
    NhaCungCap, NhapHang, ChiTietNhapHang, SanPhamImage,
    HoaDon, ChiTietHoaDon, TaiKhoan, ChiNhanh, EmailOTP,
    ChiNhanhImage  # <-- Nhớ kéo thêm ChiNhanhImage vào đây
)

# Đổi giao diện Admin
admin.site.site_header = "Quản trị BHX"
admin.site.site_title = "BHX Admin"
admin.site.index_title = "Hệ thống quản lý Bách Hóa Xanh"

# ========================================================
# 1. CẤU HÌNH UP NHIỀU ẢNH CHO CỬA HÀNG (CHI NHÁNH)
# ========================================================
class ChiNhanhImageInline(admin.TabularInline):
    model = ChiNhanhImage
    extra = 3 # Hiển thị sẵn 3 ô up ảnh trống

@admin.register(ChiNhanh)
class ChiNhanhAdmin(admin.ModelAdmin):
    list_display = ('ten_chi_nhanh', 'dia_chi', 'dien_thoai')
    inlines = [ChiNhanhImageInline]

# ========================================================
# 2. ĐĂNG KÝ CÁC BẢNG CÒN LẠI (ĐÃ BỎ CHỮ CHINHANH ĐI)
# ========================================================
admin.site.register(NhanVien)
admin.site.register(KhachHang)
admin.site.register(LoaiSanPham)
admin.site.register(SanPham)      # Nãy sếp import mà quên đăng ký nè!
admin.site.register(SanPhamImage) # Quên đăng ký cả ảnh sản phẩm luôn!
admin.site.register(NhaCungCap)
admin.site.register(NhapHang)
admin.site.register(ChiTietNhapHang)
admin.site.register(HoaDon)
admin.site.register(ChiTietHoaDon)
admin.site.register(TaiKhoan)
admin.site.register(EmailOTP)

# Nếu sếp muốn quản lý cả Bình Luận trong Admin thì mở thêm 2 dòng này:
# from .models import BinhLuanChiNhanh, BinhLuanChiNhanhImage
# admin.site.register(BinhLuanChiNhanh)
# admin.site.register(BinhLuanChiNhanhImage)