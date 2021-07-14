import jwt, os
from datetime import datetime, timedelta, timezone
import json, copy

SECRET_KEY = 'secret'
ALGORITHM = "HS256"
PRIVATE_KEY = "coding_code"


def create_token(data):
  token = {
    'id': data.id,
    'name': data.name,
    'email': data.email,
    'password': data.password,
    'exp': datetime.utcnow() + timedelta(minutes=15)
  } # Usar 1 minuto para testes


  return {'token': jwt.encode(token, os.environ['SECRET_KEY'], algorithm='HS256')}

def decode_token(token):
  try:
    return jwt.decode(token, os.environ['SECRET_KEY'], algorithms=['HS256'])
  except jwt.ExpiredSignatureError:
    return None

# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#handle-jwt-tokens

# https://pyjwt.readthedocs.io/en/stable/

# https://pyjwt.readthedocs.io/en/stable/usage.html#encoding-decoding-tokens-with-hs256