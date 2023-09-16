"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Address, Customer, Driver, VehicleType, Products, Order
from api.utils import generate_sitemap, APIException
import re

 
# Define a function for
# for validating an Email
def check(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    # pass the regular expression
    # and the string into the fullmatch() method
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

api = Blueprint('api', __name__)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200


@api.route('/accounts/customer', methods=['POST'])
def create_driver():
    
    body = request.get_json()

    country = body.get("country", None)
    city = body.get("city", None)
    address = body.get("address", None)
    postal_code = body.get("postal_code", None)

    if city == None:
        return { "message": "city field is missing in request body" }, 400
    if address == None:
        return { "message": "address field is missing in request body" }, 400
    if country == None:
            return { "message": "country field is missing in request body" }, 400
    if postal_code == None:
        return { "message": "postal_code field is missing in request body" }, 400

    email = body.get("email", None)
    password = body.get("password", None)
    
    if email != None and password != None:

        if check(email) == False:
            return { "message" : "email format is invalid" }, 400

        try:
            new_address = Address(country=country, city=city, address=address, postal_code=postal_code)

            db.session.add(new_address) # Memoria Ram los querys a la BD

            new_customer = Customer(email=email, password=password, address=new_address)

            db.session.add(new_customer)

            db.session.commit() # Datos en la BD postgrest

            return new_customer.serialize(), 200

        except ValueError as error:

            return { "message " : "Ah ocurrido un error inesperado " + error} , 500
    else:
        return { "message" : "user fields missing in request body" }, 400

    
    return jsonify(body), 200


@api.route('/accounts/driver', methods=['POST'])
def create_customer():
    
    body = request.get_json()

    email = body.get("email", None)
    password = body.get("password", None)

    vehicle = body.get("vehicle", None)
    matricula = body.get("matricula", None)

    if email != None and password != None:

        if check(email) == False:
            return { "message" : "email format is invalid" }, 400

        try:

            if vehicle == 'moto':
                new_driver = Driver(email=email, password=password, matricula=matricula, vehicle=VehicleType.MOTO)
            else:
                new_driver = Driver(email=email, password=password, matricula=matricula, vehicle=VehicleType.CARRO)

            db.session.add(new_driver)

            db.session.commit() # Datos en la BD postgrest

            return new_driver.serialize(), 200

        except ValueError as error:

            return { "message " : "Ah ocurrido un error inesperado " + error} , 500
    else:
        return { "message" : "user fields missing in request body" }, 400

    
    return jsonify(body), 200


@api.route("/products", methods=['POST'])
def create_product():
    body = request.get_json()

    name = body.get("name", None)
    description = body.get("description", '')
    amount = body.get("amount", 1)
    price = body.get("price", None)

    if name == None or price == None:
        return { "message" : "request body missing name or price" }, 400

    new_product = Products.create(name=name, amount=amount, description=description, price=price)
    if new_product == None:
        return { "message" : "An error has occurd during product creation" }, 500

    return new_product.serialize() , 200


@api.route("/orders", methods=['GET'])
def get_all_orders():

    try:
        all_orders = Order.query.all()

        return [ orden.serialize() for orden in all_orders ]

    except ValueError as err:
        return {"message": "failed to retrive orders " + err}, 500


