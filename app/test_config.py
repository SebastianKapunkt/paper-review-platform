""" Config file for Flask """
DEBUG = True
WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SEND_FILE_MAX_AGE_DEFAULT = 0
