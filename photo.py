import os
import imghdr
import exifread
from shutil import copyfile
from datetime import datetime


class Photo(object):
    created = None
    filepath = None
    filename = None

    EXIF_DATETIME_KEY = 'EXIF DateTimeOriginal'

    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.created = self.get_created()

    @classmethod
    def is_photo(obj, filepath):
        try:
            filetype = imghdr.what(filepath)
            return type(filetype) == str
        except FileNotFoundError:
            return False

    def get_exif(self):
        img = open(self.filepath, 'rb')
        exif = exifread.process_file(img)
        img.close()
        return exif

    def get_exif_created(self):
        exif = self.get_exif()
        date = exif.get(self.EXIF_DATETIME_KEY, None)
        if date:
            return datetime.strptime(date.printable, '%Y:%m:%d %H:%M:%S')

    def get_created(self):
        timestamp = self.get_exif_created()
        if timestamp:
            return timestamp

        timestamp = os.path.getctime(self.filepath)
        timestamp = datetime.fromtimestamp(timestamp)
        return timestamp

    def get_organized_folder(self, folder_format='%Y-%m-%d'):
        folder_name = self.created.strftime(folder_format)
        return folder_name

    def copy_to(self, target_path):
        if not os.path.exists(target_path):
            os.makedirs(target_path)
        copyfile(self.filepath, os.path.join(target_path, self.filename))
