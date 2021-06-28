import unittest

from src.models.product import Product

class ProductTest(unittest.TestCase):

  def test_create_product(self):
    self.assertEqual(Product('Xiaomi', 'Very fast', 'http', 'page.jpg').name, 'Xiaomi')

