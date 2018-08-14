import pyexcel
import json
import dateutil.parser

from srs_sqlite import db
from srs_sqlite.databases import SrsRecord, SrsTuple


def import_excel(filename, sheet_name):
    db.create_all()
    for record in pyexcel.iget_records(file_name=filename, sheet_name=sheet_name):
        data = json.loads(record['data'])
        data['vocab'] = record['vocab']
        data['is_user'] = record['is_user']
        created = dateutil.parser.parse(record['created'])
        modified = dateutil.parser.parse(record['modified'])

        all_english = [item['english'] for item in data['dictionary']]

        if data['is_user'] and len(all_english) > 0:
            front = ', '.join(all_english)
        else:
            front = data['vocab']

        queried_record = SrsRecord.query.filter_by(front=front).first()
        if queried_record is None:
            srs_record = SrsRecord(id=record['id'],
                                   front=front,
                                   data=json.dumps(data, ensure_ascii=False),
                                   created=created,
                                   modified=modified)
            db.session.add(srs_record)
        else:
            if data['is_user'] and json.loads(queried_record.data)['is_user'] == 0:
                queried_record.data = json.dumps(data, ensure_ascii=False)
                queried_record.modified = modified

    db.session.commit()


if __name__ == '__main__':
    import_excel('../user/HanziLevelUp.xlsx', 'vocab')
