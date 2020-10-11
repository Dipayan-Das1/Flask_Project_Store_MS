from marshmallow import Schema,fields
from storeapp.flaskmarshmallow import flask_marshmallow
from storeapp.models.usermodel import UserModel
#
# class UserSchema(Schema):
#
#     class Meta:
#         load_only = ("password",)
#         dump_only = ("id",)
#
#     id = fields.Int()
#     username = fields.Str(required=True)
#     password = fields.Str(required=True)

class UserSchema(flask_marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        dump_only = ("id","activated")
        load_only = ("password",)
        model = UserModel
        load_instance = True






