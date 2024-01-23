from decouple import config # Using python-decouple library
from pathlib import Path
import os
import redis
from social_core.backends.google import GoogleOAuth2
import certifi


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "w**#mn)b#a5kn74+!rd@k6so%&kxg2(@4w9uoucg!)$r0=+f3&"
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1',"localhost"]


# Application definition

INSTALLED_APPS = [
    'game.apps.GameConfig',
    'home.apps.HomeConfig',
    'user_profile.apps.UserProfileConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd Party Libraries
    'channels',
    'social_django',  # Social Media Login
    'imagekit',
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Added for deployment
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Middleware to handle Login through Social Media Platform requests
    'social_django.middleware.SocialAuthExceptionMiddleware'
]

ROOT_URLCONF = 'artic_game.urls'
ASGI_APPLICATION = "artic_game.routing.application"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',  # To access Media URL in templates
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',


                # Context Preprocessors for Social media login
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect'

            ],
        },
    },
]

WSGI_APPLICATION = 'artic_game.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
import dj_database_url
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)
DATABASES['default']['CONN_MAX_AGE'] = 500


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Settings for uploading Media (User's Avatar)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# os.path.join(BASE_DIR, 'media')



#  Add configuration for static files storage using whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# DONOT USE BELOW AS IT GIVES SERVER ERROR 500:-(Source: https://stackoverflow.com/a/56259827/11070092)
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# r = redis.from_url(os.environ.get("REDIS_URL", 'redis://localhost:6379'))
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            # "hosts": [("127.0.0.1", 6379)],
            # Below commented line to be used in case of Production (Example: heroku)
            "hosts": [os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379')],
            # "hosts": [config('REDIS_URL', default="redis://localhost:6379")]
        },
        "symmetric_encryption_keys": [SECRET_KEY],
    },
}


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # Default Django Authentication Backend
    'social_core.backends.github.GithubOAuth2',  # for Github authentication
    'social_core.backends.facebook.FacebookOAuth2',  # for Facebook authentication
    'social_core.backends.open_id.OpenIdAuth',  # for Google authentication
    'social_core.backends.google.GoogleOAuth2',  # for Google authentication
    'home.models.EmailBackend',  # Enables Login using Email as well as username
)

SOCIAL_AUTH_GITHUB_KEY = config('SOCIAL_AUTH_GITHUB_KEY', default="")
SOCIAL_AUTH_GITHUB_SECRET = config('SOCIAL_AUTH_GITHUB_SECRET', default="")

SOCIAL_AUTH_FACEBOOK_KEY = config('SOCIAL_AUTH_FACEBOOK_KEY', default="")
SOCIAL_AUTH_FACEBOOK_SECRET = config('SOCIAL_AUTH_FACEBOOK_SECRET', default="")

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = "199005728880-opegakivqlsbtm21ktjg0qf7cdj0lu0k.apps.googleusercontent.com"
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "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"

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'home'

# Email Setup
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = SERVER_EMAIL = DEFAULT_FROM_EMAIL = "nehalc2107@gmail.com"
EMAIL_HOST_PASSWORD = "gmai zptt xdlr dlfq"
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_LOCAL_TIME = True

EMAIL_SSL_CA_FILE = certifi.where()

# Peer JS Server
PEER_JS_HOST_NAME = "127.0.0.1"
PEER_JS_PORT_NUMBER = "8000"
PEERJS_SERVER_URL = '127.0.0.1:8000'

WINNING_THRESHOLD_SCORE = int(config('WINNING_THRESHOLD_SCORE', default="100"))
