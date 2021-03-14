from flask_restful import Resource
from oauthapp.oauth import github
from flask import g, request, url_for
from oauthapp.models.user import UserModel
from flask_jwt_extended import create_access_token, create_refresh_token, fresh_jwt_required
from oauthapp.schemas.user import UserSchema

class GitHubLoginResource(Resource):

    @classmethod
    def get(cls):
        url = url_for("github.authorized",_external=True)
        print(url)
        return github.authorize(callback=url)

class GitHubAuthorizedResource(Resource):

    @classmethod
    def get(cls):
        resp = github.authorized_response()
        if resp is None or resp.get('access_token') is None:
            error_response ={"error":request.args["error"]}
            return error_response,401
        g.access_token = resp['access_token']
        github_user = github.get('user',)
        github_username = github_user.data['login']
        user = UserModel.find_by_username(github_username)
        if not user:
            user = UserModel(username=github_username,password=None)
            user.save_to_db()
        print(user.id)
        access_token = create_access_token(identity=user.id,fresh=True)
        refresh_token = create_refresh_token(identity=user.id)

        return {"access_token": access_token, "refresh_token": refresh_token}, 200


class SetPasswordResource(Resource):

    @classmethod
    @fresh_jwt_required
    def post(cls):
        req_json = request.get_json()
        user_data = UserSchema.load(req_json)
        user = UserModel.find_by_username(user_data.username)
        if not user:
            return {"message":"User does not exist"}, 404
        user.password = user_data.password
        user.save_to_db()
        return {"message": "User password saved successfully"}, 200
