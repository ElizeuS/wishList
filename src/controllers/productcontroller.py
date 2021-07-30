from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, desc, update
from fastapi import HTTPException
from src.database.database import sessionLocal
from src.database.schemas import Product, WishList

from sqlalchemy.sql import insert

class ProductController:

  def __init__(self):
    self.session = sessionLocal()

  def index(self):
    query = self.session.query(Product.id, Product.title, Product.desc).all()

    return query

  def create(self, products, created_by):
    product_list = []
    refresh_list = []
    for pro_n in products:
      product_list.append(Product(
        title = pro_n.title,
        desc = pro_n.desc,
        uri = pro_n.uri,
        img = pro_n.img,
        created_by = created_by
        )
      )

    try:
      self.session.add_all(product_list)
      self.session.commit()
      size = len(product_list)
    except IntegrityError:
      self.session.rollback()

      return {'msg': "Products have not been created"}

    return self.get_id(created_by, size)

  def search_by_body(self, product, user_id):
      result = self.session.query(Product.id) \
        .where(Product.title == product.title,
                      Product.desc == product.desc,
                      Product.uri == product.uri,
                      Product.img == product.img,
                      Product.created_by == user_id).first()

      return result

  def update(self, product, user_id, product_id):
      try:

        stmt = update(Product).where(Product.id == product_id).values({'title':product.title, 'desc':product.desc,
                                                                        'uri': product.uri, 'img': product.img})

        stmt2 = update(WishList).where(WishList.product_id == product_id).values({'status': bool(product.status)})
        self.session.execute(stmt)
        self.session.execute(stmt2)
        self.session.commit()
      except:
        self.session.rollback()
        return {"msg": "Não atualizou"}

      return {"msg": "product was updated"}
      #return result

  def delete(self, product_id, user_id):
      '''
       This method delete to the product
      '''
      try:
        self.session.query(WishList).where(
          and_(
                      WishList.product_id == product_id,
                      WishList.user_id == user_id
                  )
        ).delete()
        self.session.commit()

        if self.session.query(WishList).filter(WishList.product_id == product_id) is None:
           self.session.query(Product).filter(Product.id == product_id).delete()
           self.session.commit()

      except:
        return HTTPException(status_code=404, detail="Item not found")

      return {"msg": self.session.query(Product).filter(Product.id == product_id).one_or_none()}

  def get_id(self, user_id, list_size):
    query = self.session.query(Product.id) \
              .filter(Product.created_by == user_id) \
              .order_by(desc(Product.id)) \
              .limit(list_size).all()

    return query

  def get_products_owned(self, user_id):
    return self.session.query(Product, WishList) \
                      .join(WishList, WishList.product_id == Product.id) \
                      .filter(WishList.user_id == user_id, WishList.status == True).all()
