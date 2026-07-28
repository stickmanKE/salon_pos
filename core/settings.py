"""
Django settings for core project.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-9v_(9g(tzg3ee@gds-l^*t5di_l^g(@fx@m#fx#!lzop0+64o$'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'jazzmin',  # MUST be first
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Your apps
    'salons',
    'clients',
    'staff',
    'salon_services',
    'inventory',
    'sales.apps.SalesConfig',
    'frontend',
    'beverages',
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

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'salon_db',
        'USER': 'postgres',
        'PASSWORD': 'test@123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ── Localisation ──────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'   # ← FIXED: was UTC, now Nairobi time
USE_I18N = True
USE_TZ = True

# ── Static ────────────────────────────────────────────────────
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'frontend' / 'static']

# ── Sessions ──────────────────────────────────────────────────
SESSION_COOKIE_AGE = 28800          # 8 hours (auto-logout after 8h idle)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = True   # Refresh session on each request

# ── Auth redirects ────────────────────────────────────────────
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# ── Jazzmin (Admin) ───────────────────────────────────────────
JAZZMIN_SETTINGS = {
    "site_title": "Happy Hair POS Admin",
    "site_header": "Happy Hair POS",
    "site_brand": "Happy Hair",
    "welcome_sign": "Happy Hair POS — Admin Panel",
    "search_model": ["sales.Sale", "clients.Client", "staff.StaffMember"],

    "topmenu_links": [
        {"name": "Dashboard", "url": "/", "new_window": False},
        {"name": "POS", "url": "/pos/", "new_window": False},
        {"name": "Reports", "url": "/reports/", "new_window": False},
    ],

    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "salons.Salon": "fas fa-store",
        "clients.Client": "fas fa-users",
        "staff.StaffMember": "fas fa-user-tie",
        "salon_services.Service": "fas fa-cut",
        "salon_services.ServiceCategory": "fas fa-tags",
        "inventory.Product": "fas fa-box",
        "inventory.StockMovement": "fas fa-exchange-alt",
        "sales.Sale": "fas fa-receipt",
        "sales.SaleItem": "fas fa-list",
        "sales.Payment": "fas fa-money-bill",
        "beverages.Beverage": "fas fa-coffee",
        "beverages.BeverageCategory": "fas fa-tag",
        "beverages.BeverageStock": "fas fa-warehouse",
    },

    "order_with_respect_to": [
        "sales", "clients", "staff", "salon_services",
        "inventory", "beverages", "salons", "auth",
    ],

    "custom_css": "css/admin.css",
    "show_sidebar": True,
    "navigation_expanded": True,
}
