import environ
from pathlib import Path

# 1. Главные пути проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Инициализация робота-сейфа .env
env = environ.Env(
    DEBUG=(bool, True),
    ALLOWED_HOSTS=(list, ['*'])
)
# Читаем локальный скрытый файл .env в корне проекта
environ.Env.read_env(BASE_DIR / '.env')

# 3. Безопасные настройки из переменных окружения
SECRET_KEY = env('SECRET_KEY', default='django-insecure-safe-default-key-for-dev-12345')
DEBUG = env.bool('DEBUG')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# 4. Список всех подключенных приложений
INSTALLED_APPS = [
    # ⚠️ Добавляем плагин WhiteNoise на самый верх для правильного перехвата статики
    'whitenoise.runserver_nostatic',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Сторонние библиотеки
    'rest_framework',
    'django_filters',
    'drf_spectacular',

    # Твои личные приложения проекта API
    'catalog',
    'users',
]

# 5. Прослойки безопасности и обработки запросов
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # ⚠️ ВАЖНО: WhiteNoise обязан стоять строго на ВТОРОМ месте!
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'

# 6. База данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 7. Валидация паролей
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

# 8. Язык и время
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# 9. ⚠️ РАБОТА СО СТАТИКОЙ: настройки для WhiteNoise в интернете
STATIC_URL = 'static/'
# Папка, куда Django принудительно соберет все файлы стилей админки и Swagger
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 10. Глобальные настройки Django REST Framework
REST_FRAMEWORK = {
    # Схема автогенерации меню документации Swagger
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    # Список инструментов для фильтрации и поиска по тексту
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],

    # Постраничная пагинация списков
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,

    # Охрана: вход для записи, анонимам — только просмотр
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],

    # Переводчик входящих токенов JWT
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# 11. Настройки оформления меню Swagger UI
SPECTACULAR_SETTINGS = {
    'TITLE': 'Магазин API Каталог',
    'DESCRIPTION': 'Интерактивное меню нашего магазина с товарами, категориями и отзывами',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}
