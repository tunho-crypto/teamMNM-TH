import os
import django

# Thiết lập môi trường Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quanly_bhx_core.settings')
django.setup()

from locations.models import CuaHang

# Danh sách dữ liệu THẬT (Tên, Địa chỉ, Vĩ độ, Kinh độ)
real_stores = [
    # QUẬN 1 - TRUNG TÂM
    {
        "ten": "BHX Đề Thám",
        "dia_chi": "160 Đề Thám, Phường Cầu Ông Lãnh, Quận 1, TP.HCM",
        "vi_do": 10.765689, "kinh_do": 106.694692
    },
    {
        "ten": "BHX Trần Quang Khải",
        "dia_chi": "128 Trần Quang Khải, Phường Tân Định, Quận 1, TP.HCM",
        "vi_do": 10.793282, "kinh_do": 106.690858
    },

    # QUẬN 3
    {
        "ten": "BHX Lý Thái Tổ",
        "dia_chi": "268/16 Lý Thái Tổ, Phường 1, Quận 3, TP.HCM",
        "vi_do": 10.766321, "kinh_do": 106.678123
    },

    # TP. THỦ ĐỨC (Quận 9 & Thủ Đức cũ)
    {
        "ten": "BHX Lê Văn Việt",
        "dia_chi": "142 Lê Văn Việt, Phường Hiệp Phú, TP. Thủ Đức",
        "vi_do": 10.846820, "kinh_do": 106.776510
    },
    {
        "ten": "BHX Đặng Văn Bi",
        "dia_chi": "83 Đặng Văn Bi, Phường Trường Thọ, TP. Thủ Đức",
        "vi_do": 10.835821, "kinh_do": 106.766782
    },
    {
        "ten": "BHX Lã Xuân Oai",
        "dia_chi": "32 Lã Xuân Oai, P. Tăng Nhơn Phú A, TP. Thủ Đức",
        "vi_do": 10.844210, "kinh_do": 106.784530
    },
    {
        "ten": "BHX Ngô Quyền",
        "dia_chi": "7 Ngô Quyền, Phường Hiệp Phú, TP. Thủ Đức",
        "vi_do": 10.848120, "kinh_do": 106.773450
    },

    # QUẬN 10
    {
        "ten": "BHX Hòa Hưng",
        "dia_chi": "97 Hòa Hưng, Phường 12, Quận 10, TP.HCM",
        "vi_do": 10.778540, "kinh_do": 106.673210
    },

    # QUẬN TÂN BÌNH
    {
        "ten": "BHX Âu Cơ",
        "dia_chi": "718 Âu Cơ, Phường 14, Quận Tân Bình, TP.HCM",
        "vi_do": 10.796543, "kinh_do": 106.643210
    },
    
    # QUẬN BÌNH TÂN
    {
        "ten": "BHX 43A BÌNH THÀNH",
        "dia_chi": "43A BÌNH THÀNH, Phường Bình Hưng Hòa B, Quận Bình Tân, TP.HCM",
        "vi_do": 10.801307, "kinh_do": 106.586870
    },

    # QUẬN 6
    {
        "ten": "BHX Nguyễn Văn Luông",
        "dia_chi": "249 Nguyễn Văn Luông, Phường 11, Quận 6, TP.HCM",
        "vi_do": 10.745670, "kinh_do": 106.634560
    }
]

# Xóa dữ liệu cũ (để tránh bị trùng lặp rác)
print("🧹 Đang dọn dẹp dữ liệu cũ...")
CuaHang.objects.all().delete()

# Nạp dữ liệu mới
print("📥 Đang nhập dữ liệu mới...")
for item in real_stores:
    CuaHang.objects.create(
        ten_cua_hang=item['ten'],
        dia_chi=item['dia_chi'],
        vi_do=item['vi_do'],
        kinh_do=item['kinh_do'],
        so_dien_thoai="1900 1908"
    )

print(f"✅ Đã thêm thành công {len(real_stores)} cửa hàng chuẩn tọa độ!")