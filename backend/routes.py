# backend/routes.py

from flask import Blueprint

routes_bp = Blueprint('main', __name__)

@routes_bp.route('/', methods=['GET'])
def home():
    return "<h1>Welcome to ParkEase</h1>"
