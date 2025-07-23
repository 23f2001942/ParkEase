# backend/app/__init__.py
from flask import Flask
from .config import Config
from .database import db, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
