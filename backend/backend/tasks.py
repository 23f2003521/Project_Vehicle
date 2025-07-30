from celery import shared_task
import csv
from collections import Counter
from jinja2 import Template
from .email import send_email
from .models import Reservation, User , ParkingLot , ParkingSpot
from datetime import datetime, timedelta,date
import pytz
import requests
import os
from .database import db
from app import create_app 
from pytz import timezone

app = create_app()
#task1 User Triggered Async Job - Export as CSV - Devise a CSV format details for the parking spots used by the user till date
@shared_task(ignore_results=False,name="Download_CSV_report")
def csv_report(user_id):
    kolkata = pytz.timezone('Asia/Kolkata')
    now_kolkata = datetime.now(kolkata)
    reservations = Reservation.query.filter_by(user_id=user_id).all()
    if not reservations:
        return f"No reservation data found for user_id {user_id}"

    csv_file_name = f"user_{user_id}_{now_kolkata.strftime('%d-%m-%y_%H-%M')}.csv"
    with open(f'static/reports/{csv_file_name}', 'w', newline = "") as csvfile:
    # Write to CSV
        sr_no=0
        writer = csv.writer(csvfile,delimiter=',')
        writer.writerow(['Sr No','Reservation ID', 'Lot Address', 'Spot ID', 'Status', 'Entry Time', 'Exit Time'])
        for r in reservations:
            sr_no+=1
            writer.writerow([
                sr_no,
                r.id,
                r.spot.lot.address,  # adjust as per relationship
                r.spot_id,
                r.reservation_status,
                r.parking_time.strftime('%Y-%m-%d %H:%M:%S') if r.parking_time else 'N/A',
                r.leaving_time.strftime('%Y-%m-%d %H:%M:%S') if r.leaving_time else 'N/A',
            ])

    return csv_file_name



#task 2    Scheduled Job - Monthly Activity Report - Devise a monthly report for the user created using HTML and sent via mail.
@shared_task(ignore_results=False, name="monthly_report")
def monthly_report():

    today = datetime.today()
    first_day = today.replace(day=1)

    users = User.query.all()
    for user in users:
        user_data = {}
        user_data['username'] = user.username
        user_data['email'] = user.email
        details = []

        # Filter reservations of this user in the current month
        reservations = Reservation.query.filter(
            Reservation.user_id == user.id,
            Reservation.parking_time >= first_day,
            Reservation.parking_time <= today
        ).all()

        if not reservations:
            continue  # Skip if no data for the user

        lot_usage = Counter()
        total_spent = 0

        for r in reservations:
            lot_name = r.spot.lot.prime_location_name

            lot_usage[lot_name] += 1
            total_spent += r.parking_cost if r.parking_cost else 0

            details.append({
                "lot": lot_name,
                "spot_id": r.spot.id if r.spot else "N/A",
                "entry": r.parking_time.strftime("%Y-%m-%d %H:%M"),
                "exit": r.leaving_time.strftime("%Y-%m-%d %H:%M"),
                "cost": f"Rs {r.parking_cost:.2f}",
                "status": r.reservation_status
            })

        most_used_lot = lot_usage.most_common(1)[0][0] if lot_usage else "N/A"
        user_data["details"] = details
        user_data["total_bookings"] = len(reservations)
        user_data["most_used_lot"] = most_used_lot
        user_data["total_spent"] = f"Rs {total_spent:.2f}"
        

        # exampleoutput
        # userdata{
        #     "username": "preeti",
        #     "email": "preeti@example.com",
        #     "total_bookings": 4,
        #     "most_used_lot": "Lot A",
        #     "total_spent": "₹120.00",
        #     "details": [...]  # ← this is a list of dictionaries
        # }

        mail_template = """
        <h3>Dear {{user_data.username}},</h3>
        <p>Here is your <strong>monthly parking activity report</strong> for {{today.strftime('%B %Y')}}:</p>
        <ul>
            <li><strong>Total Bookings:</strong> {{user_data.total_bookings}}</li>
            <li><strong>Most Used Parking Lot:</strong> {{user_data.most_used_lot}}</li>
            <li><strong>Total Amount Spent:</strong> {{user_data.total_spent}}</li>
        </ul>
        <p>Booking Details:</p>
        <table border="1" cellpadding="5" cellspacing="0">
            <tr>
                <th>Lot Name</th>
                <th>Spot ID</th>
                <th>Entry Time</th>
                <th>Exit Time</th>
                <th>Cost</th>
                <th>Status</th>
            </tr>
            {% for detail in user_data.details %}
            <tr>
                <td>{{detail.lot}}</td>
                <td>{{detail.spot_id}}</td>
                <td>{{detail.entry}}</td>
                <td>{{detail.exit}}</td>
                <td>{{detail.cost}}</td>
                <td>{{detail.status}}</td>
            </tr>
            {% endfor %}
        </table>
        <br>
        <p>Thank you for using our parking system!</p>
        <h5>Smart Parking Team</h5>
        """

        message = Template(mail_template).render(user_data=user_data, today=today)
        send_email(user.email, subject="Monthly Parking Report - Smart Parking", message=message)

    return "Monthly reports sent"




    #task 3 daily reminders

    
@shared_task(ignore_results=False, name="daily_parking_reminder")
def daily_parking_reminder():
    with app.app_context():
        today = date.today()
        users = User.query.filter_by(type="user").all()

    # Check if any lot is added today
        new_lot_added = ParkingLot.query.filter(
            db.func.date(ParkingLot.created_at) == today  # if id is auto increment, you can alternatively add a created_at column
        ).count() > 0

        for user in users:
        # Check if user has booked today
            has_booked_today = Reservation.query.filter(
                Reservation.user_id == user.id,
                db.func.date(Reservation.parking_time) == today
            ).count() > 0

        # If user hasn't booked today OR a new lot is added, send reminder
            if not has_booked_today or new_lot_added:
                message = f"""
                Hi {user.username}, 

                This is your daily parking reminder. 
            
                - You haven't booked a parking spot today. 🚗
                -{' A new parking lot is available for booking. 🅿️' if new_lot_added else ''}

                Book now if needed: http://127.0.0.1:5173

                – Smart Parking System
                """

            # POST to Google Chat webhook
            
                webhook_url = "https://chat.googleapis.com/v1/spaces/AAQATX3CHF0/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=ph7AEMOE5r11BiMGMYNQAAQGMzYZ0k2SmZDhF06ZVVs"
                payload = {"text": message.strip()}
                response = requests.post(webhook_url, json=payload)
                print(f"Sent to {user.username}: Status {response.status_code}")

        return "Daily reminders sent."
    



@shared_task(ignore_results=False, name="update_booked_to_occupied")
def update_booked_to_occupied():
    print("[TASK STARTED] update_booked_to_occupied")
    with app.app_context():
        now = datetime.now(pytz.timezone('Asia/Kolkata'))
        two_minutes_ago = now + timedelta(minutes=5)
        print(f"[Task Start] Checking bookings between {two_minutes_ago} and {now}")
        # Find reservations where parking time has come and still status is "Booked"
        reservations_to_update = Reservation.query.filter(
            Reservation.reservation_status == 'Booked',
            Reservation.parking_time <= two_minutes_ago
        ).all()
        print(f"[Found] {len(reservations_to_update)} reservations to update")
        for reservation in reservations_to_update:
            print(f"Updating reservation ID {reservation.id} to 'Occupied'")
            reservation.reservation_status = 'Occupied'
            if reservation.spot:
                print(f" -> Spot ID {reservation.spot.id} set to 'O'")
                reservation.spot.status = 'O'

        db.session.commit()
        print("[Commit] Changes committed to DB")
        return f"{len(reservations_to_update)} reservations updated to Occupied"
    

#Handling Overstays
@shared_task(ignore_results=False, name="handle_overstays")
def handle_overstays():
    print("[TASK STARTED] handle_overstays")
    with app.app_context():
        tz = timezone('Asia/Kolkata')
        now = datetime.now(tz)
        # === GRACE PERIOD SETUP ===
        # grace_period = timedelta(hours=24)  # ✅ Actual overstay limit: 24 hours

        # For testing, change to 5 minutes like this:
        grace_period = timedelta(minutes=5)

        # === GET ALL OCCUPIED RESERVATIONS ===
        occupied_reservations = Reservation.query.filter(
            Reservation.reservation_status == 'Occupied'
        ).all()

        overstayed_reservations = []

        for res in occupied_reservations:
            if res.leaving_time.tzinfo is None:
                leaving_time = tz.localize(res.leaving_time)
            else:
                leaving_time = res.leaving_time

            # If current time is more than (leaving_time + grace), it’s overstayed
            if now > (leaving_time + grace_period):
                overstayed_reservations.append(res)

        print(f"[INFO] Found {len(overstayed_reservations)} overstayed reservations")
        
        for res in overstayed_reservations:
            if res.leaving_time.tzinfo is None:
                leaving_time = tz.localize(res.leaving_time)
            else:
                leaving_time = res.leaving_time
            spot = ParkingSpot.query.get(res.spot_id)
            user = User.query.get(res.user_id)
            lot = ParkingLot.query.get(spot.lot_id)

            penalty_per_hour = lot.price_per_hour
            hours_overstayed = (now - (leaving_time + grace_period)).total_seconds() / 3600
            print(hours_overstayed)
            penalty = int(hours_overstayed * penalty_per_hour)

            print(f"[PENALTY] User {user.username} overstayed {hours_overstayed} hour(s) at Lot {lot.prime_location_name}, Spot {spot.id}. Penalty: ₹{penalty}")

            res.parking_cost += penalty
            res.reservation_status = "Released"
            spot.status = "A"

            html_template = """
            <h3>Dear {{ username }},</h3>
            <p><strong>Notice:</strong> You have exceeded your parking time by more than <strong>{{ hours_overstayed }}</strong> hours at <strong>{{ lot_name }}</strong>.</p>

            <p>Your reservation details:</p>
            <ul>
                <li><strong>Spot ID:</strong> {{ spot_id }}</li>
                <li><strong>Scheduled Exit:</strong> {{ leaving_time }}</li>
                <li><strong>Current Time:</strong> {{ now }}</li>
                <li><strong>Overstayed by:</strong> {{ hours_overstayed }} hour(s)</li>
                <li><strong>Penalty Cost:</strong> ₹{{ penalty }}</li>
            </ul>

            <p>Please vacate the spot immediately and clear any pending dues.</p>
            <p>If you've already left, please ignore this message.</p>

            <br>
            <p>Regards,</p>
            <h5>Smart Parking Team</h5>
            """

            rendered_html = Template(html_template).render(
                username=user.username,
                lot_name=lot.prime_location_name,
                spot_id=spot.id,
                leaving_time=res.leaving_time.strftime("%Y-%m-%d %H:%M"),
                now=now.strftime("%Y-%m-%d %H:%M"),
                hours_overstayed=hours_overstayed,
                penalty=penalty
            )

            print(f"[EMAIL] Sending email to {user.email}")
            send_email(user.email, subject="Overstay Penalty Notice – Smart Parking", message=rendered_html)

        db.session.commit()
        print("[COMMIT] All penalties applied and reservations updated")

        return f"{len(overstayed_reservations)} overstay notices sent."