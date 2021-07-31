from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(environ['DATABASE_URL'], echo=True)
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
