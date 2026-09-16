import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

# Set SECRET_KEY in Vercel for production. The fallback is only for local use.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-tourism-site-secret-key')
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
ALLOWED_HOSTS = [
    'tourist-web-ucjt.onrender.com',
    # Render assigns a hostname to each service; accepting its subdomains
    # prevents Django from rejecting a newly created or renamed service.
    '.onrender.com',
    'touristwebs.vercel.app',
    'abdishan12.vercel.app',
    # Allows Vercel's generated preview deployment subdomains.
    '.vercel.app',
    'localhost',
    '127.0.0.1',
]

# Vercel is the public origin; it proxies each request to this Render service.
# Trust it for Django's CSRF validation when a customer submits a booking.
CSRF_TRUSTED_ORIGINS = [
    'https://touristwebs.vercel.app',
    'https://abdishan12.vercel.app',
    'https://*.vercel.app',
]

# Render terminates HTTPS at its proxy before forwarding a request to Gunicorn.
# Respect that signal so Django keeps production redirects and cookies secure.
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tour_app',
    'site_admin',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tourism.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'tour_app.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'tourism.wsgi.application'
ASGI_APPLICATION = 'tourism.asgi.application'

DATABASE_URL = os.environ.get('DATABASE_URL')

require_database_url = (
    os.environ.get('RENDER')
    or os.environ.get('REQUIRE_DATABASE_URL', '').lower() == 'true'
)

if not DATABASE_URL and require_database_url:
    # Render's web-service filesystem is ephemeral.  Refuse to start there
    # without the managed Postgres connection, rather than losing admin edits
    # in a newly created SQLite database after a restart.
    raise ImproperlyConfigured(
        'DATABASE_URL must be set on Render. Link the Render PostgreSQL '
        'database to this web service before deploying.'
    )

if DATABASE_URL:
    import dj_database_url

    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # SQLite is intentionally limited to local development.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Serve the assets collected during deployment when running behind Gunicorn.
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

WHATSAPP_PHONE_NUMBER = '255612001424'
WHATSAPP_DEFAULT_MESSAGE = 'Hello, I would like more information about your travel packages.'
CONTACT_EMAIL = os.environ.get('CONTACT_EMAIL', 'burminho098@gmail.com')

# FormSubmit delivers every booking to this verified mailbox; no SMTP password
# is required. The value can be changed in Render with BOOKING_NOTIFICATION_URL.
BOOKING_NOTIFICATION_URL = os.environ.get(
    'BOOKING_NOTIFICATION_URL', 'https://formsubmit.co/burminho098@gmail.com'
)
CONTACT_NOTIFICATION_URL = os.environ.get(
    'CONTACT_NOTIFICATION_URL', BOOKING_NOTIFICATION_URL
)
BOOKING_SITE_URL = os.environ.get(
    'BOOKING_SITE_URL', 'https://abdishan12.vercel.app/'
)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
