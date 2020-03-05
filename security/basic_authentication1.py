from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

from model.user1 import User
from errors1 import ApplicationError

def get_password_hash(password):
    return generate_password_hash(password)


def __verify_password(name, password):
    user = None
    try:
        user = User.find_by_name(name)
    except ApplicationError as err:
        if err.status_code != 404:
            raise err

    return user is not None and check_password_hash(user.password, password)


def init_basic_auth():
    auth = HTTPBasicAuth()
    auth.verify_password(__verify_password)
    return auth
