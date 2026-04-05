from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from decimal import Decimal
from django.utils.dateparse import parse_date
from django.db.models import Prefetch, Q
from collections import OrderedDict
from django.http import JsonResponse 
from ..models import ChiTietHoaDon, HoaDon, KhachHang, NhanVien, SanPham, TaiKhoan, ChiNhanh

try:
    from locations.models import CuaHang
except Exception:
    CuaHang = None


TIME_SLOTS = [
    "7H-8H",
    "8H-9H",
    "9H-10",
    "10H-11H",
    "13H-14H",
    "14H-15H",
    "15H-16H",
    "16H-17H",
]


def _get_cart(request):
    return request.session.get("cart", {})


def _save_cart(request, cart):
    request.session["cart"] = cart
    request.session.modified = True


def _get_checkout_state(request):
    return {
        "delivery_method": request.session.get("delivery_method", "delivery"),
        "payment_method": request.session.get("payment_method", "BANK"),
        "delivery_time_slot": request.session.get("delivery_time_slot", ""),
        "address_type": request.session.get("address_type", "current_location"),
        "dia_chi_giao_hang": request.session.get("dia_chi_giao_hang", ""),
        "ten_nguoi_nhan": request.session.get("ten_nguoi_nhan", ""),
        "sdt_nguoi_nhan": request.session.get("sdt_nguoi_nhan", ""),
        "selected_store_id": request.session.get("selected_store_id", ""),
        "selected_store_name": request.session.get("selected_store_name", ""),
        "selected_store_address": request.session.get("selected_store_address", ""),
    }


def _build_cart_items(cart):
    cart_items = []
    tong_tien = Decimal("0")

    for product_id, item in cart.items():
        san_pham = SanPham.objects.filter(pk=product_id).prefetch_related("images").first()
        if not san_pham:
            continue

        don_gia = Decimal(str(item["don_gia"]))
        so_luong = int(item["so_luong"])
        thanh_tien = don_gia * so_luong
        tong_tien += thanh_tien

        anh_chinh = san_pham.anh_chinh
        hinh_anh_url = anh_chinh.image.url if anh_chinh and anh_chinh.image else ""

        cart_items.append(
            {
                "product_id": product_id,
                "ten_san_pham": san_pham.ten_san_pham,
                "don_gia": don_gia,
                "so_luong": so_luong,
                "thanh_tien": thanh_tien,
                "gia_goc": san_pham.gia_goc,
                "anh_chinh": anh_chinh,
                "hinh_anh_url": hinh_anh_url,
            }
        )

    return cart_items, tong_tien




def add_to_cart(request, pk):
    product = get_object_or_404(SanPham, pk=pk)

    cart = _get_cart(request)
    product_id = str(product.id)
    don_gia = float(product.gia_hien_tai)

    if product_id in cart:
        cart[product_id]["so_luong"] += 1
    else:
        cart[product_id] = {
            "ten_san_pham": product.ten_san_pham,
            "don_gia": don_gia,
            "so_luong": 1,
        }

    _save_cart(request, cart)
    
    # Tính tổng số lượng để mốt cập nhật cái số nhỏ nhỏ trên icon giỏ hàng
    tong_sp = sum(item["so_luong"] for item in cart.values())

    # Kiểm tra xem đây có phải là request chạy ngầm (AJAX) không
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success', 
            'cart_count': tong_sp, 
            'message': f'Đã thêm {product.ten_san_pham} vào giỏ!'
        })
    
    # Nếu lỡ trình duyệt không hỗ trợ AJAX thì dùng cách cũ chống cháy
    trang_hien_tai = request.META.get('HTTP_REFERER')
    if trang_hien_tai:
        return redirect(trang_hien_tai)
    else:
        return redirect("store:product_list")


def cart_detail(request):
    cart = _get_cart(request)
    cart_items, tong_tien = _build_cart_items(cart)
    state = _get_checkout_state(request)

    # Lấy dữ liệu từ bảng ChiNhanh (nơi sếp đã nhập tọa độ)
    stores = ChiNhanh.objects.all().order_by("ten_chi_nhanh")

    return render(
        request,
        "store/cart.html",
        {
            "cart_items": cart_items,
            "tong_tien": tong_tien,
            "time_slots": TIME_SLOTS,
            "stores": stores,
            **state,
        },
    )


def update_cart_quantity(request, pk):
    if request.method != "POST":
        return redirect("store:cart_detail")

    action = request.POST.get("action", "").strip()
    cart = _get_cart(request)
    product_id = str(pk)

    if product_id not in cart:
        return redirect("store:cart_detail")

    current_qty = int(cart[product_id].get("so_luong", 1))

    if action == "increase":
        cart[product_id]["so_luong"] = current_qty + 1
    elif action == "decrease":
        new_qty = current_qty - 1
        if new_qty <= 0:
            del cart[product_id]
        else:
            cart[product_id]["so_luong"] = new_qty

    _save_cart(request, cart)
    return redirect("store:cart_detail")


def remove_from_cart(request, pk):
    if request.method != "POST":
        return redirect("store:cart_detail")

    cart = _get_cart(request)
    product_id = str(pk)

    if product_id in cart:
        del cart[product_id]
        _save_cart(request, cart)

    return redirect("store:cart_detail")


def save_checkout_options(request):
    if request.method != "POST":
        return redirect("store:cart_detail")

    request.session["delivery_method"] = request.POST.get("delivery_method", "delivery")
    request.session["payment_method"] = request.POST.get("payment_method", "CHUYEN_KHOAN")
    request.session["delivery_time_slot"] = request.POST.get("delivery_time_slot", "")
    request.session["address_type"] = request.POST.get("address_type", "current_location")
    request.session["dia_chi_giao_hang"] = request.POST.get("dia_chi_giao_hang", "").strip()
    request.session["ten_nguoi_nhan"] = request.POST.get("ten_nguoi_nhan", "").strip()
    request.session["sdt_nguoi_nhan"] = request.POST.get("sdt_nguoi_nhan", "").strip()
    request.session["selected_store_id"] = request.POST.get("selected_store_id", "").strip()
    request.session["selected_store_name"] = request.POST.get("selected_store_name", "").strip()
    request.session["selected_store_address"] = request.POST.get("selected_store_address", "").strip()
    request.session.modified = True

    return redirect("store:cart_detail")

def checkout(request):
    cart = _get_cart(request)
    cart_items, tong_tien = _build_cart_items(cart)

    if not cart_items:
        return redirect("store:product_list")

    state = _get_checkout_state(request)

    if request.method == "POST":
        ten_nguoi_nhan = request.POST.get("ten_nguoi_nhan") or state["ten_nguoi_nhan"]
        sdt_nguoi_nhan = request.POST.get("sdt_nguoi_nhan") or state["sdt_nguoi_nhan"]
        dia_chi_giao_hang = request.POST.get("dia_chi_giao_hang") or state["dia_chi_giao_hang"]
        
        # SỬA LỖI 1: Đồng bộ chữ BANK / CASH từ HTML sang Database
        phuong_thuc_thanh_toan = request.POST.get("phuong_thuc_thanh_toan") or state["payment_method"]
        if phuong_thuc_thanh_toan == "BANK":
            phuong_thuc_thanh_toan = "CHUYEN_KHOAN"
        elif phuong_thuc_thanh_toan == "CASH":
            phuong_thuc_thanh_toan = "TIEN_MAT"
        elif phuong_thuc_thanh_toan not in ["CHUYEN_KHOAN", "TIEN_MAT"]:
            phuong_thuc_thanh_toan = "CHUYEN_KHOAN"
            
        delivery_method = request.POST.get("delivery_method") or state["delivery_method"]

        if delivery_method == "pickup":
            ten_cua_hang = request.POST.get("selected_store_name") or state["selected_store_name"]
            dia_chi_cua_hang = request.POST.get("selected_store_address") or state["selected_store_address"]
            dia_chi_giao_hang = f"Nhận tại cửa hàng: {ten_cua_hang} - {dia_chi_cua_hang}".strip(" -")

        # SỬA LỖI 2 (QUAN TRỌNG): Liên kết Khách Hàng với Tài Khoản đang đăng nhập
        tai_khoan_id = request.session.get("tai_khoan_id")
        tai_khoan = None
        if tai_khoan_id:
            tai_khoan = TaiKhoan.objects.filter(id=tai_khoan_id).first()

        if tai_khoan:
            # Nếu có tài khoản, tìm hoặc tạo Khách hàng gắn với tài khoản đó
            khach_hang = KhachHang.objects.filter(tai_khoan=tai_khoan).first()
            if not khach_hang:
                khach_hang = KhachHang.objects.create(
                    tai_khoan=tai_khoan,
                    ten_khach_hang=ten_nguoi_nhan or tai_khoan.ho_ten,
                    dien_thoai=sdt_nguoi_nhan,
                    dia_chi=dia_chi_giao_hang,
                )
        else:
            # Khách mua không cần đăng nhập
            khach_hang, _ = KhachHang.objects.get_or_create(
                dien_thoai=sdt_nguoi_nhan,
                defaults={
                    "ten_khach_hang": ten_nguoi_nhan or "Khách hàng",
                    "dia_chi": dia_chi_giao_hang,
                },
            )

        # Tránh lỗi nếu chưa tạo Nhân viên trong hệ thống
        nhan_vien = NhanVien.objects.first()

        # Tạo Hóa Đơn
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

        for item in cart_items:
            san_pham = SanPham.objects.get(pk=item["product_id"])
            ChiTietHoaDon.objects.create(
                hoa_don=hoa_don,
                san_pham=san_pham,
                so_luong=item["so_luong"],
                don_gia=item["don_gia"],
            )

        request.session["cart"] = {}
        request.session.modified = True
        return redirect("store:order_history")

    return render(
        request,
        "store/checkout.html",
        {
            "cart_items": cart_items,
            "tong_tien": tong_tien,
            **state,
        },
    )

def _normalize_order_data(orders):
    grouped_orders = OrderedDict()

    for order in orders:
        tong_tien = Decimal("0")
        tong_so_luong = 0
        first_images = []

        for index, ct in enumerate(order.chi_tiets.all()):
            ct.thanh_tien = ct.so_luong * ct.don_gia
            tong_tien += ct.thanh_tien
            tong_so_luong += ct.so_luong

            anh = getattr(ct.san_pham, "anh_chinh", None)
            image_url = ""
            if anh and getattr(anh, "image", None):
                try:
                    image_url = anh.image.url
                except Exception:
                    image_url = ""

            if index < 3:
                first_images.append(
                    {
                        "ten_san_pham": ct.san_pham.ten_san_pham,
                        "image_url": image_url,
                    }
                )

        order.tong_tien = tong_tien
        order.tong_so_luong = tong_so_luong
        order.preview_images = first_images
        order.more_items_count = max(order.chi_tiets.count() - 3, 0)

        ngay_key = order.ngay_lap.date()
        if ngay_key not in grouped_orders:
            grouped_orders[ngay_key] = {
                "date": ngay_key,
                "orders": []
            }

        grouped_orders[ngay_key]["orders"].append(order)

    return list(grouped_orders.values())


def order_history(request):
    role = request.session.get("role", "USER")
    tai_khoan_id = request.session.get("tai_khoan_id")

    selected_date_from = request.GET.get("date_from", "").strip()
    selected_date_to = request.GET.get("date_to", "").strip()
    selected_branch = request.GET.get("branch", "").strip()

    orders = HoaDon.objects.select_related(
        "khach_hang",
        "khach_hang__tai_khoan",
        "nhan_vien",
        "nhan_vien__tai_khoan",
        "nhan_vien__chi_nhanh",
    ).prefetch_related(
        Prefetch("chi_tiets", queryset=HoaDon.chi_tiets.rel.related_model.objects.select_related("san_pham").prefetch_related("san_pham__images"))
    ).order_by("-ngay_lap", "-id")

    if selected_date_from:
        date_from = parse_date(selected_date_from)
        if date_from:
            orders = orders.filter(ngay_lap__date__gte=date_from)

    if selected_date_to:
        date_to = parse_date(selected_date_to)
        if date_to:
            orders = orders.filter(ngay_lap__date__lte=date_to)

    current_account = None
    current_staff = None

    if tai_khoan_id:
        current_account = TaiKhoan.objects.filter(id=tai_khoan_id).first()

    if role == "USER":
        if current_account:
            orders = orders.filter(khach_hang__tai_khoan=current_account)
        else:
            orders = HoaDon.objects.none()

    elif role == "STAFF":
        if current_account:
            current_staff = NhanVien.objects.select_related("chi_nhanh").filter(tai_khoan=current_account).first()

            if current_staff and current_staff.chi_nhanh_id:
                orders = orders.filter(nhan_vien__chi_nhanh=current_staff.chi_nhanh)
            else:
                orders = HoaDon.objects.none()
        else:
            orders = HoaDon.objects.none()

    elif role == "ADMIN":
        if selected_branch:
            orders = orders.filter(nhan_vien__chi_nhanh_id=selected_branch)

    for order in orders:
        order.branch_name = ""
        if order.nhan_vien and order.nhan_vien.chi_nhanh:
            order.branch_name = order.nhan_vien.chi_nhanh.ten_chi_nhanh

        order.customer_name = ""
        if order.khach_hang:
            order.customer_name = order.khach_hang.ten_khach_hang or "Khách lẻ"

        order.customer_phone = ""
        if order.khach_hang:
            order.customer_phone = order.khach_hang.dien_thoai or order.sdt_nguoi_nhan or ""

        order.is_guest = not bool(getattr(order.khach_hang, "tai_khoan", None))

    grouped_orders = _normalize_order_data(orders)
    branches = ChiNhanh.objects.all().order_by("ten_chi_nhanh")

    return render(
        request,
        "store/order_history.html",
        {
            "grouped_orders": grouped_orders,
            "role": role,
            "branches": branches,
            "selected_branch": selected_branch,
            "selected_date_from": selected_date_from,
            "selected_date_to": selected_date_to,
            "current_staff": current_staff,
        },
    )