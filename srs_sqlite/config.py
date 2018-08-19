import os


class Config(object):
    DATABASE_URI = os.path.abspath(os.getenv('DATABASE_URI', 'new.db'))
    IMAGE_DATABASE_FOLDER = os.path.splitext(DATABASE_URI)[0]

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
