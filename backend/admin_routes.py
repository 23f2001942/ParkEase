# backend/admin_routes.py

from datetime import datetime, time
from sqlalchemy import func
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth import role_required
from db import db
from models import ParkingLot, ParkingSpot, User, Reservation
from cache import cache 

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

def lot_summary(lot):
    occupied = sum(1 for s in lot.spots if s.status == 'O')
    total    = len(lot.spots)
    return {
        'id':             lot.id,
        'name':           lot.name,
        'address':        lot.address,
        'pin_code':       lot.pin_code,
        'price_per_hour': float(lot.price_per_hour),
        'total_spots':    total,
        'occupied_spots': occupied
    }


@admin_bp.route('/lots', methods=['GET'])
@jwt_required()
@role_required('admin')
@cache.cached(timeout=30, key_prefix="admin:lots") 
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

    for num in range(1, lot.total_spots + 1):
        spot = ParkingSpot(lot_id=lot.id, spot_number=num)
        db.session.add(spot)

    db.session.commit()
    cache.delete("admin:lots")
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
@cache.cached(timeout=15, key_prefix=lambda: f"admin:lot:{request.view_args['lot_id']}:spots")
def list_spots_by_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)

    spots = ParkingSpot.query.filter_by(lot_id=lot_id) \
                             .order_by(ParkingSpot.spot_number) \
                             .all()

    out = []
    for s in spots:
        spot_data = {
            'id':          s.id,
            'spot_number': s.spot_number,
            'status':      s.status
        }
        if s.status == 'O':
            res = Reservation.query.filter_by(spot_id=s.id, status='ongoing').first()
            if res:
                spot_data.update({
                    'user_id':           res.user_id,
                    'vehicle_number':    res.vehicle_number,
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

    lot.name           = data.get('name', lot.name)
    lot.address        = data.get('address', lot.address)
    lot.pin_code       = data.get('pin_code', lot.pin_code)
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
    cache.delete("admin:lots")
    cache.delete(f"admin:lot:{lot_id}:spots")
    return jsonify(lot_summary(lot)), 200


@admin_bp.route('/lots/<int:lot_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    db.session.delete(lot)
    db.session.commit()
    cache.delete("admin:lots") 
    cache.delete(f"admin:lot:{lot_id}:spots")
    return jsonify(msg="Deleted"), 200


@admin_bp.route('/spots/<int:spot_id>', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_spot(spot_id):
    spot = ParkingSpot.query.get_or_404(spot_id)
    data = {
        'id':          spot.id,
        'lot_id':      spot.lot_id,
        'spot_number': spot.spot_number,
        'status':      spot.status
    }
    if spot.status == 'O':
        res = Reservation.query.filter_by(spot_id=spot.id, status='ongoing').first()
        if res:
            data.update({
                'user_id':           res.user_id,
                'vehicle_number':    res.vehicle_number,
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
    cache.delete(f"admin:lot:{spot.lot_id}:spots")
    return jsonify(msg="Spot deleted"), 200


@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@role_required('admin')
def list_users():
    users = User.query.filter_by(role='user').all()
    out = []
    for u in users:
        out.append({
            'id':        u.id,
            'email':     u.email,
            'username':  u.username,
            'full_name': u.full_name,
            'address':   u.address,
            'pin_code':  u.pin_code
        })
    return jsonify(out), 200

@admin_bp.route('/summary', methods=['GET'])
@jwt_required()
@role_required('admin')
@cache.cached(timeout=60, key_prefix="admin:summary") 
def admin_summary():
    now = datetime.now()
    today = now.date()
    start_today = datetime.combine(today, time.min)
    month_start = today.replace(day=1)
    start_month = datetime.combine(month_start, time.min)

    lots = ParkingLot.query.all()
    by_lot = []
    sum_revenue_month = 0
    sum_occ_pct = 0.0

    for lot in lots:
        # occupancy metrics
        total_spots = len(lot.spots)
        occupied_spots = sum(1 for s in lot.spots if s.status == 'O')
        occ_pct = (occupied_spots / total_spots) if total_spots else 0

        # revenue today for this lot
        rev_today = (
            db.session.query(func.coalesce(func.sum(Reservation.parking_cost), 0))
            .join(ParkingSpot, ParkingSpot.id == Reservation.spot_id)
            .filter(
                ParkingSpot.lot_id == lot.id,
                Reservation.leaving_timestamp >= start_today,
                Reservation.status == 'done'
            )
            .scalar()
        ) or 0

        # revenue this month for this lot
        rev_month = (
            db.session.query(func.coalesce(func.sum(Reservation.parking_cost), 0))
            .join(ParkingSpot, ParkingSpot.id == Reservation.spot_id)
            .filter(
                ParkingSpot.lot_id == lot.id,
                Reservation.leaving_timestamp >= start_month,
                Reservation.status == 'done'
            )
            .scalar()
        ) or 0

        sum_revenue_month += rev_month
        sum_occ_pct += occ_pct

        by_lot.append({
            'lot_id':         lot.id,
            'lot_name':       lot.name,
            'total_spots':    total_spots,
            'occupied_pct':   occ_pct,
            'revenue_today':  float(rev_today),
            'revenue_month':  float(rev_month)
        })

    overall = {
        'total_revenue_month': float(sum_revenue_month),
        'avg_occupancy_pct':   (sum_occ_pct / len(lots)) if lots else 0
    }

    return jsonify(by_lot=by_lot, overall=overall), 200