from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from app import db
from models import Reservation, Showtime, Seat
from flask_jwt_extended import jwt_required, get_jwt_identity

reservation_bp = Blueprint('reservation', __name__)

@reservation_bp.route('/reservations', methods=['GET'])
@jwt_required()
def list_reservations():
    user_identity = get_jwt_identity()
    reservations = Reservation.query.filter_by(user_id=user_identity["id"]).all()
    return render_template('reservations.html', reservations=reservations, user=user_identity)

@reservation_bp.route('/reservations', methods=['POST'])
@jwt_required()
def make_reservation():
    data = request.form
    showtime_id = data['showtime_id']
    seat_number = data['seat_number']
    
    seat = Seat.query.filter_by(showtime_id=showtime_id, seat_number=seat_number, is_reserved=False).first()
    if not seat:
        return jsonify({"msg": "Seat already reserved"}), 400

    seat.is_reserved = True
    reservation = Reservation(user_id=get_jwt_identity()['id'], showtime_id=showtime_id, seats=seat_number)
    db.session.add(reservation)
    db.session.commit()

    return redirect(url_for('reservation.list_reservations'))
