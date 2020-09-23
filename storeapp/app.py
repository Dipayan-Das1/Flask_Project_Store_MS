from flask import Flask
from flask_restful import Api,Resource
from storeapp.resources.userresource import UserRegister
from storeapp.resources.storeresource import Store
from storeapp.resources.itemresource import Item
from flask_jwt import JWT
from storeapp.security import authenticate,identity

##initialize flask app
app = Flask(__name__)

#initialize flask restful api
api = Api(app)

#initialize db config
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#initialize jwt security
app.secret_key = "secret@111"
jwt = JWT(app,authenticate,identity)

#configure resources
api.add_resource(UserRegister,"/register")
api.add_resource(Store,"/store/<string:name>")
api.add_resource(Item,"/store/<string:store_name>/item/<string:item_name>")

#flask decorator to setup before first request executes
@app.before_first_request
def create_db():
    db.create_all()

#start app
if __name__ == '__main__':
    from storeapp.db import db
    db.init_app(app)
    app.run(port=5000,debug=True)