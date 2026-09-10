from .base import *
import os
from pathlib import Path

DEBUG=config("DEBUG")

BASE_DIR = Path(__file__).resolve().parent.parent

ALLOWED_HOSTS=['api.energitek.us', 'www.energitek.us']

SECRET_KEY = config("SECRET_KEY")

STATIC_URL = '/static/'
STATIC_ROOT= os.path.join(BASE_DIR, 'staticfiles')
GDAL_LIBRARY_PATH = '/usr/lib/x86_64-linux-gnu/libgdal.so'

STATICFILES_DIR = []
MEDIA_URL= '/media/'
MEDIA_ROOT= os.path.join( BASE_DIR,'media')

CORS_ALLOWED_ORIGINS=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
	"http://localhost:5174",
    "http://127.0.0.1:8000"
    ]


CORS_ALLOW_CREDENTIALS=True

DATABASES={
	'default':{
		'ENGINE':config("DB_ENGINE"),
		'NAME':	config("DB_NAME"),
		'USER':	config("DB_USER"),
		'PASSWORD':	config("DB_PASSWORD"),
		'HOST':	config("DB_HOST"),
		'PORT':	config("DB_PORT"),
				
    }
}