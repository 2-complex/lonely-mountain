import sqlalchemy
import re
import hashlib
import datetime


class Implementation:

    def __init__(self, models, session):
        self.models = models
        self.session = session

    def new_file(self, filename, content):
        in_file = self.models.File(filename, content)
        map( self.session.delete, self.models.File.query.filter_by(hashcode=in_file.hashcode) )
        self.session.add(in_file)
        self.session.commit()
        return {"hashcode":in_file.hashcode}

    def get_file(self, hashcode):
        files = list(self.models.File.query.filter_by(hashcode=hashcode))
        if len(files) == 0:
            return None, None

        file = files[0]
        file.timestamp = datetime.datetime.utcnow()
        self.session.commit()

        return file.filename, file.content

