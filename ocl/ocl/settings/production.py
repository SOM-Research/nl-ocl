from .base import *
from pathlib import Path

DEBUG = False

ADMINS = (
    ('DAVID D', 'ddelgadoc@uoc.edu'),
)

ALLOWED_HOSTS = ['127.0.0.1', '*',]
DATABASES = {
    'default': {
        'ENGINE': os.environ.get("SQL_ENGINE"),
        'NAME': os.environ.get("SQL_DATABASE"),
        'USER': os.environ.get("SQL_USER"),
        'PASSWORD': os.environ.get("SQL_PASSWORD"),
        'HOST': os.environ.get("SQL_HOST"),
        'PORT': os.environ.get("SQL_PORT"),
    }
}

CSRF_TRUSTED_ORIGINS.append( "http://ellie.a2sistemas.com:8000", "http://%s"%(os.environ.get("ENV_NGINX_HOST")) )

# USE_X_FORWARDED_HOST = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = False
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True