class DevelopmentConfig(object):
    DATABASE_URI = "postgresql://ericsokolov:thinkful@localhost:5432/capstone"
    DEBUG = True

class TestingConfig(object):
    DATABASE_URI = "postgresql://ericsokolov:thinkful@localhost:5432/capstone-test"
    DEBUG = True
