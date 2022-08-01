from re import M
from .base import *
from pathlib import Path

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': "django.db.backends.mysql",
        'NAME': "SOMOCL",
        'USER': "root",
        'PASSWORD': "root",
        'HOST': "127.0.0.1",
        'PORT': "3306",
    }
}
