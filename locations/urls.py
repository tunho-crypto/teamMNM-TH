# File: locations/urls.py
from django.urls import path
from . import views

# Bắt buộc phải có biến này thì Django mới hết lỗi
urlpatterns = [
    path('ban-do/', views.ban_do_tim_kiem, name='map_search'),
    path('danh-sach/', views.danh_sach_cua_hang, name='store_list'),
    path('chi-tiet/<int:pk>/', views.chi_tiet_cua_hang, name='store_detail'),
]
