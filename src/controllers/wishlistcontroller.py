from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from src.database.database import sessionLocal
from src.database.schemas import WishList, Product, User
import hashlib, json
from sqlalchemy import func
class WishListController:

  def __init__(self):
    self.session = sessionLocal()

  def index(self, user_id):
    result = self.session.query(WishList) \
            .filter(WishList.user_id == user_id) \
            .all()

    return result

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

  def search_list(self, user_id):
    result = self.session.query(WishList.status, Product) \
            .join(Product, WishList.product_id == Product.id) \
            .filter(WishList.user_id == user_id) \
            .all()

    return result


  def search_by_username(self, nickname: str):
    result = self.session.query(WishList.id, WishList.status, Product) \
          .join(Product, WishList.product_id == Product.id) \
          .join(User, WishList.user_id == User.id) \
          .filter(User.nickname == nickname) \
          .all()

    return result

  def random(self, user_id):
    return self.session.query(Product).join(WishList, WishList.product_id == Product.id)\
      .filter(WishList.user_id == user_id)\
      .order_by(func.random()).first()

  def favorite_item(self, product_id, user_id):
    product = self.session.query(WishList) \
                          .filter(WishList.product_id == product_id, WishList.user_id == user_id) \
                          .all()

    if( len(product) == 0 ):
      try:
        new_list = WishList(user_id = user_id, status=False, product_id = product_id)
        self.session.add(new_list)

        self.session.commit()

        return {'msg': 'Product was followed!'}
      except IntegrityError:
        self.session.rollback()

        return {'msg': "Product wasn't fallowed!"}
  
    try:
      self.session.query(WishList) \
                  .filter(WishList.product_id == product_id, WishList.user_id == user_id) \
                  .delete()
      
      self.session.commit()

      return {'msg': 'Product was unfollowed'}
    except IntegrityError:
      self.session.rollback()

      return {'msg': "Product wasn't unfollowed"}