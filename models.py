import database

from sqlalchemy import Column, Integer, String, Boolean, Text, LargeBinary, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

import hashlib
import base64
import datetime

class File(database.Model):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    hashcode = Column(String(86))
    filename = Column(String(260))
    timestamp = Column(DateTime())
    content = Column(LargeBinary)

    def __init__(self, filename, content):
        self.hashcode = base64.b64encode(hashlib.sha512(content).digest())
        self.filename = filename
        self.timestamp = datetime.datetime.utcnow()
        self.content = content

    def __repr__(self):
        return '<File %s/%s>' % (self.hashcode, self.filename)
