class Config(object):
    DEBUG = False
    TESTING = False
    SESSION_PERMANENT = False
    DATABASE = 'test_db'
    OAUTH2_CLIENT_ID = "test_web_app"
    OAUTH2_CLIENT_SECRET = 'BbyZrpYjSf6JRxOEs1tVBFUcYVcfAYIQ'
    OAUTH2_ISSUER = 'http://localhost:8080/realms/myorg'
    OAUTH2_ISSUER_HOST = "http://localhost:8080"
    FLASK_SECRET = 'somelongrandomstring'
    FLASK_PORT: 5000


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
