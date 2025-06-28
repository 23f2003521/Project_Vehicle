from flask_jwt_extended import JWTManager
from backend.models import User

jwt=JWTManager()


@jwt.user_identity_loader
def load_user_identity(user):
    return user.username


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    user = User.query.filter_by(username=identity).one_or_none()
    return user