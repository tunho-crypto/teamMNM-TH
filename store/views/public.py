from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.db import IntegrityError

from ..models import (
    LoaiSanPham,
    SanPham,
    SanPhamImage,
    DanhGiaSanPham,
    BinhLuanSanPham,
    TaiKhoan,
)
from .common import paginate_queryset
from ..forms import DanhGiaSanPhamForm, BinhLuanSanPhamForm


def home(request):
    categories = LoaiSanPham.objects.all().order_by("ten_loai")
    products_km = SanPham.objects.prefetch_related("images").filter(is_khuyen_mai=True).order_by("-id")[:8]
    products_new = SanPham.objects.prefetch_related("images").all().order_by("-id")[:12]

    return render(
        request,
        "store/home.html",
        {
            "categories": categories,
            "products_km": products_km,
            "products_new": products_new,
        },
    )

def product_list(request):
    q = request.GET.get("q", "")
    category_id = request.GET.get("category", "")
    # 1. Bắt tín hiệu Mức giá từ HTML gửi lên
    selected_price = request.GET.get("price", "")

    products = SanPham.objects.prefetch_related("images").all().order_by("id")
    categories = LoaiSanPham.objects.all().order_by("ten_loai")

    # Lọc theo từ khóa tìm kiếm
    if q:
        products = products.filter(ten_san_pham__icontains=q)

    # Lọc theo danh mục
    if category_id:
        products = products.filter(loai_id=category_id)

    # 2. Xử lý bộ lọc theo GIÁ (Dựa vào cột don_gia của bạn)
    if selected_price == 'under_50':
        products = products.filter(don_gia__lt=50000)
    elif selected_price == '50_100':
        products = products.filter(don_gia__gte=50000, don_gia__lte=100000)
    elif selected_price == 'over_100':
        products = products.filter(don_gia__gt=100000)

    page_obj = paginate_queryset(request, products, 8)

    return render(
        request,
        "store/product_list.html",
        {
            "page_obj": page_obj,
            "products": page_obj,
            "categories": categories,
            "query": q,
            "selected_category": category_id,
            # 3. Truyền biến selected_price ra HTML để nó in đậm cái menu đang chọn
            "selected_price": selected_price, 
        },
    )

def product_detail(request, pk):
    product = get_object_or_404(
        SanPham.objects.prefetch_related("images", "binh_luans__tai_khoan"),
        pk=pk
    )
    images = product.images.all()
    binh_luans = product.binh_luans.filter(hien_thi=True)

    tai_khoan_id = request.session.get("tai_khoan_id")
    tai_khoan = None
    my_comment = None

    if tai_khoan_id:
        tai_khoan = TaiKhoan.objects.filter(id=tai_khoan_id).first()
        if tai_khoan:
            my_comment = BinhLuanSanPham.objects.filter(
                san_pham=product,
                tai_khoan=tai_khoan
            ).first()

    if request.method == "POST":
        if not tai_khoan_id:
            messages.error(request, "Vui lòng đăng nhập để bình luận.")
            return redirect("store:login")

        if my_comment:
            messages.warning(request, "Bạn đã bình luận sản phẩm này rồi. Hãy sửa hoặc xóa bình luận cũ.")
            return redirect("store:product_detail", pk=product.pk)

        form = BinhLuanSanPhamForm(request.POST)
        if form.is_valid():
            binh_luan = form.save(commit=False)
            binh_luan.san_pham = product
            binh_luan.tai_khoan_id = tai_khoan_id
            if not binh_luan.so_sao:
                binh_luan.so_sao = 5

            try:
                binh_luan.save()
                messages.success(request, "Đã gửi bình luận của bạn.")
            except IntegrityError:
                messages.warning(request, "Bạn đã bình luận sản phẩm này rồi. Hãy sửa hoặc xóa bình luận cũ.")

            return redirect("store:product_detail", pk=product.pk)
    else:
        form = BinhLuanSanPhamForm(initial={"so_sao": 5})

    return render(
        request,
        "store/product_detail.html",
        {
            "product": product,
            "images": images,
            "binh_luans": binh_luans,
            "comment_form": form,
            "my_comment": my_comment,
        },
    )


def edit_product_comment(request, pk):
    tai_khoan_id = request.session.get("tai_khoan_id")
    if not tai_khoan_id:
        messages.error(request, "Vui lòng đăng nhập để sửa bình luận.")
        return redirect("store:login")

    comment = get_object_or_404(
        BinhLuanSanPham.objects.select_related("san_pham", "tai_khoan"),
        pk=pk,
        tai_khoan_id=tai_khoan_id,
    )

    if request.method != "POST":
        return redirect("store:product_detail", pk=comment.san_pham_id)

    form = BinhLuanSanPhamForm(request.POST, instance=comment)
    if form.is_valid():
        updated_comment = form.save(commit=False)
        if not updated_comment.so_sao:
            updated_comment.so_sao = 5
        updated_comment.save()
        messages.success(request, "Đã cập nhật bình luận của bạn.")
    else:
        messages.error(request, "Dữ liệu không hợp lệ. Vui lòng kiểm tra lại.")

    return redirect("store:product_detail", pk=comment.san_pham_id)


def delete_product_comment(request, pk):
    tai_khoan_id = request.session.get("tai_khoan_id")
    if not tai_khoan_id:
        messages.error(request, "Vui lòng đăng nhập để xóa bình luận.")
        return redirect("store:login")

    comment = get_object_or_404(
        BinhLuanSanPham.objects.select_related("san_pham", "tai_khoan"),
        pk=pk,
        tai_khoan_id=tai_khoan_id,
    )

    product_id = comment.san_pham_id

    if request.method == "POST":
        comment.delete()
        messages.success(request, "Đã xóa bình luận của bạn.")

    return redirect("store:product_detail", pk=product_id)


def set_delivery_location(request):
    if request.method == "POST":
        city = request.POST.get("city", "").strip()
        district = request.POST.get("district", "").strip()
        address = request.POST.get("address", "").strip()

        full_address = ", ".join([item for item in [address, district, city] if item])
        request.session["delivery_address"] = full_address

    return redirect(request.META.get("HTTP_REFERER", "/"))