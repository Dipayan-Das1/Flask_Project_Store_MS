from storeapp.db import db
from time import time
#pip install requests

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
    confirmation = db.relationship("ConfirmationModel", lazy="dynamic", cascade="all, delete-orphan")


    @classmethod
    def find_by_name(cls,username:str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls,_id:int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_email(cls, email_id: str) -> "UserModel":
        return cls.query.filter_by(email=email_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()


from uuid import uuid4
import time

CONFIRMATION_EXPIRATION_DELTA = 6 * 60 * 60


class ConfirmationModel(db.Model):
    # table name
    __tablename__ = "confirmation"

    # column definitions
    id = db.Column(db.String(50), primary_key=True)
    expire_at = db.Column(db.Integer, nullable= False)
    confirmed = db.Column(db.Boolean, nullable= False, default= False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("UserModel")

    def __init__(self,user_id:int):
        self.user_id = user_id
        self.id = uuid4().hex
        self.expire_at= int(time.time()) + CONFIRMATION_EXPIRATION_DELTA
        self.confirmed = False

    @classmethod
    def find_by_id(cls,_id:str) -> "ConfirmationModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) :
        return cls.query.all()

    def expired(self):
        return int(time.time()) > self.expire_at

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()