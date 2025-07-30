# backend/user_routes.py

from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth import role_required
from db import db
from models import ParkingLot, ParkingSpot, Reservation

user_bp = Blueprint('user_bp', __name__, url_prefix='/user')


@user_bp.route('/lots', methods=['GET'])
@jwt_required()
@role_required('user')
def list_available_lots():
    loc = request.args.get('location')
    pin = request.args.get('pin_code')
    q = ParkingLot.query
    if pin:   q = q.filter_by(pin_code=pin)
    if loc:   q = q.filter(ParkingLot.address.ilike(f"%{loc}%"))
    out = []
    for lot in q.all():
        avail = ParkingSpot.query.filter_by(lot_id=lot.id, status='A').count()
        out.append({
            'id': lot.id,
            'name': lot.name,
            'address': lot.address,
            'pin_code': lot.pin_code,
            'price_per_hour': float(lot.price_per_hour),
            'available_spots': avail
        })
    return jsonify(lots=out), 200


@user_bp.route('/reserve', methods=['POST'])
@jwt_required()
@role_required('user')
def reserve_spot():
    data = request.get_json() or {}
    lot_id  = data.get('lot_id')
    vehicle = data.get('vehicle_number')
    if not lot_id or not vehicle:
        return jsonify(msg="lot_id & vehicle_number required"), 400

    spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').first()
    if not spot:
        return jsonify(msg="No available spots"), 404
    
    identity = get_jwt_identity()
    if isinstance(identity, dict):
        user_id = identity.get('id')
    else:
        user_id = identity

    spot.status = 'O'

    res = Reservation(
        user_id=user_id,
        spot_id=spot.id,
        vehicle_number=vehicle,
        status='ongoing'
    )
    db.session.add(res)
    db.session.commit()

    return jsonify({
        'reservation_id': res.id,
        'spot_id':        spot.id,
        'lot_id':         lot_id,
        'start_time':     res.parking_timestamp.isoformat()
    }), 201


@user_bp.route('/reservations', methods=['GET'])
@jwt_required()
@role_required('user')
def list_reservations():
    identity = get_jwt_identity()
    uid = identity['id'] if isinstance(identity, dict) else identity

    resv_q = (Reservation.query
                   .filter_by(user_id=uid)
                   .order_by(Reservation.parking_timestamp.desc())
                   .all()
    )

    out = []
    for r in resv_q:
        lot_id = None
        if hasattr(r, 'lot_id'):
            lot_id = getattr(r, 'lot_id')
        else:
            lot_id = r.spot.lot_id if r.spot else None

        out.append({
            'reservation_id': r.id,
            'spot_id': r.spot_id,
            'lot_id':  lot_id,
            'vehicle_number': r.vehicle_number,
            'start_time':     r.parking_timestamp.isoformat(),
            'end_time':       (r.leaving_timestamp.isoformat() if r.leaving_timestamp else None),
            'status':         r.status
        })

    return jsonify(reservations=out), 200



@user_bp.route('/reservations/<int:res_id>/release', methods=['POST'])
@jwt_required()
@role_required('user')
def release_reservation(res_id):
    res = Reservation.query.get_or_404(res_id)

    identity = get_jwt_identity()
    user_id = identity.get('id') if isinstance(identity, dict) else identity

    if res.user_id != int(user_id):
        return jsonify(msg="Forbidden"), 403

    if res.status != 'ongoing':
        return jsonify(msg="Already released"), 400

    res.status            = 'done'
    res.leaving_timestamp = datetime.now(timezone.utc)

    spot = ParkingSpot.query.get_or_404(res.spot_id)
    spot.status = 'A'

    db.session.commit()

    return jsonify({
        'reservation_id': res.id,
        'end_time':       res.leaving_timestamp.isoformat(),
        'status':         res.status
    }), 200