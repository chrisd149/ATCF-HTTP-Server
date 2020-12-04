from os import environ, path

from dotenv import load_dotenv
basedir = path.abspath(path.dirname(__file__))

load_dotenv()  # Initializes dotenv


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    DATA_DIR = 'data'


class ProductionConfig(Config):
    # Don't actually use this for real production with Flask alone
    DEBUG = False
    FLASK_IP = environ.get('PROD_FLASK_IP')
    FLASK_PORT = environ.get('PROD_FLASK_PORT')


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = False
    RELOADER = False
    FLASK_IP = environ.get('PROD_FLASK_IP')
    FLASK_PORT = environ.get('PROD_FLASK_PORT')


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    RELOADER = False
    FLASK_IP = environ.get('DEV_FLASK_IP')
    FLASK_PORT = environ.get('DEV_FLASK_PORT')


class TestingConfig(Config):
    TESTING = True
    RELOADER = False

