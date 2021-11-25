from os import access
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import validators
from src.constants.http_status_code import *
from src.database import *
from flasgger import swag_from
from src.function.users import *
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

user = UserManager()


auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post('/register')
def register():
    fullname = request.json['fullname']
    email = request.json['email']
    password = request.json['password']
    is_merchant = request.json['isMerchant']
    return user.user_registration(fullname, email, password, is_merchant)
    
    


@auth.post('/login')
def login():
    email = request.json.get('email', '')
    password = request.json.get('password', '')
    return user.login(email, password)


@auth.get('/current_user')
@jwt_required()
def current_user():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    data = {
        "currentUser": {
            "fullname": user.fullname,
            "email": user.email,
            "is_merchant": user.is_merchant,
            "created_at": user.created_at
        }
    }
    return jsonify(data), HTTP_200_OK


@auth.get('/token/refresh')
@jwt_required(refresh=True)
def refresh_user_access_token():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)
    
    data = {
        "access": access
    }
    return jsonify(data)

