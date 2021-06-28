import sys
sys.setrecursionlimit(1500)

class Product():

  def __init__(self, title, description, link, image_name):
    self.id = 0
    self.title = title
    self.description = description
    self.link = link
    self.image_name = image_name

  def get_id(self):
    return self._id

  def set_id(self, new_id):
    self._id = new_id

  def get_title(self):
    return self.title

  def set_title(self, new_title):
    self.title = new_title

  def get_description(self):
    return self.description

  def set_description(self, new_description):
    self.description = new_description

  def get_link(self):
    return self.link

  def set_link(self, new_link):
    self.link = new_link

  def get_image_name(self):
    return self.image_name

  def set_image_name(self, new_image_name):
    self.image_name = new_image_name


  id = property(fget=get_id, fset=set_id)
  title = property(fget=get_title, fset=set_title)
  description = property(fget=get_description, fset=set_description)
  link = property(fget=get_link, fset=set_link)
  image_name = property(fget=get_image_name, fset=set_image_name)