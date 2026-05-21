from rest_framework import serializers
from .models import SanPham
from .models import LoaiSanPham

class SanPhamSerializer(serializers.ModelSerializer):
    # Khai báo thêm một trường tự tạo để chứa link ảnh
    hinh_anh_url = serializers.SerializerMethodField()

    class Meta:
        model = SanPham
        fields = '__all__'

    # Hàm này sẽ chạy cho từng sản phẩm để lấy link ảnh chính
    def get_hinh_anh_url(self, obj):
        anh = obj.anh_chinh # Gọi cái @property trong models.py của sếp
        if anh and anh.image:
            # Gắn thêm gốc localhost:8000 để VueJS gọi sang cho đúng
            return f"https://teammnm-th.onrender.com{anh.image.url}"
        # Nếu sản phẩm chưa có ảnh, trả về một ảnh mặc định cho đỡ trống
        return "https://via.placeholder.com/300x200?text=Chưa+có+ảnh"
    


class LoaiSanPhamSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoaiSanPham
        fields = '__all__'

from .models import ChiNhanh

class ChiNhanhSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChiNhanh
        fields = '__all__'

from .models import BinhLuanSanPham, TaiKhoan, KhachHang

class BinhLuanSanPhamSerializer(serializers.ModelSerializer):
    # Tự động lấy tên người viết bình luận từ bảng tài khoản ra ngoài
    ten_nguoi_dung = serializers.CharField(source='tai_khoan.ho_ten', read_only=True)

    class Meta:
        model = BinhLuanSanPham
        fields = ['id', 'noi_dung', 'so_sao', 'ngay_binh_luan', 'ten_nguoi_dung']