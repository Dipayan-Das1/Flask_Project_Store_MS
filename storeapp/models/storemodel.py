from storeapp.db import db
from typing import Dict, Union, List

ItemJson = Dict[str,Union[str,int,float]]
StoreJson = Dict[str,Union[str,List[ItemJson]]]

class StoreModel(db.Model):
    """Model class for store"""
    __tablename__ = "store"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False,unique=True)
    email = db.Column(db.String(100),nullable=False,unique=True)

    def __init__(self,name:str,email:str):
        self.name = name
        self.email = email

    #Back reference ...lazy loading enabled
    items = db.relationship("ItemModel")

    @classmethod
    def get_store_by_name(cls,name:str) -> "StoreModel":
        return cls.query.filter_by(name=name).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        db.session.remove(self)
        db.session.commit()



class ItemModel(db.Model):
    """Model class for Item"""

    __tablename__ = "item"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    price = db.Column(db.Float(precision=2),nullable=False)

    #foreign key reference to store table.... store.id follows the pattern tablename.primarycolumnname
    store_id = db.Column(db.Integer,db.ForeignKey('store.id'))
    store = db.relationship("StoreModel")

    @classmethod
    def get_item_by_name(cls,name,storeId) -> "ItemModel":
        return cls.query.filter_by(name=name,store_id=storeId).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_item(self):
        db.session.delete(self)
        db.session.commit()