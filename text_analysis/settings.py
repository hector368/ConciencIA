"""
Django settings for text_analysis project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path
from .config import PERSPECTIVE_API_KEY

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-fjen@2_b@^y2jbn-(9qzp02ra)fz-$h5ilz3934$^p3kfh6^w='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = [
    'conciencia.onrender.com',
    'localhost',
    '127.0.0.1',
]


# Uso de la clave API
print(PERSPECTIVE_API_KEY)  # Esto imprimirá la clave para verificar que funciona

# Application definition

INSTALLED_APPS = [
    'corsheaders',
    'analysis',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # Requerido por allauth
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Agrega aquí
]

ROOT_URLCONF = 'text_analysis.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / "templates",  
        ],
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

WSGI_APPLICATION = 'text_analysis.wsgi.application'

CORS_ALLOW_ALL_ORIGINS = True  # Para permitir todas las solicitudes

CSRF_TRUSTED_ORIGINS = [
    'https://conciencia.onrender.com',
]

CSRF_COOKIE_DOMAIN = '.onrender.com'

CSRF_COOKIE_SECURE = True  # Para asegurarse de que la cookie CSRF se envíe solo a través de HTTPS
SESSION_COOKIE_SECURE = True  # Para garantizar que las cookies de sesión solo se envíen a través de HTTPS


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# Tamaño máximo del archivo (por ejemplo, 1 MB)
MAX_UPLOAD_SIZE = 1048576  # 1 MB en bytes

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Autenticación normal
]

SITE_ID = 1  # Necesario para django-allauth

LOGIN_REDIRECT_URL = '/'  # Redirigir después del inicio de sesión
LOGOUT_REDIRECT_URL = '/'  # Redirigir después del cierre de sesión


SOCIALACCOUNT_GOOGLE_CLIENT_ID = '75648015386-o30as3f8u1uil6mj3do0b06k2lbc3ako.apps.googleusercontent.com'
SOCIALACCOUNT_GOOGLE_CLIENT_SECRET = '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'
