from storeapp.flaskmarshmallow import flask_marshmallow
from storeapp.models.storemodel import ItemModel, StoreModel

class ItemSchema(flask_marshmallow.SQLAlchemyAutoSchema):

    class Meta:
        model = ItemModel
        dump_only = ("id",)
        load_only = ("store",)
        include_fk = True
        load_instance = True


class StoreSchema(flask_marshmallow.SQLAlchemyAutoSchema):

    items = flask_marshmallow.Nested(ItemSchema,many=True)
    class Meta:
        model = StoreModel
        dump_only = ("id")
        include_fk = True
        load_instance = True
