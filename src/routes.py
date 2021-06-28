from main import app, Form
from pydantic import BaseModel
import hashlib

class Item(BaseModel):
  name: str
  email: str
  password: str

@app.get('/')
def home():
  return {'msg': "Hello world"}

@app.get('/user')
def list_user():
  return 0

@app.post('/user')
def create_user(item: Item):
  if( item ):
    hash = hashlib.sha512()
    hash.update(item.password.encode('utf-8'))
    pass_hash = hash.hexdigest()

    return {
      "name": item.name,
      "email": item.email,
      "password": pass_hash
    }

  return {"error": "Product not existing!"}

# https://fastapi.tiangolo.com/tutorial/body/