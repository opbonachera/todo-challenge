from pathlib import Path
from datetime import timedelta
import environ

env = environ.Env(
    DEBUG=(bool, False)  
)

CORS_ALLOW_ALL_ORIGINS = env("CORS_ALLOW_ALL_ORIGINS", default=False)
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(BASE_DIR / ".env")
API_VERSION = 'v1'
SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
AUTH_USER_MODEL = "authentication.User"
ROOT_URLCONF = "core.urls"
STATIC_URL = "/static/"
APPEND_SLASH = False
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INSTALLED_APPS = [
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
    'drf_standardized_errors',
    'rest_framework.authtoken',
    'corsheaders',
    'django.contrib.auth',
    'core',
    'task',
    'authentication',
]

MIDDLEWARE = MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware', 
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "drf_standardized_errors.handler.exception_handler",
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
SIMPLE_JWT = {
        'ACCESS_TOKEN_LIFETIME': timedelta(minutes=20), 
        'REFRESH_TOKEN_LIFETIME': timedelta(days=1),   
        'ROTATE_REFRESH_TOKENS': True,                  
        'BLACKLIST_AFTER_ROTATION': True,               
    }
DATABASES = {
    'default': {
        'ENGINE': env("DB_ENGINE"),
        'NAME': BASE_DIR / env("DB_NAME") if env("DB_ENGINE") == "django.db.backends.sqlite3" else env("DB_NAME"),
    }
}
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])
AUTH_PASSWORD_VALIDATORS = [
    # {
    #     "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    # },
    # {
    #     "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    # },
    # {
    #     "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    # },
    # {
    #     "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    # },
]