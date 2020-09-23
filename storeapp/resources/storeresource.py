from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from storeapp.models.storemodel import StoreModel

class Store(Resource):
    """Store Resource /store/{name}"""

    parser = reqparse.RequestParser()
    parser.add_argument("email",type=str,required=True,help="Store email id is required")

    ###@jwt_required() parentheses is required
    @jwt_required()
    def get(self,name):
        store = StoreModel.get_store_by_name(name)
        if store:
            return store.json()
        else:
            return {"message":"Store {} does not exist".format(name)}

    @jwt_required()
    def post(self,name):
        store = StoreModel.get_store_by_name(name)
        if store:
            return {"message":"Store with name {} already exists".format(name)}, 400
        else:
            args = Store.parser.parse_args()
            store = StoreModel(name,args["email"])
            store.save_to_db()
        return {"message":"Store created successfully"}, 201

    @jwt_required()
    def delete(self,name):
        store = StoreModel.get_store_by_name(name)
        if store:
            store.delete()
        else:
            return {"message":"Store with name {} does not exist".format(name)}, 400

