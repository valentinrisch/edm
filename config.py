import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'hasshasshass'
    #SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:hasshasshass@localhost:5432/hate_store'
    SQLALCHEMY_DATABASE_URI = 'sqlite:/Users/valentin/Downloads/million_post_corpus/corpus.sqlite3'


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
