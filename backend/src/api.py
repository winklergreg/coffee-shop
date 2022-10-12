import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

@app.after_request
def after_request(response):
    response.headers.add(
        "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
    )
    response.headers.add(
        "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
    )
    return response

db_drop_and_create_all()

# ROUTES
@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.order_by(Drink.title).all()

    return jsonify({
        'success': True,
        'drinks': [d.short() for d in drinks]
    }), 200

@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drink_details(payload):
    drinks = Drink.query.order_by(Drink.id).all()
    
    return jsonify({
        'success': True,
        'drinks': [d.long() for d in drinks]
    }), 200
    
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
    req = request.get_json()

    try:
        recipe = req['recipe']

        if isinstance(recipe, dict):
            recipe = [recipe]

        drink = Drink()
        drink.title = req['title']
        drink.recipe = json.dumps(recipe)
        drink.insert()
    except:
        abort(400)

    return jsonify({
        'success': True, 
        'drinks': [drink.long()]
    }), 200

@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, drink_id):
    req = request.get_json()
    drink = Drink.query.filter(Drink.id==drink_id).one_or_none()

    if not drink:
        abort(404)
    try: 
        if req.get('title'):
            drink.title = req.get('title')
        if req.get('recipe'):
            drink.recipe = json.dumps(req.get('recipe'))
        drink.update()
    except:
        abort(400)

    return jsonify({
        'success': True,
        'drinks': [drink.long()]
    }), 200

@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id):
    drink = Drink.query.filter(Drink.id==drink_id).one_or_none()

    if not drink:
        abort(404)
    try: 
        drink.delete()
    except:
        abort(400)

    return jsonify({
        'succss': True,
        'delete': drink_id
    }), 200

# Error Handling
@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad Request"
    }), 400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized"
    }), 401

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal Server Error"
    }), 500
