from flask import Flask
from backend.database import db,migrate
from backend.models import User
from backend.config import LocalDevelopmentConfig 

from backend.security import jwt
from flask_cors import CORS

from backend.celery import celery_init_App
from celery.schedules import crontab
from flask_caching import Cache


app=None
cache = Cache()
def create_app():
    app=Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    CORS(app, origins=["http://localhost:5173"], supports_credentials=True)
    app.config['CACHE_TYPE'] = 'SimpleCache'  # In-memory
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # default timeout (optional)
    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    # datastore=SQLAlchemyUserDatastore(db, User, Role)
    jwt.init_app(app)
    app.app_context().push()
    return app


app=create_app()
celery=celery_init_App(app)
celery.autodiscover_tasks()

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # Task 1: Monthly report on 2nd of every month at midnight
    sender.add_periodic_task(
        crontab(minute='*/2'),
        # crontab(0, 0, day_of_month='2'),
        monthly_report.s(),
        name="Monthly Report"
    )

    # Task 2: Daily parking reminder at 7:10 PM
    sender.add_periodic_task(
        crontab(minute='*/2'),
        daily_parking_reminder.s(),
        name='Daily Parking Reminder at 7:10 PM'
    )

    # Task 3: Every 2 minutes - update booked to occupied
    sender.add_periodic_task(
        crontab(minute='*/2'),
        update_booked_to_occupied.s(),
        name="Update Booked to Occupied"
    )

    # Task 4: Every 2 minutes - handle overstays
    sender.add_periodic_task(
        crontab(minute='*/2'),
        handle_overstays.s(),
        name="Handle Overstays"
    )
# #creating default users and serive entries into db.
# with app.app_context():
#     db.create_all()
    
    # app.security.datastore.find_or_create_role(name="admin",description="super user of app")
    # app.security.datastore.find_or_create_role(name="professional",description="service professional of app")
    # app.security.datastore.find_or_create_role(name="customer",description="customer of app")
    # db.session.commit()

    # if not app.security.datastore.find_user(email="user0@admin.com"):
    #     app.security.datastore.create_user(name="admin",
    #                                        email="user0@admin.com",
    #                                        password=hash_password("1234"),
    #                                        roles=['admin'])

    # if not app.security.datastore.find_user(email="user1@user.com"):
    #     app.security.datastore.create_user(name="user01",
    #                                        email="user1@user.com",
    #                                        password=hash_password("1234"),
    #                                        roles=["professional"])


    # if not app.security.datastore.find_user(email="user2@user.com"):
    #     app.security.datastore.create_user(name="user02",
    #                                        email="user2@user.com",
    #                                        password=hash_password("1234"),
    #                                        roles=["customer"])                                          
    # db.session.commit()
 

from backend.controllers import *

if __name__=="__main__":
    app.run() 