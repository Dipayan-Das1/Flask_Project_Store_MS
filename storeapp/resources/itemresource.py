from flask_restful import Resource,reqparse
from flask import request
from storeapp.models.storemodel import ItemModel,StoreModel
from flask_jwt_extended import jwt_required, get_jwt_claims, fresh_jwt_required
from storeapp.schemas.itemschema import ItemSchema
from marshmallow import ValidationError

class Item(Resource):

    PRICE_MSG = "Item price is mandatory"
    STORE_NOT_FOUND = "Store {} not found"
    ITEM_NOT_FOUND = "Item {} not found in store {}"
    ITEM_EXISTS = "Item already exists"
    ITEM_CREATED = "Item created"
    ITEM_UPDATED = "Item updated"
    ITEM_DELETED = "Item deleted"

    itemSchema = ItemSchema()

    @classmethod
    @jwt_required
    def get(cls,store_name,item_name):
        store = StoreModel.get_store_by_name(store_name)
        if store:
            item = ItemModel.get_item_by_name(item_name,store.id)
            if item:
                return cls.itemSchema.dump(item)
            else:
                return {"message":cls.ITEM_NOT_FOUND.format(item_name,store_name)},404
        else:
            return {"message": cls.STORE_NOT_FOUND.format(store_name)}, 404

    @classmethod
    @fresh_jwt_required
    def post(cls,store_name,item_name):
        """@fresh_jwt_required means always a fresh jwt token is needed"""
        store = StoreModel.get_store_by_name(store_name)
        if store:
            item = ItemModel.get_item_by_name(item_name, store.id)
            if item:
                return {"message":cls.ITEM_EXISTS},400
            else:
                req_json = request.get_json()
                req_json["name"] = item_name
                req_json["store_id"] = store.id
                try:
                    item = cls.itemSchema.load(req_json)
                    item.save_to_db()
                except ValidationError as e:
                    return e.messages,400
                return {"message":Item.ITEM_CREATED}, 201
        else:
            return {"message":cls.STORE_NOT_FOUND.format(store_name)},404

    @classmethod
    @jwt_required
    def put(cls,store_name,item_name):
        store = StoreModel.get_store_by_name(store_name)
        if store:
            item = ItemModel.get_item_by_name(item_name, store.id)
            req_json = request.get_json()
            req_json["name"] = item_name
            req_json["store_id"] = store.id
            if item:
                try:
                    item_req = cls.itemSchema.load(req_json)
                    item.price = item_req.price
                    item.save_to_db()
                except ValidationError as e:
                    return e.messages, 400
                return {"message": Item.ITEM_UPDATED}, 200
            else:
                try:
                    item_req = cls.itemSchema.load(req_json)
                    item.save_to_db()
                except ValidationError as e:
                    return e.messages, 400
                return {"message": Item.ITEM_CREATED}, 201
        else:
            return {"message": Item.STORE_NOT_FOUND.format(store_name)}, 404

    @classmethod
    @jwt_required
    def delete(cls,store_name,item_name):
        store = StoreModel.get_store_by_name(store_name)
        if store:
            item = ItemModel.get_item_by_name(item_name, store.id)
            if item:
                item.delete_item()
                return {"message":cls.ITEM_DELETED}, 200
            else:
                return {"message": cls.ITEM_NOT_FOUND.format(item_name, store_name)}, 404
        else:
            return {"message": cls.STORE_NOT_FOUND.format(store_name)}, 404