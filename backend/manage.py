# backend/manage.py
#!/usr/bin/env python3

import os
from app import create_app, db
from app.models import User

app = create_app()

@app.cli.command('init-db')
def init_db():
    """Create tables and seed the single Admin user with default credentials."""
    db.create_all()
    print('Database tables created.')

    if not User.query.filter_by(role='admin').first():
        admin = User(
            username='Admin',
            email='admin@gmail.com',
            full_name='ADMIN',
            role='admin'
        )
        admin.set_password('Admin')
        db.session.add(admin)
        db.session.commit()
        print('Default Admin user created (Admin / Admin).')
    else:
        print('Admin already exists.')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
