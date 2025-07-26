# backend/routes.py

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from auth import role_required

routes_bp = Blueprint('main', __name__)

@routes_bp.route('/', methods=['GET'])
def home():
    return "<h1>Welcome to ParkEase</h1>"


@routes_bp.route('/admin/dashboard', methods=['GET'])
@jwt_required()
@role_required('admin')
def admin_dashboard():
    return jsonify(msg="Hello, Admin!"), 200


@routes_bp.route('/user/dashboard', methods=['GET'])
@jwt_required()
@role_required('user')
def user_dashboard():
    identity = get_jwt_identity()
    return jsonify(msg=f"Hello, {identity.get('full_name')}!"), 200

