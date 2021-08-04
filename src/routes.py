from pydantic.types import Json
from pydantic import BaseModel
from fastapi import status, Header
from typing import Optional, Dict, List
import json

from src import app
from src.database.schemas import *
from src.headers import create_token, decode_token
from src.controllers.usercontroller import UserController
from src.controllers.authcontroller import UserProfileController
from src.controllers.productcontroller import ProductController
from src.controllers.wishlistcontroller import WishListController

class UserModel(BaseModel):
  name: Optional[str]
  nickname: Optional[str]
  email: Optional[str]
  password: Optional[str]

class ProductModel(BaseModel):
  title: str
  desc: Optional[str]
  uri: Optional[str]
  img: Optional[str]
  status: Optional[str]


# User Routes

@app.post('/register/', tags=["Users"])
def create_user(user: UserModel):
  """
  This will allow the registration of new users in the system.
  """
  if( user ):
    controller = UserController()

    return controller.create(user)

  return {'msg': 'Body is required!'}

@app.post('/login/', tags=["Users"])
def login(data: dict):
  """
  This will allow the login of users in the system.
  """
  userProfile = UserProfileController()
  result = userProfile.auth_login(data)

  if( not result ):
    return {'msg': 'Invalid login'}

  return create_token(result)

@app.post('/logout/', tags=["Users"])
def logout(token: Optional[str] = Header(None)):
  if( decode_token(token) == None):
    return {'msg': 'token is required'}

  return {'token': None}

@app.put("/update-user/{user_id}", tags=["Users"])
def update_user(user_id:int, user: UserModel, token: Optional[str] = Header(None)):
  """
  This will allow you to update user data.
  """
  token_decoded = decode_token(token)

  if( token_decoded == None):
    return {'msg': 'token is required'}

  if( user ):

    controller = UserController()

    return controller.update(token_decoded['id'], user)

  return {'msg': 'Body is required!'}

@app.delete('/delete-user/{user_id}', tags=["Users"])
def delete_user(password: UserModel, token: Optional[str] = Header(None)):
  """
  This will allow the exclusion of users registered in the system.
  """
  token_decoded = decode_token(token)

  if( token_decoded == None):
    return {'msg': 'token is required'}

  if( not password ):
    return json.dumps({'msg': 'body is required'})

  controller = UserController()
  return controller.delete(password, token_decoded['id'])


#Product Routes

@app.get('/list-products/', tags=["Products"])
def list_products():
  controller = ProductController()

  return controller.index()

@app.post('/create-product/', tags=["Products"])
def create_product(data: List[ProductModel], token: Optional[str] = Header(None)):
  """
  This method allows you to insert a product list in the system.
  """
  token_decoded = decode_token(token)
  if( token_decoded == None ):
    return {'msg': 'token is required'}

  controller = ProductController()
  product_list = controller.create(data, token_decoded['id'])

  wishcontroller = WishListController()
  wishcontroller.create(product_list, token_decoded['id'])

  return product_list

@app.post('/update-product', tags=["Products"])
def update_product(products: List[ProductModel], token: Optional[str] = Header(None)):
  """
  This method allows you to update values of a product in the system.
  """
  token_decoded = decode_token(token)
  if ( token_decoded == None ):
    return {'msg': 'token is required'}

  controller = ProductController()
  id_product = controller.search_by_body(products[0], token_decoded['id'])

  return controller.update(products[1], token_decoded['id'], id_product[0])

@app.delete('/delete-product', tags=["Products"])
def delete_product(product, token: Optional[str] = Header(None)):
  """
  This method allows you to delete registered products.
  """
  token_decoded = decode_token(token)
  if( token_decoded == None ):
      return {'msg': 'token is required'}

  if( not product ):
    return json.dumps({'msg': 'body is required'})

  controller = ProductController()

  return controller.delete(product, token_decoded['id'])

# WishList Routes

@app.get('/wishlist/', tags=["Wishlists"])
def get_wishlist(username: Optional[str] = None, token: Optional[str] = Header(None)):
  """
  This method returns all products from a user's wish list by nickname.
  """
  token_decoded = decode_token(token)
  controller = WishListController()
  if( token_decoded == None ):
    return {'msg': 'token is required'}

  if( not username ):
    username = token_decoded['nickname']

  return controller.search_by_username(username)

@app.post('/have-product', tags=["Wishlists"])
def status_update(product: ProductModel, status, token: Optional[str] = Header(None)):
  """
  This method updates the item status value if the user has already received/purchased it.
  True indicates the user already owns the item. Default value is false.
  """
  return {'product': product, 'status': status}

@app.get('/wishlist/random', tags=["Wishlists"])
def random_list(token: Optional[str] = Header(None)):
  token_decoded = decode_token(token)

  if( token_decoded == None ):
    return {'msg': 'token is required'}
  controller = WishListController()

  return controller.random(token_decoded['id'])

@app.get('/wishlist/owned', tags=["Wishlists"])
def owned_products(token: Optional[str] = Header(None)):
  """
  This method returns all products already received/purchased from the user.
  """
  token_decoded = decode_token(token)

  if( token_decoded == None ):
     return {'msg': 'token is required'}

  controller = ProductController()

  return controller.get_products_owned(token_decoded['id'])


@app.post('/wishlist/favorite-item/{product_id}', tags=["Wishlists"])
def favorite_item(product_id: Optional[int], token: Optional[str] = Header(None)):
  """
  This method allows you to covet/favor an item from another user's wish list. The item will be added to your wish list.
  """
  token_decoded = decode_token(token)

  if( token_decoded == None ):
     return {'msg': 'token is required'}

  controller = WishListController()

  return controller.favorite_item(product_id, token_decoded['id'])
