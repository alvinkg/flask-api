from flask import Flask, request, json, jsonify
# , render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, DateTime
import os
import psycopg2
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
from flask_cors import CORS

from flask_jwt_extended import create_access_token, create_refresh_token

# Use this if we don't connect via SQLAlchemy
# print(dotenv_path)
# https://dev.to/jakewitcher/using-env-files-for-environment-variables-in-python-applications-55a1
# dotenv_path = Path('../.env-remote')
load_dotenv('../.env-local') # can use the var dotenv_path, # take environment variables from .env.
url = os.getenv("SQLALCHEMY_DATABASE_URI")
print('url:', url)
connection = psycopg2.connect(url)

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# import env var from settings.py, in turn from .env
# app.config.from_pyfile('/Users/alvinlim/Documents/Code/baby-tracker/settings.py')
# app.config.get('SQLALCHEMY_DATABASE_URI')

app.config['SQLALCHEMY_DATABASE_URI']= url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# instantiate cors
CORS(app)

class Cart(db.Model):
    cartId = db.Column(db.Integer, primary_key=True)
    purchased = db.Column(db.Boolean)
    id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # used for debugging to give string representation of obj
    def __repr__(self):
        return f'Cart: {self.cartId, self.purchased}'
    
    def __init__(self, sessionID, purchased): #
        self.cartID = sessionID
        self.purchased = purchased

# Takes entry and passes it jsonified to the FE
def format_cart(cart):
    return {
        "cartId": cart.id,
        "created_at": cart.created_at
    }

@app.route('/cart', methods=['POST'])
def create_cart():
    #1 Grab the params from the request & assign to var
    title = request.json['title']
    price = request.json['price']
    
    # instan Cart? obj
    cart = Cart(title,price)
    db.session.add(cart)
    db.session.commit()
    return format_cart(cart)

@app.route('/carts', methods=['GET'])
def get_carts():
    carts = Cart.query.order_by(Cart.created_at.asc()).all() # Cart.id.asc()
    cart_list = []
    for cart in carts:
        cart_list.append(format_cart(cart))
    return {'cart': cart_list}

# @app.route('/products/<id>', methods=['GET'])
# def get_product(id):
#     product = Product.query.filter_by(id=id).one()
#     formatted_product = format_product(product)
#     return {'product': formatted_product}

# @app.route('/products/<id>', methods=['DELETE'])
# def delete_product(id):
#     product = Product.query.filter_by(id=id).one()
#     db.session.delete(product)
#     db.session.commit()
#     return f"Product {id} has been deleted successfully."
    # formatted_event = format_event(event)
    # return {'event': formatted_event}


#####################################

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # used for debugging to give string representation of obj
    def __repr__(self):
        return f'Product: {self.title}'
    
    def __init__(self, title, price, image): #
        self.title = title
        self.price = price
        self.image = image

# Takes entry and passes it jsonified to the FE
def format_product(product):
    return {
        "title": product.title,
        "id": product.id,
        "price": product.price,
        "image": product.image,
        "created_at": product.created_at
    }

@app.route('/product', methods=['POST'])
def create_product():
    #1 Grab the params from the request & assign to var
    title = request.json['title']
    price = request.json['price']
    image = request.json['image']
    
    # instan Cart? obj
    product = Product(title,price,image)
    db.session.add(product)
    db.session.commit()
    return format_product(product)

@app.route('/products/<id>', methods=['PUT'])
def update_product(id):
    # #1 Grab the params from the request & assign to vars
    # description = request.json['description']
    # #2 inst event obj from db
    # event = Event.query.get(id)
    # #3 update the event obj
    # event.description = description
    # #4 commit changes
    # db.session.commit()
    # #5 return serialized/formatted obj
    # return  {'event': format_event(event)}

    # Option 2
    #1 Grab the params from the request & assign to vars
    title = request.json['title']
    price = request.json['price']
    image = request.json['image']
    #2 gets obj as a list
    product = Product.query.filter_by(id=id)
    #3 update the event obj with vars
    product.update(dict(title=title,price=price,image=image,created_at=datetime.utcnow()))
     # #4 commit changes
    db.session.commit()
    #5 return serialized/formatted obj
    return {'product': format_product(product.one())}

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.order_by(Product.created_at.asc()).all() # Cart.id.asc()
    product_list = []
    for product in products:
        product_list.append(format_product(product))
    return {'products': product_list}

@app.route('/products/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.filter_by(id=id).one()
    formatted_product = format_product(product)
    return {'product': formatted_product}

@app.route('/products/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.filter_by(id=id).one()
    db.session.delete(product)
    db.session.commit()
    return f"Product {id} has been deleted successfully."
    # formatted_event = format_event(event)
    # return {'event': formatted_event}


#####################################
    
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'Event: {self.description}'
    
    def __init__(self, description):
        self.description = description
        
def format_event(event):
    return {
        "description": event.description,
        "id": event.id,
        "created_at": event.created_at
    }
        
@app.route('/')
def hello():
    # return render_template('index.html')
    # access_token = create_access_token()
    # return jsonify(message='password exists.')
    response = jsonify(message='success') #,access_token=access_token
    return response, 201

# create an event
@app.route('/events', methods=['POST'])
def create_event():
    #1 Grab the params from the request & assign to var
    description = request.json['description']
    # instan Event obj
    event = Event(description)
    db.session.add(event)
    db.session.commit()
    return format_event(event)

# get all events
@app.route('/events', methods=['GET'])
def get_events():
    # order by created_at / id
    events = Event.query.order_by(Event.id.asc()).all()
    # events = Event.query.order_by(Event.created_at.desc()).all()

    # create empty event list
    event_list = []
    for event in events:
        # append each event to the list
        event_list.append(format_event(event))
    return {'events': event_list}

# get single event
@app.route('/events/<id>', methods=['GET'])
def get_event(id):
    event = Event.query.filter_by(id=id).one()
    formatted_event = format_event(event)
    return {'event': formatted_event}

# delete an event by id
@app.route('/events/<id>', methods=['DELETE'])
def delete_event(id):
    event = Event.query.filter_by(id=id).one()
    db.session.delete(event)
    db.session.commit()
    return f"Event {id} has been deleted successfully."

# edit an event with id  
@app.route('/events/<id>', methods=['PUT'])
def update_event(id):
    # Option 2
    #1 Grab the event by id
    event = Event.query.filter_by(id=id)
    #2 gets description
    description = request.json['description']
    #3 update the event obj with description
    event.update(dict(description=description, created_at=datetime.utcnow()))
     # #4 commit changes
    db.session.commit()
    #5 return serialized/formatted obj
    return {'event': format_event(event.one())}

    # #1 Grab the params from the request & assign to vars
    # description = request.json['description']
    # #2 inst event obj from db
    # event = Event.query.get(id)
    # #3 update the event obj
    # event.description = description
    # #4 commit changes
    # db.session.commit()
    # #5 return serialized/formatted obj
    # return  {'event': format_event(event)}


#####################################

with app.app_context():
#     from app import db
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
    