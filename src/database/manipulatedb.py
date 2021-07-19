from src.database.database import engine
from src.database.schemas import Base

def create_tables():
  Base.metadata.create_all(engine)

def drop_tables():
  Base.metadata.drop_all(engine)