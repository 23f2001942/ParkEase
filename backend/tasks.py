# backend/tasks.py

import os, csv
from datetime import datetime, timedelta
from celery import shared_task, Celery
from config import Config
from flask import Flask
from flask_mail import Message
from db import db
from models import Reservation, User, ParkingSpot, ParkingLot
from flask_mail import Mail
from celery_worker import celery  

# bootstrap a minimal Flask app for context
def make_context_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    Mail(app)
    return app

app_context = make_context_app()                            

# Daily reminders ##
@celery.task(name='tasks.send_daily_reminders')
def send_daily_reminders():
    with app_context.app_context():
        tomorrow = datetime.now().date() + timedelta(days=1)
        start    = datetime.combine(tomorrow, datetime.min.time())
        end      = datetime.combine(tomorrow, datetime.max.time())

        resvs = Reservation.query.filter(
            Reservation.parking_timestamp.between(start,end)
        ).all()

        by_user = {}
        for r in resvs:
            by_user.setdefault(r.user_id, []).append(r)

        for uid, items in by_user.items():
            user = User.query.get(uid)
            if not user or not user.email: continue
            msg = Message(
                subject="ParkEase: Tomorrow’s Reservations",
                recipients=[user.email]
            )
            body_lines = [
                f"• Reservation #{r.id} at Lot {r.spot.lot_id}, Spot {r.spot_id}"
                for r in items
            ]
            msg.body = f"Hello {user.full_name},\n\nYour reservations for {tomorrow}:\n\n" + "\n".join(body_lines)
            Mail(app_context).send(msg)

## Monthly reports ##
@celery.task(name='tasks.send_monthly_reports')
def send_monthly_reports():
    with app_context.app_context():
        now        = datetime.now()
        last_month = (now.replace(day=1) - timedelta(days=1))
        ms = last_month.replace(day=1)
        me = last_month.replace(day=last_month.day)

        for user in User.query.filter_by(role='user').all():
            resvs = Reservation.query.filter(
                Reservation.user_id==user.id,
                Reservation.leaving_timestamp.between(ms,me)
            ).all()
            total = sum(r.parking_cost or 0 for r in resvs)
            html  = f"<h2>ParkEase Report: {ms.strftime('%B %Y')}</h2>"
            html += f"<p>Total Spent: ₹{total:.2f}</p><ul>"
            for r in resvs:
                html += f"<li>#{r.id} — ₹{r.parking_cost:.2f}</li>"
            html += "</ul>"

            msg = Message(
                subject=f"{ms.strftime('%B %Y')} ParkEase Report",
                recipients=[user.email],
                html=html
            )
            Mail(app_context).send(msg)

# CSV export ##
@celery.task(bind=True, name='tasks.export_user_history')
def export_user_history(self, user_id):
    with app_context.app_context():
        resvs = Reservation.query.filter_by(user_id=user_id).all()
        fname = f"user_{user_id}_history_{self.request.id}.csv"
        path  = os.path.join(Config.EXPORT_FOLDER, fname)

        with open(path,'w',newline='') as f:
            w = csv.writer(f)
            w.writerow(['ID','Lot','Spot','Start','End','Cost','Status'])
            for r in resvs:
                w.writerow([
                    r.id,
                    r.spot.lot_id,
                    r.spot_id,
                    r.parking_timestamp.isoformat(),
                    r.leaving_timestamp.isoformat() if r.leaving_timestamp else '',
                    r.parking_cost or 0,
                    r.status
                ])
        return {'file_path': path}
