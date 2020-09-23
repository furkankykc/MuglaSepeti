import os

DEBUG = True
ALLOWED_HOSTS = ['*']
HTTP_METHOD = 'http'
SITE_URL = 'localhost:8000'
STATICFILES_DIRS = (os.path.join('static'),)
STATIC_ROOT = ""
# STATIC_ROOT = os.path.join('static')
