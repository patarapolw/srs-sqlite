import os
os.environ['DATABASE_URI'] = '../user/PathoImages.db'

import re

from srs_sqlite import db, Config
from srs_sqlite.databases import SrsRecord


if __name__ == '__main__':
    records = dict()

    for srs_record in SrsRecord.query:
        match_obj = re.search(r'(.*)(image)(\d+)(\.png)', srs_record.front)
        if match_obj is not None:
            groups = match_obj.groups()
            records[int(groups[2])] = srs_record, groups

    for i, pair in enumerate([v for k, v in sorted(records.items(), key=lambda x: x[0])]):
        srs_record, groups = pair
        groups = list(groups)
        groups[2] = str(i)
        old_path = srs_record.front
        srs_record.front = ''.join(groups)
        os.rename(
            os.path.join(Config.IMAGE_DATABASE_FOLDER, os.path.split(old_path)[1]),
            os.path.join(Config.IMAGE_DATABASE_FOLDER, os.path.split(srs_record.front)[1])
        )

    db.session.commit()
