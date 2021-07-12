import jwt, os
from datetime import datetime, timedelta

SECRET_KEY = 'secret'
ALGORITHM = "HS256"
PRIVATE_KEY = "coding_code"

def create_token(data):
  token = data.copy()
  token.update({'exp': datetime.utcnow() + timedelta(minutes=15)})

  return {'token': jwt.encode(token, os.environ['SECRET_KEY'], algorithm='HS256')}

def decode_token(token):
  try:
    return jwt.decode(token, os.environ['SECRET_KEY'], algorithms=['HS256'])
  except jwt.ExpiredSignatureError:
    return {'token': None}

# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#handle-jwt-tokens

# https://pyjwt.readthedocs.io/en/stable/

# https://pyjwt.readthedocs.io/en/stable/usage.html#encoding-decoding-tokens-with-hs256