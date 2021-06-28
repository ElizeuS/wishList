from models.wishlist import WishList
from models.product import Product

p = Product('Xiaomi', 'Very fast', 'http', 'page.jpg')
wish = WishList('Elizeu')
wish.add_to_cart(p)

print(wish.get_products())