from flask_restful import Resource,reqparse
from storeapp.models.storemodel import ItemModel,StoreModel
from flask_jwt_extended import jwt_required, get_jwt_claims, fresh_jwt_required


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("price",type=float,required=True,help="Item price is mandatory")

    @jwt_required
    def get(self,store_name,item_name):
        store = StoreModel.get_store_by_name(store_name)
        if store:
            item = ItemModel.get_item_by_name(item_name,store.id)
            if item:
                return item.json()
            else:
                return {"message":"Item {} not found in store {}".format(item_name,store_name)},404
        else:
            return {"message": "Store {} not found".format(store_name)}, 404

    @fresh_jwt_required
    def post(self,store_name,item_name):
        """@fresh_jwt_required means always a fresh jwt token is needed"""
        store = StoreModel.get_store_by_name(store_name)
        if store:
            item = ItemModel.get_item_by_name(item_name, store.id)
            if item:
                return {"message":"Item already exists"},400
            else:
                args = Item.parser.parse_args()
                item = ItemModel(item_name,args["price"],store.id)
                item.save_to_db()
                return {"message":"Item created"}, 201
        else:
            return {"message":"Store {} not available".format(store_name)},404

    @jwt_required
    def put(self,store_name,item_name):
        args = Item.parser.parse_args()
        store = StoreModel.get_store_by_name(store_name)
        if store:
            item = ItemModel.get_item_by_name(item_name, store.id)
            if item:
                item.price = args["price"]
                item.save_to_db()
                return {"message": "Item updated"}, 200
            else:
                args = Item.parser.parse_args()
                item = ItemModel(item_name, args["price"], store.id)
                item.save_to_db()
                return {"message": "Item created"}, 201
        else:
            return {"message": "Store {} not available".format(store_name)}, 404

    @jwt_required
    def delete(self,store_name,item_name):
        claims = get_jwt_claims()
        if not claims['isadmin']:
            return {"message":"User does not have enough permissions to delete"},401
        store = StoreModel.get_store_by_name(store_name)
        if store:
            item = ItemModel.get_item_by_name(item_name, store.id)
            if item:
                item.delete_item()
                return {"message":"Item deleted"}, 200
            else:
                return {"message": "Item {} not found in store {}".format(item_name, store_name)}, 404
        else:
            return {"message": "Store {} not available".format(store_name)}, 404