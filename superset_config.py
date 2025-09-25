import os
from flask_caching import Cache
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Feature Flags - Combining both feature flag configurations
FEATURE_FLAGS = {
    "ALERT_REPORTS": True,
    "EMBEDDED_SUPERSET": True,
    "CACHE_DASHBOARD_THUMBNAIL": True,
    "ENABLE_TEMPLATE_PROCESSING": True,
    "DASHBOARD_NATIVE_FILTERS": True,
    "DASHBOARD_CACHE": True,
    "ENABLE_CHART_EXPORT": True
}

# Security configurations
# WTF_CSRF_ENABLED = False
ENABLE_PROXY_FIX = True
ENABLE_CORS = True
SESSION_COOKIE_SAMESITE = None
TALISMAN_ENABLED = False
PUBLIC_ROLE_LIKE_GAMMA = True
GUEST_ROLE_NAME = "Gamma"
PERMANENT_SESSION_LIFETIME = int(os.getenv('SESSION_TIMEOUT', 3600))

# HTTP Headers
HTTP_HEADERS = {
    'X-Frame-Options': 'ALLOWALL'
}

# CORS Options
CORS_OPTIONS = {
    'supports_credentials': True,
    'allow_headers': ['*'],
    'resources': ['*'],
    'origins': ['*']
}

# Database Connection - Using environment variables
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME')

SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Secret Key - Using environment variable
SECRET_KEY = os.getenv('SECRET_KEY')

# Row Limits - Using environment variables with defaults
SQL_MAX_ROW = int(os.getenv('SQL_MAX_ROW', 1000000000))
DISPLAY_MAX_ROW = int(os.getenv('DISPLAY_MAX_ROW', 1000000000))
ROWS_LIMIT = int(os.getenv('ROWS_LIMIT', 1000000000))

# Redis Configuration - Using environment variables
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6380))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
REDIS_SSL = os.getenv('REDIS_SSL', 'true').lower() == 'true'

# Base Cache Configuration
CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": int(os.getenv('CACHE_DEFAULT_TIMEOUT', 86400)),
    "CACHE_KEY_PREFIX": "superset_",
    "CACHE_REDIS_HOST": REDIS_HOST,
    "CACHE_REDIS_PORT": REDIS_PORT,
    "CACHE_REDIS_PASSWORD": REDIS_PASSWORD,
    "CACHE_OPTIONS": {"ssl": REDIS_SSL}
}

# Specific Cache Configurations
DATA_CACHE_CONFIG = {
    **CACHE_CONFIG,
    "CACHE_DEFAULT_TIMEOUT": int(os.getenv('DATA_CACHE_TIMEOUT', 90000)),  # 1 hour for query data
}

FILTER_STATE_CACHE_CONFIG = {
    **CACHE_CONFIG,
    "CACHE_DEFAULT_TIMEOUT": int(os.getenv('FILTER_STATE_CACHE_TIMEOUT', 1800)),  # 30 minutes
}

EXPLORE_FORM_DATA_CACHE_CONFIG = {
    **CACHE_CONFIG,
    "CACHE_DEFAULT_TIMEOUT": int(os.getenv('EXPLORE_FORM_DATA_CACHE_TIMEOUT', 7200)),  # 2 hours
}

# Results Backend Configuration