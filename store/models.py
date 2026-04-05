from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator

class ChiNhanh(models.Model):
    ten_chi_nhanh = models.CharField(max_length=100)
    dia_chi = models.CharField(max_length=200)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True,
        validators=[MinValueValidator(8.0), MaxValueValidator(24.0)],
        help_text="Vĩ độ (Chỉ nhận giá trị tại VN: 8.0 đến 24.0)"
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True,
        validators=[MinValueValidator(102.0), MaxValueValidator(110.0)],
        help_text="Kinh độ (Chỉ nhận giá trị tại VN: 102.0 đến 110.0)"
    )
    dien_thoai = models.CharField(max_length=15)
    hinh_anh = models.ImageField(upload_to='store_images/', null=True, blank=True, verbose_name="Ảnh đại diện chính (Sẽ hiện ở ngoài danh sách)")
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

    ho_ten = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=True, null=True)
    dien_thoai = models.CharField(max_length=15, unique=True, blank=True, null=True)
    password_hash = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="USER")
    trang_thai = models.CharField(max_length=15, choices=STATUS_CHOICES, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tai_khoan"

    def __str__(self):
        return self.ho_ten


class NhanVien(models.Model):
    ten_nhan_vien = models.CharField(max_length=100)
    chuc_vu = models.CharField(max_length=50, blank=True, default="")
    luong = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    chi_nhanh = models.ForeignKey(
        "ChiNhanh",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="nhan_viens"
    )
    tai_khoan = models.OneToOneField(
        "TaiKhoan",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="nhan_vien"
    )

    class Meta:
        db_table = "nhan_vien"

    def __str__(self):
        return self.ten_nhan_vien


class KhachHang(models.Model):
    ten_khach_hang = models.CharField(max_length=100)
    dien_thoai = models.CharField(max_length=15, blank=True, null=True)
    dia_chi = models.CharField(max_length=200, blank=True, null=True)
    tai_khoan = models.OneToOneField(
        "TaiKhoan",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="khach_hang"
    )

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


class NhaCungCap(models.Model):
    ten_ncc = models.CharField(max_length=150)
    dien_thoai = models.CharField(max_length=15)
    dia_chi = models.CharField(max_length=200)

    class Meta:
        db_table = "nha_cung_cap"

    def __str__(self):
        return self.ten_ncc


class SanPham(models.Model):
    ten_san_pham = models.CharField(max_length=150)
    don_gia = models.DecimalField(max_digits=12, decimal_places=2)
    so_luong = models.IntegerField()
    loai = models.ForeignKey(
        "LoaiSanPham",
        on_delete=models.CASCADE,
        related_name="san_phams"
    )
    mo_ta = models.TextField(blank=True, null=True)
    is_khuyen_mai = models.BooleanField(default=False)
    gia_khuyen_mai = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    gia_goc = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = "san_pham"

    def __str__(self):
        return self.ten_san_pham

    @property
    def anh_chinh(self):
        first = self.images.filter(la_anh_chinh=True).first()
        if not first:
            first = self.images.first()
        return first

    @property
    def gia_hien_tai(self):
        if self.is_khuyen_mai and self.gia_khuyen_mai:
            return self.gia_khuyen_mai
        return self.don_gia


class SanPhamImage(models.Model):
    san_pham = models.ForeignKey(
        "SanPham",
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="san_pham/%Y/%m/")
    la_anh_chinh = models.BooleanField(default=False)
    thu_tu = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = "san_pham_image"
        ordering = ["thu_tu", "id"]

    def __str__(self):
        return f"Ảnh của {self.san_pham.ten_san_pham}"

    def save(self, *args, **kwargs):
        if self.la_anh_chinh:
            SanPhamImage.objects.filter(
                san_pham=self.san_pham,
                la_anh_chinh=True
            ).exclude(pk=self.pk).update(la_anh_chinh=False)
        super().save(*args, **kwargs)


class NhapHang(models.Model):
    ngay_nhap = models.DateTimeField()
    nha_cung_cap = models.ForeignKey(
        "NhaCungCap",
        on_delete=models.CASCADE,
        related_name="nhap_hangs"
    )

    class Meta:
        db_table = "nhap_hang"

    def __str__(self):
        return f"Nhập hàng #{self.id}"


class ChiTietNhapHang(models.Model):
    nhap_hang = models.ForeignKey(
        "NhapHang",
        on_delete=models.CASCADE,
        related_name="chi_tiets"
    )
    san_pham = models.ForeignKey(
        "SanPham",
        on_delete=models.CASCADE,
        related_name="chi_tiet_nhap_hangs"
    )
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
    khach_hang = models.ForeignKey(
        "KhachHang",
        on_delete=models.CASCADE,
        related_name="hoa_dons"
    )
    nhan_vien = models.ForeignKey(
        "NhanVien",
        on_delete=models.CASCADE,
        related_name="hoa_dons"
    )
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
    hoa_don = models.ForeignKey(
        "HoaDon",
        on_delete=models.CASCADE,
        related_name="chi_tiets"
    )
    san_pham = models.ForeignKey(
        "SanPham",
        on_delete=models.CASCADE,
        related_name="chi_tiet_hoa_dons"
    )
    so_luong = models.IntegerField()
    don_gia = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = "chi_tiet_hoa_don"
        unique_together = ("hoa_don", "san_pham")

    def __str__(self):
        return f"{self.hoa_don_id} - {self.san_pham.ten_san_pham}"


class EmailOTP(models.Model):
    tai_khoan = models.ForeignKey(
        "TaiKhoan",
        on_delete=models.CASCADE,
        related_name="email_otps"
    )
    email = models.EmailField()
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    class Meta:
        db_table = "email_otp"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.email} - {self.otp_code}"

    def is_expired(self):
        return timezone.now() > self.expires_at


@receiver(post_save, sender=TaiKhoan)
def tu_dong_tao_nhan_vien(sender, instance, **kwargs):
    if instance.role in ["STAFF", "ADMIN"]:
        if not hasattr(instance, "nhan_vien") or instance.nhan_vien is None:
            NhanVien.objects.create(
                tai_khoan=instance,
                ten_nhan_vien=instance.ho_ten,
                chuc_vu="Nhân viên mới"
            )
class DanhGiaSanPham(models.Model):
    san_pham = models.ForeignKey(
        "SanPham",
        on_delete=models.CASCADE,
        related_name="danh_gias"
    )
    ten_nguoi_dung = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    so_sao = models.PositiveSmallIntegerField(default=5)
    noi_dung = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    hien_thi = models.BooleanField(default=True)

    class Meta:
        db_table = "danh_gia_san_pham"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.ten_nguoi_dung} - {self.san_pham.ten_san_pham} - {self.so_sao} sao"

class BinhLuanSanPham(models.Model):
    san_pham = models.ForeignKey(
        "SanPham",
        on_delete=models.CASCADE,
        related_name="binh_luans"
    )
    tai_khoan = models.ForeignKey(
        "TaiKhoan",
        on_delete=models.CASCADE,
        related_name="binh_luan_san_phams"
    )
    noi_dung = models.TextField()
    so_sao = models.PositiveSmallIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    hien_thi = models.BooleanField(default=True)

    class Meta:
        db_table = "binh_luan_san_pham"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["san_pham", "tai_khoan"],
                name="unique_binh_luan_per_user_per_product",
            )
        ]

    def __str__(self):
        return f"{self.tai_khoan.ho_ten} - {self.san_pham.ten_san_pham}"


class BinhLuanChiNhanh(models.Model):
    chi_nhanh = models.ForeignKey(ChiNhanh, on_delete=models.CASCADE, related_name='binh_luans')
    tai_khoan = models.ForeignKey(TaiKhoan, on_delete=models.CASCADE)
    so_sao = models.IntegerField(default=5)
    noi_dung = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Khóa cứng: 1 Tài khoản chỉ được đánh giá 1 lần cho 1 Cửa hàng
        unique_together = ('chi_nhanh', 'tai_khoan')

# BẢNG CHỨA NHIỀU ẢNH CHO CỬA HÀNG
class ChiNhanhImage(models.Model):
    chi_nhanh = models.ForeignKey(ChiNhanh, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='store_gallery/%Y/%m/')
    
    class Meta:
        db_table = "chi_nhanh_image"

# BẢNG CHỨA ẢNH ĐÍNH KÈM CỦA BÌNH LUẬN
class BinhLuanChiNhanhImage(models.Model):
    binh_luan = models.ForeignKey(BinhLuanChiNhanh, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='comment_images/%Y/%m/')
    
    class Meta:
        db_table = "binh_luan_chi_nhanh_image"