# backend/app.py

import click
from flask import Flask
from werkzeug.security import generate_password_hash

from config import Config
from db import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)

    # late‐import to avoid circular refs
    from routes import routes_bp
    app.register_blueprint(routes_bp)

    return app

app = create_app()

@app.cli.command('init-db')
def init_db():
    """Create all tables and seed default Admin."""
    # import User here, after db is ready
    from models import User

    db.create_all()
    click.echo("Tables created.")

    if not User.query.filter_by(username='Admin').first():
        admin = User(
            username='Admin',
            email='admin@gmail.com',
            password_hash=generate_password_hash('Admin'),
            role='admin',
            full_name='ADMIN'
        )
        db.session.add(admin)
        db.session.commit()
        click.echo("Default Admin created (Admin/Admin).")
    else:
        click.echo("Admin already exists, skipping seed.")

if __name__ == '__main__':
    app.run(debug=True)
