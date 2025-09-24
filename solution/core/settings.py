from pathlib import Path
import environ

env = environ.Env(
    DEBUG=(bool, False)  # default value = False
)

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

INSTALLED_APPS = [
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'core',
    'task',
    'authentication',
]

MIDDLEWARE = []

ROOT_URLCONF = "core.urls"

STATIC_URL = "/static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DATABASES = {
    'default': {
        'ENGINE': env("DB_ENGINE"),
        'NAME': BASE_DIR / env("DB_NAME") if env("DB_ENGINE") == "django.db.backends.sqlite3" else env("DB_NAME"),
    }
}
