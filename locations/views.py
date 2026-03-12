# File: locations/views.py
from django.shortcuts import render, get_object_or_404
from .models import CuaHang
import json

# --- 1. Hàm cho trang Bản đồ ---
def ban_do_tim_kiem(request):
    # Lấy dữ liệu cửa hàng từ Database
    tat_ca_cua_hang = CuaHang.objects.all()
    
    # Chuyển dữ liệu sang JSON để JavaScript vẽ được bản đồ
    danh_sach_json = []
    for ch in tat_ca_cua_hang:
        danh_sach_json.append({
            'ten': ch.ten_cua_hang,
            'lat': ch.vi_do,
            'lon': ch.kinh_do,
            'id': ch.id,
            'dia_chi': ch.dia_chi # Thêm địa chỉ để hiển thị popup
        })

    context = {
        'stores_json': json.dumps(danh_sach_json) # Gửi cục JSON này qua HTML
    }
    return render(request, 'locations/map_search.html', context)

# --- 2. Hàm cho trang Danh sách ---
# locations/views.py
from django.db.models import Q # Nhớ import cái này

def danh_sach_cua_hang(request):
    stores = CuaHang.objects.all()
    
    # Lấy từ khóa tìm kiếm từ thanh địa chỉ (URL)
    quan_huyen = request.GET.get('quan') # Ví dụ: ?quan=Quận 1
    tu_khoa = request.GET.get('q')       # Ví dụ: ?q=Lê Lợi

    # Lọc theo Quận (Nếu có chọn)
    if quan_huyen and quan_huyen != 'all':
        stores = stores.filter(dia_chi__icontains=quan_huyen)

    # Lọc theo từ khóa tự nhập (Tên hoặc Địa chỉ)
    if tu_khoa:
        stores = stores.filter(
            Q(ten_cua_hang__icontains=tu_khoa) | 
            Q(dia_chi__icontains=tu_khoa)
        )

    # Danh sách các quận để hiển thị trong Dropdown (Hardcode cho nhanh)
    danh_sach_quan = ['Quận 1', 'Quận 3', 'Quận 4', 'Quận 5', 'Quận 7', 'Quận 10', 'Bình Thạnh', 'Thủ Đức', 'Tân Bình', 'Gò Vấp']

    context = {
        'stores': stores,
        'danh_sach_quan': danh_sach_quan,
        'dang_chon_quan': quan_huyen, # Để giữ lại lựa chọn cũ
        'dang_tim_kiem': tu_khoa
    }
    return render(request, 'locations/store_list.html', context)
# --- 3. Hàm cho trang Chi tiết ---
def chi_tiet_cua_hang(request, pk):
    store = get_object_or_404(CuaHang, pk=pk)
    return render(request, 'locations/store_detail.html', {'store': store})
# Trong file views.py
from store.models import ChiNhanh

def map_view(request):
    # Lấy danh sách tên cửa hàng
    danh_sach_ten = ChiNhanh.objects.values_list('ten_chi_nhanh', flat=True)
    
    context = {
        'danh_sach_ten': danh_sach_ten,
        # ... các biến khác của bạn
    }
    return render(request, 'locations/map_search.html', context)