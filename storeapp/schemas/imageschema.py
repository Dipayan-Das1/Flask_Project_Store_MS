from marshmallow import Schema, fields
from werkzeug.datastructures import FileStorage
import typing
class FileStorageField(fields.Field):

    default_error_messages = {"invalid":"Not a valid image"}

    def _deserialize(
        self,
        value: typing.Any,
        attr: typing.Optional[str],
        data: typing.Optional[typing.Mapping[str, typing.Any]],
        **kwargs
    ):
        if value  is None:
            return None
        if not isinstance(value,FileStorage):
            self.fail("invalid")
        return value


class ImageSchema(Schema):
    image = FileStorageField(required=True)