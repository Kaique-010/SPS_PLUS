from pathlib import Path
import os
from dotenv import load_dotenv
from django.db import connections
from licencas.database_utils import load_databases


load_dotenv()
print("DB_USER:", os.getenv('DB_USER'))
print("DB_PASSWORD:", os.getenv('DB_PASSWORD'))
print("DB_NAME:", os.getenv('DB_NAME'))
print("DB_PORT:", os.getenv('DB_PORT'))

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES_FILE = BASE_DIR / "databases.json"



SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("Chave secreta não definida no .env")

DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')





# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    
    #Aplicações
    'Entidades',
    'Entradas_Produtos',
    'licencas',
    'Menu',
    'Pedidos',
    'produto',
    
    'Saidas_Produtos',
    'Ordemservico',
    'orcamentos',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', 
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'licencas.middleware.ThreadLocalMiddleware',

    

]


LOGIN_REDIRECT_URL ='home'

ROOT_URLCONF = 'sps_plus.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sps_plus.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'default_db_name'),
        'USER': os.getenv('DB_USER', 'default_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'default_password'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5433'),
        'ATOMIC_REQUESTS': True, 
        'OPTIONS': {}, 
        'CONN_MAX_AGE': 600,
        'AUTOCOMMIT': True,
        'CONN_HEALTH_CHECKS': False,
    },
}

from licencas.database_utils import load_databases

DATABASES.update(load_databases())


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


#modelos de autenticação
AUTHENTICATION_BACKENDS = [
    #'licencas.auth_backends.DocumentoAuthBackend',  
    'django.contrib.auth.backends.ModelBackend',  
    'licencas.auth_backends.LoginBackend',  
]


#modelo personalizado de usuários
AUTH_USER_MODEL = 'licencas.Usuarios'


# Language and Time Zone
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

DATABASE_ROUTERS = [ "licencas.db_router.LicenseDatabaseManager",
                     "licencas.db_router.LicenseDatabaseRouter",
                    
                    ]

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'Entidades/static'),
    os.path.join(BASE_DIR, 'Pedidos/static'),
    os.path.join(BASE_DIR, 'produto/static'),
    os.path.join(BASE_DIR, 'menu/static'),
    os.path.join(BASE_DIR, 'Ordemservico/static'),
    #os.path.join(BASE_DIR, 'Ordemproducao/static'),
    os.path.join(BASE_DIR, 'Saidas_Produtos/static'),
    os.path.join(BASE_DIR, 'Entradas_Produtos/static'),
    os.path.join(BASE_DIR, 'orcamentos/static'),
    os.path.join(BASE_DIR, 'licencas/static'),
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SESSION_ENGINE = 'django.contrib.sessions.backends.db' 
SESSION_COOKIE_AGE = 3600  # Tempo em segundos para expiração do cookie (1 hora
SESSION_COOKIE_NAME = 'sessionid'  # Nome do cookie de sessão
SESSION_SAVE_EVERY_REQUEST = True  
SESSION_EXPIRE_AT_BROWSER_CLOSE = False 
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000']
SESSION_COOKIE_SECURE = False  # Se estiver testando localmente
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"  # Teste com "None" se necessário

LOGOUT_REDIRECT_URL = 'login'  # Ou a página que você preferir
LOGIN_URL = '/licencas/login/'


CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000',
    'https://seu-dominio.com',  # Exemplo para produção
]
