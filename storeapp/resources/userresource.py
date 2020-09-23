from flask_restful import Resource, reqparse
from flask import Request
from storeapp.models.usermodel import UserModel

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
            return {"message":"User with name {} already exists".format(username_arg)},404
        else:
            userModel = UserModel(args["username"],args["password"])
            userModel.save_to_db()
            return {"message":"User created"}, 201
