import random
import json
from datetime import datetime

from .databases import SrsRecord


def iter_quiz():
    def _filter():
        for srs_record in SrsRecord.query.order_by(SrsRecord.modified.desc()):
            # record_data = srs_record.data
            # if record_data:
            #     record_data = json.loads(record_data)
            #     if (record_data['level'] <= 5 and record_data['is_user'] == 1 and
            #             (not srs_record.next_review or srs_record.next_review < datetime.now())):
            #         yield srs_record
            # else:
                yield srs_record

    all_records = list(_filter())
    random.shuffle(all_records)

    return iter(all_records)
