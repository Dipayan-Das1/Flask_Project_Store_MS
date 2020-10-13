from storeapp.flaskmarshmallow import flask_marshmallow
from storeapp.models.usermodel import ConfirmationModel

class ConfirmationSchema(flask_marshmallow.ModelSchema):

    class Meta:
        model = ConfirmationModel
        load_only = ("user",)
        dump_only = ("id","expired_at","confirmed")
        include_fk = True

