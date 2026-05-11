"""
Django settings for quanly_bhx_core project.
"""
from pathlib import Path

# ==========================================
# 1. BASE CONFIGURATION
# ==========================================
BASE_DIR = Path(__file__).resolve().parent.parent

# Giữ lại SECRET_KEY của bạn (bảo mật hơn)
SECRET_KEY = 'django-insecure-qdde6o+=xh=v3e%4uu+8uf-n93wi1$1pi7&uw%mi$wm5yjyzf!'

DEBUG = True

ALLOWED_HOSTS = []


# ==========================================
# 2. APPLICATIONS & MIDDLEWARE
# ==========================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    
    # Custom Apps (Gộp của cả 2 người)
    'store',
    'locations',
    'dashboard',
    'import_export',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ==========================================
# 3. URLS & TEMPLATES
# ==========================================
ROOT_URLCONF = 'quanly_bhx_core.urls'
WSGI_APPLICATION = 'quanly_bhx_core.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Thư mục templates chung
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug', # Lấy từ bạn của bạn (hỗ trợ debug)
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ==========================================
# 4. DATABASE
# ==========================================
# CHÚ Ý QUAN TRỌNG: Bạn giữ nguyên cấu hình Database của BẠN (bachhoaxanh_db)
# vì bạn đang là người cầm trịch dữ liệu Seed nãy giờ.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'BHX',    
        'USER': 'postgres',          
        'PASSWORD': '123456', # Nếu máy của bạn bạn kia pass là '123' thì bạn ấy phải tự sửa ở máy bạn ấy       
        'HOST': 'localhost', # localhost hay 127.0.0.1 đều giống nhau
        'PORT': '5432',
    }
}


# ==========================================
# 5. PASSWORD VALIDATION
# ==========================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ==========================================
# 6. INTERNATIONALIZATION (I18N)
# ==========================================
# Lấy cấu hình Tiếng Việt chuẩn của bạn
LANGUAGE_CODE = 'vi'

TIME_ZONE = 'Asia/Ho_Chi_Minh'

USE_I18N = True
USE_TZ = True


# ==========================================
# 7. STATIC & MEDIA FILES
# ==========================================
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ==========================================
# 8. DEFAULT PRIMARY KEY
# ==========================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "your_email@gmail.com"
EMAIL_HOST_PASSWORD = "your_app_password"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# ==========================================
# 9. EMAIL CONFIGURATION (MAILTRAP)
# ==========================================
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
EMAIL_PORT = '2525'
EMAIL_USE_TLS = True

# Cặp User/Pass xịn sò sếp vừa lấy:
EMAIL_HOST_USER = 'e2d47aa43fe576'
EMAIL_HOST_PASSWORD = '35c5aa70490c6c'

DEFAULT_FROM_EMAIL = "no-reply@bhx.local"
ADMIN_REVIEW_EMAIL = "admin@example.com"

DEBUG = True
ALLOWED_HOSTS = ["*"]