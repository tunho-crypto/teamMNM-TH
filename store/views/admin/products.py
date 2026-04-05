from django.contrib import messages
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, render, redirect

from ...forms import SanPhamForm
from ...models import LoaiSanPham, SanPham, SanPhamImage
from ..common import admin_required, paginate_queryset


# FormSet: tối đa 10 ảnh, tối thiểu hiển thị 5 ô trống
SanPhamImageFormSet = inlineformset_factory(
    SanPham,
    SanPhamImage,
    fields=("image", "la_anh_chinh", "thu_tu"),
    extra=5,
    max_num=10,
    can_delete=True,
)


@admin_required
def admin_product_list(request):
    q = request.GET.get("q", "").strip()
    loai_id = request.GET.get("loai", "").strip()

    products = SanPham.objects.select_related("loai").prefetch_related("images").order_by("-id")
    categories = LoaiSanPham.objects.all().order_by("ten_loai")

    if q:
        products = products.filter(ten_san_pham__icontains=q)
    if loai_id:
        products = products.filter(loai_id=loai_id)

    page_obj = paginate_queryset(request, products, 8)

    return render(
        request,
        "store/admin/product_list.html",
        {
            "page_obj": page_obj,
            "categories": categories,
            "q": q,
            "loai_id": loai_id,
        },
    )


@admin_required
def admin_product_create(request):
    if request.method == "POST":
        form = SanPhamForm(request.POST, request.FILES)
        formset = SanPhamImageFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            product = form.save()
            formset.instance = product
            formset.save()
            messages.success(request, f"Đã thêm sản phẩm: {product.ten_san_pham}")
            return redirect("store:admin_product_list")
    else:
        form = SanPhamForm()
        formset = SanPhamImageFormSet()

    return render(
        request,
        "store/admin/product_form.html",
        {
            "form": form,
            "formset": formset,
            "title": "Thêm sản phẩm",
        },
    )


@admin_required
def admin_product_edit(request, pk):
    product = get_object_or_404(SanPham, pk=pk)

    if request.method == "POST":
        form = SanPhamForm(request.POST, request.FILES, instance=product)
        formset = SanPhamImageFormSet(request.POST, request.FILES, instance=product)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, f"Đã cập nhật sản phẩm: {product.ten_san_pham}")
            return redirect("store:admin_product_list")
    else:
        form = SanPhamForm(instance=product)
        formset = SanPhamImageFormSet(instance=product)

    return render(
        request,
        "store/admin/product_form.html",
        {
            "form": form,
            "formset": formset,
            "title": f"Sửa sản phẩm: {product.ten_san_pham}",
            "product": product,
        },
    )


@admin_required
def admin_product_delete(request, pk):
    product = get_object_or_404(SanPham, pk=pk)

    if request.method == "POST":
        ten_san_pham = product.ten_san_pham
        product.delete()
        messages.success(request, f"Đã xóa sản phẩm: {ten_san_pham}")
        return redirect("store:admin_product_list")

    return render(
        request,
        "store/admin/confirm_delete.html",
        {
            "title": "Xóa sản phẩm",
            "object": product,
            "cancel_url": "store:admin_product_list",
        },
    )