from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator

from .models import (
    HoaDon,
    ChiTietHoaDon,
    KhachHang,
    SanPham,
    LoaiSanPham,
    TaiKhoan,
    ChiNhanh,
    NhanVien,
)


def ensure_admin_account():
    admin_acc, created = TaiKhoan.objects.get_or_create(
        username="admin",
        defaults={
            "password_hash": "admin123",
            "ho_ten": "Quản trị viên",
            "dien_thoai": "0909000000",
            "role": "ADMIN",
            "trang_thai": "ACTIVE",
        }
    )

    if not created:
        updated = False

        if admin_acc.password_hash != "admin123":
            admin_acc.password_hash = "admin123"
            updated = True
        if admin_acc.ho_ten != "Quản trị viên":
            admin_acc.ho_ten = "Quản trị viên"
            updated = True
        if admin_acc.dien_thoai != "0909000000":
            admin_acc.dien_thoai = "0909000000"
            updated = True
        if admin_acc.role != "ADMIN":
            admin_acc.role = "ADMIN"
            updated = True
        if admin_acc.trang_thai != "ACTIVE":
            admin_acc.trang_thai = "ACTIVE"
            updated = True

        if updated:
            admin_acc.save()


def home(request):
    categories = LoaiSanPham.objects.all().order_by("ten_loai")
    products_km = SanPham.objects.filter(is_khuyen_mai=True).order_by("-id")[:8]
    products_new = SanPham.objects.all().order_by("-id")[:12]

    return render(request, "home.html", {
        "categories": categories,
        "products_km": products_km,
        "products_new": products_new,
    })


def product_list(request):
    q = request.GET.get("q", "")
    category_id = request.GET.get("category", "")

    products = SanPham.objects.all().order_by("id")
    categories = LoaiSanPham.objects.all().order_by("ten_loai")

    if q:
        products = products.filter(ten_san_pham__icontains=q)

    if category_id:
        products = products.filter(loai_id=category_id)

    paginator = Paginator(products, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "store/product_list.html", {
        "page_obj": page_obj,
        "products": page_obj,
        "categories": categories,
        "query": q,
        "selected_category": category_id,
    })


def product_detail(request, pk):
    product = get_object_or_404(SanPham, pk=pk)
    return render(request, "store/product_detail.html", {"product": product})


def add_to_cart(request, pk):
    product = get_object_or_404(SanPham, pk=pk)

    cart = request.session.get("cart", {})
    product_id = str(product.id)

    if product_id in cart:
        cart[product_id]["so_luong"] += 1
    else:
        cart[product_id] = {
            "ten_san_pham": product.ten_san_pham,
            "don_gia": float(product.don_gia),
            "so_luong": 1,
        }

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("store:cart_detail")


def cart_detail(request):
    cart = request.session.get("cart", {})
    cart_items = []
    tong_tien = 0

    for product_id, item in cart.items():
        thanh_tien = item["don_gia"] * item["so_luong"]
        tong_tien += thanh_tien

        cart_items.append({
            "product_id": product_id,
            "ten_san_pham": item["ten_san_pham"],
            "don_gia": item["don_gia"],
            "so_luong": item["so_luong"],
            "thanh_tien": thanh_tien,
        })

    return render(request, "store/cart.html", {
        "cart_items": cart_items,
        "tong_tien": tong_tien,
    })


def remove_from_cart(request, pk):
    cart = request.session.get("cart", {})
    product_id = str(pk)

    if product_id in cart:
        del cart[product_id]
        request.session["cart"] = cart
        request.session.modified = True

    return redirect("store:cart_detail")


def checkout(request):
    cart = request.session.get("cart", {})
    cart_items = []
    tong_tien = 0

    for product_id, item in cart.items():
        thanh_tien = item["don_gia"] * item["so_luong"]
        tong_tien += thanh_tien
        cart_items.append({
            "product_id": product_id,
            "ten_san_pham": item["ten_san_pham"],
            "don_gia": item["don_gia"],
            "so_luong": item["so_luong"],
            "thanh_tien": thanh_tien,
        })

    if not cart:
        return redirect("store:product_list")

    if request.method == "POST":
        ten_nguoi_nhan = request.POST.get("ten_nguoi_nhan")
        sdt_nguoi_nhan = request.POST.get("sdt_nguoi_nhan")
        dia_chi_giao_hang = request.POST.get("dia_chi_giao_hang")
        phuong_thuc_thanh_toan = request.POST.get("phuong_thuc_thanh_toan", "COD")

        khach_hang, _ = KhachHang.objects.get_or_create(
            dien_thoai=sdt_nguoi_nhan,
            defaults={
                "ten_khach_hang": ten_nguoi_nhan,
                "dia_chi": dia_chi_giao_hang,
            }
        )

        nhan_vien = NhanVien.objects.first()

        hoa_don = HoaDon.objects.create(
            ngay_lap=timezone.now(),
            khach_hang=khach_hang,
            nhan_vien=nhan_vien,
            dia_chi_giao_hang=dia_chi_giao_hang,
            sdt_nguoi_nhan=sdt_nguoi_nhan,
            ten_nguoi_nhan=ten_nguoi_nhan,
            trang_thai="CHO_XU_LY",
            phuong_thuc_thanh_toan=phuong_thuc_thanh_toan,
        )

        for product_id, item in cart.items():
            san_pham = SanPham.objects.get(pk=product_id)
            ChiTietHoaDon.objects.create(
                hoa_don=hoa_don,
                san_pham=san_pham,
                so_luong=item["so_luong"],
                don_gia=item["don_gia"],
            )

        request.session["cart"] = {}
        request.session.modified = True

        return redirect("store:order_history")

    return render(request, "store/checkout.html", {
        "cart_items": cart_items,
        "tong_tien": tong_tien,
    })


def order_history(request):
    orders = HoaDon.objects.prefetch_related(
        "chi_tiets__san_pham",
        "khach_hang",
        "nhan_vien"
    ).order_by("-ngay_lap")

    for order in orders:
        tong_tien = 0
        for ct in order.chi_tiets.all():
            ct.thanh_tien = ct.so_luong * ct.don_gia
            tong_tien += ct.thanh_tien
        order.tong_tien = tong_tien

    return render(request, "store/order_history.html", {"orders": orders})


def set_delivery_location(request):
    if request.method == "POST":
        city = request.POST.get("city", "").strip()
        district = request.POST.get("district", "").strip()
        address = request.POST.get("address", "").strip()

        full_address = ", ".join([item for item in [address, district, city] if item])
        request.session["delivery_address"] = full_address

    return redirect(request.META.get("HTTP_REFERER", "/"))


def login_view(request):
    ensure_admin_account()
    error = ""

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        try:
            tai_khoan = TaiKhoan.objects.get(
                username=username,
                password_hash=password,
                trang_thai="ACTIVE"
            )

            request.session["user_id"] = tai_khoan.id
            request.session["username"] = tai_khoan.username
            request.session["role"] = tai_khoan.role
            request.session["ho_ten"] = tai_khoan.ho_ten

            return redirect("home")

        except TaiKhoan.DoesNotExist:
            error = "Sai tài khoản hoặc mật khẩu"

    return render(request, "store/login.html", {"error": error})


def logout_view(request):
    request.session.flush()
    return redirect("home")


def register_view(request):
    error = ""
    success = ""

    if request.method == "POST":
        ho_ten = request.POST.get("ho_ten", "").strip()
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        dien_thoai = request.POST.get("dien_thoai", "").strip()

        if not ho_ten or not username or not password:
            error = "Vui lòng nhập đầy đủ thông tin bắt buộc."
        elif TaiKhoan.objects.filter(username=username).exists():
            error = "Tên đăng nhập đã tồn tại."
        else:
            TaiKhoan.objects.create(
                username=username,
                password_hash=password,
                ho_ten=ho_ten,
                dien_thoai=dien_thoai,
                role="USER",
                trang_thai="ACTIVE",
            )
            success = "Đăng ký thành công. Bạn có thể đăng nhập ngay."

    return render(request, "store/register.html", {
        "error": error,
        "success": success,
    })


def admin_dashboard(request):
    if not request.session.get("user_id"):
        return redirect("store:login")

    if request.session.get("role") != "ADMIN":
        return redirect("home")

    tong_san_pham = SanPham.objects.count()
    tong_khach_hang = KhachHang.objects.count()
    tong_don_hang = HoaDon.objects.count()
    tong_chi_nhanh = ChiNhanh.objects.count()

    don_hang_moi = HoaDon.objects.select_related(
        "khach_hang",
        "nhan_vien"
    ).order_by("-ngay_lap")[:5]

    san_pham_sap_het = SanPham.objects.filter(
        so_luong__lte=10
    ).order_by("so_luong")[:8]

    return render(request, "store/admin_dashboard.html", {
        "tong_san_pham": tong_san_pham,
        "tong_khach_hang": tong_khach_hang,
        "tong_don_hang": tong_don_hang,
        "tong_chi_nhanh": tong_chi_nhanh,
        "don_hang_moi": don_hang_moi,
        "san_pham_sap_het": san_pham_sap_het,
    })