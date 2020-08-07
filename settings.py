# -*- coding: utf-8 -*-
"""Application configuration.

Most configuration is set via environment variables.

For local development, use a .env file to set
environment variables.
"""
from environs import Env
import datetime

env = Env()
env.read_env()

ENV = env.str("FLASK_ENV", default="production")
DEBUG = ENV == "development"
SECRET_KEY = env.str("SECRET_KEY")
BCRYPT_LOG_ROUNDS = env.int("BCRYPT_LOG_ROUNDS", default=13)
DEBUG_TB_ENABLED = DEBUG
DEBUG_TB_INTERCEPT_REDIRECTS = False


ERROR_CODES = [400, 401, 403, 404, 405, 500, 502]

# # database
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@192.168.17.128:3306/{db}?charset=utf8'.format(
    user='root',
    password='123456',
    db='ptdevops')
SQLALCHEMY_BINDS = {
    "user": 'mysql+pymysql://{user}:{password}@192.168.17.128:3306/{db}?charset=utf8'.format(
    user='root',
    password='123456',
    db='ptdevops')
}
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_recycle': 300,
}

# # cache
CACHE_TYPE = "redis"
CACHE_REDIS_HOST = "192.168.17.128"
CACHE_REDIS_PORT = 6379
CACHE_KEY_PREFIX = "Devops:"
CACHE_DEFAULT_TIMEOUT = 3000
REDIS_MAX_CONN = "100"

# # log
LOG_PATH = './logs/app.log'
LOG_LEVEL = 'DEBUG'


# # mail
MAIL_SERVER = ''
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_DEBUG = True
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
DEFAULT_MAIL_SENDER = ''

# # queue
REDIS_MAX_CONN = 100
CELERY_RESULT_BACKEND = "redis://192.168.17.128:6379/2"
BROKER_URL = 'redis://192.168.17.128:6379/2'
BROKER_VHOST = '/'
REDIS_DB = 2

BOOL_TRUE = ['true', 'TRUE', 'True', True, '1', 1, "Yes", "YES", "yes", 'Y', 'y']

AUTHENTICATION_EXCLUDES = (
    '/api/login'
)