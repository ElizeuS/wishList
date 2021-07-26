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

  """
  [
  {
    "id": 2,
    "status": false,
    "Product": {
      "id": 2,
      "desc": null,
      "img": "https://a-static.mlcdn.com.br/1500x1500/quarto-de-bebe-com-guarda-roupa-3-portas-comoda-e-berco-faz-de-conta-espresso-moveis-branco-rustico/madeiramadeira-openapi/517184/285420addfba945e9948d27ac953b8b8.jpg",
      "uri": "https://www.magazineluiza.com.br/quarto-de-bebe-com-guarda-roupa-3-portas-comoda-e-berco-faz-de-conta-espresso-moveis-branco-rustico/p/bg2c7g4gf2/mo/qdbc/",
      "title": "Quarto de Bebê com Guarda Roupa 3 Portas Cômoda e Berço Faz de Conta Espresso Móveis Branco/Rústico",
      "created_by": 3
    }
  }
]
  """