import os
import sys
import django
from decimal import Decimal
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quanly_bhx_core.settings")
django.setup()

from store.models import (
    ChiNhanh, NhanVien, KhachHang, LoaiSanPham, SanPham,
    NhaCungCap, NhapHang, ChiTietNhapHang,
    HoaDon, ChiTietHoaDon, TaiKhoan
)


def run():
    # Xoa du lieu cu de seed lai cho sach
    ChiTietHoaDon.objects.all().delete()
    HoaDon.objects.all().delete()
    ChiTietNhapHang.objects.all().delete()
    NhapHang.objects.all().delete()
    NhaCungCap.objects.all().delete()
    SanPham.objects.all().delete()
    LoaiSanPham.objects.all().delete()
    KhachHang.objects.all().delete()
    NhanVien.objects.all().delete()
    TaiKhoan.objects.all().delete()
    ChiNhanh.objects.all().delete()

    # 1. Chi nhanh
    cn1 = ChiNhanh.objects.create(
        ten_chi_nhanh="BHX Quận 1",
        dia_chi="12 Nguyễn Huệ, Q1, TP.HCM",
        latitude=10.773100,
        longitude=106.704800,
        dien_thoai="02838220001"
    )
    cn2 = ChiNhanh.objects.create(
        ten_chi_nhanh="BHX Quận 7",
        dia_chi="120 Nguyễn Thị Thập, Q7, TP.HCM",
        latitude=10.733200,
        longitude=106.721500,
        dien_thoai="02838220002"
    )

    # 2. Tai khoan
    admin_acc = TaiKhoan.objects.create(
        username="admin",
        password_hash="admin123",
        ho_ten="Quản trị hệ thống",
        dien_thoai="0909000000",
        role="ADMIN",
        trang_thai="ACTIVE"
    )

    # 3. Nhan vien
    nv1 = NhanVien.objects.create(
        ten_nhan_vien="Nguyễn Văn An",
        chuc_vu="Quản lý",
        luong=Decimal("18000000"),
        chi_nhanh=cn1,
        tai_khoan=admin_acc
    )
    nv2 = NhanVien.objects.create(
        ten_nhan_vien="Trần Thị Bình",
        chuc_vu="Thu ngân",
        luong=Decimal("9000000"),
        chi_nhanh=cn2
    )

    # 4. Khach hang
    kh1 = KhachHang.objects.create(
        ten_khach_hang="Nguyễn Thị Mai",
        dien_thoai="0909123456",
        dia_chi="Q1, TP.HCM"
    )
    kh2 = KhachHang.objects.create(
        ten_khach_hang="Lê Văn Hùng",
        dien_thoai="0909888777",
        dia_chi="Q7, TP.HCM"
    )
    kh_le = KhachHang.objects.create(
        ten_khach_hang="Khách lẻ",
        dien_thoai="0000000000",
        dia_chi=""
    )

    # 5. Loai san pham
    rau_cu = LoaiSanPham.objects.create(ten_loai="Rau củ")
    thit_ca = LoaiSanPham.objects.create(ten_loai="Thịt cá")
    do_uong = LoaiSanPham.objects.create(ten_loai="Đồ uống")
    banh_keo = LoaiSanPham.objects.create(ten_loai="Bánh kẹo")
    hoa_pham = LoaiSanPham.objects.create(ten_loai="Hóa phẩm")
    gia_vi = LoaiSanPham.objects.create(ten_loai="Gia vị")

    # 6. San pham
    ds_san_pham = [
        ("Rau muống 500g", "18000", 120, rau_cu, True,"/static/images/raumuong.jpeg"),
        ("Cà chua 1kg", "32000", 80, rau_cu, True,"/static/images/cachua.jpeg"),
        ("Xà lách 300g", "22000", 70, rau_cu, False,"/static/images/xalach.jpeg"),
        ("Cải ngọt 500g", "19000", 90, rau_cu, False,"/static/images/caingot.jpeg"),
        ("Bắp cải 1 cái", "25000", 60, rau_cu, True,"/static/images/bapcai.jpeg"),
        ("Cà rốt 1kg", "28000", 100, rau_cu, False,"/static/images/carot.jpeg"),
        ("Khoai tây 1kg", "35000", 85, rau_cu, False,"/static/images/khoaitay.jpeg"),
        ("Dưa leo 1kg", "27000", 95, rau_cu, True,"/static/images/dualeo.jpeg"),
        ("Bí đỏ 1kg", "24000", 50, rau_cu, False,"/static/images/bido.jpeg"),
        ("Hành lá 200g", "12000", 150, rau_cu, False,"/static/images/hanhlatrứng.jpeg"),

        ("Thịt heo ba rọi 1kg", "145000", 40, thit_ca, False,"/static/images/thitheobao.jpg"),
        ("Thịt bò thăn 500g", "185000", 35, thit_ca, True,"/static/images/thitbo.jpeg"),
        ("Cá hồi phi lê 300g", "99000", 45, thit_ca, True,"/static/images/cahoi.jpeg"),
        ("Cá basa 1kg", "89000", 55, thit_ca, False,"/static/images/cabasa.jpeg"),
        ("Tôm sú 500g", "129000", 30, thit_ca, True,"/static/images/tomsu.jpeg"),
        ("Mực ống 500g", "119000", 25, thit_ca, False,"/static/images/muc.jpeg"),
        ("Trứng gà hộp 10 quả", "32000", 150, thit_ca, False,"/static/images/trungga.jpg"),
        ("Xúc xích tiệt trùng", "25000", 100, thit_ca, True,"/static/images/xucxich.jpeg"),

        ("Nước suối 500ml", "6000", 300, do_uong, False, "/static/images/nuocsuoi.jpeg"),
        ("Coca Cola lon", "11000", 220, do_uong, True, "/static/images/cocacola.jpeg"),
        ("Pepsi lon", "10000", 210, do_uong, True, "/static/images/pesi.jpeg"),
        ("7Up lon", "10000", 180, do_uong, False, "/static/images/7up.jpeg"),
        ("Sữa tươi không đường 1L", "38000", 140, do_uong, True, "/static/images/suatuoikhongduong.jpeg"),
        ("Sữa tươi có đường 1L", "39000", 130, do_uong, False, "/static/images/suatuoiduong.jpeg"),
        ("Nước cam ép 1L", "45000", 75, do_uong, True, "/static/images/nuoccamep.jpeg"),
        ("Trà xanh chai", "12000", 160, do_uong, False, "/static/images/traxanh.jpeg"),
        ("Cà phê lon", "15000", 110, do_uong, False, "/static/images/caphelon.jpeg"),

        ("Bánh Oreo", "18000", 150, banh_keo, True, "/static/images/bahoreo.jpeg"),
        ("Bánh Chocopie", "36000", 100, banh_keo, False, "/static/images/banhchocopie.jpg"),
        ("Snack khoai tây", "12000", 180, banh_keo, True, "/static/images/snackkhoaitay.jpeg"),
        ("Kẹo dẻo trái cây", "22000", 90, banh_keo, False, "/static/images/keodeotraicay.jpeg"),
        ("Socola thanh", "27000", 95, banh_keo, True, "/static/images/socolathanh.jpeg"),
        ("Bánh quy bơ", "31000", 80, banh_keo, False, "/static/images/banhquybo.jpeg"),

        ("Nước rửa chén 750ml", "42000", 70, hoa_pham, True, "/static/images/nuocruachen.jpeg"),
        ("Nước giặt 2.7kg", "135000", 50, hoa_pham, True, "/static/images/nuocgiat.jpeg"),
        ("Nước lau sàn 1L", "49000", 65, hoa_pham, False, "/static/images/nuoclausan.jpeg"),
        ("Khăn giấy hộp", "28000", 120, hoa_pham, False, "/static/images/khangayhop.jpeg"),
        ("Giấy vệ sinh 10 cuộn", "69000", 95, hoa_pham, True, "/static/images/giayvesinh.jpeg"),
        ("Kem đánh răng", "32000", 105, hoa_pham, False, "/static/images/kemdanhrang.jpeg"),
        ("Dầu gội 650g", "89000", 60, hoa_pham, True, "/static/images/daugoi.jpeg"),
        ("Sữa tắm 900g", "99000", 55, hoa_pham, False, "/static/images/suatam.jpeg"),

        ("Nước mắm 500ml", "39000", 100, gia_vi, True, "/static/images/nuocmam.jpeg"),
        ("Tương ớt 250g", "17000", 140, gia_vi, False, "/static/images/tuongot.jpeg"),
        ("Muối i-ốt 500g", "9000", 200, gia_vi, False, "/static/images/muoiiot.jpeg"),
        ("Đường trắng 1kg", "26000", 160, gia_vi, False, "/static/images/duongtrang.jpeg"),
        ("Hạt nêm 400g", "42000", 110, gia_vi, True, "/static/images/hatnem.jpeg"),
        ("Tiêu xay 100g", "28000", 90, gia_vi, False, "/static/images/tieuxay.jpeg"),
        ("Dầu ăn 1L", "52000", 130, gia_vi, True, "/static/images/dauan.jpeg"),
        ("Bột ngọt 454g", "36000", 100, gia_vi, False, "/static/images/botngot.jpeg"),
    ]
    san_phams = []
    for ten, gia, so_luong, loai, km, hinh_anh in ds_san_pham:
        gia_decimal = Decimal(gia)
        gia_km = gia_decimal * Decimal("0.9") if km else None

        sp = SanPham.objects.create(
            ten_san_pham=ten,
            don_gia=gia_decimal,
            so_luong=so_luong,
            loai=loai,
            mo_ta="Sản phẩm demo cho website BHX, tươi ngon và phù hợp mua sắm gia đình.",
            hinh_anh_url=hinh_anh,
            is_khuyen_mai=km,
            gia_goc=gia_decimal if km else None,
            gia_khuyen_mai=gia_km if km else None
        )
        san_phams.append(sp)

    # 7. Nha cung cap
    ncc1 = NhaCungCap.objects.create(
        ten_ncc="Công ty Nông Sản Sạch",
        dien_thoai="02839990001",
        dia_chi="Hóc Môn, TP.HCM"
    )
    ncc2 = NhaCungCap.objects.create(
        ten_ncc="Công ty Thực Phẩm Tươi",
        dien_thoai="02839990002",
        dia_chi="Bình Chánh, TP.HCM"
    )

    # 8. Nhap hang
    nh1 = NhapHang.objects.create(
        ngay_nhap=datetime.strptime("2026-01-10 08:15:00", "%Y-%m-%d %H:%M:%S"),
        nha_cung_cap=ncc1
    )
    nh2 = NhapHang.objects.create(
        ngay_nhap=datetime.strptime("2026-01-15 09:00:00", "%Y-%m-%d %H:%M:%S"),
        nha_cung_cap=ncc2
    )

    for sp in san_phams[:10]:
        ChiTietNhapHang.objects.create(
            nhap_hang=nh1,
            san_pham=sp,
            so_luong=200,
            don_gia_nhap=sp.don_gia * Decimal("0.7")
        )

    for sp in san_phams[10:20]:
        ChiTietNhapHang.objects.create(
            nhap_hang=nh2,
            san_pham=sp,
            so_luong=120,
            don_gia_nhap=sp.don_gia * Decimal("0.75")
        )

    # 9. Hoa don
    hd1 = HoaDon.objects.create(
        ngay_lap=datetime.strptime("2026-01-22 18:05:00", "%Y-%m-%d %H:%M:%S"),
        khach_hang=kh1,
        nhan_vien=nv1,
        dia_chi_giao_hang="Q1, TP.HCM",
        sdt_nguoi_nhan="0909123456",
        ten_nguoi_nhan="Nguyễn Thị Mai",
        trang_thai="CHO_XU_LY",
        phuong_thuc_thanh_toan="COD"
    )

    hd2 = HoaDon.objects.create(
        ngay_lap=datetime.strptime("2026-01-26 20:10:00", "%Y-%m-%d %H:%M:%S"),
        khach_hang=kh2,
        nhan_vien=nv2,
        dia_chi_giao_hang="Q7, TP.HCM",
        sdt_nguoi_nhan="0909888777",
        ten_nguoi_nhan="Lê Văn Hùng",
        trang_thai="DA_XAC_NHAN",
        phuong_thuc_thanh_toan="COD"
    )

    hd3 = HoaDon.objects.create(
        ngay_lap=datetime.strptime("2026-02-01 10:30:00", "%Y-%m-%d %H:%M:%S"),
        khach_hang=kh_le,
        nhan_vien=nv2,
        trang_thai="CHO_XU_LY",
        phuong_thuc_thanh_toan="COD"
    )

    # 10. Chi tiet hoa don
    ChiTietHoaDon.objects.create(
        hoa_don=hd1,
        san_pham=san_phams[0],
        so_luong=2,
        don_gia=san_phams[0].don_gia
    )
    ChiTietHoaDon.objects.create(
        hoa_don=hd1,
        san_pham=san_phams[18],
        so_luong=6,
        don_gia=san_phams[18].don_gia
    )
    ChiTietHoaDon.objects.create(
        hoa_don=hd2,
        san_pham=san_phams[10],
        so_luong=1,
        don_gia=san_phams[10].don_gia
    )
    ChiTietHoaDon.objects.create(
        hoa_don=hd2,
        san_pham=san_phams[42],
        so_luong=2,
        don_gia=san_phams[42].don_gia
    )
    ChiTietHoaDon.objects.create(
        hoa_don=hd3,
        san_pham=san_phams[20],
        so_luong=10,
        don_gia=san_phams[20].don_gia
    )
    
    admin_acc = TaiKhoan.objects.create(
    username="admin",
    password_hash="admin123",
    ho_ten="Quản trị hệ thống",
    dien_thoai="0909000000",
    role="ADMIN",
    trang_thai="ACTIVE"
)

    print("Seed dữ liệu thành công. Đã tạo dữ liệu mẫu cho web BHX.")


if __name__ == "__main__":
    run()
