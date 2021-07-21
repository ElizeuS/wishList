from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from src.database.database import sessionLocal
from src.database.schemas import WishList, Product, User

class WishListController:

  def __init__(self):
    self.session = sessionLocal()

  def index(self, user_id):
    result = self.session.query(WishList).filter(WishList.user_id == user_id).all()

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
    result = self.session.query(WishList.status, Product) \
          .join(Product, WishList.product_id == Product.id) \
          .join(User, WishList.user_id == User.id) \
          .filter(User.nickname == nickname) \
          .all()

    return result