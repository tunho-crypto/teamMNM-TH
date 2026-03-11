import os
import django

# Thiết lập môi trường Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quanly_bhx_core.settings')
django.setup()

from locations.models import CuaHang

# Danh sách dữ liệu THẬT (Tên, Địa chỉ, Vĩ độ, Kinh độ)
real_stores = [
    # --- QUẬN 1 & QUẬN 3 ---
    {"ten": "BHX Đề Thám", "dia_chi": "160 Đề Thám, P. Cầu Ông Lãnh, Quận 1", "vi_do": 10.765689, "kinh_do": 106.694692},
    {"ten": "BHX Trần Quang Khải", "dia_chi": "128 Trần Quang Khải, P. Tân Định, Quận 1", "vi_do": 10.793282, "kinh_do": 106.690858},
    {"ten": "BHX Bùi Viện", "dia_chi": "15 Bùi Viện, P. Phạm Ngũ Lão, Quận 1", "vi_do": 10.767111, "kinh_do": 106.693444},
    {"ten": "BHX Cống Quỳnh", "dia_chi": "189 Cống Quỳnh, P. Nguyễn Cư Trinh, Quận 1", "vi_do": 10.765222, "kinh_do": 106.687333},
    {"ten": "BHX Lý Thái Tổ", "dia_chi": "268/16 Lý Thái Tổ, Phường 1, Quận 3", "vi_do": 10.766321, "kinh_do": 106.678123},
    {"ten": "BHX CMT8 Q3", "dia_chi": "456 Cách Mạng Tháng 8, Phường 11, Quận 3", "vi_do": 10.785642, "kinh_do": 106.666321},
    {"ten": "BHX Nguyễn Đình Chiểu", "dia_chi": "23 Nguyễn Đình Chiểu, Phường 4, Quận 3", "vi_do": 10.776512, "kinh_do": 106.685432},
    {"ten": "BHX Lê Văn Sỹ Q3", "dia_chi": "350 Lê Văn Sỹ, Phường 14, Quận 3", "vi_do": 10.787111, "kinh_do": 106.674222},

    # --- QUẬN 4 & QUẬN 5 ---
    {"ten": "BHX Tôn Đản", "dia_chi": "120 Tôn Đản, Phường 10, Quận 4", "vi_do": 10.760214, "kinh_do": 106.705632},
    {"ten": "BHX Hoàng Diệu", "dia_chi": "85 Hoàng Diệu, Phường 12, Quận 4", "vi_do": 10.762831, "kinh_do": 106.700142},
    {"ten": "BHX Bến Vân Đồn", "dia_chi": "300 Bến Vân Đồn, Phường 2, Quận 4", "vi_do": 10.761111, "kinh_do": 106.695222},
    {"ten": "BHX Đoàn Văn Bơ", "dia_chi": "250 Đoàn Văn Bơ, Phường 14, Quận 4", "vi_do": 10.758333, "kinh_do": 106.708111},
    {"ten": "BHX Nguyễn Trãi", "dia_chi": "400 Nguyễn Trãi, Phường 8, Quận 5", "vi_do": 10.756281, "kinh_do": 106.675392},
    {"ten": "BHX Trần Hưng Đạo", "dia_chi": "800 Trần Hưng Đạo, Phường 7, Quận 5", "vi_do": 10.753123, "kinh_do": 106.671234},
    {"ten": "BHX An Dương Vương", "dia_chi": "105 An Dương Vương, Phường 8, Quận 5", "vi_do": 10.757891, "kinh_do": 106.673456},
    {"ten": "BHX Nguyễn Tri Phương", "dia_chi": "150 Nguyễn Tri Phương, Phường 9, Quận 5", "vi_do": 10.759222, "kinh_do": 106.668111},

    # --- QUẬN 10 & QUẬN 11 ---
    {"ten": "BHX Hòa Hưng", "dia_chi": "97 Hòa Hưng, Phường 12, Quận 10", "vi_do": 10.778540, "kinh_do": 106.673210},
    {"ten": "BHX 3/2 Q10", "dia_chi": "450 Đường 3/2, Phường 12, Quận 10", "vi_do": 10.768912, "kinh_do": 106.668912},
    {"ten": "BHX Sư Vạn Hạnh", "dia_chi": "780 Sư Vạn Hạnh, Phường 12, Quận 10", "vi_do": 10.774111, "kinh_do": 106.667222},
    {"ten": "BHX Thành Thái", "dia_chi": "112 Thành Thái, Phường 14, Quận 10", "vi_do": 10.771222, "kinh_do": 106.663111},
    {"ten": "BHX Lạc Long Quân Q11", "dia_chi": "300 Lạc Long Quân, Phường 5, Quận 11", "vi_do": 10.765432, "kinh_do": 106.645678},
    {"ten": "BHX Bình Thới", "dia_chi": "150 Bình Thới, Phường 14, Quận 11", "vi_do": 10.766789, "kinh_do": 106.642345},
    {"ten": "BHX Ông Ích Khiêm", "dia_chi": "80 Ông Ích Khiêm, Phường 5, Quận 11", "vi_do": 10.768111, "kinh_do": 106.648222},
    {"ten": "BHX Minh Phụng", "dia_chi": "220 Minh Phụng, Phường 9, Quận 11", "vi_do": 10.762222, "kinh_do": 106.644111},

    # --- QUẬN 6 & QUẬN 8 ---
    {"ten": "BHX Nguyễn Văn Luông", "dia_chi": "249 Nguyễn Văn Luông, Phường 11, Quận 6", "vi_do": 10.745670, "kinh_do": 106.634560},
    {"ten": "BHX Hậu Giang", "dia_chi": "600 Hậu Giang, Phường 12, Quận 6", "vi_do": 10.748912, "kinh_do": 106.625678},
    {"ten": "BHX Bà Hom", "dia_chi": "120 Bà Hom, Phường 13, Quận 6", "vi_do": 10.752111, "kinh_do": 106.628222},
    {"ten": "BHX Bình Tiên", "dia_chi": "85 Bình Tiên, Phường 3, Quận 6", "vi_do": 10.744222, "kinh_do": 106.638111},
    {"ten": "BHX Phạm Thế Hiển Q8", "dia_chi": "1500 Phạm Thế Hiển, Phường 6, Quận 8", "vi_do": 10.735671, "kinh_do": 106.654321},
    {"ten": "BHX Tạ Quang Bửu", "dia_chi": "890 Tạ Quang Bửu, Phường 5, Quận 8", "vi_do": 10.741234, "kinh_do": 106.661234},
    {"ten": "BHX Tùng Thiện Vương", "dia_chi": "210 Tùng Thiện Vương, Phường 11, Quận 8", "vi_do": 10.748912, "kinh_do": 106.656789},
    {"ten": "BHX Phạm Hùng Q8", "dia_chi": "350 Phạm Hùng, Phường 5, Quận 8", "vi_do": 10.738111, "kinh_do": 106.665222},

    # --- QUẬN 7 & NHÀ BÈ & BÌNH CHÁNH ---
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

    # --- TÂN BÌNH & TÂN PHÚ ---
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

    # --- BÌNH TÂN ---
    {"ten": "BHX 43A Bình Thành", "dia_chi": "43A Bình Thành, P. Bình Hưng Hòa B, Bình Tân", "vi_do": 10.801307, "kinh_do": 106.586870},
    {"ten": "BHX Tỉnh Lộ 10", "dia_chi": "1000 Tỉnh Lộ 10, P. Tân Tạo, Bình Tân", "vi_do": 10.756789, "kinh_do": 106.601234},
    {"ten": "BHX Lê Văn Quới", "dia_chi": "400 Lê Văn Quới, P. Bình Hưng Hòa A, Bình Tân", "vi_do": 10.771234, "kinh_do": 106.612345},
    {"ten": "BHX Mã Lò", "dia_chi": "650 Mã Lò, P. Bình Trị Đông A, Bình Tân", "vi_do": 10.765111, "kinh_do": 106.605222},
    {"ten": "BHX Tân Hòa Đông", "dia_chi": "280 Tân Hòa Đông, P. Bình Trị Đông, Bình Tân", "vi_do": 10.758222, "kinh_do": 106.618111},
    {"ten": "BHX Hương Lộ 2", "dia_chi": "800 Hương Lộ 2, P. Bình Trị Đông A, Bình Tân", "vi_do": 10.769111, "kinh_do": 106.602222},
    {"ten": "BHX Kinh Dương Vương", "dia_chi": "550 Kinh Dương Vương, P. An Lạc, Bình Tân", "vi_do": 10.735222, "kinh_do": 106.615111},

    # --- BÌNH THẠNH & PHÚ NHUẬN ---
    {"ten": "BHX Xô Viết Nghệ Tĩnh", "dia_chi": "450 Xô Viết Nghệ Tĩnh, Phường 25, Bình Thạnh", "vi_do": 10.804567, "kinh_do": 106.712345},
    {"ten": "BHX Nơ Trang Long", "dia_chi": "230 Nơ Trang Long, Phường 12, Bình Thạnh", "vi_do": 10.815678, "kinh_do": 106.701234},
    {"ten": "BHX Bùi Đình Túy", "dia_chi": "115 Bùi Đình Túy, Phường 24, Bình Thạnh", "vi_do": 10.806789, "kinh_do": 106.704567},
    {"ten": "BHX Lê Quang Định", "dia_chi": "400 Lê Quang Định, Phường 11, Bình Thạnh", "vi_do": 10.812345, "kinh_do": 106.694567},
    {"ten": "BHX Chu Văn An", "dia_chi": "180 Chu Văn An, Phường 26, Bình Thạnh", "vi_do": 10.811111, "kinh_do": 106.708222},
    {"ten": "BHX Phan Đình Phùng", "dia_chi": "200 Phan Đình Phùng, Phường 1, Phú Nhuận", "vi_do": 10.795432, "kinh_do": 106.682345},
    {"ten": "BHX Huỳnh Văn Bánh", "dia_chi": "150 Huỳnh Văn Bánh, Phường 12, Phú Nhuận", "vi_do": 10.791234, "kinh_do": 106.675678},
    {"ten": "BHX Nguyễn Kiệm PN", "dia_chi": "600 Nguyễn Kiệm, Phường 4, Phú Nhuận", "vi_do": 10.805111, "kinh_do": 106.681222},

    # --- GÒ VẤP ---
    {"ten": "BHX Quang Trung GV", "dia_chi": "650 Quang Trung, Phường 11, Gò Vấp", "vi_do": 10.835432, "kinh_do": 106.654321},
    {"ten": "BHX Lê Văn Thọ", "dia_chi": "230 Lê Văn Thọ, Phường 11, Gò Vấp", "vi_do": 10.842345, "kinh_do": 106.656789},
    {"ten": "BHX Phan Huy Ích GV", "dia_chi": "150 Phan Huy Ích, Phường 12, Gò Vấp", "vi_do": 10.837891, "kinh_do": 106.641234},
    {"ten": "BHX Nguyễn Văn Nghi", "dia_chi": "112 Nguyễn Văn Nghi, Phường 7, Gò Vấp", "vi_do": 10.824567, "kinh_do": 106.685678},
    {"ten": "BHX Phạm Văn Chiêu", "dia_chi": "350 Phạm Văn Chiêu, Phường 9, Gò Vấp", "vi_do": 10.845111, "kinh_do": 106.648222},
    {"ten": "BHX Thống Nhất", "dia_chi": "200 Thống Nhất, Phường 10, Gò Vấp", "vi_do": 10.838222, "kinh_do": 106.665111},
    {"ten": "BHX Nguyễn Oanh", "dia_chi": "400 Nguyễn Oanh, Phường 6, Gò Vấp", "vi_do": 10.841111, "kinh_do": 106.678222},
    {"ten": "BHX Lê Đức Thọ", "dia_chi": "800 Lê Đức Thọ, Phường 15, Gò Vấp", "vi_do": 10.848222, "kinh_do": 106.668111},

    # --- TP. THỦ ĐỨC (Q2, Q9, Thủ Đức) ---
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

    # --- QUẬN 12, HÓC MÔN & CỦ CHI ---
    {"ten": "BHX Nguyễn Ảnh Thủ Q12", "dia_chi": "150 Nguyễn Ảnh Thủ, P. Hiệp Thành, Quận 12", "vi_do": 10.875678, "kinh_do": 106.631234},
    {"ten": "BHX Lê Văn Khương", "dia_chi": "350 Lê Văn Khương, P. Thới An, Quận 12", "vi_do": 10.881234, "kinh_do": 106.645678},
    {"ten": "BHX Tô Ký", "dia_chi": "400 Tô Ký, P. Tân Chánh Hiệp, Quận 12", "vi_do": 10.865111, "kinh_do": 106.618222},
    {"ten": "BHX Vườn Lài", "dia_chi": "120 Vườn Lài, P. An Phú Đông, Quận 12", "vi_do": 10.845222, "kinh_do": 106.685111},
    {"ten": "BHX Phan Văn Hớn HM", "dia_chi": "120 Phan Văn Hớn, Bà Điểm, Hóc Môn", "vi_do": 10.841234, "kinh_do": 106.601234},
    {"ten": "BHX Đặng Thúc Vịnh", "dia_chi": "250 Đặng Thúc Vịnh, Đông Thạnh, Hóc Môn", "vi_do": 10.901111, "kinh_do": 106.615222},
    {"ten": "BHX Nguyễn Văn Bứa", "dia_chi": "180 Nguyễn Văn Bứa, Xuân Thới Sơn, Hóc Môn", "vi_do": 10.875222, "kinh_do": 106.568111},
    {"ten": "BHX Tỉnh Lộ 8", "dia_chi": "500 Tỉnh Lộ 8, TT Củ Chi, Củ Chi", "vi_do": 10.971111, "kinh_do": 106.515222},
    {"ten": "BHX Quốc Lộ 22", "dia_chi": "1200 Quốc Lộ 22, Tân An Hội, Củ Chi", "vi_do": 10.965222, "kinh_do": 106.501111},
    {"ten": "BHX Tỉnh Lộ 15", "dia_chi": "300 Tỉnh Lộ 15, Tân Thạnh Đông, Củ Chi", "vi_do": 10.951111, "kinh_do": 106.585222}
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