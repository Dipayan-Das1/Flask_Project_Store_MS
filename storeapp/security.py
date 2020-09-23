from storeapp.models.usermodel import UserModel


def authenticate(username,password):
    "used by jwt to authorize the user"
    user = UserModel.find_by_name(username)
    if user and user.password == password:
        return user


def identity(payload):
    "used by jwt to fetch the user details"
    user = UserModel.find_by_id(payload['identity'])
    if user:
        return user
