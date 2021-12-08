from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

DEBUG = os.environ.get("DEBUG", "") == "1"

SECRET_KEY = "django-insecure-zsssebfy%j#!#6gw*w3xki6g#czt%l8xyownn+3o90thkn$i$t"

# Dangerous: disable host header validation
ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.sqlite3",
        "ATOMIC_REQUESTS": True,
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.common.CommonMiddleware",
]

INSTALLED_APPS = [
    # Project
    "owela_club",
    # Third Party
    "debug_toolbar",
    # Contrib
    "django.contrib.staticfiles",
]

INTERNAL_IPS = [
    "127.0.0.1",
]


ROOT_URLCONF = "owela_club.urls"

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
            ]
        },
    }
]

USE_TZ = True
