from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, fresh_jwt_required
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt
from flask import Request
from storeapp.models.usermodel import UserModel
from storeapp.blacklist import BLACKLIST_JTI
from storeapp.schemas.userschema import UserSchema
from marshmallow import ValidationError
from storeapp.mail import emailsender

REQUIRED_FIELD = "{} is mandatory"
user_schema = UserSchema()

class UserRegister(Resource):
    """This class is a resource class to be used for user registration"""

    USER_EXISTS = "User with name {} already exists"
    USER_CREATED = "User created"
    USER_CREATED_MAIL_SENT = "User created successfully. To complete registration click on the link sent in registration mail"
    USER_CREATION_FAILED = "User creation failed"


    @classmethod
    def post(cls):
        """register user post method"""
        try:
            user_data = user_schema.load(request.get_json())
        except ValidationError as ve:
            return ve.messages,400
        print(user_data)
        print(type(user_data))
        userModel = UserModel.find_by_name(user_data.username)
        if userModel:
            return {"message":cls.USER_EXISTS.format(user_data.username)},400
        userModel = UserModel.find_by_email(user_data.email)
        if userModel:
            return {"message":cls.USER_EXISTS.format(user_data.email)},400
        else:
            try:
                user_data.save_to_db()
                link = "http://localhost:5000/confirm/" + str(user_data.id)
                emailsender.send_email_confirmation(["dipayan1.das@gmail.com"],"Registration Confirmation","Please confirm your mail by clicking on this link, <a href='"+link+"'>"+link+"</a>")
                return {"message": cls.USER_CREATED}, 201
            except emailsender.MailGunException as e:
                user_data.delete()
                return {"message": cls.USER_CREATION_FAILED}, 500
            except Exception as e:
                print(e)
                return {"message": cls.USER_CREATION_FAILED}, 500


class User(Resource):
    """For managing application users"""

    USER_DELETED = "User deleted successfully"
    USER_NOT_FOUND = "User not found"

    @classmethod
    @fresh_jwt_required
    def delete(cls,userid):
        user = UserModel.find_by_id(userid)
        if (user):
            user.delete()
            return {"message":cls.USER_DELETED}, 200
        else:
            return {"message": cls.USER_NOT_FOUND}, 400

    @classmethod
    @jwt_required
    def get(cls,userid):
        user = UserModel.find_by_id(userid)
        print(user);
        if(user):
            return user_schema.dump(user),200
        else:
            return {"message":cls.USER_NOT_FOUND},400

class UserLogin(Resource):

    def post(self):
        try:
            user_data = user_schema.load(request.get_json(),partial=("mail",))
        except ValidationError as ve:
            return ve.messages,400

        user = UserModel.find_by_name(user_data.username)
        print(user.id)
        if user  and user.password == user_data.password and user.activated:
            access_token =create_access_token(identity=user.id,fresh=True)
            refresh_token = create_refresh_token((user.id))
            #refresh token is a token that can be used when the original token has expired, dont allow access to sensitive resources
            #using this token, then again ask to reauthenticate
            return {"access_token":access_token,"refresh_token":refresh_token}
        elif not  user.activated:
            return {"message": "User has not been activated till now"}, 400
        else:
            return {"message":"invalid credentials"},401


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

from flask import  make_response, render_template

class UserConfirmationResource(Resource):

    @classmethod
    def get(cls,userid:int):
        user = UserModel.find_by_id(userid)
        if(user):
            user.activated = True
            user.save_to_db()
            return make_response(render_template('confirmation_page.html',email=user.email),200, {"Content-Type":"text/html"})
        else:
            return {"message": cls.USER_NOT_FOUND}, 400


