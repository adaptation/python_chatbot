import os

##アプリ名とプロジェクト名を入力##
APP_NAME = 'myApp'
PROJECT_NAME = 'myProject'


#許可するホストを指定
ALLOWED_HOSTS = ['*']


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', #使用するDBによって変更
        'NAME': 'dbname',
        'USER':'username',
        'PASSWORD':'password',
        'HOST':'hostname',
        'PORT':'port',
    }
}


MYAPP_DIR='C:\\Users\\Admin\\Documents\\Hirose\\hirose_Py\\myProject\\myApp'

LOGFILE_DIR = 'C:\\Users\\Admin\\Documents\\Hirose\\hirose_Py\\myProject\\log'

FILE_UPLOAD_TEMP_DIR = 'C:\\Users\\Admin\\Documents\\Hirose\\hirose_Py\\myProject\\myApp\\temp'

STATICFILES_DIR='C:\\Users\\Admin\\Documents\\Hirose\\hirose_Py\\myProject\\myApp\\static'

FILE_UPLOAD_TEMP_DIR = 'C:\\Users\\Admin\\Documents\\Hirose\\hirose_Py\\myProject\\myApp\\temp'


####以下は変更しない####


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'kbccn9k*#*@7)qy2779r!8yk5%x5v4le5ofm_3t69h8iv!2dju'
DEBUG = False


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    APP_NAME
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]


ROOT_URLCONF = PROJECT_NAME + '.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = PROJECT_NAME + '.wsgi.application'


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


LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = False


STATIC_URL = '/static/'

FILE_UPLOAD_MAX_MEMORY_SIZE = 0
TEMP_FILE_NAME = 'temp.xlsx'


#LOG出力
LOGGING = {
	'version': 1,   
	'formatters': { 
		'all': {    
			'format': '\t'.join([
				"[%(levelname)s]",
				"asctime:%(asctime)s",
				"module:%(module)s",
				"message:%(message)s",
				"process:%(process)d",
				"thread:%(thread)d",
			])
		},
		'simple': {    
			'format': '[%(levelname)s] %(message)s'
		},
	},
	'handlers': {
		'file': {
			'level': 'DEBUG',  
			'class': 'logging.FileHandler',  
			'filename': os.path.join(LOGFILE_DIR, 'myApp.log'),  
			'formatter': 'simple',  
		},
		'console': { 
			'level': 'DEBUG',
			'class': 'logging.StreamHandler',
			'formatter': 'all'
		},
	},
	'loggers': {
		'samplelogger': {
			'handlers': ['file', 'console'],
			'level': 'DEBUG',
		},
	},
}

