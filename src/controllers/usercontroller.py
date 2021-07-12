from sqlalchemy.exc import IntegrityError
import hashlib
from fastapi import status, HTTPException

from src.database.database import sessionLocal
from src.database.schemas import User


class UserController:

  def __init__(self):
    self.session = sessionLocal()

  def index(self):
    query = self.session.query(User.name, User.email).all()

    return query

  def create(self, user):
    hash = hashlib.sha512()
    hash.update(user.password.encode('utf-8'))

    password = hash.hexdigest()

    new_user = User(
      name=user.name,
      email=user.email,
      password=password
    )

    try:
      self.session.add(new_user)
      self.session.commit()

      self.session.refresh(new_user)
    except IntegrityError:
      self.session.rollback()

      return {'message': 'Username and/or email in using!'}

    return {"user_id": new_user.id}

  def update(self, user_id, user):
    '''
     This method updates the values referring to the user
    '''
    try:
      session.query(User).filter(User.id == user_id).update({"email": user.email})
      session.commit()
    except:
      session.rollback()

    #https://www.tutlinks.com/fastapi-with-postgresql-crud-async/
    #https://fastapi.tiangolo.com/tutorial/security/first-steps/
    return {"msg": "user updated"}

  def delete(self, user_id, status_code = status.HTTP_200_OK):
    # Remover um registro da tabela.
    # print('Registro ANTES da remoção:', session.query(NomeDaTabela).filter(NomeDaTabela.id == 1).one_or_none())

    try:
      session.query(User).filter(User.id == user_id).delete()
      session.commit()
    except:
      return HTTPException(status_code=404, detail="Item not found")
    return {"msg": session.query(User).filter(User.id == user_id).one_or_none()}
