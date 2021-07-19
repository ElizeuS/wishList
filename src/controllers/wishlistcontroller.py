from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from src.database.database import sessionLocal
from src.database.schemas import WishList

class WishListController:

  def __init__(self):
    self.session = sessionLocal()

  def index(self):
    pass

  def create(self, products, user_id):
    print(products)
    product_list = []
    for product in products:
      wish = WishList(user_id = user_id, product_id = product[0], status=False)
      product_list.append(wish)

    try:
      self.session.add_all(product_list)
      self.session.commit()
    except IntegrityError:
      self.session.rollback()

      return {"msg": "the relationship already exists"}
