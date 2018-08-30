import os
os.environ['DATABASE_URI'] = '../user/PathoImages.db'

import PyPDF2
import os

from srs_sqlite.databases import SrsRecord
from srs_sqlite.config import Config
from srs_sqlite import db


def main():
    for filename in os.listdir(Config.DATABASE_FOLDER):
        if filename.endswith('.pdf'):
            print(filename)
            with open(os.path.join(Config.DATABASE_FOLDER, filename), 'rb') as f:
                reader = PyPDF2.PdfFileReader(f)
                num_pages = reader.getNumPages()
                topic = filename.replace('.pdf', '').lower()

                for i in range(2, num_pages+1, 2):
                    srs_record = SrsRecord()
                    srs_record.front = '/pdf/{}/{}'.format(filename, i)
                    srs_record.back = '/pdf/{}/{}'.format(filename, i+1)
                    # page = reader.getPage(i)
                    # print(page.extractText())
                    srs_record.tags = topic
                    db.session.add(srs_record)
                    # break

    db.session.commit()


if __name__ == '__main__':
    main()
