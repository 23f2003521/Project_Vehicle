from .database import db
from .models import User, ParkingLot, ParkingSpot, Reservation
from flask import current_app as app , jsonify , request , abort , send_from_directory #this app refers to the app=create_app() line 20 from app.py
from datetime import datetime
import pytz
from flask_jwt_extended import create_access_token, current_user , jwt_required ,get_jwt_identity
import bcrypt
from functools import wraps
from celery.result import AsyncResult
from .tasks import daily_parking_reminder,csv_report, handle_overstays,monthly_report
from app import cache  # if cache is initialized in app.py



def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            if not current_user:
                return jsonify({"message": "Authentication required"}), 401

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
    return jsonify({
        "access_token":access_token,
        "role":user.type
    }),200



##USER DASHBOARD

@app.route("/api/dashboard", methods=['GET']) 
@jwt_required()
def dashboard():
    user=User.query.get(current_user.id)
    if user.type=='user':
        booked_reservations=Reservation.query.filter_by(user_id=current_user.id).all()
        br_json=[]
        for br in booked_reservations:
            br_dict={}
            br_dict['id'] = br.id
            br_dict['username']=user.username
            br_dict['spot_id'] = br.spot_id
            br_dict['parking_time'] = br.parking_time.strftime('%Y-%m-%d %H:%M:%S')
            br_dict['leaving_time'] = br.leaving_time.strftime('%Y-%m-%d %H:%M:%S')
            br_dict['vehicle_no'] = user.vehicle_no
            br_dict['location']=br.spot.lot.address
            br_dict['reservation_status'] = br.reservation_status
            br_json.append(br_dict)
        return jsonify({
            "username": user.username,
            "user_id":user.id,
            "email": user.email,
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

@app.route("/api/user/lot_search", methods=['GET', 'POST'])
@jwt_required()
def user_search():
    def normalize(text):
        return text.lower().replace(" ", "") if text else ""

    data = request.get_json()
    criteria = data.get("criteria", "").strip().lower()
    search = data.get("search", "").strip().lower()


    # Fetch all lots
    all_lots = ParkingLot.query.all()
    filtered_lots = []

    # Normalize user input
    search_nospace = normalize(search)

    for lot in all_lots:
        # Get the field based on selected criteria
        if criteria == "pincode":
            value = lot.pin_code or ""
        elif criteria == "primelocation":
            value = lot.prime_location_name or ""
        elif criteria == "address":
            value = lot.address or ""
        else:
            value = f"{lot.address} {lot.prime_location_name}"  # fallback if no criteria

        value = str(value)
        value_clean = value.lower()
        value_nospace = normalize(value)

        if (
            not search or
            search in value_clean or              # regular substring match
            search_nospace in value_nospace       # match after removing spaces
        ):
            filtered_lots.append(lot)

    if not filtered_lots:
        return jsonify({"message": "No lots found"}), 404

    result = []
    for lot in filtered_lots:
        available = sum(1 for spot in lot.spots if spot.status == 'A')
        result.append({
            "id": lot.id,
            "address": lot.address,
            "availability": available
        })

    return jsonify({
        "message": "Lots Found",
        "result": result,
        "username": current_user.username
    }), 200



##USER BOOKING

@app.route("/api/user/booking/<int:lotid>",methods=['POST'])
@jwt_required()
def user_booking(lotid):
    available_spot = ParkingSpot.query.filter_by(lot_id=lotid, status='A').first()
    vehicle_no=request.json.get("vehicle_no",None)
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
    conflict = Reservation.query.filter(Reservation.spot_id == available_spot.id,Reservation.reservation_status == "Booked",Reservation.leaving_time > parking_time).first()

    if conflict:
        return jsonify({"message": "This spot is already booked during the selected time"}), 409

    parking_cost = available_spot.lot.price_per_hour * duration_in_hours
    reservation=Reservation(spot_id=available_spot.id,user_id=current_user.id,parking_time=parking_time,
                            leaving_time=leaving_time,parking_cost=parking_cost)
    available_spot.status = "B"
    db.session.add(reservation)
    db.session.commit()
    return jsonify({
        "message": "Booking successful",
        "reservation_id": reservation.id,
        "parking_cost": parking_cost,
        "username": current_user.username
    }), 201

# Reservation Data
@app.route("/api/user/get_reservation/<int:rvid>",methods=['GET','POST'])
@jwt_required()
def get_rv(rvid):
    reservation=Reservation.query.filter_by(id=rvid).first()
    if not reservation:
        return jsonify({"message": "No lots found"}), 404

    return ({
        "lotId":reservation.spot.lot.id,
            "vehicle_no":reservation.user.vehicle_no,
            "parking_time":reservation.parking_time,
            "leaving_time":reservation.leaving_time,
            "userId":reservation.user_id,
            "spotId":reservation.spot_id
    })










## USER UPDATE BOOKING

@app.route("/api/user/update_booking/<int:rvid>",methods=['Post'])
@jwt_required()
def update_booking(rvid):
    vehicle_no=request.json.get("vehicle_no",None)
    leaving_time=request.json.get("leaving_time",None)
    parking_time=request.json.get("parking_time",None)
    print(parking_time)
    parking_time = datetime.fromisoformat(parking_time)
    print(parking_time)
    leaving_time = datetime.fromisoformat(leaving_time)
    
    reservation=Reservation.query.filter_by(id=rvid).first()
    reservation.leaving_time=leaving_time
    reservation.parking_time=parking_time
    duration_in_hours = (leaving_time - parking_time).total_seconds() / 3600
    parking_cost = reservation.spot.lot.price_per_hour * duration_in_hours
    reservation.parking_cost=parking_cost
    db.session.commit()
    return jsonify({
        "message": "Booking updated",
        "reservation_id": reservation.id,
        "parking_cost": parking_cost
    }), 201


# ##USER CANCEL BOOKING
# @app.route("/api/user/cancel_booking/<int:rvid>",methods=['GET','POST'])
# @jwt_required()
# def cancel_booking(rvid):
#     cancel_time = datetime.utcnow()
#     reservation = Reservation.query.filter_by(id=rvid).first()
     
#     if reservation is None:
#         return jsonify({"message": "Reservation not found"}), 404
    
#     if reservation.parking_time < cancel_time and reservation.leaving_time > cancel_time:
#         return jsonify({"message": "Cannot cancel a past or active booking"}), 400
#     else:
#         spot=ParkingSpot.query.filter_by(id=reservation.spot_id).first()
#         spot.status='A'
#         db.session.delete(reservation) 
#         db.session.commit() 
#         return jsonify({"message": "Reservation cancelled successfully"}), 200



#Automatically updating bookeed to occupied status of reservation




##USER RELEASE PARKING SPOT
@app.route("/api/user/release_booking/<int:resid>",methods=['GET','POST'])
@jwt_required()
def release_spot(resid):
    reservation=Reservation.query.filter_by(id=resid).first()
    spot=ParkingSpot.query.filter_by(id=reservation.spot_id).first()
    spot.status='A'
    reservation.reservation_status='Released'
    now = datetime.now(pytz.timezone('Asia/Kolkata'))
    if now < reservation.leaving_time:
        reservation.leaving_time = now
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


#**************GET LOT***************
@app.route("/api/admin/get_lot/<int:lotid>")
@role_required("admin")
def get_lot(lotid):
    lot=ParkingLot.query.get(lotid)
    if not lot:
        return jsonify({"message": "Parking Lot not found"}), 404
    return jsonify({
        "prime_location_name": lot.prime_location_name,
        "price_per_hour": lot.price_per_hour,
        "address": lot.address,
        "pin_code": lot.pin_code,
        "no_of_spot": lot.number_of_spot
    })



#************ Edit LOT ************8

@app.route("/api/admin/update_lot/<int:lotid>",methods=['POST','PUT'])
@role_required("admin")
def edit_lot(lotid):
    print(lotid)
    print(request.get_json())
    data = request.get_json()
    if data is None:
        return jsonify({"message": "No JSON received"}), 400

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

@app.route("/api/admin/delete_lot/<int:lotid>",methods=['DELETE'])
@role_required("admin")
def delete_lot(lotid):
    print('indelete')
    lot=ParkingLot.query.filter_by(id=lotid).first()
    if not lot:
        return jsonify({"message": "Lot not found"}), 404
    no_of_occupied_spot=0
    for spot in lot.spots:
        if (spot.status=='O' or spot.status=='B') :
            no_of_occupied_spot+=1
    if no_of_occupied_spot==0:
        db.session.delete(lot)
        db.session.commit()
        return jsonify({"message":"Lot has been deleted Successfully"}),200
    else:
        return jsonify({"message":"Can not delete occupied lots"}),400
    
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

@app.route("/api/admin/delete_spot/<int:spotid>",methods=['GET','POST'])
@role_required("admin")
def delete_spot(spotid):
    spot=ParkingSpot.query.get(spotid)
    if not spot:
        return jsonify({"message": "Parking Spot not found"}), 404
    
    if spot.status in ['O','B']:
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
            user_dict['vehicle_no']=user.vehicle_no
            user_dict['no_of_reservations']=len(user.reservations)
            user_json.append(user_dict)
        return jsonify(user_json)
    else:
        return jsonify({"message":"There are not any User registered"})
    




#************** Lot details **********

@app.route("/api/admin/lot_search", methods=['POST'])
@role_required('admin')
def admin_lot_search():
    data = request.get_json()
    criteria = data.get("criteria", "").strip().lower()
    search = data.get("search", "").strip().lower()

    # Filter logic
    if criteria and search:
        if criteria == "pincode":
            lots = ParkingLot.query.filter(ParkingLot.pin_code.ilike(f"%{search}%")).all()
        elif criteria == "primelocation":
            lots = ParkingLot.query.filter(ParkingLot.prime_location_name.ilike(f"%{search}%")).all()
        elif criteria == "address":
            lots = ParkingLot.query.filter(ParkingLot.address.ilike(f"%{search}%")).all()
        else:
            return jsonify({"message": "Invalid search criteria"}), 400
    else:
        # No filter — return all lots
        lots = ParkingLot.query.all()

    if not lots:
        return jsonify({"message": "No lots found"}), 404

    # Serialize the lot data
    lot_json = []
    for lot in lots:
        lot_dict = {
            'id': lot.id,
            'address': lot.address,
            'prime_address': lot.prime_location_name,
            'spots': [],
            'occupied': 0
        }

        for spot in lot.spots:
            spot_info = {
                'id': spot.id,
                'status': spot.status
            }

            if spot.status == 'O':
                lot_dict['occupied'] += 1
                reservation = Reservation.query.filter_by(spot_id=spot.id).first()
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

        lot_json.append(lot_dict)

    return jsonify(results=lot_json)




#Summary
@app.route('/api/most_occupied_lots', methods=['GET'])
@role_required('admin')
def most_occupied_lots():
    lots = ParkingLot.query.all()
    lot_data = []

    for lot in lots:
        occupied = sum(1 for spot in lot.spots if spot.status == 'O')
        lot_data.append((lot.prime_location_name, occupied))

    # Sort by most occupied
    sorted_data = sorted(lot_data, key=lambda x: x[1], reverse=True)[:5]

    return jsonify({
        "labels": [x[0] for x in sorted_data],
        "values": [x[1] for x in sorted_data],
        "label": "Occupied Spots",
        "bgColors": ['rgba(255, 99, 132, 0.6)'] * len(sorted_data),
        "title": "Top 5 Most Occupied Lots"
    })


@app.route('/api/least_used_lots', methods=['GET'])
@role_required('admin')
def least_used_lots():
    lots = ParkingLot.query.all()
    lot_data = []

    for lot in lots:
        occupied = sum(1 for spot in lot.spots if spot.status == 'O')
        lot_data.append((lot.prime_location_name, occupied))

    # Sort by least occupied
    sorted_data = sorted(lot_data, key=lambda x: x[1])[:5]

    return jsonify({
        "labels": [x[0] for x in sorted_data],
        "values": [x[1] for x in sorted_data],
        "label": "Occupied Spots",
        "bgColors": ['rgba(153, 102, 255, 0.6)'] * len(sorted_data),
        "title": "Top 5 Least Used Lots"
    })

@app.route('/api/lots_by_price_range', methods=['GET'])
@role_required('admin')
def lots_by_price_range():
    lots = ParkingLot.query.all()
    
    ranges = {
        'Low (<= ₹30)': 0,
        'Medium (₹31-₹50)': 0,
        'High (> ₹50)': 0
    }

    for lot in lots:
        if lot.price_per_hour <= 30:
            ranges['Low (<= ₹30)'] += 1
        elif lot.price_per_hour <= 50:
            ranges['Medium (₹31-₹50)'] += 1
        else:
            ranges['High (> ₹50)'] += 1

    return jsonify({
        "labels": list(ranges.keys()),
        "values": list(ranges.values()),
        "label": "Lots Count",
        "bgColors": [
            "rgba(75, 192, 192, 0.6)",
            "rgba(255, 206, 86, 0.6)",
            "rgba(255, 159, 64, 0.6)"
        ],
        "title": "Lots by Price Range"
    })


@app.route('/api/lots_by_location', methods=['GET'])
@role_required('admin')
def lots_by_location():
    lots = ParkingLot.query.all()
    location_counts = {}

    for lot in lots:
        location = lot.prime_location_name
        location_counts[location] = location_counts.get(location, 0) + 1

    return jsonify({
        "labels": list(location_counts.keys()),
        "values": list(location_counts.values()),
        "label": "Lots Count",
        "bgColors": ['rgba(255, 205, 86, 0.6)'] * len(location_counts),
        "title": "Total Lots by Prime Location"
    })


@app.route('/api/user/lots_by_status',methods=['GET'])
@jwt_required()
def lot_by_status():
    user=User.query.get(current_user.id)
    reservation=Reservation.query.filter_by(user_id=user.id).all()
    occupied=Reservation.query.filter_by(user_id=user.id,reservation_status='Occupied').count()
    booked=Reservation.query.filter_by(user_id=user.id,reservation_status='Booked').count()
    released=Reservation.query.filter_by(user_id=user.id,reservation_status='Released').count()
    return jsonify({
        "title": "Your Parking by Status",
        "label": "Reservations",
        "labels": ["Occupied", "Booked", "Released"],
        "values": [occupied, booked, released],
        "bgColors": ["#ef4444", "#facc15", "#10b981"]
    })

@app.route('/api/user/total_hours_by_status', methods=['GET'])
@jwt_required()
def user_hours_by_status():
    statuses = ['Booked', 'Occupied', 'Released']
    labels = []
    values = []

    for status in statuses:
        reservations = Reservation.query.filter_by(user_id=current_user.id, reservation_status=status).all()
        total_hours = sum([(r.leaving_time - r.parking_time).total_seconds() / 3600 for r in reservations])
        labels.append(status)
        values.append(round(total_hours, 2))

    return jsonify({
        "title": "Total Reserved Hours by Status",
        "label": "Hours",
        "labels": labels,
        "values": values,
        "bgColors": ["#3498db", "#2ecc71", "#e74c3c"]
    })


# BACKENED JOBS
@app.route('/export_csv/<int:user_id>', methods=['GET'])
def trigger_csv_export(user_id):
    task = csv_report.delay(user_id)
    return jsonify({
        "status": "CSV export task has been started",
        "task_id": task.id
    })



@app.route('/task_status/<task_id>', methods=['GET'])
def get_task_status(task_id):
    task = AsyncResult(task_id)
    return send_from_directory('static/reports',task.result)

#Profile Handling
# Profile API for Vue frontend
@app.route('/api/profile/<int:user_id>')
@jwt_required()
def get_user_profile(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    all_reservations = Reservation.query.filter_by(user_id=user_id).order_by(Reservation.parking_time.desc()).all()
    total_reservations = len(all_reservations)
    active_reservations = sum(1 for r in all_reservations if r.reservation_status == "Booked")
    total_amount_spent = round(sum(r.parking_cost for r in all_reservations), 2)

    recent_reservations = [
        {
            "lot_name": r.spot.lot.prime_location_name,
            "spot_id": r.spot_id,
            "parking_time": r.parking_time.strftime("%Y-%m-%d %H:%M"),
            "leaving_time": r.leaving_time.strftime("%Y-%m-%d %H:%M"),
            "parking_cost": r.parking_cost,
            "reservation_status": r.reservation_status
        }
        for r in all_reservations[:5]
    ]

    return jsonify({
        "user": {
            "id": user.id,
            "name": user.username,
            "email": user.email,
            "vehicle_no": user.vehicle_no
        },
        "total_reservations": total_reservations,
        "active_reservations": active_reservations,
        "total_amount_spent": total_amount_spent,
        "recent_reservations": recent_reservations
    })


