import os

BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = "postgresql://developer:devpassword@localhost:5432/developer"
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = "dev"