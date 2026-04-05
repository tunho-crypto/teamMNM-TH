from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect

from ...forms import ChiNhanhForm
from ...models import ChiNhanh, ChiNhanhImage # <--- QUAN TRỌNG: Import bảng chứa ảnh vào đây
from ..common import admin_required, paginate_queryset, render_admin_delete, render_admin_form


@admin_required
def admin_branch_list(request):
    q = request.GET.get("q", "").strip()
    branches = ChiNhanh.objects.all().order_by("-id")

    if q:
        branches = branches.filter(ten_chi_nhanh__icontains=q)

    page_obj = paginate_queryset(request, branches, 8)

    return render(
        request,
        "store/admin/branch_list.html",
        {
            "page_obj": page_obj,
            "q": q,
        },
    )


@admin_required
def admin_branch_create(request):
    # Chạy hàm lưu mặc định của hệ thống
    response = render_admin_form(
        request,
        ChiNhanhForm,
        title="Thêm chi nhánh",
        success_url="store:admin_branch_list",
    )

    # NẾU LƯU THÀNH CÔNG (Mã 302 là thành công) -> Hứng ảnh và lưu luôn!
    if request.method == "POST" and response.status_code == 302:
        new_branch = ChiNhanh.objects.latest('id') # Lấy chi nhánh vừa được tạo
        danh_sach_anh = request.FILES.getlist('hinh_anh_phu')
        for file_anh in danh_sach_anh:
            ChiNhanhImage.objects.create(chi_nhanh=new_branch, image=file_anh)

    return response

@admin_required
def admin_branch_edit(request, pk):
    branch = get_object_or_404(ChiNhanh, pk=pk)
    
    # =======================================================
    # XỬ LÝ XÓA ẢNH TRƯỚC KHI LƯU THÔNG TIN KHÁC
    # =======================================================
    if request.method == "POST":
        # 1. Trị dứt điểm lỗi nút Xóa ảnh đại diện (checkbox mặc định của Django tên là hinh_anh-clear)
        if request.POST.get("hinh_anh-clear") == "on":
            if branch.hinh_anh:
                branch.hinh_anh.delete(save=False) # Xóa file vật lý trong máy
                branch.hinh_anh = None
                branch.save()

        # 2. Xóa các ảnh phụ được sếp tick chọn
        danh_sach_xoa = request.POST.getlist("xoa_anh_phu")
        if danh_sach_xoa:
            # Tìm các ảnh mang ID bị tick xóa và tiêu diệt chúng
            for img in ChiNhanhImage.objects.filter(id__in=danh_sach_xoa, chi_nhanh=branch):
                img.image.delete(save=False) # Xóa file vật lý trong máy
                img.delete() # Xóa record trong Database
    # =======================================================

    # Chạy hàm lưu mặc định của hệ thống
    response = render_admin_form(
        request,
        ChiNhanhForm,
        instance=branch,
        title=f"Sửa chi nhánh: {branch.ten_chi_nhanh}",
        success_url="store:admin_branch_list",
    )

    # NẾU LƯU THÀNH CÔNG (Mã 302) -> Nhét đống ảnh phụ mới vào Database
    if request.method == "POST" and response.status_code == 302:
        danh_sach_anh = request.FILES.getlist('hinh_anh_phu')
        for file_anh in danh_sach_anh:
            ChiNhanhImage.objects.create(chi_nhanh=branch, image=file_anh)

    return response

@admin_required
def admin_branch_delete(request, pk):
    branch = get_object_or_404(ChiNhanh, pk=pk)
    return render_admin_delete(
        request,
        branch,
        title="Xóa chi nhánh",
        success_url="store:admin_branch_list",
    )