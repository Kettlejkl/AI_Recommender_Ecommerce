# Django settings for ecommerce_project project.

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from the .env file
from dotenv import load_dotenv
load_dotenv()

# Environment variables
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'fallback_dev_secret')  # Default to a fallback secret in dev
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'  # Defaults to True for development
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost 127.0.0.1 ai-recommender-ecommerce-xxdd.onrender.com').split()

# Add your environment variables for MongoDB and OpenAI
OPENAI_KEY = os.getenv("OPENAI_KEY", "default_openai_key")  # Example: 'dab82bcf11b83362167ef1634b859e6a'
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/ecommerce_db")  # Example: MongoDB URI

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecommerce_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'store', 'templates'),  # Add this line to specify template directory
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce_project.wsgi.application'

# Database configuration
# MongoDB configuration for Djongo
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'ecommerce_db',
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
            'host': MONGO_URI,  # Use the environment variable here
        }
    }
}

# Password validation
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

# Localization settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
