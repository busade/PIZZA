import os
from decouple import config
from datetime import timedelta
BASE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

class Config:
    SECRET_KEY=config('SECRET_KEY', 'secret')
    SQLALCHEMY_TRACK_MODIFICATION = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_SECRET_KEY = config('JWT_SECRET_KEY')

class DevConfig(Config):
    DEBUG= config('DEBUG', cast = bool)
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.join(BASE_DIRECTORY, 'db.sqlte3')

class TestConfig(Config):
    Testing = True
    DEBUG=config('DEBUG', cast=bool)
    SQLALCHEMY_ECHO= True
    SQLALCHEMY_DATABASE_URI='sqlite://'


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = config('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATION= False
    DEBUG= config('DEBUG', cast= bool)
    uri = config('DATABASE_URL')
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)

config_dict={
    'dev':DevConfig,
    'test': TestConfig,
    'prod': ProdConfig
}