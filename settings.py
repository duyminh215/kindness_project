# -*- coding: utf-8 -*-

import os
from . import db_configs


class Config(object):

    DEBUG = True
    TESTING = False


    # mail settings
    MAIL_SERVER = 'smtp.126.com'
    MAIL_PORT = 25

    # mail authentication
    MAIL_USERNAME = 'bababa'
    MAIL_PASSWORD = 'bababa'


class DevelopmentConfig(Config):

    ENV = 'development'
    DEBUG = True

    # session
    CSRF_ENABLED = True
    SECRET_KEY = "dcbTbOi0EK1xbHnULktbqA"

    # datebase
    SQLALCHEMY_DATABASE_URI = 'mysql://' + db_configs.user + ':' + db_configs.password + '@' + db_configs.host + ":" + db_configs.port + '/' + db_configs.db_name
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):

    ENV = 'testing'
    TESTING = True


class StagingConfig(Config):

    ENV = 'staging'
    TESTING = True


class ProductionConfig(Config):

    ENV = 'production'
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
