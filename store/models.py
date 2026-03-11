from django.db import models


class ChiNhanh(models.Model):
    ten_chi_nhanh = models.CharField(max_length=100)
    dia_chi = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    dien_thoai = models.CharField(max_length=15)

    class Meta:
        db_table = "chi_nhanh"

    def __str__(self):
        return self.ten_chi_nhanh


class TaiKhoan(models.Model):
    ROLE_CHOICES = [
        ("USER", "User"),
        ("STAFF", "Staff"),
        ("ADMIN", "Admin"),
    ]

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("ACTIVE", "Active"),
        ("LOCKED", "Locked"),
    ]

    username = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=255)
    ho_ten = models.CharField(max_length=100, blank=True, null=True)
    dien_thoai = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="USER")
    trang_thai = models.CharField(max_length=15, choices=STATUS_CHOICES, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tai_khoan"

    def __str__(self):
        return self.username


class NhanVien(models.Model):
    ten_nhan_vien = models.CharField(max_length=100)
    chuc_vu = models.CharField(max_length=50)
    luong = models.DecimalField(max_digits=12, decimal_places=2)
    chi_nhanh = models.ForeignKey(ChiNhanh, on_delete=models.CASCADE, related_name="nhan_viens")
    tai_khoan = models.ForeignKey(
        TaiKhoan,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="nhan_viens"
    )

    class Meta:
        db_table = "nhan_vien"

    def __str__(self):
        return self.ten_nhan_vien


class KhachHang(models.Model):
    ten_khach_hang = models.CharField(max_length=100)
    dien_thoai = models.CharField(max_length=15)
    dia_chi = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = "khach_hang"

    def __str__(self):
        return self.ten_khach_hang


class LoaiSanPham(models.Model):
    ten_loai = models.CharField(max_length=100)

    class Meta:
        db_table = "loai_san_pham"

    def __str__(self):
        return self.ten_loai


class SanPham(models.Model):
    ten_san_pham = models.CharField(max_length=150)
    don_gia = models.DecimalField(max_digits=12, decimal_places=2)
    so_luong = models.IntegerField()
    loai = models.ForeignKey(LoaiSanPham, on_delete=models.CASCADE, related_name="san_phams")

    mo_ta = models.TextField(blank=True, null=True)
    hinh_anh_url = models.CharField(max_length=500, blank=True, null=True)
    is_khuyen_mai = models.BooleanField(default=False)
    gia_khuyen_mai = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    gia_goc = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = "san_pham"

    def __str__(self):
        return self.ten_san_pham


class NhaCungCap(models.Model):
    ten_ncc = models.CharField(max_length=150)
    dien_thoai = models.CharField(max_length=15)
    dia_chi = models.CharField(max_length=200)

    class Meta:
        db_table = "nha_cung_cap"

    def __str__(self):
        return self.ten_ncc


class NhapHang(models.Model):
    ngay_nhap = models.DateTimeField()
    nha_cung_cap = models.ForeignKey(NhaCungCap, on_delete=models.CASCADE, related_name="nhap_hangs")

    class Meta:
        db_table = "nhap_hang"

    def __str__(self):
        return f"Nhập hàng #{self.id}"


class ChiTietNhapHang(models.Model):
    nhap_hang = models.ForeignKey(NhapHang, on_delete=models.CASCADE, related_name="chi_tiets")
    san_pham = models.ForeignKey(SanPham, on_delete=models.CASCADE, related_name="chi_tiet_nhap_hangs")
    so_luong = models.IntegerField()
    don_gia_nhap = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = "chi_tiet_nhap_hang"
        unique_together = ("nhap_hang", "san_pham")

    def __str__(self):
        return f"{self.nhap_hang_id} - {self.san_pham.ten_san_pham}"


class HoaDon(models.Model):
    TRANG_THAI_CHOICES = [
        ("CHO_XU_LY", "Chờ xử lý"),
        ("DA_XAC_NHAN", "Đã xác nhận"),
        ("DANG_GIAO", "Đang giao"),
        ("HOAN_TAT", "Hoàn tất"),
        ("HUY", "Hủy"),
    ]

    ngay_lap = models.DateTimeField()
    khach_hang = models.ForeignKey(KhachHang, on_delete=models.CASCADE, related_name="hoa_dons")
    nhan_vien = models.ForeignKey(NhanVien, on_delete=models.CASCADE, related_name="hoa_dons")

    dia_chi_giao_hang = models.CharField(max_length=200, blank=True, null=True)
    sdt_nguoi_nhan = models.CharField(max_length=15, blank=True, null=True)
    ten_nguoi_nhan = models.CharField(max_length=100, blank=True, null=True)
    trang_thai = models.CharField(max_length=30, choices=TRANG_THAI_CHOICES, default="CHO_XU_LY")
    phuong_thuc_thanh_toan = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        db_table = "hoa_don"

    def __str__(self):
        return f"Hóa đơn #{self.id}"


class ChiTietHoaDon(models.Model):
    hoa_don = models.ForeignKey(HoaDon, on_delete=models.CASCADE, related_name="chi_tiets")
    san_pham = models.ForeignKey(SanPham, on_delete=models.CASCADE, related_name="chi_tiet_hoa_dons")
    so_luong = models.IntegerField()
    don_gia = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = "chi_tiet_hoa_don"
        unique_together = ("hoa_don", "san_pham")

    def __str__(self):
        return f"{self.hoa_don_id} - {self.san_pham.ten_san_pham}"