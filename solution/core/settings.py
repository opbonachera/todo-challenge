from pathlib import Path
from datetime import timedelta
import environ


env = environ.Env(
    DEBUG=(bool, False)  
)

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
AUTH_USER_MODEL = "authentication.User"


INSTALLED_APPS = [
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
    'rest_framework.authtoken',
    'django.contrib.auth',
    'core',
    'task',
    'authentication',
]

MIDDLEWARE = MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware', 
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.common.CommonMiddleware',
]

REST_FRAMEWORK = {
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

ROOT_URLCONF = "core.urls"
STATIC_URL = "/static/"
APPEND_SLASH = False
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
DATABASES = {
    'default': {
        'ENGINE': env("DB_ENGINE"),
        'NAME': BASE_DIR / env("DB_NAME") if env("DB_ENGINE") == "django.db.backends.sqlite3" else env("DB_NAME"),
    }
}
