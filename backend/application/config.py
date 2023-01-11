import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    # SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"



class LocalDevelopmentConfig(Config):
    SQLITE_DB_DIR = os.path.join(basedir, "../db_directory")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "db.sqlite3")
    DEBUG = True
    SECRET_KEY = "vjksiut78hJKfilu"
    SECURITY_PASSWORD_HASH="bcrypt"
    SECURITY_PASSWORD_SALT="KJLSFHIU5873SDFGG"
    SECURITY_PASSWORD_LENGTH_MIN=6
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL=False
    SECURITY_UNAUTHORIZED_VIEW = None
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = "redis://localhost:6379/7"
    CACHE_DEFAULT_TIMEOUT = 500
    CELERY_BROKER_URL= "redis://localhost:6379/1"
    CELERY_BACKEND= "redis://localhost:6379/2"

    # CACHE_KEY_PREFIX = 'MY_APP'



