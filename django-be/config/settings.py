from pathlib import Path

# --- Base Directory and Security Settings ---
BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = True  # Set to False in production

# --- Installed Applications ---
INSTALLED_APPS = [
    # Django core apps for essential functionality
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',

    # Third-party apps for REST API support and CORS handling
    'corsheaders',
    'ninja',

    # Custom applications for project-specific features
    'data_processor',
]

# --- Middleware Configuration ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Handles CORS for API requests
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --- CORS Configuration ---
CORS_ALLOW_ALL_ORIGINS = True  # Use with caution in production; specify allowed origins if needed

# --- URL Configuration ---
ROOT_URLCONF = 'config.urls'

# --- Templates Configuration ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Add template directories here if needed
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
            ],
        },
    },
]

# --- WSGI Application ---
WSGI_APPLICATION = 'config.wsgi.application'

# --- Database Configuration ---
DATABASES = {}  # No database used; add configuration if a database is required

# --- Internationalization ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- Static Files ---
STATIC_URL = '/static/'

# --- Default Auto Field ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
