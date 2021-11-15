from flask import Blueprint, json, request, jsonify
from mcu_inventory.helpers import token_required
from mcu_inventory.models import db, User, Character, character_schema, characters_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return {'some':"value"}
    
# CREATE DRONE ROUTE
@api.route('/characters', methods = ['POST'])
@token_required
def create_character(current_user_token):
    id = request.json['id']
    name = request.json['name']
    description = request.json['description']
    comics_appeared_in = request.json['comics_appeared_in']
    super_power = request.json['super_power']
    user_token = current_user_token.token

    character = Character(name, description, comics_appeared_in, super_power, user_token, id)
    db.session.add(character)
    db.session.commit()

    response = character_schema.dump(character)
    return jsonify(response)
    
# Retrieve all characters endpoint
@api.route('/characters', methods = ['GET'])
@token_required
def get_characters(current_user_token):
    owner = current_user_token.token
    characters = Character.query.filter_by(user_token = owner).all()
    response = characters_schema.dump(characters)
    return jsonify(response)

# Retrieve single character endpoint
@api.route('/characters/<id>', methods = ['GET'])
@token_required
def get_character(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        character = Character.query.get(id)
        response = character_schema.dump(character)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid token required'}), 401


# Update character endpoint
@api.route('/characters/<id>', methods = ['POST', 'PUT'])
@token_required
def update_character(current_user_token, id):
    character = Character.query.get(id) #Get the character instance

    character.id = request.json['id']
    character.name = request.json['name']
    character.description = request.json['description']
    character.comics_appeared_in = request.json['comics_appeared_in']
    character.super_power = request.json['super_power']
    character.date_created = request.json['date_created']
    character.user_token = current_user_token.token

    db.session.commit()
    response = character_schema.dump(character)
    return jsonify(response)

# Delete character endpoint
@api.route('/characters/<id>', methods = ['DELETE'])
@token_required
def delete_character(current_user_token, id):
    character = Character.query.get(id)
    db.session.delete(character)
    db.session.commit()

    response = character_schema.dump(character)
    return jsonify(response)