import os
os.environ['DATABASE_URI'] = '../user/PathoImages.db'

import PyPDF2
import os

from srs_sqlite.databases import SrsRecord
from srs_sqlite.config import Config
from srs_sqlite import db


def import_pdf(filename):
    print(filename)
    with open(os.path.join(Config.DATABASE_FOLDER, filename), 'rb') as f:
        reader = PyPDF2.PdfFileReader(f)
        num_pages = reader.getNumPages()
        topic = filename.replace('.pdf', '').lower()

        for i in range(2, num_pages+1, 2):
            front = '/pdf/{}/{}'.format(filename, i)

            if SrsRecord.query.filter_by(front=front).first() is None:
                srs_record = SrsRecord()
                srs_record.front = front
                srs_record.back = '/pdf/{}/{}'.format(filename, i+1)

                srs_record.tags = topic
                db.session.add(srs_record)

    db.session.commit()


if __name__ == '__main__':
    import_pdf('Salivary.pdf')
