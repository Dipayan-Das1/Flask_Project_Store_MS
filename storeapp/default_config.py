import os
DEBUG = True
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = False
##Needed for 401 exceptions
PROPAGATE_EXCEPTIONS = True
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access','refresh']

#initialize jwt security
SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
UPLOADED_IMAGES_DEST = os.path.join("static","images")
