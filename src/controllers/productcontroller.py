from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, desc
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

  def update(self, product):
      '''
       This method updates the values referring to the product

       sess.query(User).filter(User.age == 25).\
            update({User.age: User.age - 10}, synchronize_session=False)
      '''
      try:
        self.session.query(Product) \
                    .join(WishList) \
                    .filter(Product.id == product.id) \
                    .update({
                      Product.title : product.title,
                      Product.desc : product.desc,
                      Product.uri : product.uri,
                      Product.img : product.img,
                      WishList.status : Product.status
                    })

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

  def get_id(self, user_id, list_size):
    query = self.session.query(Product.id) \
              .filter(Product.created_by == user_id) \
              .order_by(desc(Product.id)) \
              .limit(list_size).all()
    # select id from product where created_by = (user_id) order by id desc limit (n);
    '''
    SELECT product_id FROM product
            ORDER BY id DESC LIMIT n;
    '''
    return query
