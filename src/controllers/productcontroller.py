from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from src.database.database import sessionLocal
from src.database.schemas import Product

class ProductController:

  def __init__(self):
    self.session = sessionLocal()

  def index(self):
    query = self.session.query(Product.id, Product.title, Product.desc).all()

    return query

  def create(self, products):
    product_list = []
    for pro_n in products:
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

      return {'msg': 'User was created'}

    # return {"product_id": new_product.id}
    return {'msg': 'nice'}

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

def delete(self, product):
    '''
     This method delete to the product

     @TODO Corrigir método e implementar lógica de excluir item
    '''

    try:
      self.session.query(Product).filter(Product.id == product.id).delete()
      self.session.commit()
    except:
      return HTTPException(status_code=404, detail="Item not found")

    return {"msg": self.session.query(Product).filter(Product.id == product.id).one_or_none()}