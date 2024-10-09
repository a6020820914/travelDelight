import os
from pathlib import Path
import dj_database_url


# 奕誠
AUTH_USER_MODEL = 'members.Member'

# 設置專案的根目錄路徑
BASE_DIR = Path(__file__).resolve().parent.parent

# 快速開發設置，這些設置不適合用於生產環境
SECRET_KEY = "django-insecure-18p*)w2q+_7p*o8@@8+14y1erm__6+@a#$@c8%h1@j93z#06@8"

# 注意：生產環境中不要啟用 debug 模式
DEBUG = True

ALLOWED_HOSTS = ['*']

# 應用程式定義
INSTALLED_APPS = [
    'widget_tweaks',
    'jazzmin',  # Django Admin 美化介面
    'django_extensions',
    'members',  # 自定義會員系統
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise 处理静态文件
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # 确保这一行在前
    'django.middleware.locale.LocaleMiddleware',  # 語言中間件需放在這裏
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # 认证中间件
    'django.contrib.messages.middleware.MessageMiddleware',  # 消息中间件
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # 防止点击劫持
]

# URL 配置
ROOT_URLCONF = 'projectname.urls'

# 模板配置
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI 應用程式
WSGI_APPLICATION = 'projectname.wsgi.application'

BASE_DIR = Path(__file__).resolve().parent.parent

# 默认数据库为 SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 只在环境变量存在且非 SQLite 时使用 dj_database_url
if 'DATABASE_URL' in os.environ and not os.environ['DATABASE_URL'].startswith('sqlite:///'):
    DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)
# 密碼驗證
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# 國際化設置
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# 靜態檔案設置
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
# 你需要收集静态文件的目录
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # 这里的 'staticfiles' 是你收集静态文件的目标目录

# 媒體文件設置
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 指定主鍵類型
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 郵件設置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'a6020820914@gmail.com'
EMAIL_HOST_PASSWORD = 'myef kcph eyil qppk'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Jazzmin 设置
JAZZMIN_SETTINGS = {
    'site_title': 'Library Admin',
    'site_header': 'Library',
    'site_brand': '管理者頁面',
    'site_logo': 'travel.wed_logo.png',
    'site_logo_classes': 'img-responsive logo-custom-size',
    'welcome_sign': 'Welcome to the library',
    'copyright': 'Acme Library Ltd',
    'search_model': ['members.Member', 'auth.Group'],
    'user_avatar': None,
    'logo_size': {
        'max_width': 150,
        'height': 'auto',
    },
    'topmenu_links': [
        {'name': 'Home', 'url': 'admin:index', 'permissions': ['auth.view_user']},
        {'name': 'Support', 'url': 'https://github.com/farridav/django-jazzmin/issues', 'new_window': True},
        {'model': 'members.Member'},
    ],
    'usermenu_links': [
        {'name': 'Support', 'url': 'https://github.com/farridav/django-jazzmin/issues', 'new_window': True},
        {'model': 'members.Member'}
    ],
    'show_sidebar': True,
    'navigation_expanded': True,
    'order_with_respect_to': ['auth'],
    'custom_links': {
        'books': [{
            'name': 'Make Messages',
            'url': 'make_messages',
            'icon': 'fas fa-comments',
            'permissions': ['books.view_book']
        }]
    },
    'icons': {
        'auth': 'fas fa-users-cog',
        'members.Member': 'fas fa-user',
        'auth.Group': 'fas fa-users',
    },
    'default_icon_parents': 'fas fa-chevron-circle-right',
    'default_icon_children': 'fas fa-circle',
    'changeform_format': 'horizontal_tabs',
    'changeform_format_overrides': {'members.Member': 'collapsible', 'auth.group': 'vertical_tabs'},
    'language_chooser': True,
}

# 語言設置
LANGUAGES = [
    ('en', 'English'),
    ('zh-hant', 'Traditional Chinese'),
]

# 第三方登入功能（如需使用，请取消注释）
# AUTHENTICATION_BACKENDS = (
#     'django.contrib.auth.backends.ModelBackend',
#     'allauth.account.auth_backends.AuthenticationBackend',
# )
# SITE_ID = 1
# LOGIN_REDIRECT_URL = '/'  # 登入後重定向路徑
# ACCOUNT_EMAIL_VERIFICATION = 'none'
# ACCOUNT_EMAIL_REQUIRED = True