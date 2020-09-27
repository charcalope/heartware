from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.beginning import Base
from datetime import datetime


class Tap(Base):
    __tablename__ = 'taps'
    id = Column(Integer, primary_key=True)
    rfid_tag = Column(String(40), unique=True)
    time_created = Column(DateTime)

    def __init__(self, rfid_tag=None, time_created=None):
        self.rfid_tag = rfid_tag
        self.time_created = datetime.now()

    def __repr__(self):
        return str(f"{self.rfid_tag} tapped at {self.time_created}")


class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    rfid_tag = Column(String(40), unique=True)
    username = Column(String(50), unique=True)
    password = Column(String(40))
    token = Column(String(32), nullable=True)

    def __init__(self, username=None, password=None, rfid_tag=None):
        self.username = username
        self.password = password
        self.rfid_tag = rfid_tag

    def __repr__(self):
        return str(f"<Customer {self.username}>")


class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer,primary_key=True)
    username = Column(String(40), unique=True)
    password = Column(String(40))

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def __repr__(self):
        return str(f"<Employee {self.id}>")


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(40), unique=True)
    stock_qty = Column(Integer)
    price = Column(Float)
    rfid_tag = Column(String(40), unique=True)

    def __init__(self, name=None, stock_qty=None, price=None, rfid_tag=None):
        self.name = name
        self.stock_qty = stock_qty
        self.price = price
        self.rfid_tag = rfid_tag

    def __repr__(self):
        return str(f"<Product {self.name}>")


class CartItem(Base):
    __tablename__ = 'cartitems'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    customer_id = Column(Integer, ForeignKey('customers.id'))
    qty = Column(Integer)

    customer = relationship("Customer", back_populates="cartitems")

    def __init__(self, product_id=None, customer_id=None, qty=None):
        self.product_id = product_id
        self.customer_id = customer_id
        self.qty = qty

    def __repr__(self):
        return str(f"<Customer {self.customer_id} purchased {self.product_id} x {self.qty}>")


Customer.cartitems = relationship("CartItem", order_by=CartItem.id, back_populates="customer")
