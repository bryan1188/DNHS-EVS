"""
Django settings for DNHS_EVS project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import hashlib

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR,'templates')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@r#ql!gfrgc5#6=9*7%*8(lha)!5os8kiqdqsex8#*85eoq&!!'

# hashing secret key
HASHING_SECRET_KEY = 'b0ch523jOhn316ForGodSoLoveTheWorldThatHeGaveHISOnlySon...'
HASHING_SALT = 'b0ch523matthew2830'

#hassing settings
HASHLIB_VOTER_NEW_TOKEN = hashlib.sha512

#flag to make counting more secure. This may degrade performance.
#disable if performance is degraded
#used in registration.models.Vote
VOTE_SECURITY = True

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap3',
    'bootstrap4',
    'widget_tweaks',
    'searchableselect',
    'crispy_forms',
    'registration',
    'election',
    'reporting'
    ]

# https://simpleisbetterthancomplex.com/tutorial/2018/08/13/how-to-use-bootstrap-4-forms-with-django.html
CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.contrib.auth.context_processors.auth',
]

ROOT_URLCONF = 'DNHS_EVS.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR,],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'registration.context_processor.set_school_home'
            ],
        },
    },
]

WSGI_APPLICATION = 'DNHS_EVS.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'E_voting',
        'USER': 'django',
        'PASSWORD': 'ikpakduwoq!',
        'HOST': 'localhost',
        'PORT': '5454'
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Manila'

DATE_FORMAT = 'm/d/Y'

TIME_FORMAT = 'A'

SHORT_DATETIME_FORMAT = 'm/d/Y h:i A'
DATE_TIME_FORMAT = 'm/d/Y h:i A'
USE_L10N = True

DATE_INPUT_FORMATS = ['%m-%d-%Y']

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_REDIRECT_URL = 'admin/'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')]
MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_URL = '/media/'
UPLOAD_DIR = os.path.join(MEDIA_ROOT,'uploaded_files')

'''
Something wrong with the file. changes can't be detected. An alternative is
to rename the file and set the filename here so it will be update on all
templates that using it
'''
MODAL_AJAX_LOCATION = 'registration/js/modal_ajax_2.js'
