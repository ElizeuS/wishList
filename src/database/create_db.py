from src.database.database import engine
from src.database.schemas import Base

Base.metadata.create_all(engine)