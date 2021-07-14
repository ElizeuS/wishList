from sqlalchemy.exc import IntegrityError

from src.database.database import sessionLocal
from src.database.schemas import Product

class ProductController:

  def __init__(self):
    self.session = sessionLocal()

  def index(self):
    query = self.session.query(Product.id, Product.title, Product.desc).all()

    return query

  def create(self, product):
    product_list = []
    for pro_n in product:
      product_list.append(Product(
        title = pro_n.title,
        desc = pro_n.desc,
        uri = pro_n.uri,
        img = pro_n.img
        )
      )

    try:
      self.session.add_all(product_list)
      # self.session.add(new_product)
      self.session.commit()

      #self.session.refresh(new_product)
    except IntegrityError:
      self.session.rollback()

      return {'msg': 'Error'}

    # return {"product_id": new_product.id}
    return {'msg': 'nice'}