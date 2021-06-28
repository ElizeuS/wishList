class User():

  def __init__(self, name, email, password):
    self.id = 0
    self.name = name
    self.email = email
    self.password = password

  def get_id(self):
    return self._id

  def set_id(self, new_id):
    self._id = new_id

  def get_email(self):
    return self.email

  def set_email(self, new_email):
    self.email = new_email

  def get_name(self):
    return self.name

  def set_name(self, new_name):
    self.name = new_name

  def get_password(self):
    return self.password

  def set_password(self, new_pass):
    self.password = new_pass


  id = property(fget=get_id, fset=set_id)
  name = property(fget=get_name, fset=set_name)
  email = property(fget=get_email, fset=set_email)
  password = property(fget=get_password, fset=set_password)
