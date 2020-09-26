from database.models import Customer
from database.beginning import db_session

def create_customer(username, password, rfid_tag):
    c = Customer(
        username=username,
        password=password,
        rfid_tag=rfid_tag
    )
    db_session.add(c)
    db_session.commit()

def fetch_customers():
    customers = []
    for customer in Customer.query.all():
        c = {
            "username": customer.username,
            "password": customer.password,
            "rfid_tag": customer.rfid_tag
        }
        customers.append(c)
    return customers
