from flask_oauthlib.client import OAuth, OAuthException
import os
from flask import g

oauth = OAuth()

GITHUB_CONSUMER_ID = os.environ.get("GITHUB_CONSUMER_ID")
GITHUB_CONSUMER_SECRET = os.environ.get("GITHUB_CONSUMER_SECRET")

#https://docs.github.com/en/free-pro-team@latest/developers/apps/authorizing-oauth-apps
print(GITHUB_CONSUMER_ID)
print(GITHUB_CONSUMER_SECRET)

github = oauth.remote_app(
    'github',
    consumer_key=GITHUB_CONSUMER_ID,
    consumer_secret=GITHUB_CONSUMER_SECRET,
    request_token_params={"scope":"user:email"},
    base_url="https://api.github.com/",
    request_token_url=None,
    access_token_method="POST",
    access_token_url="https://github.com/login/oauth/access_token",
    authorize_url="https://github.com/login/oauth/authorize"
)

@github.tokengetter
def token_getter():
    if "access_token" in g:
        return g.access_token

