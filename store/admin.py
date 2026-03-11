from django.contrib import admin
from .models import (
     NhanVien, KhachHang, LoaiSanPham, SanPham,
    NhaCungCap, NhapHang, ChiTietNhapHang,
    HoaDon, ChiTietHoaDon
)

admin.site.register(NhanVien)
admin.site.register(KhachHang)
admin.site.register(LoaiSanPham)
admin.site.register(SanPham)
admin.site.register(NhaCungCap)
admin.site.register(NhapHang)
admin.site.register(ChiTietNhapHang)
admin.site.register(HoaDon)
admin.site.register(ChiTietHoaDon)
admin.site.site_header = "Quản trị BHX"
admin.site.site_title = "BHX Admin"
admin.site.index_title = "Hệ thống quản lý Bách Hóa Xanh"
