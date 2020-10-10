from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt
from flask import Request
from storeapp.models.usermodel import UserModel
from storeapp.blacklist import BLACKLIST_JTI

class UserRegister(Resource):
    """This class is a resource class to be used for user registration"""

    parser = reqparse.RequestParser()
    parser.add_argument("username",type=str,required=True,help="Username is mandatory")
    parser.add_argument("password", type=str, required=True, help="Password is mandatory")

    def post(self):
        """register user post method"""
        args = UserRegister.parser.parse_args()
        username_arg = args["username"]
        userModel = UserModel.find_by_name(username_arg)
        if userModel:
            return {"message":"User with name {} already exists".format(username_arg)},400
        else:
            userModel = UserModel(args["username"],args["password"])
            userModel.save_to_db()
            return {"message":"User created"}, 201


class User(Resource):
    """For managing application users"""
    @jwt_required
    def delete(self,userid):
        user = UserModel.find_by_id(userid)
        if (user):
            user.delete()
            return {"message":"User deleted successfully"}, 200
        else:
            return {"message": "User not found"}, 400


    @jwt_required
    def get(self,userid):
        print("Inside get method")
        user = UserModel.find_by_id(userid)
        print(user);
        if(user):
            return user.json_secure(),200
        else:
            return {"message":"User not found"},400



class UserLogin(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str, required=True, help="Username is mandatory")
    parser.add_argument("password", type=str, required=True, help="Password is mandatory")

    def post(self):
        print("inside login")
        args = UserLogin.parser.parse_args()
        user = UserModel.find_by_name(args["username"])
        print(user.id)
        if user and user.password == args["password"]:
            access_token =create_access_token(identity=user.id,fresh=True)
            refresh_token = create_refresh_token((user.id))
            #refresh token is a token that can be used when the original token has expired, dont allow access to sensitive resources
            #using this token, then again ask to reauthenticate
            return {"access_token":access_token,"refresh_token":refresh_token}
        else:
            return {"invalid credentials"},401


class TokenRefresh(Resource):

    @jwt_refresh_token_required
    def post(self):
        """this endpoint is going to return a  access token that is not fresh
            in post refresh_token must be passed"""
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token":access_token}


class LogoutResource(Resource):

    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti'] ##gives back jti  (JWT id) unique jwt identityfier
        BLACKLIST_JTI.add(jti)
        return {"message":"User successfully logged out"}
