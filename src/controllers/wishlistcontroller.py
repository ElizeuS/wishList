from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from src.database.database import sessionLocal
from src.database.schemas import WishList

class WishListController:

  def __init__(self):
    self.session = sessionLocal()
  
  def index(self):
    pass

  def create(self):
    pass

    """
    [{
      "title": "Readmi note 10"
    }, {
      "title": "samsung"
    }]

    """