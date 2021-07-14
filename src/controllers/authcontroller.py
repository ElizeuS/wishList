from src.database.database import sessionLocal
from sqlalchemy.sql import select
from src.database.schemas import *

class UserProfileController:

  def __init__(self):
    self.session = sessionLocal()

  def auth_login(self, data):
    query = select(User.id, User.name, User.email, User.password).where(User.email == data['email'] and User.password == data['password'])

    result = self.session.execute(query).fetchone()
    self.session.close()

    return result