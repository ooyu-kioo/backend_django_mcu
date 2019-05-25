import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'unw0o)6)=tmp!)2rzi@2q33_#r5ws@1(ynwi95yfvx9bd=9(l3'
# SECURITY WARNING: don't run with debug turned on in production!
# エラー時にエラー内容を画面に出力(※本番環境ではfalse)
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # add
    'rest_framework',
    'corsheaders',  # CORS許可用(開発環境でのみ必要)
    'scraping.apps.ScrapingConfig',  # TODO 普通のアプリめいじゃないのなぜ？
    'apiv1.apps.Apiv1Config'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # request, responceのセキュリティ強化
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRFトークンの検証
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # add：CORS(開発環境でのみ必要)
    'whitenoise.middleware.WhiteNoiseMiddleware'  # add：heroku用
]

# TODO ドメイン指定ちゃんとやっとく
# add：CORS 本来はALLはfalseで特定のoriginだけ許可する(開発環境でのみ必要)
CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = {
#     'localhost:8080',
#     '127.0.0.1:8080'
#     'localhost:8001'
#     'mcu.netlify'
# }

ROOT_URLCONF = 'django_vue_mcu.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # add
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

WSGI_APPLICATION = 'django_vue_mcu.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ja'  # fix

TIME_ZONE = 'Asia/Tokyo'  # fix

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # add

# add heroku
DEBUG = False
try:
    from .local_settings import *
except ImportError:
    pass

if not DEBUG:
    import django_heroku
    django_heroku.settings(locals())
