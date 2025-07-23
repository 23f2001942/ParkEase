# backend/app/models.py
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from .database import db

class User(db.Model):
    __tablename__ = 'users'

    id             = db.Column(db.Integer, primary_key=True)
    username       = db.Column(db.String(80), unique=True, nullable=False)
    email          = db.Column(db.String(120), unique=True, nullable=False)
    password_hash  = db.Column(db.String(128), nullable=False)
    role           = db.Column(db.Enum('admin', 'user', name='user_roles'), nullable=False, default='user')
    full_name      = db.Column(db.String(100))
    address        = db.Column(db.Text)
    pin_code       = db.Column(db.String(10))
    created_at     = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at     = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc),
                               nullable=False)

    reservations   = db.relationship('Reservation', back_populates='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class ParkingLot(db.Model):
    __tablename__ = 'parking_lots'

    id             = db.Column(db.Integer, primary_key=True)
    name           = db.Column(db.String(100), nullable=False)
    address        = db.Column(db.Text, nullable=False)
    pin_code       = db.Column(db.String(10))
    price_per_hour = db.Column(db.Numeric(10, 2), nullable=False)
    total_spots    = db.Column(db.Integer, nullable=False)
    created_at     = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at     = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc),
                               nullable=False)

    spots          = db.relationship('ParkingSpot', back_populates='lot', cascade='all, delete-orphan')


class ParkingSpot(db.Model):
    __tablename__ = 'parking_spots'

    id           = db.Column(db.Integer, primary_key=True)
    lot_id       = db.Column(db.Integer, db.ForeignKey('parking_lots.id'), nullable=False)
    spot_number  = db.Column(db.Integer, nullable=False)
    status       = db.Column(db.Enum('A', 'O', name='spot_status'), nullable=False, default='A')
    created_at   = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at   = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc),
                             nullable=False)

    lot          = db.relationship('ParkingLot', back_populates='spots')
    reservations = db.relationship('Reservation', back_populates='spot')


class Reservation(db.Model):
    __tablename__ = 'reservations'

    id                = db.Column(db.Integer, primary_key=True)
    spot_id           = db.Column(db.Integer, db.ForeignKey('parking_spots.id'), nullable=False)
    user_id           = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vehicle_number    = db.Column(db.String(20), nullable=False)
    parking_timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    leaving_timestamp = db.Column(db.DateTime)
    parking_cost      = db.Column(db.Numeric(10, 2))
    remarks           = db.Column(db.Text)
    status            = db.Column(db.Enum('ongoing', 'done', name='reservation_status'), nullable=False, default='ongoing')
    created_at        = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at        = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc),
                                  nullable=False)
    user              = db.relationship('User', back_populates='reservations')
    spot              = db.relationship('ParkingSpot', back_populates='reservations')
