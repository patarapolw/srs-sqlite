from datetime import datetime, timedelta
import dateutil.parser
from IPython.display import IFrame
import os

from . import db
from .srs import SRS
from .tags import tag_reader, to_raw_tags


class SrsRecord(db.Model):
    __tablename__ = 'srs'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)

    front = db.Column(db.String, nullable=False, unique=True)
    back = db.Column(db.String)

    data = db.Column(db.String)

    keywords = db.Column(db.String)
    tags = db.Column(db.String)

    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime, default=datetime.now)

    srs_level = db.Column(db.Integer)
    next_review = db.Column(db.DateTime)

    def hide(self):
        return IFrame('http://{}:{}/card/{}'.format(os.getenv('HOST', 'localhost'),
                                                    os.getenv('PORT', 8000),
                                                    self.id),
                      width=800, height=100)

    def show(self):
        return IFrame('http://{}:{}/card/{}/show'.format(os.getenv('HOST', 'localhost'),
                                                         os.getenv('PORT', 8000),
                                                         self.id),
                      width=800, height=100)

    def next_srs(self):
        if not self.srs_level:
            self.srs_level = 1
        else:
            self.srs_level = self.srs_level + 1

        self.next_review = (datetime.now()
                            + SRS.get(int(self.srs_level), timedelta(weeks=4)))
        self.modified = datetime.now()

    correct = right = next_srs

    def previous_srs(self, duration=timedelta(hours=4)):
        if self.srs_level and self.srs_level > 1:
            self.srs_level = self.srs_level - 1

        self.bury(duration)

    incorrect = wrong = previous_srs

    def bury(self, duration=timedelta(hours=4)):
        self.next_review = datetime.now() + duration
        self.modified = datetime.now()

    def mark(self, tag_name: str='marked'):
        if self.tags is None:
            self.tags = ''

        all_tags = tag_reader(self.tags)
        all_tags.add(tag_name)
        self.tags = to_raw_tags(all_tags)

    def unmark(self, tag_name: str='marked'):
        if self.tags is None:
            self.tags = ''

        all_tags = tag_reader(self.tags)
        if tag_name in all_tags:
            all_tags.remove(tag_name)
        self.tags = to_raw_tags(all_tags)


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

        yield 'data', srs_record.data
