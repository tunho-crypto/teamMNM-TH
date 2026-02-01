# File: quanly_bhx_core/urls.py
from django.contrib import admin
from django.urls import path, include # <--- Nhớ import include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Nối dây đến app locations
    path('locations/', include('locations.urls')), 
    
    # (Sau này làm store và dashboard thì thêm tiếp vào đây)
]