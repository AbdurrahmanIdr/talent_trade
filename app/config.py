import os
from secrets import token_urlsafe

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    FLASK_APP = 'run.py'
    UPLOAD_FOLDER = 'app/static/images/profile_pics/'
    SECRET_KEY = token_urlsafe(32)
    FLASK_DEBUG = False
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{base_dir}/app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    TESTING = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')


class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = False


class DevConfig(Config):
    FLASK_DEBUG = True


class TestConfig(Config):
    TESTING = True
    DEBUG = True


config = {
    "development": DevConfig(),
    "production": ProdConfig(),
    "testing": TestConfig()
}
