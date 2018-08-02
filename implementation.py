import json
import sqlalchemy
import re
import hashlib


class Implementation:

    def __init__(self, models, session):
        self.models = models
        self.session = session

    def new_file(self, filename, content):
        my_file = self.models.File(filename, content)
        self.session.add(my_file)
        self.session.commit()
        return json.dumps({"hashcode":my_file.hashcode})

    def get_file(self, hashcode):
        files = list(self.models.File.query.filter_by(hashcode=hashcode))
        if len(files) == 0:
            return None, None

        return files[0].filename, files[0].content

