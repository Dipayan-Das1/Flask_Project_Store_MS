from flask import Flask
from flask_restful import Api,Resource
from storeapp.resources.userresource import UserRegister, User, UserLogin, TokenRefresh,LogoutResource
from storeapp.resources.storeresource import Store
from storeapp.resources.itemresource import Item
#from flask_jwt import JWT
from flask_jwt_extended import JWTManager, get_jwt_identity
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

#pip install marshamallow,flask-marshmallow, sqlalchemy-marshamllow

from storeapp.flaskmarshmallow import flask_marshmallow

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

@app.errorhandler(SQLAlchemyError)
def handleValidationError(err):
    return {"message":"Database threw an error"}, 500

#start app
if __name__ == '__main__':
    from storeapp.db import db
    db.init_app(app)
    flask_marshmallow.init_app(app)
    app.run(port=5000,debug=True)