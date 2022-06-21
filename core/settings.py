from datetime import timedelta
from pathlib import Path
import os
import environ
import cloudinary
import django
from django.utils.encoding import force_str

django.utils.encoding.force_text = force_str
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env()
ENVIRONMENT = env

cloudinary.config(
    cloud_name=os.environ.get('CLOUD_NAME'),
    api_key=os.environ.get('CLOUD_API_KEY'),
    api_secret=os.environ.get('CLOUD_API_SECRET')
)

SECRET_KEY = os.environ.get('SECRET_KEY')
DOMAIN = os.environ.get('DOMAIN')

DEBUG = True

ALLOWED_HOSTS = ['*']

DJANGO_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

]

PROJECT_APPS = [
    'apps.user',
    'apps.account',
    'drf_yasg',
]

MAIN_APPS = [
    'apps.product',
    'apps.cart',
    'apps.wishlist',
    'apps.shipping',
    'apps.coupon',
    'apps.order',
]

THIRD_PARTY_APPS = [
    'corsheaders',
    'rest_framework',
    'djoser',
    'social_django',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
]
INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + MAIN_APPS + THIRD_PARTY_APPS


MIDDLEWARE = [
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

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
        'DIRS': [],
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

WSGI_APPLICATION = 'core.wsgi.application'


DATABASES = {
    "default": env.db("HEROKU_POSTGRESQL_MAROON_URL", default="postgres:///pgaton"),
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True


CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
    'http://localhost:3001',
    'http://localhost:8000',

    'http://127.0.0.1:8000',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:3001',

    'https://frontend-surf-academy.herokuapp.com',
    'https://backend-surf-academy.herokuapp.com'
]
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:8000',
    'http://127.0.0.1:3001',

    'http://127.0.0.1:8000',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:3001',

    'https://frontend-surf-academy.herokuapp.com',
    'https://backend-surf-academy.herokuapp.com'
]


PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.ScryptPasswordHasher',
]

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


LANGUAGE_CODE = 'es'
TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ = True


STATIC_URL = 'static/'


JAZZMIN_SETTINGS = {
    "site_title": "Aton Admin",
    "site_header": "Aton Admin",
    "site_brand": "ATON",

    "welcome_sign": "Bienvenido a Aton Admin",
    "copyright": "ATON",

    "topmenu_links": [
        {"name": "Home",  "url": "admin:index",
            "permissions": ["auth.view_user"]},
        {"model": "user.UserAccount"},
        {"app": "product"},
    ],

    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [
        "auth",
        "social_django",
        "rest_framework_simplejwt",
        "token_blacklist"
    ],

    "hide_models": [
        "cart.CartItem",
        "order.OrderItem",
        "account.UserAddress",
        "product.CharacteristicProduct",
        "product.ProductImage",
    ],

    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": ["user", "product", "order", "shipping", "coupon", "cart", "account"],

    # Custom links to append to app groups, keyed on app name


    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "user.UserAccount": "fas fa-user",
        "product.brand": "fas fa-copyright",
        "product.category": "fas fa-boxes",
        "product.CharacteristicProduct": "fas fa-list",
        "product.ProductImage": "fas fa-image",
        "product.Product": "fas fa-dolly",
        "order.Order": "fas fa-box-open",
        "shipping.Shipping": "fas fa-truck",
        "coupon.Coupon": "fas fa-tags",
        "cart.Cart": "fas fa-shopping-cart",
        "account.UserProfile": "fas fa-user-circle",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fa fa-check",




}
JAZZMIN_UI_TWEAKS = {
    "brand_colour": "navbar-success",
    "accent": "accent-navy",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": True,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-success",
    "sidebar_nav_child_indent": True,

    "theme": "minty",
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-outline-warning",
        "danger": "btn-outline-danger",
        "success": "btn-outline-success"
    },
    "site_brand": "ATON"
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 9,
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT', ),
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10080),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESFH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_TOKEN_CLASSES': (
        'rest_framework_simplejwt.tokens.AccessToken',
    )
}
SITE_NAME = ('Aton SA')
DJOSER = {
    'LOGIN_FIELD': 'email',
    'USER_CREATE_PASSWORD_RETYPE': True,
    'USERNAME_CHANGED_EMAIL_CONFIRMATION': True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    'SEND_CONFIRMATION_EMAIL': True,
    'SET_USERNAME_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'SET_PASSWORD_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
    'USERNAME_RESET_CONFIRM_URL': 'email/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    'SOCIAL_AUTH_TOKEN_STRATEGY': 'djoser.social.token.jwt.TokenStrategy',
    'SOCIAL_AUTH_ALLOWED_REDIRECT_URIS': ['http://localhost:8000/google', 'http://localhost:8000/facebook'],
    'SERIALIZERS': {
        'user_create': 'apps.user.serializers.UserCreateSerializer',
        'user': 'apps.user.serializers.UserCreateSerializer',
        'current_user': 'apps.user.serializers.UserCreateSerializer',
        'user_delete': 'djoser.serializers.UserDeleteSerializer',
    },
    'EMAIL': {
        'activation': 'djoser.email.ActivationEmail',
        'confirmation': 'djoser.email.ConfirmationEmail',
        'password_reset': 'djoser.email.PasswordResetEmail',
        'password_changed_confirmation': 'djoser.email.PasswordChangedConfirmationEmail',
        'username_changed_confirmation': 'djoser.email.UsernameChangedConfirmationEmail',
        'username_reset': 'djoser.email.UsernameResetEmail',
    }
}



AUTH_USER_MODEL = "user.UserAccount"


# if not DEBUG:
DEFAULT_FROM_EMAIL = 'ATON - Empresa  <anthoni_pydev@anthonidev.me>'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_USE_TLS = env('EMAIL_USE_TLS')
