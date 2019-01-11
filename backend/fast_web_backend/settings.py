"""
Django settings for fast_web_backend project.
"""

import os
from datetime import timedelta
from configurations import Configuration


# Base configuration
class Base(Configuration):
    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Application definition
    INSTALLED_APPS = [
        'django_extensions',
        'dj_pagination',
        'admin_interface',
        'colorfield',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.postgres',

        # Localization of fields (different from localization of static resources)
        'localized_fields.apps.LocalizedFieldsConfig',

        # GraphQL server
        'graphene_django',

        # FaST apps
        'core',
        'farming',
        'additional_services',
        'messaging',
        'nmp'
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

    ROOT_URLCONF = 'fast_web_backend.urls'

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

    WSGI_APPLICATION = 'fast_web_backend.wsgi.application'

    AUTH_USER_MODEL = 'core.FaSTUSer'

    AUTH_PASSWORD_VALIDATORS = [
        {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
        {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
        {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
        {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
    ]

    AUTHENTICATION_BACKENDS = [
        'graphql_jwt.backends.JSONWebTokenBackend',
        'django.contrib.auth.backends.ModelBackend',
    ]

    LANGUAGE_CODE = 'en'

    LANGUAGES = (
        ('en', 'English'),
        ('es', 'Español'),
        ('fr', 'Français'),
    )

    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    MEDIA_URL = '/media/'
    STATIC_URL = '/static/'

    # Load the static files from the backend and all the built files from the farmer mobile app
    STATICFILES_DIRS = [os.path.join(BASE_DIR, '..', 'farmer_mobile_app', 'dist'),
                        os.path.join(BASE_DIR, 'static')]

    STATICFILES_FINDERS = [
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    ]

    GRAPHENE = {
        'SCHEMA': 'fast_web_backend.schema.schema',
        'MIDDLEWARE': [
            'graphql_jwt.middleware.JSONWebTokenMiddleware',
        ],
    }

    GRAPHQL_JWT = {
        'JWT_VERIFY_EXPIRATION': True,
        'JWT_EXPIRATION_DELTA': timedelta(days=30),
        'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=365),
    }


# Development configuration


class Dev(Base):
    DEBUG = True
    SECRET_KEY = "g!7z60jk^6(#jg-3b$in28qr4ho%)jtiv&725)_shzi)#6faz+"
    ALLOWED_HOSTS = ['*']

    MEDIA_ROOT = os.path.join(Base.BASE_DIR, '../data/dev/media')
    STATIC_ROOT = os.path.join(Base.BASE_DIR, '../data/dev/static')

    DATABASES = {
        'default': {
            'ENGINE': 'psqlextra.backend',
            'NAME': 'fast',
            'USER': 'fast',
            'PASSWORD': 'fast',
            'HOST': '',
            'PORT': '5432'
        }
    }

    WEBPACK_LOADER = {
        'DEFAULT': {
            'CACHE': False,
            'BUNDLE_DIR_NAME': 'farmer_mobile_app/',
            'STATS_FILE': os.path.join(Base.BASE_DIR, '..', 'farmer_mobile_app', 'dist', 'farmer_mobile_app',
                                       'webpack-stats.json'),
            'POLL_INTERVAL': 0.1,
            'TIMEOUT': None,
            'IGNORE': ['.+\.hot-update.js', '.+\.map']
        }
    }

    INSTALLED_APPS = Base.INSTALLED_APPS + ['webpack_loader']


# Production configuration


class Prod(Base):
    """
    Production configuration

    See docker-compose setup and .env file for production configuration.
    """
    DEBUG = False
    SECRET_KEY = os.getenv('FAST_WEBAPP_DJANGO_SECRET_KEY')
    ALLOWED_HOSTS = ['*']

    MEDIA_ROOT = '/fast/media'
    STATIC_ROOT = '/fast/static'

    DATABASES = {
        'default': {
            'ENGINE': 'psqlextra.backend',
            'NAME': os.getenv('FAST_POSTGRES_WEBAPP_DATABASE'),
            'USER': os.getenv('FAST_POSTGRES_WEBAPP_USER'),
            'PASSWORD': os.getenv('FAST_POSTGRES_WEBAPP_PASSWORD'),
            'HOST': os.getenv('FAST_POSTGRES_WEBAPP_HOST'),
            'PORT': os.getenv('FAST_POSTGRES_WEBAPP_PORT')
        }
    }

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': '/fast/log/webapp.log',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': True
            },
        },
    }
