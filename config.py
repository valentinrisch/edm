import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'hasshasshass'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:hasshasshass@localhost:5432/hate_store'



class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
