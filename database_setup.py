"""
    Create the application database, if it doesn't exist.
    Create database schema.
"""

from config import *
from catalog.models import Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 

# Make database connection
engine = create_engine(DATABASE_URI)

# Get a database session object
DBSession = sessionmaker(bind=engine)
db_session = DBSession()


def main():
    clearDb()


def clearDb():
    """ Drop and create tables """
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    main()
