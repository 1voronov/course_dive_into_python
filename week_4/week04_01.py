import os
import tempfile
import random


class File:
    def __init__(self, file_path):
        self.file_path = file_path
        try:
            with open(self.file_path, 'r') as f:
                pass
        except FileNotFoundError:
            with open(file_path, 'w') as f:
                pass

    def __add__(self, obj):
        result_file = self.read() + obj.read()
        random_name = 'file' + str(random.randint(100000, 999999))
        result_file_path = os.path.join(tempfile.gettempdir(), 
                                        random_name)
        result = File(result_file_path)
        result.write(result_file)
        return result

    def __iter__(self):
        return FileIterator(self)

    def __str__(self):
        return os.path.abspath(self.file_path)

    def read(self):
        with open(self.file_path, 'r') as f:
            return f.read()

    def write(self, new_content):
        with open(self.file_path, 'w') as f:
            f.write(new_content)


class FileIterator:
    def __init__(self, File):
        with open(File.file_path) as f:
            self._file = f.readlines()
        self._cursor = 0
        self._file_length = len(self._file)
    
    def __iter__(self):
        return self

    def __next__(self):
        if self._cursor >= self._file_length:
            raise StopIteration
        result = self._file[self._cursor]
        self._cursor += 1
        return result