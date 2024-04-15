from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Customer(db.Model):
    __tablename__ = 'Customer'
    Customer_id = db.Column(db.Integer,unique=True, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    registration_date = db.Column(db.Date, nullable=False)


class Products(db.Model):
    __tablename__ = 'Products'
    Products_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.DECIMAL(10, 2), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('Categories.category_id'), nullable=False)

class Order(db.Model):
    __tablename__ = 'Orders'
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Customer_id = db.Column(db.Integer, db.ForeignKey('Customer.Customer_id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False)
    total_amount = db.Column(db.DECIMAL(10, 2), nullable=False)
    status = db.Column(db.String(20), nullable=False)

class OrderDetail(db.Model):
    __tablename__ = 'OrderDetails'
    order_detail_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('Orders.order_id'), nullable=False)
    Products_id = db.Column(db.Integer, db.ForeignKey('Products.Products_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.DECIMAL(10, 2), nullable=False)

class Categories(db.Model):
    __tablename__ = 'Categories'  # Define the table name explicitly
    category_id = db.Column(db.Integer,unique=True, primary_key=True,autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    parent_category_id = db.Column(db.Integer, db.ForeignKey('Categories.category_id'))
    created_at = db.Column(db.DateTime, nullable=False)


class Payment(db.Model):
    __tablename__ = 'Payments'   
    payment_id = db.Column(db.Integer,unique=True, primary_key=True,autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('Orders.order_id'), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.DECIMAL(10, 2), nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False)


class ShippingAddress(db.Model):
    __tablename__ = 'ShippingAddresses'
    address_id = db.Column(db.Integer,unique=True, primary_key=True,autoincrement=True)
    Customer_id = db.Column(db.Integer, db.ForeignKey('Customer.Customer_id'), nullable=False)
    recipient_name = db.Column(db.String(100), nullable=False)
    address_line1 = db.Column(db.String(255), nullable=False)
    address_line2 = db.Column(db.String(255))
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(100), nullable=False)

class Feedback(db.Model):
    feedback_id = db.Column(db.Integer,unique=True, primary_key=True,autoincrement=True)
    Customer_id = db.Column(db.Integer, db.ForeignKey('Customer.Customer_id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('Orders.order_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    feedback_date = db.Column(db.DateTime, nullable=False)

class AdminLogs(db.Model):
    __tablename__ = 'AdminLogs'
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Customer_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    action_date = db.Column(db.DateTime, nullable=False)
    ip_address = db.Column(db.String(50), nullable=False)

class Users(db.Model):
    __tablename__ = 'Users'
    user_id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    username=db.Column(db.String(50), nullable=False)
    password_hash=db.Column(db.String(100), nullable=False)
    email=db.Column(db.String(100), nullable=False)
    role=db.Column(db.String(20), nullable=False)