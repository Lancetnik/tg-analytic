import secrets

from propan.config import settings


DATABASE_URL = f'postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}\
@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}'

SECRET_KEY = secrets.token_urlsafe(32)
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8
BACKEND_CORS_ORIGINS = []

PROJECT_NAME = 'Authentication'

SMTP_TLS = True
SMTP_PORT = None
SMTP_HOST = None
SMTP_USER = None
SMTP_PASSWORD = None
EMAILS_FROM_EMAIL = None
EMAILS_FROM_NAME = None

EMAIL_RESET_TOKEN_EXPIRE_HOURS = 48
EMAIL_TEMPLATES_DIR = "/app/email-templates/build"
EMAILS_ENABLED = False

EMAIL_TEST_USER = "test@example.com"
FIRST_SUPERUSER_EMAIL = "test@example.com"
FIRST_SUPERUSER_PASSWORD = '1234'
USERS_OPEN_REGISTRATION = True
