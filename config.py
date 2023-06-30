class Config(object):
    DEBUG = False
    TESTING = False
    SESSION_PERMANENT = False
    DATABASE = 'test_db'


class ProductionConfig(Config):
    """
    Production configurations
    """
    DATABASE = 'prod_db'


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DATABASE = 'dev_db'
    DEBUG = True
    TESTING = True
