from datetime import datetime
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker

from srs_sqlite import db
from srs_sqlite.databases import SrsRecord
from srs_sqlite.util import get_url_images_in_text

engine = create_engine('sqlite:///' + os.path.abspath('../user/PathoKnowledge.db'))
Base = declarative_base()
Session = sessionmaker(bind=engine)


def get_image_only():
    db.create_all()

    session = Session()
    for record in session.query(_SrsRecord):
        if len(get_url_images_in_text(record.front)) > 0:
            srs_record = SrsRecord(
                id=record.id,
                front=record.front,
                back=record.back,
                keywords=record.keywords,
                tags=record.tags,
                created=record.created,
                modified=record.modified,
                srs_level=record.srs_level,
                next_review=record.next_review
            )
            db.session.add(srs_record)

    db.session.commit()


class _SrsRecord(Base):
    __tablename__ = 'srs'

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)

    front = Column(String, nullable=False, unique=True)
    back = Column(String)

    data = Column(String)

    keywords = Column(String)
    tags = Column(String)

    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now)

    srs_level = Column(Integer)
    next_review = Column(DateTime)


if __name__ == '__main__':
    get_image_only()
