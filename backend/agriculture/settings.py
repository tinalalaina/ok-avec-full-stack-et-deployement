import os
import sys
from datetime import timedelta
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

RUNNING_TESTS = "test" in sys.argv

# Charge uniquement backend/.env pour éviter d'utiliser des secrets legacy versionnés.
load_dotenv(BASE_DIR / ".env")


def env(name: str, default: str = "") -> str:
    """Récupère une variable d'environnement en retirant les espaces parasites."""
    return os.getenv(name, default).strip()


def env_bool(name: str, default: str = "False") -> bool:
    return env(name, default).lower() in {"1", "true", "yes", "on"}


def parse_origins(value: str) -> list[str]:
    """Parse une liste d'origines séparées par des virgules (sans slash final)."""
    origins: list[str] = []
    for origin in value.split(","):
        cleaned_origin = origin.strip().rstrip("/")
        if cleaned_origin:
            origins.append(cleaned_origin)
    return origins


def parse_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


SECRET_KEY = env("SECRET_KEY", "django-insecure-agriculture-secret-2025")
DEBUG = env_bool("DEBUG", "False")

ALLOWED_HOSTS = parse_csv(env("ALLOWED_HOSTS", "localhost,127.0.0.1"))

INSTALLED_APPS = [
    # django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third-party
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_yasg",
    "corsheaders",
    # local
    "users.apps.UsersConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "agriculture.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "agriculture.wsgi.application"
ASGI_APPLICATION = "agriculture.asgi.application"

sslmode = env("DB_SSLMODE", "require")
database_url = env("DATABASE_URL")
use_sqlite = env_bool("USE_SQLITE", "False")

if use_sqlite:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": str(BASE_DIR / "db.sqlite3"),
        }
    }
elif database_url and database_url.startswith("sqlite"):
    sqlite_path = database_url.replace("sqlite:///", "", 1).strip()
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": sqlite_path or str(BASE_DIR / "db.sqlite3"),
        }
    }
elif database_url:
    parsed_url = urlparse(database_url)
    query = parse_qs(parsed_url.query)
    sslmode = query.get("sslmode", [sslmode])[0]
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": parsed_url.path.lstrip("/"),
            "USER": unquote(parsed_url.username or ""),
            "PASSWORD": unquote(parsed_url.password or ""),
            "HOST": parsed_url.hostname,
            "PORT": str(parsed_url.port or "5432"),
            "OPTIONS": {
                "sslmode": sslmode,
            },
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env("DB_NAME", "agriculture"),
            "USER": env("DB_USER", "postgres"),
            "PASSWORD": env("DB_PASS", ""),
            "HOST": env("DB_HOST", "localhost"),
            "PORT": env("DB_PORT", "5432"),
            "OPTIONS": {
                "sslmode": sslmode,
            },
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "Indian/Antananarivo"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
}

CORS_ALLOW_ALL_ORIGINS = env_bool("CORS_ALLOW_ALL_ORIGINS", "False")
CORS_ALLOWED_ORIGINS = parse_origins(env("CORS_ALLOWED_ORIGINS", ""))
CORS_ALLOW_CREDENTIALS = env_bool("CORS_ALLOW_CREDENTIALS", "False")

CSRF_TRUSTED_ORIGINS = parse_origins(env("CSRF_TRUSTED_ORIGINS", ""))

# Fallback utile en déploiement si les variables CORS/CSRF n'ont pas encore été définies.
default_frontend_url = env("FRONTEND_URL", "https://ok-avec-full-stack-et-deployement.pages.dev").rstrip("/")
if default_frontend_url and not CORS_ALLOW_ALL_ORIGINS:
    if not CORS_ALLOWED_ORIGINS:
        CORS_ALLOWED_ORIGINS = [default_frontend_url]
    if not CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS = [default_frontend_url]

EMAIL_BACKEND = env("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = env("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(env("EMAIL_PORT", "587"))
EMAIL_HOST_USER = env("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", "True")
EMAIL_USE_SSL = env_bool("EMAIL_USE_SSL", "False")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = env_bool("SECURE_SSL_REDIRECT", "True" if not DEBUG and not RUNNING_TESTS else "False")
SESSION_COOKIE_SECURE = env_bool("SESSION_COOKIE_SECURE", "True" if not DEBUG and not RUNNING_TESTS else "False")
CSRF_COOKIE_SECURE = env_bool("CSRF_COOKIE_SECURE", "True" if not DEBUG and not RUNNING_TESTS else "False")
SECURE_HSTS_SECONDS = int(env("SECURE_HSTS_SECONDS", "31536000" if not DEBUG and not RUNNING_TESTS else "0"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool("SECURE_HSTS_INCLUDE_SUBDOMAINS", "True" if not DEBUG and not RUNNING_TESTS else "False")
SECURE_HSTS_PRELOAD = env_bool("SECURE_HSTS_PRELOAD", "True" if not DEBUG and not RUNNING_TESTS else "False")

APPEND_SLASH = False

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Entrez exactement : Bearer <access_token>",
        }
    },
    "USE_SESSION_AUTH": False,
}
