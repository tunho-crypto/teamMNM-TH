from django.urls import path
from . import api_views
app_name = "store"

urlpatterns = [
    path('api/admin/products/', api_views.admin_get_products),
    path('api/admin/orders/', api_views.admin_get_orders),
    path('api/admin/orders/update-status/<int:pk>/', api_views.admin_update_order_status),
    path('api/verify-otp/', api_views.xac_thuc_otp_api),
    path('api/resend-otp/', api_views.gui_lai_otp_api),
    path('api/forgot-password/', api_views.quen_mat_khau_api),
    path('api/reset-password/', api_views.dat_lai_mat_khau_api),
    path('api/pos/checkout/', api_views.pos_thanh_toan_api),
    path('api/admin/accounts/', api_views.admin_get_accounts),
    path('api/admin/branches/', api_views.admin_get_branches),
    path('api/admin/customers/', api_views.admin_get_customers),
    path('api/locations/', api_views.api_danh_sach_cua_hang),
    path('api/locations/<int:pk>/', api_views.api_chi_tiet_cua_hang),
    path('api/locations/<int:pk>/comment/add/', api_views.api_gui_binh_luan_cua_hang),
    path('api/inventory/', api_views.api_quan_ly_ton_kho),
    path('api/inventory/update/<int:pk>/', api_views.api_cap_nhat_ton_kho),
    path('api/products/comments/edit/<int:pk>/', api_views.edit_product_comment_api),
    path('api/products/comments/delete/<int:pk>/', api_views.delete_product_comment_api),
    path('api/admin/import-excel/', api_views.import_excel_api),
    path('api/orders/history/<int:khach_hang_id>/', api_views.lich_su_don_hang_api),
    path('api/orders/cancel/<int:order_id>/', api_views.hu_don_hang_api),
    path('api/admin/dashboard-stats/', api_views.admin_dashboard_stats_api),
    path('api/admin/export-excel/', api_views.export_excel_api),
    path('api/register/', api_views.dang_ky_api, name='api_register'),
    path('api/products/<int:pk>/comments/', api_views.get_binh_luan_san_pham, name='api_get_comments'),
    path('api/products/<int:pk>/comments/add/', api_views.gui_binh_luan_api, name='api_add_comment'),
    path('api/login/', api_views.dang_nhap_api, name='api_login'),
    path('api/products/<int:pk>/', api_views.get_chi_tiet_san_pham, name='api_product_detail'),
    path('api/branches/', api_views.get_danh_sach_chi_nhanh, name='api_branches'),
    path('api/products/', api_views.get_danh_sach_san_pham, name='api_products'),
    path('api/checkout/', api_views.xu_ly_thanh_toan_api, name='api_checkout'),
    path('api/categories/', api_views.get_danh_sach_loai_san_pham, name='api_categories'),

]
