import os

class DevelopmentConfig(object):
    DATABASE_URI = "postgresql://ericsokolov:thinkful@localhost:5432/capstone"
    DEBUG = True
    SECRET_KEY = os.environ.get("CAPSTONE_SECRET_KEY", os.urandom(12))

class TestingConfig(object):
    DATABASE_URI = "postgresql://ericsokolov:thinkful@localhost:5432/capstone-test"
    DEBUG = True

class HerokuConfig(object):
    DATABASE_URI = "postgres://saizzkncluhzux:512e10fb5909bfa9da90766e55ceb9cc7445e430d92583e783df8d52ad13ae26@ec2-107-20-188-239.compute-1.amazonaws.com:5432/d9kvl5tlarbf2v"
    DEBUG = True
    SECRET_KEY = os.environ.get("HEROKU_SECRET_KEY", os.urandom(12))