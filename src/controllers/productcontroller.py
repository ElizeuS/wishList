from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_
from fastapi import HTTPException
from src.database.database import sessionLocal
from src.database.schemas import Product, WishList

from sqlalchemy.sql import insert
'''
result = conn.execute("INSERT INTO user (name, country_id) VALUES ('Homer', 123)
                        RETURNING id")
[new_id] = result.fetchone()
'''
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
      #query = insert(table=Product, values=product_list)
      self.session.add_all(product_list)
      self.session.commit()
      #print(self.get_id(product_list))
    except IntegrityError:
      self.session.rollback()

      return {'msg': 'User was created'}

    # return {"product_id": new_product.id}

    return {'msg': 'product_list'}

  def update(self, product):
      '''
       This method updates the values referring to the product
      '''
      try:
        self.session.query(Product).filter(Product.id == product.id).update(product)
        self.session.commit()
      except:
        self.session.rollback()

      return {"msg": f"product with id {product.id} was updated"}

  def delete(self, product, user_id):
      '''
       This method delete to the product
      '''
      try:
        self.session.query(WishList).where(
          and_(
                      WishList.product_id == product.id,
                      WishList.user_id == user_id
                  )
        ).delete()
        self.session.commit()

        if self.session.query(WishList).filter(WishList.product_id == product.id) is None:
           self.session.query(Product).filter(Product.id == product.id).delete()
           self.session.commit()

      except:
        return HTTPException(status_code=404, detail="Item not found")

      return {"msg": self.session.query(Product).filter(Product.id == product.id).one_or_none()}

  def get_id(self, product):
    # select id from product where created_by = (user_id) sort id desc limit (n);
    '''
    SELECT product_id FROM product
            ORDER BY 1 DESC LIMIT n;
    '''
    return self.session.query(Product).find_by(product)
