from flask import Flask
from flask_restful import Api,Resource
from storeapp.resources.userresource import UserRegister, User, UserLogin, TokenRefresh,LogoutResource
from storeapp.resources.storeresource import Store
from storeapp.resources.itemresource import Item
#from flask_jwt import JWT
from flask_jwt_extended import JWTManager, get_jwt_identity
#from storeapp.security import authenticate,identity

##initialize flask app
app = Flask(__name__)

#initialize flask restful api
api = Api(app)

#initialize db config
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
##Needed for 401 exceptions
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access','refresh']

#initialize jwt security
app.secret_key = "secret@111"
jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    print("call add claims to jwt")
    if identity == 1:
        return {"isadmin":True}
    else:
        return {"isadmin": True}

@jwt.expired_token_loader
def token_expired_callback():
    """to customize the expired token message"""
    return {"message":"Access token has expired . Please login back"},401

@jwt.invalid_token_loader
def invalid_token_callback():
    return {"message": "Access token is invalid . Please provide the correct token"}, 401

@jwt.unauthorized_loader
def unauthorized_callback():
    return {"message": "JWT token is needed to access this endpoint. Please pass JWT token"}, 401

@jwt.needs_fresh_token_loader
def fresh_token_needed_callback():
    return {"message": "Fresh token needed. Please login again"}, 401

@jwt.revoked_token_loader
def token_revoked_callback():
    return {"message": "Token has been revoked. User has been logged out already, Please login back"}, 401

@jwt.token_in_blacklist_loader
def token_inblacklist(decrypted_token):
    from storeapp.blacklist import BLACKLIST_IDS,BLACKLIST_JTI
    user = decrypted_token['identity']
    ##will invoke revoked_token_loader if true
    if user in BLACKLIST_IDS:
        return True
    jti_id = decrypted_token['jti']
    if jti_id in BLACKLIST_JTI:
        return True






#configure resources
api.add_resource(UserRegister,"/register")
api.add_resource(Store,"/store/<string:name>")
api.add_resource(Item,"/store/<string:store_name>/item/<string:item_name>")
api.add_resource(User,"/user/<int:userid>")
api.add_resource(UserLogin,"/login")
api.add_resource(TokenRefresh,"/refresh")
api.add_resource(LogoutResource,"/logout")

#flask decorator to setup before first request executes
@app.before_first_request
def create_db():
    db.create_all()



#start app
if __name__ == '__main__':
    from storeapp.db import db
    db.init_app(app)
    app.run(port=5000,debug=True)