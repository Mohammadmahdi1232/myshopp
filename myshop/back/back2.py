from functools import wraps
import json
import os
import dateutil.parser
from werkzeug.utils import secure_filename
from flask_cors import CORS
from sqlalchemy import func
from decimal import Decimal
from flask import Flask,render_template
from flask import request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import send_file
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
from flask import make_response
from sqlalchemy import or_, and_,desc, asc
from model import db, Customer, Products, Order, OrderDetail, Categories, Payment, ShippingAddress, Feedback, AdminLogs,Users
import uuid
import random
from sqlalchemy.orm import joinedload , subqueryload


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myshop.db'
db.init_app(app)

with app.app_context():
    db.create_all()

bcrypt = Bcrypt(app)

cors = CORS(app)



####################################################################Users###########################################################################
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({'error': 'not found'}), 404

    user_data = {
        'id': user.user_id,
        'username': user.username,
        'email': user.email,
         'role': user.role
    }
    return jsonify(user_data), 200





@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({'error': 'not found'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'deleted successfully', 'id': user_id}), 200







@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({'error': 'not found'}), 404

    data = request.get_json()
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.password_hash = data.get('password_hash', user.password_hash)
    user.role = data.get('role', user.role)
    db.session.commit()
    return jsonify({
        'id': user.user_id,
        'username': user.username,
        'email': user.email,
        'password_hash': user.password_hash,
        'role': user.role
    }), 200





@app.route('/users/register', methods=['POST'])
def register_user():
    data = request.json
    if not all(k in data and data[k] for k in ['username', 'password_hash', 'email', 'role']):
        return jsonify({'error': 'Missing data!'}), 400
    username = data['username']
    password_hash = data['password_hash']
    email = data['email']
    role = data['role']
    if Users.query.filter((Users.username == username) | (Users.email == email)).first():
        return jsonify({'error': 'already exists'}), 409
    new_user = Users(username=username, email=email, password_hash=password_hash, role=role)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'created successfully'}), 201





################################################################Customer#####################################################
@app.route('/Customer/<int:Customer_id>', methods=['GET'])
def get_Customer(Customer_id):
    cum = Customer.query.get(Customer_id)
    if not cum:
        return jsonify({'error': 'not found'}), 404

    Customer_data = {
        'Customer_id': cum.Customer_id,
        'username': cum.username,
        'email': cum.email,
        'phone_number': cum.phone_number,
        'registration_date': cum.registration_date
    }
    return jsonify(Customer_data), 200






@app.route('/Customer/<int:Customer_id>', methods=['DELETE'])
def delete_Customer(Customer_id):
    cum = Customer.query.get(Customer_id)
    if not cum:
        return jsonify({'error': 'not found'}), 404

    db.session.delete(cum)
    db.session.commit()
    return jsonify({'message': 'deleted successfully', 'id': Customer_id}), 200




@app.route('/Customer/<int:Customer_id>', methods=['PUT'])
def update_Customer(Customer_id):
    cmu = Customer.query.get(Customer_id)
    if not cmu:
        return jsonify({'error': 'not found'}), 404

    data = request.get_json()
    cmu.username = data.get('username', cmu.username)
    cmu.email = data.get('email', cmu.email)
    cmu.phone_number = data.get('phone_number', cmu.phone_number)
    db.session.commit()
    return jsonify({
        'Customer_id': cmu.Customer_id,
        'username': cmu.username,
        'email': cmu.email,
        'phone_number': cmu.phone_number,
        'registration_date': cmu.registration_date
    }), 200




@app.route('/Customer/register', methods=['POST'])
def register_Customer():
    data = request.json
    if not all(k in data and data[k] for k in [ 'username', 'email', 'phone_number','registration_date']):
        return jsonify({'error': 'Missing data!'}), 400
    username = data['username']
    email = data['email']
    phone_number = data['phone_number']
    registration_date = datetime.strptime(data['registration_date'], '%m-%d-%Y').date() 

    new_customer = Customer(username=username, email=email, phone_number=phone_number, registration_date=registration_date)
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'created successfully'}), 201


###########################################################feedback###############################################################
@app.route('/feedback/<int:feedback_id>', methods=['GET'])
def get_feedback(feedback_id):
    fid = Feedback.query.get(feedback_id)
    if not fid:
        return jsonify({'error': 'not found'}), 404

    feedback_data = {
        'feedback_id':fid.feedback_id,
        'Customer_id': fid.Customer_id,
        'order_id': fid.order_id,
        'rating': fid.rating,
        'comment': fid.comment,
        'feedback_date': fid.feedback_date
    }
    return jsonify(feedback_data), 200




@app.route('/feedback/<int:feedback_id>', methods=['DELETE'])
def delete_feedback(feedback_id):
    fid = Feedback.query.get(feedback_id)
    if not fid:
        return jsonify({'error': 'not found'}), 404

    db.session.delete(fid)
    db.session.commit()
    return jsonify({'message': 'deleted successfully', 'id': feedback_id}), 200





@app.route('/feedback/<int:feedback_id>', methods=['PUT'])
def update_feedback(feedback_id):
    fid = Feedback.query.get(feedback_id)
    if not fid:
        return jsonify({'error': 'not found'}), 404

    data = request.get_json()
    fid.Customer_id = data.get('Customer_id', fid.Customer_id)
    fid.order_id = data.get('order_id', fid.order_id)
    fid.rating = data.get('rating', fid.rating)
    fid.comment = data.get('comment', fid.comment)
    fid.feedback_date = data.get('feedback_date', fid.feedback_date)
    db.session.commit()
    return jsonify({
        'feedback_id': fid.feedback_id,
        'Customer_id': fid.Customer_id,
        'order_id': fid.order_id,
        'rating': fid.rating,
        'comment': fid.comment,
        'feedback_date' : fid.feedback_date
    }), 200







@app.route('/feedback/register', methods=['POST'])
def register_feedback():
    data = request.json
    if not all(k in data and data[k] for k in [ 'Customer_id', 'order_id', 'rating','comment','feedback_date']):
        return jsonify({'error': 'Missing data!'}), 400
    order_id = data['order_id']
    rating = data['rating']
    comment = data['comment']
    Feedback_date = datetime.strptime(data['registration_date'], '%m-%d-%Y').date() 
    

    new_feedback = Feedback_date(order_id=order_id, rating=rating, comment=comment , Feedback_date=Feedback_date)
    db.session.add(new_feedback)
    db.session.commit()
    return jsonify({'message': 'created successfully'}), 201


###########################################################adminLogs###############################################################

@app.route('/AdminLogs/<int:log_id>', methods=['GET'])
def get_AdminLogs(log_id):
    adLog = AdminLogs.query.get(log_id)
    if not adLog:
        return jsonify({'error': 'not found'}), 404

    AdminLogs_data = {
        'log_id': adLog.log_id,
        'Customer_id': adLog.Customer_id,
        'action': adLog.action,
        'action_date': adLog.action_date,
        'ip_address': adLog.ip_address,
    }
    return jsonify(AdminLogs_data), 200




@app.route('/AdminLogs/<int:log_id>', methods=['DELETE'])
def delete_AdminLogs(log_id):
    adLog = AdminLogs.query.get(log_id)
    if not adLog:
        return jsonify({'error': 'not found'}), 404

    db.session.delete(adLog)
    db.session.commit()
    return jsonify({'message': 'deleted successfully', 'id': log_id}), 200





@app.route('/AdminLogs/<int:log_id>', methods=['PUT'])
def update_Customer(log_id):
    adLog = AdminLogs.query.get(log_id)
    if not adLog:
        return jsonify({'error': 'not found'}), 404

    data = request.get_json()
    adLog.Customer_id = data.get('Customer_id', adLog.Customer_id)
    adLog.action = data.get('action', adLog.action)
    adLog.action_date = data.get('action_date', adLog.action_date)
    adLog.ip_address = data.get('ip_address', adLog.ip_address)
    db.session.commit()
    return jsonify({
        'Customer_id': adLog.Customer_id,
        'action': adLog.action,
        'action_date': adLog.action_date,
        'ip_address': adLog.ip_address,
    }), 200






@app.route('/AdminLogs/register', methods=['POST'])
def register_AdminLogs():
    data = request.json
    if not all(k in data and data[k] for k in [ 'Customer_id', 'action', 'action_date','ip_address']):
        return jsonify({'error': 'Missing data!'}), 400
    Customer_id = data['Customer_id']
    action = data['action']
    ip_address = data['ip_address']
    action_date = datetime.strptime(data['action_date'], '%m-%d-%Y').date() 

    new_AdminLogs = Customer(Customer_id=Customer_id, action=action, ip_address=ip_address, action_date=action_date)
    db.session.add(new_AdminLogs)
    db.session.commit()
    return jsonify({'message': 'created successfully'}), 201

########################################################################Categories######################################################################
@app.route('/Categories/<int:category_id>', methods=['GET'])
def get_Categories(category_id):
    cat = Categories.query.get(category_id)
    if not cat:
        return jsonify({'error': 'not found'}), 404

    Categories_data = {
        'category_id': cat.category_id,
        'name': cat.name,
        'description': cat.description,
        'parent_category_id': cat.parent_category_id,
        'created_at': cat.created_at
    }
    return jsonify(Categories_data), 200



@app.route('/Categories/<int:category_id>', methods=['DELETE'])
def delete_Categories(category_id):
    cat = Categories.query.get(category_id)
    if not cat:
        return jsonify({'error': 'not found'}), 404

    db.session.delete(cat)
    db.session.commit()
    return jsonify({'message': 'deleted successfully', 'id': category_id}), 200



@app.route('/Categories/<int:category_id>', methods=['PUT'])
def update_Categories(category_id):
    cmu = Categories.query.get(category_id)
    if not cmu:
        return jsonify({'error': 'not found'}), 404

    data = request.get_json()
    cmu.name = data.get('name', cmu.name)
    cmu.description = data.get('description', cmu.description)
    cmu.parent_category_id = data.get('parent_category_id', cmu.parent_category_id)
    cmu.created_at = data.get('created_at', cmu.created_at)
    db.session.commit()
    return jsonify({
        'category_id': cmu.category_id,
        'name': cmu.name,
        'description': cmu.description,
        'parent_category_id': cmu.parent_category_id,
        'created_at': cmu.created_at
    }), 200






@app.route('/Categories/register', methods=['POST'])
def register_Categories():
    data = request.json
    if not all(k in data and data[k] for k in [ 'name', 'description', 'parent_category_id','created_at']):
        return jsonify({'error': 'Missing data!'}), 400
    name = data['name']
    description = data['description']
    parent_category_id = data['parent_category_id']
    created_at = data['created_at']
    # registration_date = datetime.strptime(data['registration_date'], '%m-%d-%Y').date() 

    new_Categories = Customer(name=name, description=description, parent_category_id=parent_category_id, created_at=created_at)
    db.session.add(new_Categories)
    db.session.commit()
    return jsonify({'message': 'created successfully'}), 201

#################################################################OrderDetails#####################################################

@app.route('/OrderDetails/<int:order_detail_id>', methods=['GET'])
def get_OrderDetails(order_detail_id):
    cum = Customer.query.get(order_detail_id)
    if not cum:
        return jsonify({'error': 'not found'}), 404

    OrderDetails_data = {
        'order_detail_id': cum.order_detail_id,
        'order_id': cum.order_id,
        'product_id': cum.product_id,
        'quantity': cum.quantity,
        'unit_price': cum.unit_price
    }
    return jsonify(OrderDetails_data), 200



@app.route('/OrderDetails/<int:order_detail_id>', methods=['DELETE'])
def delete_OrderDetails(order_detail_id):
    cum = OrderDetail.query.get(order_detail_id)
    if not cum:
        return jsonify({'error': 'not found'}), 404

    db.session.delete(cum)
    db.session.commit()
    return jsonify({'message': 'deleted successfully', 'id': order_detail_id}), 200



@app.route('/OrderDetails/<int:order_detail_id>', methods=['PUT'])
def update_OrderDetails(order_detail_id):
    cmu = OrderDetail.query.get(order_detail_id)
    if not cmu:
        return jsonify({'error': 'not found'}), 404

    data = request.get_json()
    cmu.order_id = data.get('order_id', cmu.order_id)
    cmu.product_id = data.get('product_id', cmu.product_id)
    cmu.quantity = data.get('quantity', cmu.quantity)
    cmu.unit_price = data.get('unit_price', cmu.unit_price)
    db.session.commit()
    return jsonify({
        'order_detail_id': cmu.order_detail_id,
        'order_id': cmu.order_id,
        'product_id': cmu.product_id,
        'quantity': cmu.quantity,
        'unit_price': cmu.unit_price
    }), 200



@app.route('/OrderDetails/register', methods=['POST'])
def register_OrderDetails():
    data = request.json
    if not all(k in data and data[k] for k in [ 'order_id', 'product_id', 'quantity','unit_price']):
        return jsonify({'error': 'Missing data!'}), 400
    order_id = data['order_id']
    product_id = data['product_id']
    quantity = data['quantity']
    unit_price = data['unit_price']
    # registration_date = datetime.strptime(data['registration_date'], '%m-%d-%Y').date() 

    new_customer = Customer(order_id=order_id, product_id=product_id, quantity=quantity, unit_price=unit_price)
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'created successfully'}), 201





##################################################################Orders#####################################
@app.route('/Orders/<int:order_id>', methods=['GET'])
def get_Customer(order_id):
    cum = Order.query.get(order_id)
    if not cum:
        return jsonify({'error': 'not found'}), 404

    Customer_data = {
        'order_id': cum.order_id,
        'Customer_id': cum.Customer_id,
        'order_date': cum.order_date,
        'total_amount': cum.total_amount,
        'status': cum.status
    }
    return jsonify(Customer_data), 200



@app.route('/Orders/<int:order_id>', methods=['DELETE'])
def delete_Customer(order_id):
    cum = Order.query.get(order_id)
    if not cum:
        return jsonify({'error': 'not found'}), 404

    db.session.delete(cum)
    db.session.commit()
    return jsonify({'message': 'deleted successfully', 'id': order_id}), 200


@app.route('/Orders/<int:order_id>', methods=['PUT'])
def update_Orders(order_id):
    cmu = Order.query.get(order_id)
    if not cmu:
        return jsonify({'error': 'not found'}), 404

    data = request.get_json()
    cmu.username = data.get('username', cmu.username)
    cmu.email = data.get('email', cmu.email)
    cmu.phone_number = data.get('phone_number', cmu.phone_number)
    db.session.commit()
    return jsonify({
        'order_id': cmu.order_id,
        'Customer_id': cmu.Customer_id,
        'order_date': cmu.order_date,
        'total_amount': cmu.total_amount,
        'status': cmu.status
    }), 200



@app.route('/Orders/register', methods=['POST'])
def register_Orders():
    data = request.json
    if not all(k in data and data[k] for k in [ 'Customer_id', 'order_date', 'total_amount','status']):
        return jsonify({'error': 'Missing data!'}), 400
    Customer_id = data['Customer_id']
    order_date = data['order_date']
    total_amount = data['total_amount']
    status = data['status']
    # registration_date = datetime.strptime(data['registration_date'], '%m-%d-%Y').date() 

    new_customer = Customer(Customer_id=Customer_id, order_date=order_date, total_amount=total_amount, status=status)
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'created successfully'}), 201


#payments

@app.route('/payments/<int:payment_id>', methods=['DELETE'])
def delete_Customer(payment_id):
    cum = Payment.query.get(payment_id)
    if not cum:
        return jsonify({'error': 'not found'}), 404

    db.session.delete(cum)
    db.session.commit()
    return jsonify({'message': 'deleted successfully', 'id': payment_id}), 200

#product
@app.route('/Product/<int:product_id>', methods=['DELETE'])
def delete_Customer(product_id):
    cum = Products.query.get(product_id)
    if not cum:
        return jsonify({'error': 'not found'}), 404

    db.session.delete(cum)
    db.session.commit()
    return jsonify({'message': 'deleted successfully', 'id': product_id}), 200

#shiping_address
@app.route('/shippingAddresses/<int:address_id>', methods=['DELETE'])
def delete_Customer(address_id):
    cum = ShippingAddress.query.get(address_id)
    if not cum:
        return jsonify({'error': 'not found'}), 404

    db.session.delete(cum)
    db.session.commit()
    return jsonify({'message': 'deleted successfully', 'id': address_id}), 200














if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
