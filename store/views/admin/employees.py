from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from ...forms import TaiKhoanForm, NhanVienForm
from ...models import TaiKhoan, NhanVien
from ..common import admin_required, paginate_queryset, render_admin_delete, render_admin_form


@admin_required
def admin_employee_list(request):
    q = request.GET.get("q", "").strip()

    employees = (
        NhanVien.objects.select_related("chi_nhanh", "tai_khoan")
        .filter(
            Q(tai_khoan__role__in=["STAFF", "ADMIN"]) | Q(tai_khoan__isnull=True)
        )
        .order_by("-id")
    )

    if q:
        employees = employees.filter(
            Q(ten_nhan_vien__icontains=q)
            | Q(chuc_vu__icontains=q)
            | Q(tai_khoan__ho_ten__icontains=q)
            | Q(tai_khoan__email__icontains=q)
            | Q(tai_khoan__dien_thoai__icontains=q)
        )

    page_obj = paginate_queryset(request, employees, 8)

    return render(
        request,
        "store/admin/employee_list.html",
        {
            "page_obj": page_obj,
            "q": q,
        },
    )


@admin_required
def admin_employee_create(request):
    return render_admin_form(
        request,
        NhanVienForm,
        title="Thêm nhân viên",
        success_url="store:admin_employee_list",
    )


@admin_required
def admin_employee_edit(request, pk):
    employee = get_object_or_404(NhanVien, pk=pk)
    return render_admin_form(
        request,
        NhanVienForm,
        instance=employee,
        title=f"Sửa nhân viên: {employee.ten_nhan_vien}",
        success_url="store:admin_employee_list",
    )


@admin_required
def admin_employee_delete(request, pk):
    employee = get_object_or_404(NhanVien, pk=pk)

    if request.method == "POST":
        display_name = employee.ten_nhan_vien
        employee.delete()
        messages.success(request, f"Đã xóa nhân viên: {display_name}")
        return redirect("store:admin_employee_list")

    return render(
        request,
        "store/admin/confirm_delete.html",
        {
            "title": "Xóa nhân viên",
            "object": employee,
            "cancel_url": "store:admin_employee_list",
        },
    )
