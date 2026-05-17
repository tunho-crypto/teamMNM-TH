#!/usr/bin/env python
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quanly_bhx_core.settings')
django.setup()

from store.models import SanPham
from store.serializers import SanPhamSerializer

# Lấy 1 sản phẩm đầu tiên
san_pham = SanPham.objects.first()
if san_pham:
    print(f"Sản phẩm: {san_pham.ten_san_pham}")
    print(f"ID: {san_pham.id}")
    print(f"Có bao nhiêu ảnh: {san_pham.images.count()}")
    
    # In chi tiết từng ảnh
    for img in san_pham.images.all():
        print(f"  - Ảnh: {img.image.url}, Ảnh chính: {img.la_anh_chinh}")
    
    # Kiểm tra anh_chinh property
    anh_chinh = san_pham.anh_chinh
    print(f"Ảnh chính trả về: {anh_chinh}")
    if anh_chinh:
        print(f"  URL ảnh chính: {anh_chinh.image.url}")
    
    # Serialize
    serializer = SanPhamSerializer(san_pham)
    print("\n=== API RESPONSE ===")
    print(json.dumps(serializer.data, indent=2, ensure_ascii=False, default=str))
else:
    print("Không có sản phẩm nào trong database!")
