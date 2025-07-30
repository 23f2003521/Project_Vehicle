# from flask_restful import Api , Resource , reqparse
# from .models import *
# from flask_security import auth_required, roles_required ,roles_accepted, current_user

# api=Api()

# def roles_list(roles):
#     role_list=[]
#     for role in roles:
#         roles_list.append(role.name)
#     return roles_list

# class ServiceApi(Resource):
#     def get(self):
#         service=[]
#         service_json=[]
#          #user.trans => jsonify([{},{}])
#         if "admin" in roles_list(current_user.roles):
#             service=Service.query.all()
#         else:
#             transcation=current_user.            