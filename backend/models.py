# backend/models.py

from datetime import datetime, timezone
from sqlalchemy import Enum as PgEnum, Numeric, DateTime, Text
from werkzeug.security import generate_password_hash, check_password_hash
from db import db

USER_ROLE   = ('admin', 'user')
SPOT_STATUS = ('A', 'O')
RES_STATUS  = ('ongoing', 'done')


class User(db.Model):
    __tablename__ = 'users'

    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(80),  nullable=False, unique=True)
    email         = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role          = db.Column(
                       PgEnum(*USER_ROLE, name='user_roles'),
                       nullable=False,
                       default='user'
                    )
    full_name     = db.Column(db.String(100))
    address       = db.Column(Text)
    pin_code      = db.Column(db.String(10))
    created_at    = db.Column(
                       DateTime(timezone=True),
                       default=lambda: datetime.now(),
                       nullable=False
                    )
    updated_at    = db.Column(
                       DateTime(timezone=True),
                       default=lambda: datetime.now(),
                       onupdate=lambda: datetime.now(),
                       nullable=False
                    )

    reservations = db.relationship(
        'Reservation', back_populates='user', cascade='all, delete-orphan'
    )

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class ParkingLot(db.Model):
    __tablename__ = 'parking_lots'

    id             = db.Column(db.Integer, primary_key=True)
    name           = db.Column(db.String(100), nullable=False)
    address        = db.Column(Text, nullable=False)
    pin_code       = db.Column(db.String(10))
    price_per_hour = db.Column(Numeric(10, 2), nullable=False)
    total_spots    = db.Column(db.Integer, nullable=False)
    created_at     = db.Column(
                       DateTime(timezone=True),
                       default=lambda: datetime.now(),
                       nullable=False
                    )
    updated_at     = db.Column(
                       DateTime(timezone=True),
                       default=lambda: datetime.now(),
                       onupdate=lambda: datetime.now(),
                       nullable=False
                    )

    spots = db.relationship(
        'ParkingSpot', back_populates='lot', cascade='all, delete-orphan'
    )


class ParkingSpot(db.Model):
    __tablename__ = 'parking_spots'

    id            = db.Column(db.Integer, primary_key=True)
    lot_id        = db.Column(db.Integer,
                             db.ForeignKey('parking_lots.id'),
                             nullable=False)
    spot_number   = db.Column(db.Integer, nullable=False)
    status        = db.Column(
                       PgEnum(*SPOT_STATUS, name='spot_status'),
                       nullable=False,
                       default='A'
                   )
    created_at    = db.Column(
                       DateTime(timezone=True),
                       default=lambda: datetime.now(),
                       nullable=False
                   )
    updated_at    = db.Column(
                       DateTime(timezone=True),
                       default=lambda: datetime.now(),
                       onupdate=lambda: datetime.now(),
                       nullable=False
                   )

    lot           = db.relationship('ParkingLot', back_populates='spots')
    reservations  = db.relationship(
        'Reservation', back_populates='spot', cascade='all, delete-orphan'
    )


class Reservation(db.Model):
    __tablename__ = 'reservations'

    id                = db.Column(db.Integer, primary_key=True)
    spot_id           = db.Column(db.Integer,
                                  db.ForeignKey('parking_spots.id'),
                                  nullable=False)
    user_id           = db.Column(db.Integer,
                                  db.ForeignKey('users.id'),
                                  nullable=False)
    vehicle_number    = db.Column(db.String(20), nullable=False)
    parking_timestamp = db.Column(
                           DateTime(timezone=True),
                           default=lambda: datetime.now(),
                           nullable=False
                        )
    leaving_timestamp = db.Column(DateTime(timezone=True))
    parking_cost      = db.Column(Numeric(10, 2))
    remarks           = db.Column(Text)
    status            = db.Column(
                           PgEnum(*RES_STATUS, name='reservation_status'),
                           nullable=False,
                           default='ongoing'
                        )
    created_at        = db.Column(
                           DateTime(timezone=True),
                           default=lambda: datetime.now(),
                           nullable=False
                        )
    updated_at        = db.Column(
                           DateTime(timezone=True),
                           default=lambda: datetime.now(),
                           onupdate=lambda: datetime.now(),
                           nullable=False
                        )

    user = db.relationship('User', back_populates='reservations')
    spot = db.relationship('ParkingSpot', back_populates='reservations')
