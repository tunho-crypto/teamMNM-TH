import os
import sys
import django
import shutil
import random

from decimal import Decimal
from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password

# =========================================================
# 1. DJANGO SETUP
# =========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quanly_bhx_core.settings")
django.setup()

from django.conf import settings
from django.utils import timezone
from store.models import (
    ChiNhanh,
    NhanVien,
    KhachHang,
    LoaiSanPham,
    SanPham,
    SanPhamImage,
    NhaCungCap,
    NhapHang,
    ChiTietNhapHang,
    HoaDon,
    ChiTietHoaDon,
    TaiKhoan,
)

# =========================================================
# 2. DỮ LIỆU CHI NHÁNH
# =========================================================
real_stores = [
    {"ten": "BHX Đề Thám", "dia_chi": "160 Đề Thám, P. Cầu Ông Lãnh, Quận 1", "vi_do": 10.765689, "kinh_do": 106.694692},
    {"ten": "BHX Trần Quang Khải", "dia_chi": "128 Trần Quang Khải, P. Tân Định, Quận 1", "vi_do": 10.793282, "kinh_do": 106.690858},
    {"ten": "BHX Bùi Viện", "dia_chi": "15 Bùi Viện, P. Phạm Ngũ Lão, Quận 1", "vi_do": 10.767111, "kinh_do": 106.693444},
    {"ten": "BHX Cống Quỳnh", "dia_chi": "189 Cống Quỳnh, P. Nguyễn Cư Trinh, Quận 1", "vi_do": 10.765222, "kinh_do": 106.687333},
    {"ten": "BHX Lý Thái Tổ", "dia_chi": "268/16 Lý Thái Tổ, Phường 1, Quận 3", "vi_do": 10.766321, "kinh_do": 106.678123},
    {"ten": "BHX CMT8 Q3", "dia_chi": "456 Cách Mạng Tháng 8, Phường 11, Quận 3", "vi_do": 10.785642, "kinh_do": 106.666321},
    {"ten": "BHX Nguyễn Đình Chiểu", "dia_chi": "23 Nguyễn Đình Chiểu, Phường 4, Quận 3", "vi_do": 10.776512, "kinh_do": 106.685432},
    {"ten": "BHX Lê Văn Sỹ Q3", "dia_chi": "350 Lê Văn Sỹ, Phường 14, Quận 3", "vi_do": 10.787111, "kinh_do": 106.674222},
    {"ten": "BHX Tôn Đản", "dia_chi": "120 Tôn Đản, Phường 10, Quận 4", "vi_do": 10.760214, "kinh_do": 106.705632},
    {"ten": "BHX Hoàng Diệu", "dia_chi": "85 Hoàng Diệu, Phường 12, Quận 4", "vi_do": 10.762831, "kinh_do": 106.700142},
    {"ten": "BHX Bến Vân Đồn", "dia_chi": "300 Bến Vân Đồn, Phường 2, Quận 4", "vi_do": 10.761111, "kinh_do": 106.695222},
    {"ten": "BHX Đoàn Văn Bơ", "dia_chi": "250 Đoàn Văn Bơ, Phường 14, Quận 4", "vi_do": 10.758333, "kinh_do": 106.708111},
    {"ten": "BHX Nguyễn Trãi", "dia_chi": "400 Nguyễn Trãi, Phường 8, Quận 5", "vi_do": 10.756281, "kinh_do": 106.675392},
    {"ten": "BHX Trần Hưng Đạo", "dia_chi": "800 Trần Hưng Đạo, Phường 7, Quận 5", "vi_do": 10.753123, "kinh_do": 106.671234},
    {"ten": "BHX An Dương Vương", "dia_chi": "105 An Dương Vương, Phường 8, Quận 5", "vi_do": 10.757891, "kinh_do": 106.673456},
    {"ten": "BHX Nguyễn Tri Phương", "dia_chi": "150 Nguyễn Tri Phương, Phường 9, Quận 5", "vi_do": 10.759222, "kinh_do": 106.668111},
    {"ten": "BHX Hòa Hưng", "dia_chi": "97 Hòa Hưng, Phường 12, Quận 10", "vi_do": 10.778540, "kinh_do": 106.673210},
    {"ten": "BHX 3/2 Q10", "dia_chi": "450 Đường 3/2, Phường 12, Quận 10", "vi_do": 10.768912, "kinh_do": 106.668912},
    {"ten": "BHX Sư Vạn Hạnh", "dia_chi": "780 Sư Vạn Hạnh, Phường 12, Quận 10", "vi_do": 10.774111, "kinh_do": 106.667222},
    {"ten": "BHX Thành Thái", "dia_chi": "112 Thành Thái, Phường 14, Quận 10", "vi_do": 10.771222, "kinh_do": 106.663111},
    {"ten": "BHX Lạc Long Quân Q11", "dia_chi": "300 Lạc Long Quân, Phường 5, Quận 11", "vi_do": 10.765432, "kinh_do": 106.645678},
    {"ten": "BHX Bình Thới", "dia_chi": "150 Bình Thới, Phường 14, Quận 11", "vi_do": 10.766789, "kinh_do": 106.642345},
    {"ten": "BHX Ông Ích Khiêm", "dia_chi": "80 Ông Ích Khiêm, Phường 5, Quận 11", "vi_do": 10.768111, "kinh_do": 106.648222},
    {"ten": "BHX Minh Phụng", "dia_chi": "220 Minh Phụng, Phường 9, Quận 11", "vi_do": 10.762222, "kinh_do": 106.644111},
    {"ten": "BHX Nguyễn Văn Luông", "dia_chi": "249 Nguyễn Văn Luông, Phường 11, Quận 6", "vi_do": 10.745670, "kinh_do": 106.634560},
    {"ten": "BHX Hậu Giang", "dia_chi": "600 Hậu Giang, Phường 12, Quận 6", "vi_do": 10.748912, "kinh_do": 106.625678},
    {"ten": "BHX Bà Hom", "dia_chi": "120 Bà Hom, Phường 13, Quận 6", "vi_do": 10.752111, "kinh_do": 106.628222},
    {"ten": "BHX Bình Tiên", "dia_chi": "85 Bình Tiên, Phường 3, Quận 6", "vi_do": 10.744222, "kinh_do": 106.638111},
    {"ten": "BHX Phạm Thế Hiển Q8", "dia_chi": "1500 Phạm Thế Hiển, Phường 6, Quận 8", "vi_do": 10.735671, "kinh_do": 106.654321},
    {"ten": "BHX Tạ Quang Bửu", "dia_chi": "890 Tạ Quang Bửu, Phường 5, Quận 8", "vi_do": 10.741234, "kinh_do": 106.661234},
    {"ten": "BHX Tùng Thiện Vương", "dia_chi": "210 Tùng Thiện Vương, Phường 11, Quận 8", "vi_do": 10.748912, "kinh_do": 106.656789},
    {"ten": "BHX Phạm Hùng Q8", "dia_chi": "350 Phạm Hùng, Phường 5, Quận 8", "vi_do": 10.738111, "kinh_do": 106.665222},
    {"ten": "BHX Huỳnh Tấn Phát", "dia_chi": "1450 Huỳnh Tấn Phát, P. Phú Mỹ, Quận 7", "vi_do": 10.720341, "kinh_do": 106.735612},
    {"ten": "BHX Nguyễn Thị Thập", "dia_chi": "560 Nguyễn Thị Thập, P. Tân Quy, Quận 7", "vi_do": 10.740123, "kinh_do": 106.711234},
    {"ten": "BHX Lê Văn Lương Q7", "dia_chi": "230 Lê Văn Lương, P. Tân Hưng, Quận 7", "vi_do": 10.738912, "kinh_do": 106.701234},
    {"ten": "BHX Lâm Văn Bền", "dia_chi": "112 Lâm Văn Bền, P. Tân Kiểng, Quận 7", "vi_do": 10.745678, "kinh_do": 106.715678},
    {"ten": "BHX Phạm Hữu Lầu", "dia_chi": "80 Phạm Hữu Lầu, Phước Kiển, Nhà Bè", "vi_do": 10.701234, "kinh_do": 106.721345},
    {"ten": "BHX Lê Văn Lương NB", "dia_chi": "1000 Lê Văn Lương, Nhơn Đức, Nhà Bè", "vi_do": 10.685111, "kinh_do": 106.705222},
    {"ten": "BHX Quốc Lộ 50", "dia_chi": "C12/10 Quốc Lộ 50, Bình Hưng, Bình Chánh", "vi_do": 10.718111, "kinh_do": 106.662222},
    {"ten": "BHX Phạm Hùng BC", "dia_chi": "200 Phạm Hùng, Bình Hưng, Bình Chánh", "vi_do": 10.725222, "kinh_do": 106.671111},
    {"ten": "BHX Võ Văn Vân", "dia_chi": "150 Võ Văn Vân, Vĩnh Lộc B, Bình Chánh", "vi_do": 10.785111, "kinh_do": 106.568222},
    {"ten": "BHX Quách Điêu", "dia_chi": "50 Quách Điêu, Vĩnh Lộc A, Bình Chánh", "vi_do": 10.812222, "kinh_do": 106.575111},
    {"ten": "BHX Âu Cơ", "dia_chi": "718 Âu Cơ, Phường 14, Tân Bình", "vi_do": 10.796543, "kinh_do": 106.643210},
    {"ten": "BHX Hoàng Hoa Thám", "dia_chi": "120 Hoàng Hoa Thám, Phường 12, Tân Bình", "vi_do": 10.801234, "kinh_do": 106.645678},
    {"ten": "BHX Trường Chinh", "dia_chi": "800 Trường Chinh, Phường 15, Tân Bình", "vi_do": 10.815111, "kinh_do": 106.635222},
    {"ten": "BHX Cộng Hòa", "dia_chi": "450 Cộng Hòa, Phường 13, Tân Bình", "vi_do": 10.804222, "kinh_do": 106.648111},
    {"ten": "BHX Bàu Cát", "dia_chi": "115 Bàu Cát, Phường 14, Tân Bình", "vi_do": 10.795111, "kinh_do": 106.642222},
    {"ten": "BHX Lũy Bán Bích", "dia_chi": "500 Lũy Bán Bích, P. Hòa Thạnh, Tân Phú", "vi_do": 10.775678, "kinh_do": 106.632345},
    {"ten": "BHX Tân Kỳ Tân Quý", "dia_chi": "300 Tân Kỳ Tân Quý, P. Sơn Kỳ, Tân Phú", "vi_do": 10.805678, "kinh_do": 106.621234},
    {"ten": "BHX Trương Vĩnh Ký", "dia_chi": "90 Trương Vĩnh Ký, P. Tân Thành, Tân Phú", "vi_do": 10.791234, "kinh_do": 106.634567},
    {"ten": "BHX Gò Dầu", "dia_chi": "210 Gò Dầu, P. Tân Quý, Tân Phú", "vi_do": 10.798111, "kinh_do": 106.625222},
    {"ten": "BHX Bình Long", "dia_chi": "350 Bình Long, P. Phú Thạnh, Tân Phú", "vi_do": 10.782222, "kinh_do": 106.621111},
    {"ten": "BHX 43A Bình Thành", "dia_chi": "43A Bình Thành, P. Bình Hưng Hòa B, Bình Tân", "vi_do": 10.801307, "kinh_do": 106.586870},
    {"ten": "BHX Tỉnh Lộ 10", "dia_chi": "1000 Tỉnh Lộ 10, P. Tân Tạo, Bình Tân", "vi_do": 10.756789, "kinh_do": 106.601234},
    {"ten": "BHX Lê Văn Quới", "dia_chi": "400 Lê Văn Quới, P. Bình Hưng Hòa A, Bình Tân", "vi_do": 10.771234, "kinh_do": 106.612345},
    {"ten": "BHX Mã Lò", "dia_chi": "650 Mã Lò, P. Bình Trị Đông A, Bình Tân", "vi_do": 10.765111, "kinh_do": 106.605222},
    {"ten": "BHX Tân Hòa Đông", "dia_chi": "280 Tân Hòa Đông, P. Bình Trị Đông, Bình Tân", "vi_do": 10.758222, "kinh_do": 106.618111},
    {"ten": "BHX Hương Lộ 2", "dia_chi": "800 Hương Lộ 2, P. Bình Trị Đông A, Bình Tân", "vi_do": 10.769111, "kinh_do": 106.602222},
    {"ten": "BHX Kinh Dương Vương", "dia_chi": "550 Kinh Dương Vương, P. An Lạc, Bình Tân", "vi_do": 10.735222, "kinh_do": 106.615111},
    {"ten": "BHX Xô Viết Nghệ Tĩnh", "dia_chi": "450 Xô Viết Nghệ Tĩnh, Phường 25, Bình Thạnh", "vi_do": 10.804567, "kinh_do": 106.712345},
    {"ten": "BHX Nơ Trang Long", "dia_chi": "230 Nơ Trang Long, Phường 12, Bình Thạnh", "vi_do": 10.815678, "kinh_do": 106.701234},
    {"ten": "BHX Bùi Đình Túy", "dia_chi": "115 Bùi Đình Túy, Phường 24, Bình Thạnh", "vi_do": 10.806789, "kinh_do": 106.704567},
    {"ten": "BHX Lê Quang Định", "dia_chi": "400 Lê Quang Định, Phường 11, Bình Thạnh", "vi_do": 10.812345, "kinh_do": 106.694567},
    {"ten": "BHX Chu Văn An", "dia_chi": "180 Chu Văn An, Phường 26, Bình Thạnh", "vi_do": 10.811111, "kinh_do": 106.708222},
    {"ten": "BHX Phan Đình Phùng", "dia_chi": "200 Phan Đình Phùng, Phường 1, Phú Nhuận", "vi_do": 10.795432, "kinh_do": 106.682345},
    {"ten": "BHX Huỳnh Văn Bánh", "dia_chi": "150 Huỳnh Văn Bánh, Phường 12, Phú Nhuận", "vi_do": 10.791234, "kinh_do": 106.675678},
    {"ten": "BHX Nguyễn Kiệm PN", "dia_chi": "600 Nguyễn Kiệm, Phường 4, Phú Nhuận", "vi_do": 10.805111, "kinh_do": 106.681222},
    {"ten": "BHX Quang Trung GV", "dia_chi": "650 Quang Trung, Phường 11, Gò Vấp", "vi_do": 10.835432, "kinh_do": 106.654321},
    {"ten": "BHX Lê Văn Thọ", "dia_chi": "230 Lê Văn Thọ, Phường 11, Gò Vấp", "vi_do": 10.842345, "kinh_do": 106.656789},
    {"ten": "BHX Phan Huy Ích GV", "dia_chi": "150 Phan Huy Ích, Phường 12, Gò Vấp", "vi_do": 10.837891, "kinh_do": 106.641234},
    {"ten": "BHX Nguyễn Văn Nghi", "dia_chi": "112 Nguyễn Văn Nghi, Phường 7, Gò Vấp", "vi_do": 10.824567, "kinh_do": 106.685678},
    {"ten": "BHX Phạm Văn Chiêu", "dia_chi": "350 Phạm Văn Chiêu, Phường 9, Gò Vấp", "vi_do": 10.845111, "kinh_do": 106.648222},
    {"ten": "BHX Thống Nhất", "dia_chi": "200 Thống Nhất, Phường 10, Gò Vấp", "vi_do": 10.838222, "kinh_do": 106.665111},
    {"ten": "BHX Nguyễn Oanh", "dia_chi": "400 Nguyễn Oanh, Phường 6, Gò Vấp", "vi_do": 10.841111, "kinh_do": 106.678222},
    {"ten": "BHX Lê Đức Thọ", "dia_chi": "800 Lê Đức Thọ, Phường 15, Gò Vấp", "vi_do": 10.848222, "kinh_do": 106.668111},
    {"ten": "BHX Lê Văn Việt", "dia_chi": "142 Lê Văn Việt, P. Hiệp Phú, TP. Thủ Đức", "vi_do": 10.846820, "kinh_do": 106.776510},
    {"ten": "BHX Đỗ Xuân Hợp", "dia_chi": "250 Đỗ Xuân Hợp, P. Phước Long A, TP. Thủ Đức", "vi_do": 10.825111, "kinh_do": 106.768222},
    {"ten": "BHX Lã Xuân Oai", "dia_chi": "32 Lã Xuân Oai, P. Tăng Nhơn Phú A, TP. Thủ Đức", "vi_do": 10.844210, "kinh_do": 106.784530},
    {"ten": "BHX Hoàng Hữu Nam", "dia_chi": "180 Hoàng Hữu Nam, P. Long Thạnh Mỹ, TP. Thủ Đức", "vi_do": 10.865222, "kinh_do": 106.815111},
    {"ten": "BHX Nguyễn Duy Trinh", "dia_chi": "500 Nguyễn Duy Trinh, P. Bình Trưng Đông, TP. Thủ Đức", "vi_do": 10.789123, "kinh_do": 106.765432},
    {"ten": "BHX Trần Não", "dia_chi": "120 Trần Não, P. Bình An, TP. Thủ Đức", "vi_do": 10.795678, "kinh_do": 106.731234},
    {"ten": "BHX Nguyễn Thị Định", "dia_chi": "300 Nguyễn Thị Định, P. Cát Lái, TP. Thủ Đức", "vi_do": 10.768111, "kinh_do": 106.765222},
    {"ten": "BHX Lương Định Của", "dia_chi": "150 Lương Định Của, P. An Phú, TP. Thủ Đức", "vi_do": 10.785222, "kinh_do": 106.741111},
    {"ten": "BHX Kha Vạn Cân", "dia_chi": "800 Kha Vạn Cân, P. Linh Đông, TP. Thủ Đức", "vi_do": 10.838912, "kinh_do": 106.756789},
    {"ten": "BHX Đặng Văn Bi", "dia_chi": "83 Đặng Văn Bi, P. Trường Thọ, TP. Thủ Đức", "vi_do": 10.835821, "kinh_do": 106.766782},
    {"ten": "BHX Võ Văn Ngân", "dia_chi": "200 Võ Văn Ngân, P. Bình Thọ, TP. Thủ Đức", "vi_do": 10.851111, "kinh_do": 106.761222},
    {"ten": "BHX Hiệp Bình", "dia_chi": "115 Hiệp Bình, P. Hiệp Bình Chánh, TP. Thủ Đức", "vi_do": 10.832222, "kinh_do": 106.725111},
    {"ten": "BHX Quốc Lộ 13", "dia_chi": "600 Quốc Lộ 13, P. Hiệp Bình Phước, TP. Thủ Đức", "vi_do": 10.845111, "kinh_do": 106.718222},
    {"ten": "BHX Tô Ngọc Vân", "dia_chi": "250 Tô Ngọc Vân, P. Linh Đông, TP. Thủ Đức", "vi_do": 10.855222, "kinh_do": 106.751111},
    {"ten": "BHX Tam Bình", "dia_chi": "90 Tam Bình, P. Tam Phú, TP. Thủ Đức", "vi_do": 10.861111, "kinh_do": 106.745222},
    {"ten": "BHX Nguyễn Ảnh Thủ Q12", "dia_chi": "150 Nguyễn Ảnh Thủ, P. Hiệp Thành, Quận 12", "vi_do": 10.875678, "kinh_do": 106.631234},
    {"ten": "BHX Lê Văn Khương", "dia_chi": "350 Lê Văn Khương, P. Thới An, Quận 12", "vi_do": 10.881234, "kinh_do": 106.645678},
    {"ten": "BHX Tô Ký", "dia_chi": "400 Tô Ký, P. Tân Chánh Hiệp, Quận 12", "vi_do": 10.865111, "kinh_do": 106.618222},
    {"ten": "BHX Vườn Lài", "dia_chi": "120 Vườn Lài, P. An Phú Đông, Quận 12", "vi_do": 10.845222, "kinh_do": 106.685111},
    {"ten": "BHX Phan Văn Hớn HM", "dia_chi": "120 Phan Văn Hớn, Bà Điểm, Hóc Môn", "vi_do": 10.841234, "kinh_do": 106.601234},
    {"ten": "BHX Đặng Thúc Vịnh", "dia_chi": "250 Đặng Thúc Vịnh, Đông Thạnh, Hóc Môn", "vi_do": 10.901111, "kinh_do": 106.615222},
    {"ten": "BHX Nguyễn Văn Bứa", "dia_chi": "180 Nguyễn Văn Bứa, Xuân Thới Sơn, Hóc Môn", "vi_do": 10.875222, "kinh_do": 106.568111},
    {"ten": "BHX Tỉnh Lộ 8", "dia_chi": "500 Tỉnh Lộ 8, TT Củ Chi, Củ Chi", "vi_do": 10.971111, "kinh_do": 106.515222},
    {"ten": "BHX Quốc Lộ 22", "dia_chi": "1200 Quốc Lộ 22, Tân An Hội, Củ Chi", "vi_do": 10.965222, "kinh_do": 106.501111},
    {"ten": "BHX Tỉnh Lộ 15", "dia_chi": "300 Tỉnh Lộ 15, Tân Thạnh Đông, Củ Chi", "vi_do": 10.951111, "kinh_do": 106.585222},
]

CUSTOMERS = [
    {"name": "Nguyễn Minh Anh", "phone": "0901000001", "email": "minhanh01@example.com", "password": "User@123"},
    {"name": "Trần Gia Hân", "phone": "0901000002", "email": "giahan02@example.com", "password": "User@123"},
    {"name": "Lê Quốc Bảo", "phone": "0901000003", "email": "quocbao03@example.com", "password": "User@123"},
    {"name": "Phạm Khánh Linh", "phone": "0901000004", "email": "khanhlinh04@example.com", "password": "User@123"},
    {"name": "Hoàng Đức Nam", "phone": "0901000005", "email": "ducnam05@example.com", "password": "User@123"},
    {"name": "Võ Ngọc Trâm", "phone": "0901000006", "email": "ngoctram06@example.com", "password": "User@123"},
    {"name": "Đặng Hải Yến", "phone": "0901000007", "email": "haiyen07@example.com", "password": "User@123"},
    {"name": "Bùi Anh Tuấn", "phone": "0901000008", "email": "anhtuan08@example.com", "password": "User@123"},
    {"name": "Phan Thảo Nhi", "phone": "0901000009", "email": "thaonhi09@example.com", "password": "User@123"},
    {"name": "Ngô Hoài Phương", "phone": "0901000010", "email": "hoaiphuong10@example.com", "password": "User@123"},
    {"name": "Mai Nhật Huy", "phone": "0901000011", "email": "nhathuy11@example.com", "password": "User@123"},
    {"name": "Lý Thanh Vân", "phone": "0901000012", "email": "thanhvan12@example.com", "password": "User@123"},
    {"name": "Đoàn Bảo Châu", "phone": "0901000013", "email": "baochau13@example.com", "password": "User@123"},
    {"name": "Châu Tuệ Lâm", "phone": "0901000014", "email": "tuelam14@example.com", "password": "User@123"},
    {"name": "Tạ Minh Khang", "phone": "0901000015", "email": "minhkhang15@example.com", "password": "User@123"},
    {"name": "Dương Mỹ Duyên", "phone": "0901000016", "email": "myduyen16@example.com", "password": "User@123"},
    {"name": "Hồ Gia Bảo", "phone": "0901000017", "email": "giabao17@example.com", "password": "User@123"},
    {"name": "Tôn Quỳnh Anh", "phone": "0901000018", "email": "quynhanh18@example.com", "password": "User@123"},
    {"name": "La Thành Đạt", "phone": "0901000019", "email": "thanhdat19@example.com", "password": "User@123"},
    {"name": "Kiều Ngọc Mai", "phone": "0901000020", "email": "ngocmai20@example.com", "password": "User@123"},
    {"name": "Lâm Hữu Phước", "phone": "0901000021", "email": "huuphuoc21@example.com", "password": "User@123"},
    {"name": "Nguyễn Bảo Vy", "phone": "0901000022", "email": "baovy22@example.com", "password": "User@123"},
    {"name": "Trịnh Thành Công", "phone": "0901000023", "email": "thanhcong23@example.com", "password": "User@123"},
    {"name": "Phùng Diễm My", "phone": "0901000024", "email": "diemmy24@example.com", "password": "User@123"},
    {"name": "Vũ Khôi Nguyên", "phone": "0901000025", "email": "khoinguyen25@example.com", "password": "User@123"},
    {"name": "Lê Tú Uyên", "phone": "0901000026", "email": "tuyen26@example.com", "password": "User@123"},
    {"name": "Từ Bảo Long", "phone": "0901000027", "email": "baolong27@example.com", "password": "User@123"},
    {"name": "Phạm Kim Ngân", "phone": "0901000028", "email": "kimngan28@example.com", "password": "User@123"},
    {"name": "Đinh Gia Huy", "phone": "0901000029", "email": "giahuy29@example.com", "password": "User@123"},
    {"name": "Nguyễn Tuệ Minh", "phone": "0901000030", "email": "tueminh30@example.com", "password": "User@123"},
]

ADDRESSES = [
    "12 Nguyễn Trãi, Quận 1, TP.HCM",
    "85 Lê Văn Sỹ, Quận 3, TP.HCM",
    "42 Phan Xích Long, Phú Nhuận, TP.HCM",
    "219 Cách Mạng Tháng 8, Quận 10, TP.HCM",
    "88 Nguyễn Oanh, Gò Vấp, TP.HCM",
    "156 Kha Vạn Cân, Thủ Đức, TP.HCM",
    "29 Tô Ký, Quận 12, TP.HCM",
    "61 Hậu Giang, Quận 6, TP.HCM",
    "73 Bình Long, Bình Tân, TP.HCM",
    "104 Lê Trọng Tấn, Tân Phú, TP.HCM",
]

PAYMENTS = ["TIEN_MAT", "CHUYEN_KHOAN"]

# =========================================================
# 3. HELPER FUNCTIONS
# =========================================================
def copy_image(ten_file):
    static_dir = os.path.join(settings.BASE_DIR, "static", "images")
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

    src = os.path.join(static_dir, ten_file)
    dst_rel = f"san_pham/{ten_file}"
    dst_abs = os.path.join(settings.MEDIA_ROOT, dst_rel)
    os.makedirs(os.path.dirname(dst_abs), exist_ok=True)

    if os.path.exists(src):
        shutil.copy2(src, dst_abs)
        return dst_rel

    print(f"  ⚠️ Không tìm thấy ảnh: {src}")
    return None


def tao_anh_cho_san_pham(san_pham, danh_sach_anh):
    for index, ten_file in enumerate(danh_sach_anh):
        path = copy_image(ten_file)
        if path:
            SanPhamImage.objects.create(
                san_pham=san_pham,
                image=path,
                la_anh_chinh=(index == 0),
                thu_tu=index,
            )


def create_tai_khoan(email, ho_ten, dien_thoai, role, password, trang_thai="ACTIVE"):
    tai_khoan, created = TaiKhoan.objects.get_or_create(
        email=email,
        defaults={
            "password_hash": make_password(password),
            "ho_ten": ho_ten,
            "dien_thoai": dien_thoai,
            "role": role,
            "trang_thai": trang_thai,
        },
    )

    if not created:
        changed = False
        if tai_khoan.ho_ten != ho_ten:
            tai_khoan.ho_ten = ho_ten
            changed = True
        if tai_khoan.dien_thoai != dien_thoai:
            tai_khoan.dien_thoai = dien_thoai
            changed = True
        if tai_khoan.role != role:
            tai_khoan.role = role
            changed = True
        if tai_khoan.trang_thai != trang_thai:
            tai_khoan.trang_thai = trang_thai
            changed = True
        if changed:
            tai_khoan.save()

    return tai_khoan


def upsert_nhan_vien_from_tai_khoan(tai_khoan, ten_nhan_vien, chuc_vu, luong, chi_nhanh):
    nhan_vien = NhanVien.objects.filter(tai_khoan=tai_khoan).first()

    if nhan_vien:
        nhan_vien.ten_nhan_vien = ten_nhan_vien
        nhan_vien.chuc_vu = chuc_vu
        nhan_vien.luong = Decimal(str(luong))
        nhan_vien.chi_nhanh = chi_nhanh
        nhan_vien.save()
        return nhan_vien

    return NhanVien.objects.create(
        tai_khoan=tai_khoan,
        ten_nhan_vien=ten_nhan_vien,
        chuc_vu=chuc_vu,
        luong=Decimal(str(luong)),
        chi_nhanh=chi_nhanh,
    )


def create_admin(chi_nhanh):
    admin_acc = create_tai_khoan(
        email="admin@bhx.vn",
        ho_ten="Quản trị viên",
        dien_thoai="0909000000",
        role="ADMIN",
        password="admin123",
    )

    admin_nv = upsert_nhan_vien_from_tai_khoan(
        tai_khoan=admin_acc,
        ten_nhan_vien="Nguyễn Văn An",
        chuc_vu="Quản lý",
        luong="18000000",
        chi_nhanh=chi_nhanh,
    )
    return admin_acc, admin_nv


def create_staff_account_and_employee(index, chi_nhanh, chuc_vu):
    stt = str(index).zfill(4)
    ho_ten = f"Nhân viên {stt}"
    email = f"staff{stt}@bhx.local"
    dien_thoai = f"09{index:08d}"

    tai_khoan = create_tai_khoan(
        email=email,
        ho_ten=ho_ten,
        dien_thoai=dien_thoai,
        role="STAFF",
        password="123456",
    )

    nhan_vien = upsert_nhan_vien_from_tai_khoan(
        tai_khoan=tai_khoan,
        ten_nhan_vien=ho_ten,
        chuc_vu=chuc_vu,
        luong="2000000",
        chi_nhanh=chi_nhanh,
    )

    return tai_khoan, nhan_vien


def create_chi_nhanh():
    result = []
    for row in real_stores:
        cn = ChiNhanh.objects.create(
            ten_chi_nhanh=row["ten"],
            dia_chi=row["dia_chi"],
            latitude=row["vi_do"],
            longitude=row["kinh_do"],
            dien_thoai="19001908",
        )
        result.append(cn)
    return result


def clear_old_data():
    ChiTietHoaDon.objects.all().delete()
    HoaDon.objects.all().delete()
    ChiTietNhapHang.objects.all().delete()
    NhapHang.objects.all().delete()
    NhaCungCap.objects.all().delete()
    SanPhamImage.objects.all().delete()
    SanPham.objects.all().delete()
    LoaiSanPham.objects.all().delete()
    KhachHang.objects.all().delete()
    NhanVien.objects.all().delete()
    TaiKhoan.objects.all().delete()
    ChiNhanh.objects.all().delete()


def create_customers():
    created_accounts = []
    created_customers = []

    for item in CUSTOMERS:
        tai_khoan = create_tai_khoan(
            email=item["email"],
            ho_ten=item["name"],
            dien_thoai=item["phone"],
            role="USER",
            password=item["password"],
        )

        khach_hang, _ = KhachHang.objects.get_or_create(
            tai_khoan=tai_khoan,
            defaults={
                "ten_khach_hang": item["name"],
                "dien_thoai": item["phone"],
                "dia_chi": random.choice(ADDRESSES),
            },
        )

        khach_hang.ten_khach_hang = item["name"]
        khach_hang.dien_thoai = item["phone"]
        if not khach_hang.dia_chi:
            khach_hang.dia_chi = random.choice(ADDRESSES)
        khach_hang.tai_khoan = tai_khoan
        khach_hang.save()

        created_accounts.append(tai_khoan)
        created_customers.append(khach_hang)

    khach_le = KhachHang.objects.create(
        ten_khach_hang="Khách lẻ",
        dien_thoai="0901999999",
        dia_chi="Mua tại cửa hàng",
        tai_khoan=None,
    )

    return created_accounts, created_customers, khach_le


def create_categories():
    return {
        "rau_cu": LoaiSanPham.objects.create(ten_loai="Rau củ"),
        "thit_ca": LoaiSanPham.objects.create(ten_loai="Thịt cá"),
        "do_uong": LoaiSanPham.objects.create(ten_loai="Đồ uống"),
        "banh_keo": LoaiSanPham.objects.create(ten_loai="Bánh kẹo"),
        "hoa_pham": LoaiSanPham.objects.create(ten_loai="Hóa phẩm"),
        "gia_vi": LoaiSanPham.objects.create(ten_loai="Gia vị"),
    }


def create_products(categories):
    ds_san_pham = [
        ("Rau muống 500g", "18000", 120, categories["rau_cu"], True, ["raumuong1.jpg", "raumuong2.jpg", "raumuong3.jpg", "raumuong4.jpg", "raumuong5.jpg"], "Rau muống tươi ngon, phù hợp bữa cơm gia đình."),
        ("Cà chua 1kg", "32000", 80, categories["rau_cu"], True, ["cachua1.jpg", "cachua2.jpg", "cachua3.jpg", "cachua4.jpg", "cachua5.jpg"], "Cà chua đỏ tươi, thích hợp nấu canh và salad."),
        ("Xà lách 300g", "22000", 70, categories["rau_cu"], False, ["xalach1.jpg", "xalach2.jpg", "xalach3.jpg", "xalach4.jpg", "xalach5.jpg"], "Xà lách sạch, giòn ngon, dùng ăn sống tiện lợi."),
        ("Cải ngọt 500g", "19000", 90, categories["rau_cu"], False, ["caingot1.jpg", "caingot2.jpg", "caingot3.jpg", "caingot4.jpg", "caingot5.jpg"], "Cải ngọt xanh tươi, thích hợp luộc hoặc nấu canh."),
        ("Bắp cải 1 cái", "25000", 60, categories["rau_cu"], True, ["bapcai1.jpg", "bapcai2.jpg", "bapcai3.jpg", "bapcai4.jpg", "bapcai5.jpg"], "Bắp cải tươi, ngọt, phù hợp nhiều món ăn."),
        ("Cà rốt 1kg", "28000", 100, categories["rau_cu"], False, ["carot1.jpg", "carot2.jpg", "carot3.jpg", "carot4.jpg", "carot5.jpg"], "Cà rốt giòn ngọt, giàu dinh dưỡng."),
        ("Khoai tây 1kg", "35000", 85, categories["rau_cu"], False, ["khoaitay1.jpg", "khoaitay2.jpg", "khoaitay3.jpg", "khoaitay4.jpg", "khoaitay5.jpg"], "Khoai tây ngon, dùng chiên, xào, nấu đều hợp."),
        ("Dưa leo 1kg", "27000", 95, categories["rau_cu"], True, ["dualeo1.jpg", "dualeo2.jpg", "dualeo3.jpg", "dualeo4.jpg", "dualeo5.jpg"], "Dưa leo tươi mát, giòn, thích hợp ăn sống."),
        ("Bí đỏ 1kg", "24000", 50, categories["rau_cu"], False, ["bido1.jpg", "bido2.jpg", "bido3.jpg", "bido4.jpg", "bido5.jpg"], "Bí đỏ thơm bùi, phù hợp nấu cháo và canh."),
        ("Hành lá 200g", "12000", 150, categories["rau_cu"], False, ["hanhla1.jpg", "hanhla2.jpg", "hanhla3.jpg", "hanhla4.jpg", "hanhla5.jpg"], "Hành lá tươi xanh, tăng hương vị món ăn."),
        ("Thịt heo ba rọi 1kg", "145000", 40, categories["thit_ca"], False, ["thitheobao1.jpg", "thitheobao2.jpg", "thitheobao3.jpg", "thitheobao4.jpg", "thitheobao5.jpg"], "Thịt ba rọi tươi, cân đối nạc mỡ."),
        ("Thịt bò thăn 500g", "185000", 35, categories["thit_ca"], True, ["thitbo1.jpg", "thitbo2.jpg", "thitbo3.jpg", "thitbo4.jpg", "thitbo5.jpg"], "Thịt bò thăn mềm ngon, phù hợp áp chảo."),
        ("Cá hồi phi lê 300g", "99000", 45, categories["thit_ca"], True, ["cahoi1.jpg", "cahoi2.jpg", "cahoi3.jpg", "cahoi4.jpg", "cahoi5.jpg"], "Cá hồi phi lê tươi, giàu omega-3."),
        ("Cá basa 1kg", "89000", 55, categories["thit_ca"], False, ["cabasa1.jpg", "cabasa2.jpg", "cabasa3.jpg", "cabasa4.jpg", "cabasa5.jpg"], "Cá basa tươi, thịt mềm, dễ chế biến."),
        ("Tôm sú 500g", "129000", 30, categories["thit_ca"], True, ["tomsu1.jpg", "tomsu2.jpg", "tomsu3.jpg", "tomsu4.jpg", "tomsu5.jpg"], "Tôm sú chắc thịt, ngọt tự nhiên."),
        ("Mực ống 500g", "119000", 25, categories["thit_ca"], False, ["muc1.jpg", "muc2.jpg", "muc3.jpg", "muc4.jpg", "muc5.jpg"], "Mực ống tươi, dai ngon, phù hợp nướng/xào."),
        ("Trứng gà hộp 10 quả", "32000", 150, categories["thit_ca"], False, ["trungga1.jpg", "trungga2.jpg", "trungga3.jpg", "trungga4.jpg", "trungga5.jpg"], "Trứng gà tươi sạch, tiện lợi cho mọi gia đình."),
        ("Xúc xích tiệt trùng", "25000", 100, categories["thit_ca"], True, ["xucxich1.jpg", "xucxich2.jpg", "xucxich3.jpg", "xucxich4.jpg", "xucxich5.jpg"], "Xúc xích tiện dùng, phù hợp bữa ăn nhanh."),
        ("Nước suối 500ml", "6000", 300, categories["do_uong"], False, ["nuocsuoi1.jpg", "nuocsuoi2.jpg", "nuocsuoi3.jpg", "nuocsuoi4.jpg", "nuocsuoi5.jpg"], "Nước suối tinh khiết, tiện mang theo."),
        ("Coca Cola lon", "11000", 220, categories["do_uong"], True, ["cocacola1.jpg", "cocacola2.jpg", "cocacola3.jpg", "cocacola4.jpg", "cocacola5.jpg"], "Nước ngọt có ga quen thuộc, giải khát hiệu quả."),
        ("Pepsi lon", "10000", 210, categories["do_uong"], True, ["pepsi1.jpg", "pepsi2.jpg", "pepsi3.jpg", "pepsi4.jpg", "pepsi5.jpg"], "Pepsi lon mát lạnh, hương vị đậm đà."),
        ("7Up lon", "10000", 180, categories["do_uong"], False, ["7up1.jpg", "7up2.jpg", "7up3.jpg", "7up4.jpg", "7up5.jpg"], "7Up vị chanh tươi mát."),
        ("Sữa tươi không đường 1L", "38000", 140, categories["do_uong"], True, ["suatuoikhongduong1.jpg", "suatuoikhongduong2.jpg", "suatuoikhongduong3.jpg", "suatuoikhongduong4.jpg", "suatuoikhongduong5.jpg"], "Sữa tươi không đường bổ dưỡng."),
        ("Sữa tươi có đường 1L", "39000", 130, categories["do_uong"], False, ["suatuoiduong1.jpg", "suatuoiduong2.jpg", "suatuoiduong3.jpg", "suatuoiduong4.jpg", "suatuoiduong5.jpg"], "Sữa tươi có đường thơm ngon."),
        ("Nước cam ép 1L", "45000", 75, categories["do_uong"], True, ["nuoccamep1.jpg", "nuoccamep2.jpg", "nuoccamep3.jpg", "nuoccamep4.jpg", "nuoccamep5.jpg"], "Nước cam ép thơm ngon, bổ sung vitamin C."),
        ("Trà xanh chai", "12000", 160, categories["do_uong"], False, ["traxanh1.jpg", "traxanh2.jpg", "traxanh3.jpg", "traxanh4.jpg", "traxanh5.jpg"], "Trà xanh thanh mát."),
        ("Cà phê lon", "15000", 110, categories["do_uong"], False, ["caphelon1.jpg", "caphelon2.jpg", "caphelon3.jpg", "caphelon4.jpg", "caphelon5.jpg"], "Cà phê lon tiện lợi, tỉnh táo mỗi ngày."),
        ("Bánh Oreo", "18000", 150, categories["banh_keo"], True, ["banhoreo1.jpg", "banhoreo2.jpg", "banhoreo3.jpg", "banhoreo4.jpg", "banhoreo5.jpg"], "Bánh Oreo giòn ngon, hấp dẫn."),
        ("Bánh Chocopie", "36000", 100, categories["banh_keo"], False, ["banhchocopie1.jpg", "banhchocopie2.jpg", "banhchocopie3.jpg", "banhchocopie4.jpg", "banhchocopie5.jpg"], "Bánh Chocopie mềm xốp, nhân marshmallow."),
        ("Snack khoai tây", "12000", 180, categories["banh_keo"], True, ["snackkhoaitay1.jpg", "snackkhoaitay2.jpg", "snackkhoaitay3.jpg", "snackkhoaitay4.jpg", "snackkhoaitay5.jpg"], "Snack khoai tây giòn rụm."),
        ("Kẹo dẻo trái cây", "22000", 90, categories["banh_keo"], False, ["keodeotraicay1.jpg", "keodeotraicay2.jpg", "keodeotraicay3.jpg", "keodeotraicay4.jpg", "keodeotraicay5.jpg"], "Kẹo dẻo thơm vị trái cây."),
        ("Socola thanh", "27000", 95, categories["banh_keo"], True, ["socolathanh1.jpg", "socolathanh2.jpg", "socolathanh3.jpg", "socolathanh4.jpg", "socolathanh5.jpg"], "Socola thanh đậm vị cacao."),
        ("Bánh quy bơ", "31000", 80, categories["banh_keo"], False, ["banhquybo1.jpg", "banhquybo2.jpg", "banhquybo3.jpg", "banhquybo4.jpg", "banhquybo5.jpg"], "Bánh quy bơ thơm ngon."),
        ("Nước rửa chén 750ml", "42000", 70, categories["hoa_pham"], True, ["nuocruachen1.jpg", "nuocruachen2.jpg", "nuocruachen3.jpg", "nuocruachen4.jpg", "nuocruachen5.jpg"], "Nước rửa chén sạch dầu mỡ hiệu quả."),
        ("Nước giặt 2.7kg", "135000", 50, categories["hoa_pham"], True, ["nuocgiat1.jpg", "nuocgiat2.jpg", "nuocgiat3.jpg", "nuocgiat4.jpg", "nuocgiat5.jpg"], "Nước giặt sạch thơm lâu."),
        ("Nước lau sàn 1L", "49000", 65, categories["hoa_pham"], False, ["nuoclausan1.jpg", "nuoclausan2.jpg", "nuoclausan3.jpg", "nuoclausan4.jpg", "nuoclausan5.jpg"], "Nước lau sàn sạch khuẩn, thơm mát."),
        ("Khăn giấy hộp", "28000", 120, categories["hoa_pham"], False, ["khangiayhop1.jpg", "khangiayhop2.jpg", "khangiayhop3.jpg", "khangiayhop4.jpg", "khangiayhop5.jpg"], "Khăn giấy mềm mại, tiện dụng."),
        ("Giấy vệ sinh 10 cuộn", "69000", 95, categories["hoa_pham"], True, ["giayvesinh1.jpg", "giayvesinh2.jpg", "giayvesinh3.jpg", "giayvesinh4.jpg", "giayvesinh5.jpg"], "Giấy vệ sinh mềm, thấm hút tốt."),
        ("Kem đánh răng", "32000", 105, categories["hoa_pham"], False, ["kemdanhrang1.jpg", "kemdanhrang2.jpg", "kemdanhrang3.jpg", "kemdanhrang4.jpg", "kemdanhrang5.jpg"], "Kem đánh răng thơm mát, sạch răng."),
        ("Dầu gội 650g", "89000", 60, categories["hoa_pham"], True, ["daugoi1.jpg", "daugoi2.jpg", "daugoi3.jpg", "daugoi4.jpg", "daugoi5.jpg"], "Dầu gội sạch tóc, lưu hương dễ chịu."),
        ("Sữa tắm 900g", "99000", 55, categories["hoa_pham"], False, ["suatam1.jpg", "suatam2.jpg", "suatam3.jpg", "suatam4.jpg", "suatam5.jpg"], "Sữa tắm dịu nhẹ cho da."),
        ("Nước mắm 500ml", "39000", 100, categories["gia_vi"], True, ["nuocmam1.jpg", "nuocmam2.jpg", "nuocmam3.jpg", "nuocmam4.jpg", "nuocmam5.jpg"], "Nước mắm đậm đà, phù hợp bữa cơm Việt."),
        ("Tương ớt 250g", "17000", 140, categories["gia_vi"], False, ["tuongot1.jpg", "tuongot2.jpg", "tuongot3.jpg", "tuongot4.jpg", "tuongot5.jpg"], "Tương ớt cay ngon, tăng vị món ăn."),
        ("Muối i-ốt 500g", "9000", 200, categories["gia_vi"], False, ["muoiiot1.jpg", "muoiiot2.jpg", "muoiiot3.jpg", "muoiiot4.jpg", "muoiiot5.jpg"], "Muối i-ốt thiết yếu cho gia đình."),
        ("Đường trắng 1kg", "26000", 160, categories["gia_vi"], False, ["duongtrang1.jpg", "duongtrang2.jpg", "duongtrang3.jpg", "duongtrang4.jpg", "duongtrang5.jpg"], "Đường trắng tinh luyện, tiện sử dụng."),
        ("Hạt nêm 400g", "42000", 110, categories["gia_vi"], True, ["hatnem1.jpg", "hatnem2.jpg", "hatnem3.jpg", "hatnem4.jpg", "hatnem5.jpg"], "Hạt nêm giúp món ăn đậm đà hơn."),
        ("Tiêu xay 100g", "28000", 90, categories["gia_vi"], False, ["tieuxay1.jpg", "tieuxay2.jpg", "tieuxay3.jpg", "tieuxay4.jpg", "tieuxay5.jpg"], "Tiêu xay thơm cay tự nhiên."),
        ("Dầu ăn 1L", "52000", 130, categories["gia_vi"], True, ["dauan1.jpg", "dauan2.jpg", "dauan3.jpg", "dauan4.jpg", "dauan5.png"], "Dầu ăn tinh luyện, dùng chiên xào tiện lợi."),
        ("Bột ngọt 454g", "36000", 100, categories["gia_vi"], False, ["botngot1.jpg", "botngot2.jpg", "botngot3.jpg", "botngot4.jpg", "botngot5.jpg"], "Bột ngọt giúp món ăn thêm đậm vị."),
    ]

    san_phams = []

    for ten, gia, so_luong, loai, km, danh_sach_anh, mo_ta in ds_san_pham:
        gia_decimal = Decimal(str(gia))
        gia_km = gia_decimal * Decimal("0.9") if km else None

        sp = SanPham.objects.create(
            ten_san_pham=ten,
            don_gia=gia_decimal,
            so_luong=so_luong,
            loai=loai,
            mo_ta=mo_ta,
            is_khuyen_mai=km,
            gia_goc=gia_decimal if km else None,
            gia_khuyen_mai=gia_km if km else None,
        )

        tao_anh_cho_san_pham(sp, danh_sach_anh)
        print(f"  ✅ {ten} - {len(danh_sach_anh)} ảnh")
        san_phams.append(sp)

    return san_phams


def create_suppliers_and_imports(san_phams):
    ncc1 = NhaCungCap.objects.create(
        ten_ncc="Công ty Nông Sản Sạch",
        dien_thoai="02839990001",
        dia_chi="Hóc Môn, TP.HCM",
    )
    ncc2 = NhaCungCap.objects.create(
        ten_ncc="Công ty Thực Phẩm Tươi",
        dien_thoai="02839990002",
        dia_chi="Bình Chánh, TP.HCM",
    )

    nh1 = NhapHang.objects.create(
        ngay_nhap=timezone.make_aware(datetime(2026, 1, 10, 8, 15)),
        nha_cung_cap=ncc1,
    )
    nh2 = NhapHang.objects.create(
        ngay_nhap=timezone.make_aware(datetime(2026, 1, 15, 9, 0)),
        nha_cung_cap=ncc2,
    )

    for sp in san_phams[:10]:
        ChiTietNhapHang.objects.create(
            nhap_hang=nh1,
            san_pham=sp,
            so_luong=200,
            don_gia_nhap=sp.don_gia * Decimal("0.7"),
        )

    for sp in san_phams[10:20]:
        ChiTietNhapHang.objects.create(
            nhap_hang=nh2,
            san_pham=sp,
            so_luong=120,
            don_gia_nhap=sp.don_gia * Decimal("0.75"),
        )


def create_orders(created_customers, khach_le, staffs, san_phams, admin_nv):
    if len(san_phams) < 3:
        raise RuntimeError(f"Cần ít nhất 3 sản phẩm để tạo dữ liệu mẫu. Hiện có {len(san_phams)} sản phẩm.")

    staff_candidates = [s for s in staffs if s.chi_nhanh_id]
    if not staff_candidates:
        staff_candidates = [admin_nv]

    for i in range(40):
        if i < 30:
            kh = created_customers[i % len(created_customers)]
        else:
            kh = khach_le if i % 5 == 0 else random.choice(created_customers)

        nhan_vien = random.choice(staff_candidates)
        order_time = timezone.now() - timedelta(
            days=random.randint(0, 45),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
        )

        dia_chi = kh.dia_chi if kh.dia_chi else random.choice(ADDRESSES)
        sdt = kh.dien_thoai if kh.dien_thoai else "0901999999"
        ten = kh.ten_khach_hang if kh.ten_khach_hang else "Khách lẻ"

        hoa_don = HoaDon.objects.create(
            ngay_lap=order_time,
            khach_hang=kh,
            nhan_vien=nhan_vien,
            dia_chi_giao_hang=dia_chi,
            sdt_nguoi_nhan=sdt,
            ten_nguoi_nhan=ten,
            trang_thai="HOAN_TAT",
            phuong_thuc_thanh_toan=random.choice(PAYMENTS),
        )

        chosen_products = random.sample(san_phams, k=random.randint(2, min(5, len(san_phams))))
        for sp in chosen_products:
            don_gia = sp.gia_hien_tai if hasattr(sp, "gia_hien_tai") else sp.don_gia
            ChiTietHoaDon.objects.create(
                hoa_don=hoa_don,
                san_pham=sp,
                so_luong=random.randint(1, 4),
                don_gia=Decimal(str(don_gia)),
            )


# =========================================================
# 4. RUN SEED
# =========================================================
def run():
    print("Đang chạy import data...")

    print("🧹 Đang dọn dẹp dữ liệu cũ...")
    clear_old_data()

    print("📍 Đang tạo chi nhánh...")
    danh_sach_chi_nhanh_db = create_chi_nhanh()
    if not danh_sach_chi_nhanh_db:
        raise RuntimeError("Không có chi nhánh để seed dữ liệu.")

    print("👑 Đang tạo tài khoản admin...")
    admin_acc, admin_nv = create_admin(danh_sach_chi_nhanh_db[0])

    print("👨‍💼 Đang tạo 2 nhân viên cho mỗi chi nhánh...")
    danh_sach_staff_nv = []
    staff_index = 1

    for chi_nhanh in danh_sach_chi_nhanh_db:
        _, nv_thu_ngan = create_staff_account_and_employee(
            index=staff_index,
            chi_nhanh=chi_nhanh,
            chuc_vu="Thu ngân",
        )
        staff_index += 1

        _, nv_kho = create_staff_account_and_employee(
            index=staff_index,
            chi_nhanh=chi_nhanh,
            chuc_vu="Nhân viên kho",
        )
        staff_index += 1

        danh_sach_staff_nv.extend([nv_thu_ngan, nv_kho])

    print(f"  ✅ Đã tạo {len(danh_sach_staff_nv)} nhân viên staff")

    print("👥 Đang tạo 30 tài khoản khách hàng...")
    created_accounts, created_customers, khach_le = create_customers()

    print("📦 Đang tạo danh mục...")
    categories = create_categories()

    print("🍎 Đang tạo sản phẩm và ảnh...")
    san_phams = create_products(categories)

    print("🚚 Đang tạo nhà cung cấp và nhập hàng...")
    create_suppliers_and_imports(san_phams)

    print("🧾 Đang tạo 40 hóa đơn hoàn tất...")
    create_orders(
        created_customers=created_customers,
        khach_le=khach_le,
        staffs=danh_sach_staff_nv,
        san_phams=san_phams,
        admin_nv=admin_nv,
    )

    print("\n🎉 Seed THÀNH CÔNG!")
    print(f"📍 Chi nhánh: {ChiNhanh.objects.count()}")
    print(f"👨‍💼 Staff: {NhanVien.objects.filter(tai_khoan__role='STAFF').count()}")
    print(f"👤 Khách hàng: {KhachHang.objects.count()}")
    print(f"📦 Sản phẩm: {SanPham.objects.count()}")
    print(f"🧾 Hóa đơn: {HoaDon.objects.count()}")
    print("🔐 Admin: admin@bhx.vn / admin123")
    print("🔐 Mật khẩu mặc định STAFF: 123456")
    print("🔐 Mật khẩu mặc định 30 USER: User@123")
    print("💰 Lương mỗi STAFF: 2.000.000")
    print("💳 Thanh toán chỉ gồm: TIEN_MAT, CHUYEN_KHOAN")
    print("✅ 40 order đều ở trạng thái HOAN_TAT")
    print("\nDanh sách 30 tài khoản khách hàng:")
    for item in CUSTOMERS:
        print(f'- {item["name"]} | {item["phone"]} | {item["email"]} | {item["password"]}')


# =========================================================
# 5. MAIN
# =========================================================
if __name__ == "__main__":
    run()