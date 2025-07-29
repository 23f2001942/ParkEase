# backend/admin_routes.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth import role_required
from db import db
from models import ParkingLot, ParkingSpot, User, Reservation

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')


def lot_summary(lot):
    occupied = sum(1 for s in lot.spots if s.status == 'O')
    return {
        'id': lot.id,
        'name': lot.name,
        'address': lot.address,
        'pin_code': lot.pin_code,
        'price_per_hour': float(lot.price_per_hour),
        'total_spots': lot.total_spots,
        'occupied_spots': occupied
    }


@admin_bp.route('/lots', methods=['GET'])
@jwt_required()
@role_required('admin')
def list_lots():
    lots = ParkingLot.query.all()
    return jsonify([lot_summary(l) for l in lots]), 200


@admin_bp.route('/lots', methods=['POST'])
@jwt_required()
@role_required('admin')
def create_lot():
    data = request.get_json() or {}
    for f in ('name','address','price_per_hour','total_spots'):
        if f not in data:
            return jsonify(msg=f"{f} is required"), 400

    lot = ParkingLot(
        name=data['name'],
        address=data['address'],
        pin_code=data.get('pin_code'),
        price_per_hour=data['price_per_hour'],
        total_spots=data['total_spots']
    )
    db.session.add(lot)
    db.session.flush() 

    # auto-generate spots
    for num in range(1, lot.total_spots + 1):
        spot = ParkingSpot(lot_id=lot.id, spot_number=num)
        db.session.add(spot)

    db.session.commit()
    return jsonify(lot_summary(lot)), 201


@admin_bp.route('/lots/<int:lot_id>', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    spots = [
        {'id': s.id, 'spot_number': s.spot_number, 'status': s.status}
        for s in lot.spots
    ]
    data = lot_summary(lot)
    data['spots'] = spots
    return jsonify(data), 200


@admin_bp.route('/lots/<int:lot_id>/spots', methods=['GET'])
@jwt_required()
@role_required('admin')
def list_spots_by_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)

    spots = ParkingSpot.query.filter_by(lot_id=lot_id).order_by(ParkingSpot.spot_number).all()

    out = []
    for s in spots:
        spot_data = {
            'id': s.id,
            'spot_number': s.spot_number,
            'status': s.status
        }
        if s.status == 'O':
            res = Reservation.query.filter_by(spot_id=s.id, status='ongoing').first()
            if res:
                spot_data.update({
                    'user_id':      res.user_id,
                    'vehicle_number': res.vehicle_number,
                    'parking_timestamp': res.parking_timestamp.isoformat()
                })
        out.append(spot_data)

    return jsonify(spots=out), 200


@admin_bp.route('/lots/<int:lot_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def update_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    data = request.get_json() or {}

    lot.name = data.get('name', lot.name)
    lot.address = data.get('address', lot.address)
    lot.pin_code = data.get('pin_code', lot.pin_code)
    lot.price_per_hour = data.get('price_per_hour', lot.price_per_hour)

    new_total = data.get('total_spots', lot.total_spots)
    old_total = lot.total_spots
    lot.total_spots = new_total

    if new_total > old_total:
        for num in range(old_total+1, new_total+1):
            db.session.add(ParkingSpot(lot_id=lot.id, spot_number=num))

    elif new_total < old_total:
        to_delete = ParkingSpot.query.filter(
            ParkingSpot.lot_id==lot.id,
            ParkingSpot.spot_number > new_total,
            ParkingSpot.status=='A'
        ).all()
        for s in to_delete:
            db.session.delete(s)

    db.session.commit()
    return jsonify(lot_summary(lot)), 200


@admin_bp.route('/lots/<int:lot_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    db.session.delete(lot)
    db.session.commit()
    return jsonify(msg="Deleted"), 200


@admin_bp.route('/spots/<int:spot_id>', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_spot(spot_id):
    spot = ParkingSpot.query.get_or_404(spot_id)
    data = {
        'id': spot.id,
        'lot_id': spot.lot_id,
        'spot_number': spot.spot_number,
        'status': spot.status
    }
    if spot.status == 'O':
        res = Reservation.query.filter_by(spot_id=spot.id, status='ongoing').first()
        if res:
            data.update({
                'user_id': res.user_id,
                'vehicle_number': res.vehicle_number,
                'parking_timestamp': res.parking_timestamp.isoformat(),
            })
    return jsonify(data), 200


@admin_bp.route('/spots/<int:spot_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_spot(spot_id):
    spot = ParkingSpot.query.get_or_404(spot_id)
    if spot.status != 'A':
        return jsonify(msg="Cannot delete occupied spot"), 400
    db.session.delete(spot)
    db.session.commit()
    return jsonify(msg="Spot deleted"), 200


@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@role_required('admin')
def list_users():
    users = User.query.all()
    users = User.query.filter_by(role='user').all()
    out = []
    for u in users:
        out.append({
            'id': u.id,
            'email': u.email,
            'username': u.username,
            'full_name': u.full_name,
            'address': u.address,
            'pin_code': u.pin_code
        })
    return jsonify(out), 200
