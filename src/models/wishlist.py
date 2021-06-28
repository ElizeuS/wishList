#from src.models.product import Product

class WishList():

  def __init__(self, name):
    self.id = 0
    self.name = name
    self.products = []

  def add_to_cart(self, product):
    if( product not in self.products ):
      self.products.append(product)

      return product.id

    return False

  def remove_to_card(self, product):
    return self.products.remove(product)

  def get_products(self):
    return self.products


