from functools import wraps
import random

from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from ..models import TaiKhoan

def ensure_admin_account():
    admin_acc, created = TaiKhoan.objects.get_or_create(
        email="admin@bhx.local",
        defaults={
            "password_hash": make_password("admin123"),
            "ho_ten": "Quản trị viên",
            "dien_thoai": "0909000000",
            "role": "ADMIN",
            "trang_thai": "ACTIVE",
        },
    )

    if created:
        return

    updated = False

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

    if not check_password("admin123", admin_acc.password_hash):
        admin_acc.password_hash = make_password("admin123")
        updated = True

    if updated:
        admin_acc.save()


def paginate_queryset(request, queryset, per_page=8):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)


def generate_otp():
    return f"{random.randint(100000, 999999)}"


def send_otp_email(email, otp_code):
    subject = "Mã OTP xác thực tài khoản BHX"
    message = (
        "Xin chào,\n\n"
        f"Mã OTP của bạn là: {otp_code}\n"
        "Mã có hiệu lực trong 5 phút.\n\n"
        "Nếu bạn không thực hiện đăng ký, hãy bỏ qua email này."
    )

    send_mail(
        subject,
        message,
        None,
        [email],
        fail_silently=False,
    )


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("tai_khoan_id"):
            return redirect("store:login")

        if request.session.get("role") not in ["ADMIN", "STAFF"]:
            return redirect("store:home")

        return view_func(request, *args, **kwargs)

    return wrapper

def render_admin_form(request, form_class, title, success_url, instance=None):
    if request.method == "POST":
        form = form_class(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            obj = form.save(commit=False)

            # =========================================================
            # XỬ LÝ MẬT KHẨU TÀI KHOẢN (ĐÃ NÂNG CẤP)
            # =========================================================
            if isinstance(obj, TaiKhoan):
                raw_password = form.cleaned_data.get("password_hash")
                
                if raw_password: 
                    # Nếu có nhập chữ vào -> Mã hóa thành mật khẩu mới
                    if not str(raw_password).startswith("pbkdf2_"):
                        obj.password_hash = make_password(raw_password)
                else:
                    # Nếu để trống -> Mò vào DB lấy lại mật khẩu cũ đắp lên
                    if instance and instance.pk:
                        old_obj = TaiKhoan.objects.get(pk=instance.pk)
                        obj.password_hash = old_obj.password_hash
            # =========================================================

            obj.save()
            return redirect(success_url)
    else:
        form = form_class(instance=instance)

    return render(
        request,
        "store/admin/form.html",
        {
            "form": form,
            "title": title,
        },
    )


def render_admin_delete(request, obj, title, success_url):
    if request.method == "POST":
        obj.delete()
        return redirect(success_url)

    return render(
        request,
        "store/admin/delete_confirm.html",
        {
            "object": obj,
            "title": title,
        },
    )