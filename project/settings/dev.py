from .base import *
import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG=config("DEBUG")

ALLOWED_HOSTS=['*']
MEDIA_ROOT=BASE_DIR /'media'
MEDIA_URL= '/media/'
STATIC_URL= '/static/'

DATABASES = {
'default': {
'ENGINE': config("DB_ENGINE"),
'NAME': config("DB_NAME"),
'USER': config("DB_USER"),
'PASSWORD': config("DB_PASSWORD"),
'HOST': config("DB_HOST"),
'PORT': config("DB_PORT"),
}
}