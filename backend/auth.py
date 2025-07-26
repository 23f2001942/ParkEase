from functools import wraps
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from db import db
from models import User

auth_bp = Blueprint('auth', __name__)

def role_required(role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            jwt_required()(lambda: None)()  # enforce JWT
            identity = get_jwt_identity()
            if identity.get('role') != role:
                return jsonify(msg="Forbidden"), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    email = data.get('email')
    pw    = data.get('password')
    if not email or not pw:
        return jsonify(msg="Email and password required"), 400

    if User.query.filter_by(email=email).first():
        return jsonify(msg="Email already registered"), 400

    user = User(
        username=email,
        email=email,
        full_name=data.get('full_name'),
        address=data.get('address'),
        pin_code=data.get('pin_code'),
        role='user'
    )
    user.set_password(pw)
    db.session.add(user)
    db.session.commit()
    return jsonify(msg="User registered"), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email')
    pw    = data.get('password')
    if not email or not pw:
        return jsonify(msg="Email and password required"), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(pw):
        return jsonify(msg="Bad credentials"), 401

    identity = {
        'id': user.id,
        'role': user.role,
        'full_name': user.full_name
    }
    token = create_access_token(identity=identity)
    return jsonify(access_token=token, role=user.role), 200
