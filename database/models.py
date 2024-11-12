from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database.connect import Base

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, unique=True)
    img = Column(Text)
    name = Column(Text)
    description = Column(Text)
    price = Column(Integer)
    category_id = Column(Integer, ForeignKey('categories.category_id'))
    availability = Column(Integer)

    # Связь с категорией
    category = relationship('Category', back_populates='products')

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

    # Связь с корзиной и заказами
    carts = relationship('Cart', back_populates='user', cascade='all, delete-orphan')
    orders = relationship('OrdersUser', back_populates='user', cascade='all, delete-orphan')

class Cart(Base):
    __tablename__ = 'cart'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer)
    count = Column(Integer)

    # Связь с пользователем
    user = relationship('User', back_populates='carts')

class Category(Base):
    __tablename__ = 'categories'
    
    category_name = Column(Text)
    category_id = Column(Integer, primary_key=True)
    availability_cat = Column(Integer)

    # Связь с продуктами
    products = relationship('Product', back_populates='category', cascade='all, delete-orphan')

class OrdersUser(Base):
    __tablename__ = 'orders_user'
    
    id = Column(Integer, primary_key=True)
    id_order = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    cart = Column(Text)
    order_date = Column(Text)
    receiving = Column(Text)
    status = Column(Text)
    payment = Column(Text)
    commentary = Column(Text)

    # Связь с пользователем
    user = relationship('User', back_populates='orders')