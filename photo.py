import imghdr
import exifread


class Photo(object):
    datetime = None
    filepath = None

    def __init__(self, filepath):
        self.filepath = filepath

    @classmethod
    def is_photo(obj, filepath):
        filetype = imghdr.what(filepath)
        return type(filetype) == str

    def get_exif(self):
        img = open(self.filepath, 'rb')
        exif = exifread.process_file(img)
        img.close()
        return exif

    def get_timestamp(self):
        exif = self.get_exif()
        return exif.get('EXIF DateTimeOriginal', None)
