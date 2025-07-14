from .database import db
from .models import User, ParkingLot, ParkingSpot, Reservation
from flask import current_app as app , jsonify , request , abort   #this app refers to the app=create_app() line 20 from app.py
from datetime import datetime
from flask_jwt_extended import create_access_token, current_user , jwt_required
import bcrypt
from functools import wraps



def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)  # <- This preserves the original function name
        @jwt_required()
        def decorator(*args, **kwargs):
            if current_user.type != required_role:
                return jsonify({"message": "Access forbidden: insufficient permissions"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper



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




@app.route('/api/login', methods=['POST'])
def login():
    email=request.json.get("email",None)
    password=request.json.get("password",None)


    user=User.query.filter_by(email=email).one_or_none()
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return jsonify({
            "message": "Wrong username or password"
        }), 400
    
    access_token=create_access_token(identity=user)
    return jsonify(access_token=access_token)



##USER DASHBOARD

@app.route("/api/dashboard", methods=['GET']) 
@jwt_required()
def dashboard():
    user=User.query.get(current_user.id)
    print(user.username)
    if user.type=='user':
        booked_reservations=Reservation.query.filter_by(user_id=current_user.id).all()
        print(booked_reservations)
        br_json=[]
        for br in booked_reservations:
            br_dict={}
            br_dict['id'] = br.id
            br_dict['username']=user.username
            br_dict['spot_id'] = br.spot_id
            br_dict['parking_time'] = br.parking_time.strftime('%Y-%m-%d %H:%M:%S')
            br_dict['leaving_time'] = br.leaving_time.strftime('%Y-%m-%d %H:%M:%S')
            br_dict['vehicle_no'] = user.vehicle_no
            br_dict['reservation_status'] = br.reservation_status
            br_json.append(br_dict)
        return jsonify({
            "username": user.username,
            "email": user.email,
            "vehicle_no": user.vehicle_no,
            "role": user.type,
            "booked_reservations": br_json
        })
    else:
        lots=ParkingLot.query.all()
        print(lots)
        print("in admin")
        lot_json=[]
        for lot in lots:
            no_of_occupied_spot=0
            lot_dict={}
            lot_dict['id']=lot.id
            lot_dict['username']=user.username
            lot_dict['address']=lot.address
            lot_dict['prime_address']=lot.prime_location_name
            lot_dict['number_of_spot']=lot.number_of_spot
            lot_dict['spots']=[]
            lot_dict['role']=user.type
            for spot in lot.spots:
                print(spot.id)
                spot_info={}
                spot_info['id']=spot.id
                spot_info['status']=spot.status
                
                if spot.status=='O':
                    no_of_occupied_spot+=1
                    reservation = Reservation.query.filter_by(spot_id=spot.id).first()
                    print((reservation))
                    if reservation:
                        user = User.query.get(reservation.user_id)
                        spot_info.update({
                            'username': user.username,
                            'vehicle_no': user.vehicle_no,
                            'parking_time': reservation.parking_time.strftime('%Y-%m-%d %H:%M'),
                            'leaving_time': reservation.leaving_time.strftime('%Y-%m-%d %H:%M'),
                            'parking_cost': reservation.parking_cost
                            })
                lot_dict['spots'].append(spot_info)
            lot_dict['occupied']=no_of_occupied_spot
            lot_json.append(lot_dict)
        return jsonify({
            "username": user.username,
            "email": user.email,
            "role": user.type,
            "lots": lot_json
        })
        






############################# USER APIS #####################



##USER SEARCH SECTION

@app.route("/api/user/search",methods=['GET','POST'])
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

@app.route("/api/user/booking/<int:spotid>",methods=['POST'])
@jwt_required()
def user_booking(spotid):
    spot=ParkingSpot.query.get(spotid)
    leaving_time=request.json.get("leaving_time",None)
    parking_time=request.json.get("parking_time",None)
    if not leaving_time or not parking_time or not vehicle_no:
        return jsonify({"message": "Missing required fields"}), 400
    try:
        leaving_time = datetime.fromisoformat(leaving_time)
        parking_time = datetime.fromisoformat(parking_time)
    except ValueError:
        return jsonify({"message": "Invalid datetime format for leaving_time"}), 400

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
    db.session.add(reservation)
    db.session.commit()
    return jsonify({
        "message": "Booking successful",
        "reservation_id": reservation.id,
        "parking_cost": parking_cost
    }), 201


## USER UPDATE BOOKING

@app.route("/api/user/update_booking/<int:spotid>",methods=['Post'])
@jwt_required()
def update_booking(spotid):
    spot=ParkingSpot.query.get(spotid)
    leaving_time=request.json.get("leaving_time",None)
    parking_time=request.json.get("parking_time",None)
    parking_time = datetime.fromisoformat(parking_time)
    leaving_time = datetime.fromisoformat(leaving_time)
    
    reservation=Reservation.query.filter_by(spot_id=spotid).first()
    reservation.leaving_time=leaving_time
    reservation.parking_time=parking_time
    duration_in_hours = (leaving_time - parking_time).total_seconds() / 3600
    parking_cost = spot.lot.price_per_hour * duration_in_hours
    reservation.parking_cost=parking_cost
    db.session.commit()
    return jsonify({
        "message": "Booking updated",
        "reservation_id": reservation.id,
        "parking_cost": parking_cost
    }), 201


##USER CANCEL BOOKING
@app.route("/api/user/cancel_booking/<int:spotid>",methods=['GET','POST'])
@jwt_required()
def cancel_booking(spotid):
    cancel_time = datetime.utcnow()
    reservation = Reservation.query.filter_by(spot_id=spotid).first()
    
    if reservation is None:
        return jsonify({"message": "Reservation not found"}), 404
    
    if reservation.parking_time < cancel_time and reservation.leaving_time > cancel_time:
        return jsonify({"message": "Cannot cancel a past or active booking"}), 400
    else:
        db.session.delete(reservation)  # delete the reservation instance
        db.session.commit() 
        return jsonify({"message": "Reservation cancelled successfully"}), 200





##USER RELEASE PARKING SPOT
@app.route("/api/user/release_booking/<int:spotid>",methods=['GET','POST'])
@jwt_required()
def release_spot(spotid):
    reservation=Reservation.query.filter_by(spot_id=spotid).first()
    spot=ParkingSpot.query.filter_by(id=spotid).first()
    spot.status='A'
    reservation.reservation_status='Released'
    db.session.commit()
    return jsonify({
            "message": "You have successfully released the parking spot"
        })
    


####################### ADMIN APIS #####################

#******  LOT CREATION **********
@app.route("/api/admin/create_lot",methods=['POST'])
@role_required("admin")
def create_lot():
    prime_location=request.json.get("prime_location_name",None)
    price_per_hour=request.json.get("price_per_hour",None)
    address=request.json.get("address",None)
    pin_Code=request.json.get("pin_code",None)
    no_of_spot=request.json.get("no_of_spot",None)
    lot=ParkingLot(prime_location_name=prime_location,price_per_hour=price_per_hour,address=address,pin_code=pin_Code,number_of_spot=no_of_spot)
    db.session.add(lot)
    db.session.commit()
    for i in range(0,no_of_spot):
        spot=ParkingSpot(lot_id=lot.id)
        db.session.add(spot)
    db.session.commit()
    return jsonify({"message": f"Parking Lot with {no_of_spot} spots created successfully."})


#************ Edit LOT ************8

@app.route("/api/admin/update_lot/<int:lotid>",methods=['POST'])
@role_required("admin")
def edit_lot(lotid):
    lot=ParkingLot.query.get(lotid)
    if not lot:
        return jsonify({"message": "Parking Lot not found"}), 404
    
    prime_location=request.json.get("prime_location_name",lot.prime_location_name)
    price_per_hour=request.json.get("price_per_hour",lot.price_per_hour)
    address=request.json.get("address",lot.address)
    pin_Code=request.json.get("pin_code",lot.pin_code)
    no_of_spot=request.json.get("no_of_spot",lot.number_of_spot)

    lot.prime_location_name=prime_location
    lot.price_per_hour=price_per_hour
    lot.address=address
    lot.pin_code=pin_Code
    lot.number_of_spot=no_of_spot
    spots=ParkingSpot.query.filter_by(lot_id=lotid).all()
    if len(spots) < no_of_spot:
        for i in range(len(spots), no_of_spot):
            spot=ParkingSpot(lot_id=lotid)
            db.session.add(spot)
    elif len(spots) > no_of_spot:
        for i in range(no_of_spot, len(spots)):
            db.session.delete(spots[i])
    db.session.commit()
    return jsonify({"message": "Parking Lot has been edited"})


#***** delete Lot (******************************8)

@app.route("/api/admin/delete_lot/<int:lotid>",methods=['GET','POST'])
@role_required("admin")
def delete_lot(lotid):
    lot=ParkingLot.query.filter_by(id=lotid)
    no_of_occupied_spot=0
    for spot in lot.spots:
        if spot.status=='O':
            no_of_occupied_spot+=1
    if no_of_occupied_spot==0:
        db.session.delete(lot)
        db.session.commit()
        return jsonify({"message":"Lot has been deleted Successfully"})
    else:
        return jsonify({"message":"Can not delete occupied lots"})
    
#**************** view spot **************88
    
@app.route("/api/admin/view_spot/<int:spotid>",methods=['GET'])
@role_required("admin")
def view_spot(spotid):
    spot=ParkingSpot.query.get(spotid)
    if not spot:
        return jsonify({"message": "Parking Spot not found"}), 404
    
    spot_info = {
        "id": spot.id,
        "status": spot.status,
        "lot_id": spot.lot_id,
        "lot_address": spot.lot.address
    }
    
    reservation = Reservation.query.filter_by(spot_id=spotid).first()
    if reservation:
        user = User.query.get(reservation.user_id)
        spot_info.update({
            'username': user.username,
            'vehicle_no': user.vehicle_no,
            'parking_time': reservation.parking_time.strftime('%Y-%m-%d %H:%M'),
            'leaving_time': reservation.leaving_time.strftime('%Y-%m-%d %H:%M'),
            'parking_cost': reservation.parking_cost
        })
    
    return jsonify(spot_info)


#************ DElete Spot *****************

@app.route("/api/admin/delete_spot/<int:spotid>",methods=['GET'])
@role_required("admin")
def delete_spot(spotid):
    spot=ParkingSpot.query.get(spotid)
    if not spot:
        return jsonify({"message": "Parking Spot not found"}), 404
    
    if spot.status == 'O':
        return jsonify({"message": "Cannot delete an occupied parking spot"}), 400
    spot.lot.number_of_spot-=1
    db.session.delete(spot)
    db.session.commit()
    return jsonify({"message": "Parking Spot deleted successfully"}), 200


#************ user details ***************88

@app.route("/api/admin/user_search",methods=['GET','POST'])
@role_required("admin")
def admin_user_search():
    users=User.query.filter_by(type='user').all()
    if users:
        user_json=[]
        for user in users:
            user_dict={}
            user_dict['id']=user.id
            user_dict['email']=user.email
            user_dict['name']=user.username
            user_dict['address']=user.address
            user_dict['pin_code']=user.pin_code
            user_json.append(user_dict)
        return jsonify(user_json)
    else:
        return jsonify({"message":"There are not any User registered"})
    




#************** Lot details **********


@app.route("/api/admin/lot_search",methods=['GET','POST'])
@role_required('admin')
def admin_lot_search():
    # pin_code=request.json.get("pin_code",None)
    # prime_location=request.json.get("prime_location_name",None)
    # address=request.json.get("address",None)
    # availability=request.json.get("availablility",None)
    criteria=request.json.get("criteria")
    search=request.json.get("search")
    search =search.strip().lower()
    if criteria=="Pincode":
        lots=ParkingLot.query.filter_by(pin_code=search).all()
        if not lot:
                return jsonify({"message":f"There are not any Lot present at pincode {search}"})
        lot_json=[]
        for lot in lots:
            no_of_occupied_spot=0
            lot_dict={}
            lot_dict['id']=lot.id
            lot_dict['username']=user.username
            lot_dict['address']=lot.address
            lot_dict['spots']=[]
            for spot in lot.spots:
                spot_info={}
                spot_info['id']=spot.id
                spot_info['status']=spot.status
                if spot.status=='O':
                    no_of_occupied_spot+=1
                    print("above_regis")
                    print(spot.id)
                    reservation = Reservation.query.filter_by(spot_id=spot.id).first()
                    print((reservation))
                    if reservation:
                        user = User.query.get(reservation.user_id)
                        spot_info.update({
                            'username': user.username,
                            'vehicle_no': user.vehicle_no,
                            'parking_time': reservation.parking_time.strftime('%Y-%m-%d %H:%M'),
                            'leaving_time': reservation.leaving_time.strftime('%Y-%m-%d %H:%M'),
                            'parking_cost': reservation.parking_cost
                            })
                    lot_dict['spots'].append(spot_info)
            lot_dict['occupied']=no_of_occupied_spot
            lot_json.append(lot_dict)
        return jsonify(lot_json)
    elif criteria=="PrimeLocation":
        lots=ParkingLot.query.filter_by(prime_location_name=search).all()
        lot_json=[]
        for lot in lots:
            no_of_occupied_spot=0
            lot_dict={}
            lot_dict['id']=lot.id
            lot_dict['username']=user.username
            lot_dict['address']=lot.address
            lot_dict['spots']=[]
            for spot in lot.spots:
                spot_info={}
                spot_info['id']=spot.id
                spot_info['status']=spot.status
                if spot.status=='O':
                    no_of_occupied_spot+=1
                    print("above_regis")
                    print(spot.id)
                    reservation = Reservation.query.filter_by(spot_id=spot.id).first()
                    print((reservation))
                    if reservation:
                        user = User.query.get(reservation.user_id)
                        spot_info.update({
                            'username': user.username,
                            'vehicle_no': user.vehicle_no,
                            'parking_time': reservation.parking_time.strftime('%Y-%m-%d %H:%M'),
                            'leaving_time': reservation.leaving_time.strftime('%Y-%m-%d %H:%M'),
                            'parking_cost': reservation.parking_cost
                            })
                    lot_dict['spots'].append(spot_info)
            lot_dict['occupied']=no_of_occupied_spot
            lot_json.append(lot_dict)
        return jsonify(lot_json)
    elif criteria=="address":
        lots=ParkingLot.query.filter_by(address=search).all()
        lot_json=[]
        for lot in lots:
            no_of_occupied_spot=0
            lot_dict={}
            lot_dict['id']=lot.id
            lot_dict['username']=user.username
            lot_dict['address']=lot.address
            lot_dict['spots']=[]
            for spot in lot.spots:
                spot_info={}
                spot_info['id']=spot.id
                spot_info['status']=spot.status
                if spot.status=='O':
                    no_of_occupied_spot+=1
                    print("above_regis")
                    print(spot.id)
                    reservation = Reservation.query.filter_by(spot_id=spot.id).first()
                    print((reservation))
                    if reservation:
                        user = User.query.get(reservation.user_id)
                        spot_info.update({
                            'username': user.username,
                            'vehicle_no': user.vehicle_no,
                            'parking_time': reservation.parking_time.strftime('%Y-%m-%d %H:%M'),
                            'leaving_time': reservation.leaving_time.strftime('%Y-%m-%d %H:%M'),
                            'parking_cost': reservation.parking_cost
                            })
                    lot_dict['spots'].append(spot_info)
            lot_dict['occupied']=no_of_occupied_spot
            lot_json.append(lot_dict)
        return jsonify(lot_json)
        