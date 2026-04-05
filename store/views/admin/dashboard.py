from django.shortcuts import render

from ...models import ChiNhanh, HoaDon, KhachHang, NhanVien, SanPham, TaiKhoan
from ..common import admin_required


@admin_required
def admin_dashboard(request):
    tong_san_pham = SanPham.objects.count()
    tong_khach_hang = KhachHang.objects.count()
    tong_don_hang = HoaDon.objects.count()
    tong_chi_nhanh = ChiNhanh.objects.count()
    tong_nhan_vien = NhanVien.objects.count()
    tong_tai_khoan = TaiKhoan.objects.count()

    don_hang_moi = HoaDon.objects.select_related("khach_hang", "nhan_vien").order_by("-ngay_lap")[:5]
    san_pham_sap_het = SanPham.objects.filter(so_luong__lte=10).order_by("so_luong")[:8]

    return render(
        request,
        "store/admin/dashboard.html",
        {
            "tong_san_pham": tong_san_pham,
            "tong_khach_hang": tong_khach_hang,
            "tong_don_hang": tong_don_hang,
            "tong_chi_nhanh": tong_chi_nhanh,
            "tong_nhan_vien": tong_nhan_vien,
            "tong_tai_khoan": tong_tai_khoan,
            "don_hang_moi": don_hang_moi,
            "san_pham_sap_het": san_pham_sap_het,
        },
    )

@admin_required
def pos_checkout_view(request):
    q = request.GET.get("q", "").strip()
    products = SanPham.objects.select_related("loai").all().order_by("ten_san_pham")

    if q:
        products = products.filter(ten_san_pham__icontains=q)

    return render(
        request,
        "store/pos_checkout.html",
        {
            "products": products[:50],
            "q": q,
        },
    )