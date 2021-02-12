"""
Django settings for hyve project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

import decouple

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = decouple.config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = decouple.config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = decouple.config('ALLOWED_HOSTS', cast=decouple.Csv())

# Wagtail

WAGTAIL_SITE_NAME = decouple.config('WAGTAIL_SITE_NAME', default='Hyve')
WAGTAIL_USER_EDIT_FORM = 'material.forms.CustomUserEditForm'
WAGTAIL_USER_CREATION_FORM = 'material.forms.CustomUserCreationForm'
WAGTAIL_MODERATION_ENABLED = False


# Application definition

INSTALLED_APPS = [
    'material.apps.MaterialConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'wagtail.contrib.forms',
    'wagtail.contrib.modeladmin',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail_react_streamfield',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'modelcluster',
    'taggit',
    'wagtail_localize',
    'wagtail_localize.locales',
    'wagtailvideos',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'corsheaders',
    # To ensure that exceptions inside other apps' signal handlers do not affect the integrity of file deletions
    # within transactions, django_cleanup should be placed last in INSTALLED_APPS.
    'django_cleanup.apps.CleanupConfig',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'djangorestframework_camel_case.parser.CamelCaseFormParser',
        'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}

BROWSABLE_API = decouple.config('BROWSABLE_API', default=False, cast=bool)
if BROWSABLE_API:
    REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] += [
        'rest_framework.authentication.SessionAuthentication',
    ]
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] += [
        'djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer',
    ]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # Django docs on order of LocaleMiddleware:
    # Make sure it’s one of the first middleware installed. It should come after SessionMiddleware,
    # because LocaleMiddleware makes use of session data. And it should come before CommonMiddleware because
    # CommonMiddleware needs an activated language in order to resolve the requested URL. If you use CacheMiddleware,
    # put LocaleMiddleware after it.
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

DJOSER = {
    'EMAIL': {
        'password_reset': 'material.email.PasswordResetEmail',
    },
    'SEND_CONFIRMATION_EMAIL': True,
    'SERIALIZERS': {
        # Note that djoser.serializers.UserSerializer, which is the default for `user` and `current_user`,
        # may contain code that we should adapt to our own UserSerializer in the future.
        'current_user': 'material.serializers.UserSerializer',
        'password_reset': 'material.serializers.PasswordResetSerializer',
        'user': 'material.serializers.UserSerializer',
    },
    'USER_ID_FIELD': 'pk',
    'USERNAME_CHANGED_EMAIL_CONFIRMATION': True,
}

ROOT_URLCONF = 'hyve.urls'

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

WSGI_APPLICATION = 'hyve.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': decouple.config('DB_ENGINE', default='django.db.backends.sqlite3'),
        'NAME': decouple.config('DB_NAME', default=str(BASE_DIR / 'db.sqlite3')),
        'USER': decouple.config('DB_USER', default=None),
        'PASSWORD': decouple.config('DB_PASSWORD', default=None),
        'HOST': decouple.config('DB_HOST', default=None),
        'PORT': decouple.config('DB_PORT', default=None),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'material.User'


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = decouple.config('LANGUAGE_CODE', default='en-us')

# Languages supported by wagtail-localize
LANGUAGES = [
    ('en', 'English'),
    ('fi', 'Suomi'),
]
WAGTAIL_CONTENT_LANGUAGES = LANGUAGES

TIME_ZONE = decouple.config('TIME_ZONE', default='Europe/Helsinki')

USE_I18N = True
WAGTAIL_I18N_ENABLED = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = decouple.config('STATIC_URL', default='/static/')
STATIC_ROOT = decouple.config('STATIC_ROOT')
MEDIA_URL = decouple.config('MEDIA_URL', default='/media/')
MEDIA_ROOT = decouple.config('MEDIA_ROOT')

# If serving from a subdirectory, you may want to set FORCE_SCRIPT_NAME
FORCE_SCRIPT_NAME = decouple.config('FORCE_SCRIPT_NAME', default=None)

CORS_ALLOWED_ORIGINS = decouple.config('CORS_ALLOWED_ORIGINS', cast=decouple.Csv())

# If Django is behind a reverse proxy, set USE_PROXY_HEADERS to true to make
# Django use the X-Forwarded-Proto and X-Forwarded-Host headers for generating
# URLs. (Make sure your reverse proxy sets these headers. See the README.)
if decouple.config('USE_PROXY_HEADERS', default=False, cast=bool):
    USE_X_FORWARDED_HOST = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Email

DEFAULT_FROM_EMAIL = decouple.config('DEFAULT_FROM_EMAIL', default='webmaster@localhost')
EMAIL_BACKEND = decouple.config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = decouple.config('EMAIL_HOST', default='localhost')
# For other setups, we may want to be able to specify the other EMAIL_* options as well in the future...
