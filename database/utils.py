import uuid
from sqlalchemy import update
from database.models import Employee, Customer, Product, CartItem, Tap
from database.beginning import db_session
from datetime import datetime

# Customer Methods

# returns product_id
def most_recent_product_tap():
    # datetime note: do newest - oldest
    current_time = datetime.now()
    product_tags = []
    taps = Tap.query.all()
    taps.reverse()  # newest taps first
    for tap in taps:
        if tap.rfid_tag in product_tags:
            tap_time = tap.time_created
            diff = current_time - tap_time
            seconds_passed = diff.total_seconds()
            if seconds_passed < 4:
                # lookup product with this tag
                p = Product.query.filter(rfid_tag=tap.rfid_tag).first()
                return p.id
    return None

# checks database for customer tap
# if none found or most recent is longer
# than X seconds, returns None
def most_recent_customer():
    # datetime note: do newest - oldest
    current_time = datetime.now()
    customer_tags = []
    taps = Tap.query.all()
    taps.reverse()  # newest taps first
    for tap in taps:
        if tap.rfid_tag in customer_tags:
            tap_time = tap.time_created
            diff = current_time - tap_time
            seconds_passed = diff.total_seconds()
            if seconds_passed < 4:
                # lookup customer with this tag
                c = Customer.query.filter(rfid_tag=tap.rfid_tag).first()
                return c.id
    return None


def add_one_to_inventory(product_id):
    product = Product.query.filter(id=product_id).first()
    product.stock_qty = product.stock_qty + 1
    db_session.commit()

def remove_one_from_inventory(product_id):
    product = Product.query.filter(id=product_id).first()
    product.stock_qty = product.stock_qty - 1
    db_session.commit()

def remove_one_from_cart(customer_id, product_id):
    if in_cart(customer_id, product_id):
        cart_item = CartItem.query.filter(customer_id == customer_id, product_id == product_id).first()
        existing_qty = cart_item.qty
        if existing_qty == 1:
            db_session.delete(cart_item)
            db_session.commit()
        else:
            cart_item.qty = cart_item.qty - 1
            db_session.commit()

def add_one_to_cart(customer_id, product_id):
    if in_cart(customer_id, product_id):
        cart_item = CartItem.query.filter(product_id == product_id, customer_id == customer_id).first()
        cart_item.qty = cart_item.qty + 1
        db_session.commit()
    else:
        cart_item = CartItem(product_id=product_id, customer_id=customer_id, qty=1)
        db_session.add(cart_item)
        db_session.commit()

def in_cart(customer_id, product_id):
    customer = Customer.query.filter(id == customer_id).first()
    result = customer.cartitems.query.filter(product_id == product_id)
    return len(result) > 0

def post_tap_transaction(rfid_tag):
    tap = Tap(rfid_tag=rfid_tag)
    db_session.add(tap)
    db_session.commit()

# Customer Authentication

def customer_login(username, password):
    result = Customer.query.filter(Customer.username == username, Customer.password == password)
    if result and result.first():
        return result.first().id

def generate_customer_token(username):
    token = uuid.uuid4().hex
    db_session.query(Customer).filter(Customer.username == username).update({Customer.token: token})
    db_session.commit()
    return token 

def invalidate_customer_token(username):
    db_session.query(Customer).filter(Customer.username == username).update({Customer.token: None})
    db_session.commit()
    
def invalidate_all_customer_tokens():
    db_session.query(Customer).update({Customer.token: None})
    db_session.commit()

# Employee Authentication

def employee_login(username, password):
    result = Employee.query.filter(Employee.username == username, Employee.password == password)
    if result:
        return result.first().id

# Employee Methods

def get_inventory():
    inventory = []
    for p in Product.query.all():
        product = dict()
        product['name'] = p.name
        product['price'] = p.price
        product['qty'] = p.stock_qty
        inventory.append(product)
    return inventory

def product_as_dict(product_id):
    cart_item = dict()
    result = Product.query.filter(id == product_id).first()
    cart_item['name'] = result.name
    cart_item['price'] = result.price
    return cart_item

def get_cart(username):
    cart = []
    customer = Customer.query.filter(username == username).first()
    for ci in customer.cartitems:
        cart_item = product_as_dict(ci.product_id)
        cart_item['qty'] = ci.qty
        cart.append(cart_item)
    return cart
