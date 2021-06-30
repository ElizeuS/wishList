from sqlalchemy import Integer, String
from sqlalchemy.sql.schema import Column

from database import Base

class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(30), nullable=False)
  email = Column(String, nullable=False, unique=True)
  password = Column(String, nullable=False)

  def __repr(self):
    return f"<User name={self.name}>"
