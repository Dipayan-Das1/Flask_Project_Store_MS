from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required
from storeapp.models.storemodel import StoreModel

class Store(Resource):
    """Store Resource /store/{name}"""

    STORE_EXISTS = "Store with name {} already exists"
    STORE_NOT_EXISTS = "Store {} does not exist"
    STORE_CREATED = "Store created successfully"

    parser = reqparse.RequestParser()
    parser.add_argument("email",type=str,required=True,help="Store email id is required")

    ###@jwt_required() parentheses is required
    @jwt_required
    @classmethod
    def get(cls,name):
        store = StoreModel.get_store_by_name(name)
        if store:
            return store.json()
        else:
            return {"message":cls.STORE_NOT_EXISTS.format(name)}

    @jwt_required
    @classmethod
    def post(cls,name):
        store = StoreModel.get_store_by_name(name)
        if store:
            return {"message":cls.STORE_EXISTS.format(name)}, 400
        else:
            args = Store.parser.parse_args()
            store = StoreModel(name,args["email"])
            store.save_to_db()
        return {"message":cls.STORE_CREATED}, 201

    @jwt_required
    @classmethod
    def delete(cls,name):
        store = StoreModel.get_store_by_name(name)
        if store:
            store.delete()
        else:
            return {"message":cls.STORE_EXISTS.format(name)}, 400

