from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required
from storeapp.models.storemodel import StoreModel
from storeapp.flaskmarshmallow import flask_marshmallow
from storeapp.schemas.itemschema import StoreSchema
from flask import request
from marshmallow import ValidationError

class Store(Resource):
    """Store Resource /store/{name}"""

    storeSchema = StoreSchema()

    STORE_EXISTS = "Store with name {} already exists"
    STORE_NOT_EXISTS = "Store {} does not exist"
    STORE_CREATED = "Store created successfully"

    ###@jwt_required() parentheses is required
    @classmethod
    @jwt_required
    def get(cls,name):
        store = StoreModel.get_store_by_name(name)
        if store:
            return cls.storeSchema.dump(store)
        else:
            return {"message":cls.STORE_NOT_EXISTS.format(name)}

    @classmethod
    @jwt_required
    def post(cls,name):
        store = StoreModel.get_store_by_name(name)
        if store:
            return {"message":cls.STORE_EXISTS.format(name)}, 400
        else:
            req_json = request.get_json()
            req_json["name"] = name
            try:
                storeModel = cls.storeSchema.load(req_json)
                print(storeModel)
                storeModel.save_to_db()
            except ValidationError as e:
                return e.messages,400
        return {"message":cls.STORE_CREATED}, 201

    @classmethod
    @jwt_required
    def delete(cls,name):
        store = StoreModel.get_store_by_name(name)
        if store:
            store.delete()
        else:
            return {"message":cls.STORE_EXISTS.format(name)}, 400

