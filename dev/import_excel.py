import pyexcel

from . import db
from .databases import SrsRecord, SrsTuple


def import_excel(filename, sheet_name):
    for record in pyexcel.iget_records(file_name=filename, sheet_name=sheet_name):
        if SrsRecord.query.filter_by(front=record['Front']).first() is None:
            srs_record = SrsRecord(**SrsTuple(*record.values()).to_db())
            db.session.add(srs_record)

    db.session.commit()
