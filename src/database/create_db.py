from database import Base, engine
from models import User

Base.metadata.create_all(engine)