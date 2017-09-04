import os

class DevelopmentConfig(object):
    DATABASE_URI = "postgresql://ericsokolov:thinkful@localhost:5432/capstone"
    DEBUG = True
    SECRET_KEY = os.environ.get("CAPSTONE_SECRET_KEY", os.urandom(12))

class TestingConfig(object):
    DATABASE_URI = "postgresql://ericsokolov:thinkful@localhost:5432/capstone-test"
    DEBUG = True
