from flask_sqlalchemy import SQLAlchemy
from storeapp.db import db

#pip install requests
from requests import Response,post,request

class UserModel(db.Model):
    """Model class for user"""

    #table name
    __tablename__ = "user"

    #column definitions
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80),nullable=False,unique=True)
    password = db.Column(db.String(100),nullable=False)
    activated = db.Column(db.Boolean,default=False)
    email = db.Column(db.String(100),nullable=False,unique=True)

    @classmethod
    def find_by_name(cls,username:str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls,_id:int):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()
