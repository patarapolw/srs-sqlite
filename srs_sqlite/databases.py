from datetime import datetime
import dateutil.parser

from . import db


class SrsRecord(db.Model):
    __tablename__ = 'srs'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)

    front = db.Column(db.String(250), nullable=False, unique=True)
    back = db.Column(db.String(10000))

    keywords = db.Column(db.String(250))
    tags = db.Column(db.String(250))

    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime, default=datetime.now)

    srs_level = db.Column(db.Integer)
    next_review = db.Column(db.DateTime)


class SrsTuple:
    __slots__ = ('front', 'back', 'keywords', 'tags', 'srs_level', 'next_review')

    def __init__(self, *args):
        for i, arg in enumerate(args):
            setattr(self, self.__slots__[i], arg)

    def to_db(self):
        entry = dict()
        for key in self.__slots__:
            entry[key] = getattr(self, key, None)

        if entry['next_review'] is not None:
            entry['next_review'] = dateutil.parser.parse(entry['next_review'])

        return entry

    def from_db(self, srs_record):
        yield 'id', srs_record.id

        for field in self.__slots__:
            value = getattr(srs_record, field)
            if isinstance(value, datetime):
                value = value.isoformat()

            setattr(self, field, value)

            yield field, value
