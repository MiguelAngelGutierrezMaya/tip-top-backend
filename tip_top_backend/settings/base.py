"""Base settings to build other settings files upon."""

# Django Enviroment
import environ

ROOT_DIR = environ.Path(__file__) - 3
APPS_DIR = ROOT_DIR.path('tip_top_backend')

env = environ.Env()

# Base
DEBUG = env.bool('DJANGO_DEBUG', False)

# Security
SECRET_KEY = env('DJANGO_SECRET_KEY')

# Language and timezone
TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'es-co'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = False

# DATABASES
DATABASES = {
    'default': env.db('DATABASE_URL'),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True

# URLs
ROOT_URLCONF = 'tip_top_backend.urls'

# WSGI
WSGI_APPLICATION = 'tip_top_backend.wsgi.application'

# Users & Authentication.
AUTH_USER_MODEL = 'users.User'

# Apps
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework.authtoken',
    'django_rest_passwordreset',
    'rest_framework',
    'corsheaders',
    'letsencrypt',
]

LOCAL_APPS = [
    'tip_top_backend.users.apps.UsersAppConfig',
    'tip_top_backend.roles.apps.RolesAppConfig',
    'tip_top_backend.documents.apps.DocumentsAppConfig',
    'tip_top_backend.cities.apps.CitiesAppConfig',
    'tip_top_backend.states.apps.StatesAppConfig',
    'tip_top_backend.countries.apps.CountriesAppConfig',
    'tip_top_backend.levels.apps.LevelsAppConfig',
    'tip_top_backend.units.apps.UnitsAppConfig',
    'tip_top_backend.lessons.apps.LessonsAppConfig',
    'tip_top_backend.students.apps.StudentsAppConfig',
    'tip_top_backend.parents.apps.ParentsAppConfig',
    'tip_top_backend.student_classes.apps.StudentClassesAppConfig',
    'tip_top_backend.memos.apps.MemosAppConfig',
    'tip_top_backend.notifications.apps.NotificationsAppConfig',
    'tip_top_backend.user_notifications.apps.UserNotificationsAppConfig',
    'tip_top_backend.time_availabilities.apps.TimeAvailabilitiesAppConfig',
    'tip_top_backend.materials.apps.MaterialsAppConfig',
    'tip_top_backend.comments.apps.CommentsAppConfig',
    'tip_top_backend.classes.apps.ClassesAppConfig',
    'tip_top_backend.class_repetitions.apps.ClassRepetitionsAppConfig',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Passwords
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]
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

# Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS
CORS_ORIGIN_WHITELIST = []

# Static files
STATIC_ROOT = str(APPS_DIR('static'))
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    str(APPS_DIR.path('static')),
]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Media
DJANGO_MEDIA_URL = env('DJANGO_MEDIA_URL')
MEDIA_ROOT = str(APPS_DIR('media'))
MEDIA_URL = '/media/'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ],
        'OPTIONS': {
            'debug': DEBUG,
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Security
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Admin
ADMIN_URL = 'admin/'
ADMINS = [
    ("""Miguel Gutierrez""", 'miguel.gutierrez@correounivalle.edu.co'),
]
MANAGERS = ADMINS

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'mgutierrez@pcasistencias.com'
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5
}
