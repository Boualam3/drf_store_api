from .common import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-wuimpstr27v6^w-c63j%k9=hb%=s1g=*-l6b+cw!=c4)&nq98l'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Im disable silk and debug_toolbar temporarily
MIDDLEWARE += [
    # 'silk.middleware.SilkyMiddleware',
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
]


INTERNAL_IPS = [
    "127.0.0.1",
]


CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'storefront3',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': 'boubou143333'
    }
}
