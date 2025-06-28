from .database import db
from .models import User, ParkingLot, ParkingSpot, Reservation
from flask import current_app as app , jsonify , request , abort   #this app refers to the app=create_app() line 20 from app.py
from datetime import datetime
from flask_jwt_extended import create_access_token, current_user , jwt_required
import bcrypt

@app.route('/', methods=['GET'])
def home():
    return "<h1>This is home page"


@app.route('/api/user_registration', methods=['POST'])
def create_user():
    username=request.json.get("username",None)
    password=request.json.get("password",None)
    email=request.json.get("email",None)
    vehicle_no=request.json.get("vehicle_no",None)
    user=User.query.filter_by(email=email).one_or_none()
    if user:
        return jsonify({
            "message": "User already exist"
        }), 400
    else:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        user=User(username=username,password=hashed_password.decode('utf-8'),email=email,vehicle_no=vehicle_no)
        db.session.add(user)
        db.session.commit()
        return jsonify({
            "message": "User created successfully"
        }), 201


def role_required(required_role):
    def wrapper(fn):
        @jwt_required()
        def decorator(*args, **kwargs):
            if current_user.role != required_role:
                return jsonify({"message": "Access forbidden: insufficient permissions"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper


@app.route('/api/login', methods=['POST'])
def login():
    email=request.json.get("email",None)
    password=request.json.get("password",None)


    user=User.query.filter_by(email=email).one_or_none()
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return jsonify({
            "message": "Wrong username or password"
        }), 401
    
    access_token=create_access_token(identity=user)
    return jsonify(access_token=access_token)


############################# USER APIS #####################


##USER DASHBOARD

@app.route("/api/user_dashboard", methods=['GET']) 
@jwt_required()
def user_dashboard():
    user=User.query.get(current_user.id)
    booked_reservations=Reservation.query.filter_by(user_id=current_user.id).all()
    br_json=[]
    for br in booked_reservations:
        br_dict={}
        br_dict['id'] = br.id
        br_dict['spot_id'] = br.spot_id
        br_dict['parking_time'] = br.parking_time.strftime('%Y-%m-%d %H:%M:%S')
        br_dict['leaving_time'] = br.leaving_time.strftime('%Y-%m-%d %H:%M:%S')
        br_dict['vehicle_no'] = user.vehicle_no
        br_dict['resercation_status'] = br.reservation_status
        br_json.append(br_dict)
    return jsonify(br_json)


##USER SEARCH SECTION

@app.route("/api/user_search",methods=['GET','POST'])
@jwt_required()
def user_search():
    pincode=request.json.get("pin_code",None)
    address=request.json.get("address",None)
    if pincode:
        lots=ParkingLot.query.filter_by(pin_code=pincode).all()
    elif address:
        lots=ParkingLot.query.filter_by(address=address).all()
    lot_json=[]
    for lot in lots:
        lot_dict={}
        lot_dict["id"]=lot.id
        lot_dict["address"]=lot.address
        lot_dict["availability"]=lot.number_of_spot
        lot_json.append(lot_dict)
    return jsonify(lot_json)



##USER BOOKING

@app.route("/api/user_booking/<int:spotid>",methods=['POST'])
@jwt_required()
def user_booking(spotid):
    spot=ParkingSpot.query.get(spotid)
    vehicle_no=request.json.get("vehicle_no",None)
    leaving_time=request.json.get("leaving_time",None)
    if not leaving_time or not vehicle_no:
        return jsonify({"message": "Missing required fields"}), 400

    try:
        leaving_time = datetime.fromisoformat(leaving_time)
    except ValueError:
        return jsonify({"message": "Invalid datetime format for leaving_time"}), 400
    parking_time = datetime.utcnow()
    duration_in_hours = (leaving_time - parking_time).total_seconds() / 3600
    if duration_in_hours <= 0:
        return jsonify({"message": "Leaving time must be in the future"}), 400
    conflict = Reservation.query.filter(Reservation.spot_id == spotid,Reservation.reservation_status == "Booked",Reservation.leaving_time > parking_time).first()

    if conflict:
        return jsonify({"message": "This spot is already booked during the selected time"}), 409

    parking_cost = spot.lot.price_per_hour * duration_in_hours
    reservation=Reservation(spot_id=spotid,user_id=current_user.id,parking_time=parking_time,
                            leaving_time=leaving_time,parking_cost=parking_cost)
    spot.status = "B"
    lot = spot.lot
    if lot.number_of_spot > 0:
        lot.number_of_spot -= 1
    else:
        return jsonify({"message": "No available spots in this parking lot"}), 400
    db.session.add(reservation)
    db.session.commit()
    return jsonify({
        "message": "Booking successful",
        "reservation_id": reservation.id,
        "parking_cost": parking_cost
    }), 201