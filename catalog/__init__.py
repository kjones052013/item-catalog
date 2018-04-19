"""
    Catalog App Initialization.
    Initialize the Flask framework.
    Initialize the SQLAlchemy ORM.
"""

 
from flask import Flask
from flask_wtf.csrf import CsrfProtect

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Initialize Flask framework
app = Flask(__name__)
app.config.from_object('config')

csrf = CsrfProtect(app)

# Connect to database
engine = create_engine(app.config['DATABASE_URI'])

# Get a database session object
DBSession = sessionmaker(bind=engine)
db_session = DBSession()

# Flask view functions
import catalog.views
