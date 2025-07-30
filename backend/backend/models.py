
from .database import db
from datetime import datetime
import pytz



class User(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String , nullable=False)
    type=db.Column(db.String , nullable=False,default='user')  # 
    email=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String , nullable=False)
    vehicle_no=db.Column(db.Integer,nullable=False)
    flag_status=db.Column(db.Boolean,nullable=False,default=0)
    reservations = db.relationship('Reservation', backref='user', lazy=True)
   

class ParkingLot(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    prime_location_name=db.Column(db.String , nullable=False)
    price_per_hour=db.Column(db.Integer,nullable=False)
    address=db.Column(db.String , nullable=False)
    pin_code=db.Column(db.Integer,nullable=False)
    number_of_spot=db.Column(db.Integer,nullable=False)
    flag_status=db.Column(db.Boolean,nullable=False,default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Kolkata')))
    spots = db.relationship('ParkingSpot', backref='lot', cascade='all, delete-orphan', lazy=True)
    # services = db.relationship('ServiceRequest', backref='service', lazy=True)




class ParkingSpot(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    status=db.Column(db.String(1),default="A")
    flag_status=db.Column(db.Boolean,nullable=False,default=0)
    reservations= db.relationship('Reservation', backref='spot',cascade='all, delete-orphan', lazy=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=False)
    



class Reservation(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    spot_id=db.Column(db.Integer, db.ForeignKey('parking_spot.id'), nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    parking_time=db.Column(db.DateTime,nullable=False,default=lambda: datetime.now(pytz.timezone('Asia/Kolkata')))
    leaving_time=db.Column(db.DateTime,nullable=False)
    parking_cost=db.Column(db.Float,nullable=False)
    reservation_status=db.Column(db.String,default="Booked")  #or released
