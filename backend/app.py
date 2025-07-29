# backend/app.py

import click
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from werkzeug.security import generate_password_hash

from config import Config
from db import db
from auth import auth_bp
from routes import routes_bp
from admin_routes import admin_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    JWTManager(app)
    CORS(app)

    app.register_blueprint(routes_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp)

    return app

app = create_app()

@app.cli.command('init-db')
def init_db():
    """Create all tables and seed default Admin."""
    from models import User

    db.create_all()
    click.echo("Tables created.")

    if not User.query.filter_by(username='Admin').first():
        admin = User(
            username='Admin',
            email='admin@gmail.com',
            full_name='ADMIN',
            role='admin'
        )
        admin.set_password('Admin')
        db.session.add(admin)
        db.session.commit()
        click.echo("Default Admin created (Admin/Admin).")
    else:
        click.echo("Admin already exists, skipping seed.")

if __name__ == '__main__':
    app.run(debug=True)
