import random
from datetime import datetime

from .databases import SrsRecord
from .tags import tag_reader


def iter_quiz(is_due=True, tag=None,
              offset=0, limit=None):
    """

    :param bool|None is_due:
    :param str|None tag:
    :param int offset:
    :param int|None limit:
    :return:
    """

    def _filter_is_due(srs_record):
        if is_due is None:
            return True
        elif is_due is True:
            if srs_record.next_review and srs_record.next_review < datetime.now():
                return True
        else:
            if srs_record.next_review is None:
                return True
        return False

    def _filter_tag(srs_record):
        if not tag:
            return True
        elif tag in tag_reader(srs_record.tags):
            return True
        else:
            return False

    def _filter():
        for srs_record in SrsRecord.query.order_by(SrsRecord.modified.desc()):
            if all((_filter_is_due(srs_record),
                    _filter_tag(srs_record))):
                yield srs_record

    def _records():
        for i, record in enumerate(_filter()):
            if i < offset:
                continue
            elif limit:
                if i >= offset + limit:
                    break

            yield record

    all_records = list(_records())
    random.shuffle(all_records)

    return iter(all_records)


def iter_all():
    return iter_quiz(is_due=None, tag=None)
