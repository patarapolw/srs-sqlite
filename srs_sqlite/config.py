import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.abspath(os.getenv('DATABASE_URI', 'new.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
