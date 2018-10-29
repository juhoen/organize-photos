import os
from threading import Thread

class FileSeeker(object):
    folder = None
    filter = None
    queue = None
    total_files_found = 0

    done = False

    def __init__(self, folder, queue, filter=None):
        self.folder = folder
        self.queue = queue
        self.filter = filter

    def matches_filter(self, filename):
        if not self.filter:
            return True
        return self.filter(filename)

    def add_to_queue(self, file):
        abspath = os.path.abspath(file)
        self.queue.put(abspath)
        self.total_files_found += 1

    def _seek(self):
        for (dirpath, dirnames, filenames) in os.walk(self.folder):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if self.matches_filter(filepath):
                    self.add_to_queue(filepath)
        self.done = True

    def seek(self):
        self.done = False
        thread = Thread(target=self._seek)
        thread.start()

    def is_done(self):
        return self.done

    def get_total_file_count(self):
        return self.total_files_found
