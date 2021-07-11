from .base import *

DEBUG = False
ALLOWED_HOSTS = []
STATIC_ROOT = BASE_DIR / "static"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
