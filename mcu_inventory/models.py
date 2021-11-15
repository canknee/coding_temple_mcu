# Always have to "flask db migrate" "flask db upgrade if you make any changes" 

from typing import Sequence
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Sequence
from flask_migrate import Migrate
import uuid
from datetime import date, datetime

# Adding Flask Security for Passwords
from werkzeug.security import generate_password_hash, check_password_hash

# Import for the Secrets Module (given by python)
import secrets
from flask_login import LoginManager, UserMixin
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    character = db.relationship('Character', backref = "owner", lazy = True)

    def __init__(self, email, first_name = '', last_name = '', id = '', password = '', token = '', g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def set_token(self, length):
        return secrets.token_hex(length)

    def __repr__(self):
        return f'User {self.email} has been added to the database.'

class Character(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(300), nullable = True)
    comics_appeared_in = db.Column(db.Integer)
    super_power = db.Column(db.String(150))
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)  
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, description, comics_appeared_in, super_power, user_token, id):
        self.id = id
        self.name = name
        self.description = description
        self.comics_appeared_in = comics_appeared_in
        self.super_power = super_power
        self.date_created = datetime.utcnow()
        self.user_token = user_token

    # def set_id(self):
    #     # return secrets.token_urlsafe()
    #     idseq = Sequence("id_seq", start=100, increment=1)
    #     return idseq

    def __repr__(self):
        return f'The following Drone has been created: {self.name}'

# Creation of API schema via the marshmallow object
class CharacterSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'description', 'comics_appeared_in', 'super_power', 'date_created']

character_schema = CharacterSchema()
characters_schema = CharacterSchema(many = True)