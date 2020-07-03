"""
Django settings for PythonServer project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import django_redis

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')e5*smkqre2_s6w%pc#bsum+$b-k82t78leth$91&&ho#r*cu='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["115.29.150.206", "0.0.0.0:8001", "127.0.0.1"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # haystack要放在应用的上面
    'haystack',
    'user',
    "movies",
    "error",
    "website",
    "user_like",
    "vip",
]
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}
# 当添加、修改、删除数据时，自动生成索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
# haystack自动分页默认每页显示20个  可以根据自己的需求设置显示个数
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 16


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # "middlewares.useragent.UserAgentMiddleware",
]

ROOT_URLCONF = 'PythonServer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, "templates")
        ],
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

WSGI_APPLICATION = 'PythonServer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
# django默认支持sqlite mysql
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pythondb',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    # '/var/www/static/',  在Linux系统中存放的地址
]

LOGIN_URL = "/login/"


# django内置发邮件配置
# 邮件服务器配置
EMAIL_HOST = 'smtp.163.com'  # 如果是 163 改成 smtp.163.com
EMAIL_PORT = 465
EMAIL_HOST_USER = 'zyh1741290057@163.com'  # 在这里填入您的QQ邮箱账号
EMAIL_HOST_PASSWORD = 'zhangyonghao1997'  # 请在这里填上您自己邮箱的授权码
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_USE_SSL = True

# settings.py中加入redis设置
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:@127.0.0.1:6379",  # 这里设定了本机的redis数据
        # "LOCATION": "redis://:passwordpassword@47.193.146.xxx:6379/0", # 如果redis设置密码的话，需要以这种格式host前面是密码
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


AUTH_USER_MODEL = "user.PythonUser"


# MEDIA_URL = 'media/'  # 上传图片的路径：D:\blog_project\uploads
MEDIA_ROOT = "static/"
# MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')  # 上传图片的根路径 BASE_DIR:D:\blog_project


UID = "2016101200668491"
ZFB_DNS = "https://openapi.alipaydev.com/gateway.do"

APP_PRIVATE = "MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCBWkjIWeZMyYVBD9YNOYP6n0qPZrM3ZYt1cVzSG/ClARgJdJqsy1eGLHKe3ieeaoqJRu8PvRzYwgbBXa8IlsddT3y7+ERi9kohMWrafHCAT2aqxXdEaRq3KH0x2el8KnSBYq6Mv1K4WVZ60+D2IYAMtRUPCjm3opIGndZ5iEdkClhynMQ/wBc4xyexxQVPdhtF+GDEFQD92WzWGk1XM8/wgwjiGvUeZa42I1+6O59yVZywaQydFFoXnAXmSaLJ1j+GOAEu6c098e8a/r1Q0WXI9WhiKgAR/is39IOPhseuyHi2ueux64DjSmpxRvRjupyBNXxkQ+V6SSBtw6uMK9/RAgMBAAECggEAJzjZGOcpjd8NKM1Een4WJshmM1VQwltoDhRxsMQIFABg6X0R6ZM+1tBjcQirur1ThIydsIgHVzJ+GePuTwxpJ0IS8Gw3UEqd77KsU9OnyUBKQT3fDD9SencsfxE0WxIEgbcKdmMNEhkEv/m/HOLLkQ7Xc9gF6EjDPn5dqjxIaWzLQqgcqKmxMOznUv5XQAp5nLRrgWgJgS3tdxPt2ojRnKsHEmfgu6jskL+X7jn4R5Br9LXjXAXS7q7tZtHI80oZzE+nGyAhdkKJgvyalpE5MnmjkbwJVasTM6Ly1CSFDpETu75ZnAHiEQIXmnMp2KJlWzlYWjRwkQtRIpU23vK2AQKBgQC6Db/LOQfxzhET5pJpYoYGdkbr1aRmGJquoi9EYTjzaMisyg+VmwzIuFrN6JuugGG3GCUG7If8sOdCiP7img4qjVHt+TE+1mQR3nHUQUeh79awNpkr7Usgbdbr9mf/pxsL5Z80mA6jLkaTMKV+WpnljsLnUEtllTNLLFViQfcd5QKBgQCx+34qsORVt9MIqiVJFiOxXo8inWOvY4AZp702iHHXgzyUMP+VeIEwmai3J41OgOMn5ieuEHtFOikQlcd0roFrqnOih6nCeGeHa3eBV4cWqQ7FNx0NoO6z0uZE2l2HeZUSyKBq6N1Nl7FIQBRrk+T3SXJUhFjTGKsJBL/+ajy7fQKBgFa268o7BYHkyj7dOyYU/mRqoflu9JWFKCr2elNDgPipwMYP0x2mS1oN2nyXyl+VhHWCslc8zNCwXsi68xkINkwM27+vYg1ofPF7HNCRsGJAV25/s/ouOdKefwoxKR2Vc9yipAYuTLwvaENX6/otHgdI93w6BzoMRQDnY9BM8HElAoGAeNqRqEFnOoFRDiAio0ciQ202+kUvDEgfEsygoafyzWkyuFmxIvipmKuuMXfs7rJ8DHqu1PYiDjbY7YcW4bcg8E/UpzdBYWjKu9yQUEZz10JCYk3zL27oxzhc3cH9ImG/hPqwWwf2RZrMaYgBla7eGcBInvUjL2wfr0cHa6UNyi0CgYBCOYdMFk72i0GCpVwMLp4/I8N97BLhDtRf0N55i/nUCZwGOQijyfFKoP0GlgfO0eSVzUNZl25sYcwTyzOZLhOpmEAX/Z1yyd4DaUUXu/vx5If5Gtr1TFiCmjDion78BRqoXg5RCHQs6uWpq2D0YhoO/2qKsrvoYqw5twsx40u/8w=="
APP_PUBLIC = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAgVpIyFnmTMmFQQ/WDTmD+p9Kj2azN2WLdXFc0hvwpQEYCXSarMtXhixynt4nnmqKiUbvD70c2MIGwV2vCJbHXU98u/hEYvZKITFq2nxwgE9mqsV3RGkatyh9MdnpfCp0gWKujL9SuFlWetPg9iGADLUVDwo5t6KSBp3WeYhHZApYcpzEP8AXOMcnscUFT3YbRfhgxBUA/dls1hpNVzPP8IMI4hr1HmWuNiNfujufclWcsGkMnRRaF5wF5kmiydY/hjgBLunNPfHvGv69UNFlyPVoYioAEf4rN/SDj4bHrsh4trnrseuA40pqcUb0Y7qcgTV8ZEPlekkgbcOrjCvf0QIDAQAB"
ZFB_PUBLIC = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAl7OwhGmH/J2aSP3j4Pbk/NxvNhBfAIBDCEujBN9vdnCu3kKA5SNkomvHvdHXM66/3LQhKzigMg9r/y6CrgQJPR8Q+wHrRiGXbLmIqJw2pMVfXgms1gr1Mz9aR3GbuIzTMOLcHALWPQ47cNtgPUg1UfRE0NyJMpZ3+crg9Dzt5fJ7BJK+7m9FDX8v7R0axahEkkO0IYaxqHOvZ5v0pygls3z2ZM0gVon63cu1K8PxD2KsNHwK8dUkw6uDY2VqkyYybQGRlT4VWQkDYdPNqzMDmjV7Y4DjX+b/JV+Wu7mYY6llosNT30yQhKhcb1C5MEPulvbeOrjdxP59+niERAV/4QIDAQAB"
