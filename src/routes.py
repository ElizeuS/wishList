from pydantic import BaseModel
from fastapi import status, Header
from typing import Optional, Dict, List

from src import app
from src.database.schemas import *
from src.headers import create_token, decode_token
from src.controllers.usercontroller import UserController
from src.controllers.authcontroller import UserProfileController
from src.controllers.productcontroller import ProductController

class UserModel(BaseModel):
  name: str
  email: str
  password: str

class ProductModel(BaseModel):
  title: str
  desc: Optional[str]
  uri: Optional[str]
  img: Optional[str]

@app.get('/')
def home():
  return {'msg': "Hello world"}

# User Routes

@app.get('/list-users/')
def list_users():
  controller = UserController()

  return controller.index()

@app.post('/register')
def create_user(user: UserModel):
  if( user ):
    controller = UserController()

    return controller.create(user)

  return {'msg': 'Body is required!'}

@app.post('/login/')
def login(data: dict):
  userProfile = UserProfileController()
  result = userProfile.auth_login(data)

  if( not result ):
    return {'message': 'Invalid login'}

  return create_token(result)

@app.post('/logout/')
def logout(token: Optional[str] = Header(None)):
  if( decode_token(token) == None):
    return {'message': 'token is required'}

  return {'token': None}

@app.put("/update-user/{user_id}")
def update_user(user_id:int, user: UserModel):
  if( user ):
    controller = UserController()

    return controller.update(user_id, user)

  return {'msg': 'Body is required!'}

@app.delete('/delete-user/{user_id}')
def delete_user(user_id):
  controller = UserController()

  return controller.delete(user_id)

#Product Routes

@app.get('/list-products/')
def list_products():
  controller = ProductController()

  return controller.index()

@app.post('/create-product/')
def create_product(data: List[ProductModel], token: Optional[str] = Header(None)):
  if( not token ):
    return {'message': 'token is required'}

  controller = ProductController()

  return controller.create(data)

# https://fastapi.tiangolo.com/tutorial/body/