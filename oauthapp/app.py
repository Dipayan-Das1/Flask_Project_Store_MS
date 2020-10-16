from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError
from dotenv import load_dotenv
load_dotenv(".env")

from oauthapp.db import db
from oauthapp.ma import ma
from oauthapp.resources.user import UserLogin, UserRegister, User
from oauthapp.oauth import oauth
from oauthapp.resources.github_login import GitHubLoginResource, GitHubAuthorizedResource, SetPasswordResource
#pip install Flask-OAuthLib

app = Flask(__name__)

app.config.from_object("default_config")
app.config.from_envvar("APPLICATION_SETTINGS")
api = Api(app)
jwt = JWTManager(app)


@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(GitHubLoginResource,"/login/github")
api.add_resource(GitHubAuthorizedResource,"/login/github/authorized",endpoint="github.authorized")
api.add_resource(SetPasswordResource,"/user/password")

if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    oauth.init_app(app)
    app.run(port=5000)
