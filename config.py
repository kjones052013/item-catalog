"""
    Application configuation.
"""
 
import os


# Database location
DATABASE_URI = 'sqlite:///catalog.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'a secret'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# Image upload folder
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'catalog/static/uploads')
