import jwt, os
from datetime import datetime, timedelta

def create_token(data):
  token = {
    'id': data.id,
    'name': data.name,
    'nickname': data.nickname,
    'email': data.email,
    'password': data.password,
    'exp': datetime.utcnow() + timedelta(minutes=40)
  } # Usar 1 minuto para testes


  return {'token': jwt.encode(token, os.environ['SECRET_KEY'], algorithm='HS256')}

def decode_token(token):
  try:
    return jwt.decode(token, os.environ['SECRET_KEY'], algorithms=['HS256'])
  except jwt.ExpiredSignatureError:
    return None
  except jwt.exceptions.InvalidSignatureError:
    return None

# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#handle-jwt-tokens

# https://pyjwt.readthedocs.io/en/stable/

# https://pyjwt.readthedocs.io/en/stable/usage.html#encoding-decoding-tokens-with-hs256