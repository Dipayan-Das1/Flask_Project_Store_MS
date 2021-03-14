from werkzeug.datastructures import FileStorage
from flask_uploads import UploadSet, IMAGES
import os
from typing import Union
import re

#This represents a single set of uploaded files. Each upload set is independent of the others.
# This can be reused across multiple application instances, as all configuration is stored on the
# application object itself and found with flask.current_app.
#images is going to be a directory inside static folder
IMAGE_SET = UploadSet("images",IMAGES)

def save_image(image:FileStorage,folder:str) -> str:
    """takes filestorage and save to a folder """
    file_name = get_basename(image)
    print(file_name)
    return IMAGE_SET.save(image,folder,file_name)

def get_path(filename:str,folder:str):
    """take image name and return path to storage folder"""
    return IMAGE_SET.path(filename,folder)

def find_image_any_format(filename:str,folder:str):
    """take image name and return image of any of the accepted formats"""
    for frmt in IMAGES:
        image = f"{filename}.{frmt}"
        image_path = IMAGE_SET.path(image,folder)
        if os.path.isfile(image_path):
            return image_path

def _retrieve_filename(file: Union[str,FileStorage]) -> str:
    """take file storage and return file name"""
    if isinstance(file,FileStorage):
        return file.filename
    return file

allowed_formats = "|".join(IMAGES)

def is_filename_safe(file: Union[str,FileStorage]):
    """chec if filename matches our regex"""
    filename = _retrieve_filename(file)
    regex = f"^[a-zA-Z0-9][a-zA-Z0-9_()-\.]*\.({allowed_formats})$"
    return re.match(regex,filename)

def get_basename(file: Union[str,FileStorage]):
    """return full name of image in path"""

    filename = _retrieve_filename(file)
    return os.path.split(filename)[1]

def get_extension(file: Union[str,FileStorage]):
    """return file extension"""
    basename = get_basename(file)
    return basename.split(".")[1]