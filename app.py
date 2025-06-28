from flask import Flask
from backend.database import db
from backend.models import User
from backend.config import LocalDevelopmentConfig 

from backend.security import jwt

app=None

def create_app():
    app=Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    # datastore=SQLAlchemyUserDatastore(db, User, Role)
    jwt.init_app(app)
    app.app_context().push()
    return app


app=create_app()

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