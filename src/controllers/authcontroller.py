from src.database.database import sessionLocal
from sqlalchemy.sql import select
from src.database.schemas import *
import hashlib

class UserProfileController:

  def __init__(self):
    self.session = sessionLocal()

  def auth_login(self, data):
    
    hash = hashlib.sha512()
    hash.update(data['password'].encode('utf-8'))

    hashed_password = hash.hexdigest()
    query = select(User.id, User.name, User.nickname, User.email, User.password).where(User.email == data['email'] and User.password == hashed_password)

    result = self.session.execute(query).fetchone()
    self.session.close()

    return result