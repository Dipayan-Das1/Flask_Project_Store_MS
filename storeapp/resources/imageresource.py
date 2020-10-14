from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask import request, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from storeapp.images.processor import save_image,get_basename,is_filename_safe, get_path
from storeapp.schemas.imageschema import ImageSchema
import os
from storeapp.localization.internalization import gettext
image_schema = ImageSchema()


class ImageUploadResource(Resource):

    @classmethod
    @jwt_required
    def post(cls,userid:str):
        data = image_schema.load(request.files) #returns a dict with Filestorage value and key image
        folder = f"user_{userid}"
        try:
            image_path = save_image(data["image"],folder=folder)
            image_name = get_basename(image_path)
            return {"message":gettext('image_uploaded')}, 201
        except UploadNotAllowed as e:
            print(e)
            return {"message":gettext('image_upload_failed')}, 500
        except Exception as e:
            print(e)
            return {"message":gettext('image_upload_failed')}, 500


class ImageResource(Resource):

    @classmethod
    @jwt_required
    def get(cls,filename:str):
        user = get_jwt_identity()
        print(user)
        folder = f"user_{user}"
        print(folder)
        if not is_filename_safe(filename):
            return {"message":gettext('bad_file_request')}, 400
        try:
            path = get_path(filename,folder)
            print(path)
            if not os.path.exists(path):
                return {"message": gettext("file_not_exist")}, 400
            return send_file(path)
        except Exception as e:
            print(e)
            return {"message":gettext('error_get_image')}, 500


    @classmethod
    @jwt_required
    def delete(cls,filename:str):
        user = get_jwt_identity()
        print(user)
        folder = f"user_{user}"
        print(folder)
        if not is_filename_safe(filename):
            return {"message": gettext('bad_file_request')}, 400
        try:
            path = get_path(filename, folder)
            print(path)
            if not os.path.exists(path):
                return {"message": gettext("file_not_exist")}, 400
            os.remove(path)
            return {"message":gettext("file_delete_success")}, 200
        except Exception as e:
            print(e)
            return {"message": gettext("error_delete_image")}, 500
