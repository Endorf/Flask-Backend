class Config(object):
    DEBUG = False
    TESTING = False
    SESSION_PERMANENT = False

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
