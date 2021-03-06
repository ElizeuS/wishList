from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Column, Table, ForeignKey
from sqlalchemy import Integer, String
from sqlalchemy.sql.sqltypes import Boolean

Base = declarative_base()

class User(Base):
  __tablename__ = "user"

  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String, nullable=False)
  nickname = Column(String, nullable=False, unique=True)
  email = Column(String, nullable=False, unique=True)
  password = Column(String, nullable=False)

  def __repr__(self):
    return f"<User name={self.name}>"

class Product(Base):
  __tablename__ = "product"

  id = Column(Integer, primary_key=True, autoincrement=True)
  title = Column(String, nullable=False)
  desc = Column(String, nullable=True)
  uri = Column(String, nullable=True)
  img = Column(String, nullable=True)
  created_by = Column(Integer, nullable=False)

  def __repr__(self):
      return f"<Product title={self.title}, desc={self.desc}, uri={self.uri}, img={self.img}, created_by={self.created_by}>"

class WishList(Base):
  __tablename__= "wishlist"

  id = Column(Integer, primary_key=True, autoincrement=True)
  user_id = Column(Integer, ForeignKey('user.id', ondelete="CASCADE"))
  product_id = Column(Integer, ForeignKey('product.id', ondelete="CASCADE"))
  status = Column(Boolean, nullable=False)


  def __repr__(self):
      return f"<WishList status={self.status}>"