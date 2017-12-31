import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 's##cretK3y(*^&%^'
    DB_NAME = os.environ['DB_NAME']
    DB_PASS = os.environ['DB_PASS']
    ADMIN_USER = os.environ['ADMIN_USER']
    ADMIN_PASS = os.environ['ADMIN_PASS']
    MONGODB_SETTINGS = {
    'db': 'project-tracker-prod',
    'host':'mongodb://pb3975:{}@cluster0-shard-00-00-fyrgs.mongodb.net:27017,cluster0-shard-00-01-fyrgs.mongodb.net:27017,cluster0-shard-00-02-fyrgs.mongodb.net:27017/{}?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin'.format(DB_PASS, DB_NAME)
}



class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True