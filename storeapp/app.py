from flask import Flask
from flask_restful import Api,Resource
from storeapp.resources.userresource import UserRegister, User, UserLogin, TokenRefresh,LogoutResource
from storeapp.resources.confirmationresource import ConfirmationResource, ResendConfirmationresource
from storeapp.resources.storeresource import Store
from storeapp.resources.itemresource import Item
from storeapp.resources.imageresource import ImageResource, ImageUploadResource
#from flask_jwt import JWT
from flask_jwt_extended import JWTManager, get_jwt_identity
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
#pip install python-doyenv
from dotenv import load_dotenv
#pip install marshamallow,flask-marshmallow, sqlalchemy-marshamllow
import storeapp.default_config

#pip install flask-uploads
from storeapp.flaskmarshmallow import flask_marshmallow

from flask_uploads import patch_request_class, configure_uploads
from storeapp.images.processor import IMAGE_SET

##initialize flask app
app = Flask(__name__)

#initialize flask restful api
api = Api(app)
load_dotenv(".env",verbose=True)
app.config.from_object("default_config")
app.config.from_envvar("APPLICATION_SETTINGS")
patch_request_class(app,10*1024*1024)
configure_uploads(app,IMAGE_SET)
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
api.add_resource(ConfirmationResource,"/confirm/<string:token>")
api.add_resource(ResendConfirmationresource,"/resend-confirm/<string:email_id>")
api.add_resource(ImageUploadResource,"/image/upload/<string:userid>")
api.add_resource(ImageResource,"/image/<string:filename>")

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