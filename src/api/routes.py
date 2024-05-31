"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from api.models import db, Users

api = Blueprint('api', __name__)
CORS(api)# Allow CORS requests to this API


@api.route('/hello', methods=['GET'])
def handle_hello():
    response_body={}
    response_body ["message"] = "Hello! I'm a message that came from the backend"
    return response_body, 200

@api.route('/users', methods=['GET'])
def handle_users():
    response_body={}
    # Hacer la logica para mostrar los usuarios que tengo en mi DB.
    users = db.session.execute(db.select(Users)).scalars()
    results = [row.serialize() for row in users]
    response_body['results'] = results
    response_body['message'] = "Users List"
    return response_body, 200
