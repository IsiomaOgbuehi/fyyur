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

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

## ROUTES

# GET DRINKS
@app.route('/drinks')
def get_drinks():
    try:
        query = Drink.query.all()
        if len(query) > 0:
            drinks = [drink.short() for drink in query]

            return jsonify({
                "success": True,
                "drinks": drinks
            })
        else:
            return jsonify({
                "success": True,
                "drinks": []
            })
    except:
        abort(422)

# GET DRINKS DETAIL
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(jwt):
    # print(jwt)
    try:
        query = Drink.query.all()
        if len(query) > 0:
            drinks = [drink.long() for drink in query]

            return jsonify({
                "success": True,
                "drinks": drinks
            })
        else:
            return jsonify({
                "success": True,
                "drinks": []
            })
    except AssertionError as e:
        print(e)
        abort(422)




# INSERT DRINKS
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def insert_drinks(jwt):
    data = request.get_json()
    if data is not None:
        try:
            title = data.get('title')
            recipe = data.get('recipe')
            # print(type(recipe))
            new_recipe = json.dumps(recipe)
            # print(type(dt))
            drinks = Drink(title=title, recipe=new_recipe)
            
            # print(drinks)
            drinks.insert()
            return jsonify({
                "success": True,
                "drinks": [{"title":title, "recipe":recipe}]
            })
        except AssertionError as e:
            print(e)
            abort(422)


# UPDATE DRINKS
@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drinks(jwt, id):
    if not id:
        abort(404)
    try:
        data = request.get_json()
        drink = Drink.query.get(id)
        
        if drink is not None:
            drink.title = data.get('title')
            drink.recipe = json.dumps(data.get('recipe'))
            drink.update()
            return jsonify({
                "success": True, 
                "drinks": [{"title": drink.title, "recipe": json.loads(drink.recipe)}]
            })
        else:
            abort(404)
    except AssertionError as e:
        print(e)
        abort(422)



# DELETE DRINKS
@app.route('/drinks/<id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(jwt, id):
    try:
        drink = Drink.query.get(id)
        if drink is not None:
            drink.delete()
            return jsonify({
                "success": True,
                "delete": drink.id
            })
        else:
            abort(404)
    except AssertionError as e:
        print(e)
        abort(422)


## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''

@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response
