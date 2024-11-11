from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, unique=True)
    img = Column(Text)
    name = Column(Text)
    description = Column(Text)
    price = Column(Integer)
    category_id = Column(Integer)
    availability = Column(Integer)

class Restaurant(Base):
    __tablename__ = 'restaurant'
    
    id = Column(Integer, primary_key=True)
    location_time = Column(Text)
    img = Column(Text)
    description = Column(Text)
    price_obtain = Column(Integer)
    limit_price = Column(Integer)
    availability = Column(Integer)
    availability_mess = Column(Text)

class Promotion(Base):
    __tablename__ = 'promotion'
    
    img = Column(Text)
    name = Column(String, primary_key=True)
    description = Column(Text)

class Anonce(Base):
    __tablename__ = 'anonce'
    
    img = Column(Text)
    description = Column(String, primary_key=True)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    name = Column(Text)
    phone_number = Column(Text)
    adress = Column(Text)
    commentary = Column(Text)
    tools_c = Column(Integer)
    obtaining = Column(Text)
    time_order = Column(Text)

class Cart(Base):
    __tablename__ = 'cart'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    product_id = Column(Integer)
    count = Column(Integer)

class Category(Base):
    __tablename__ = 'categories'
    
    category_name = Column(Text)
    category_id = Column(Integer, primary_key=True)
    availability_cat = Column(Integer)

class OrdersUser(Base):
    __tablename__ = 'orders_user'
    
    id = Column(Integer, primary_key=True)
    id_order = Column(Integer)
    user_id = Column(Integer)
    cart = Column(Text)
    order_date = Column(Text)
    receiving = Column(Text)
    status = Column(Text)
    payment = Column(Text)
    commentary = Column(Text)

