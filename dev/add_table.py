# import sqlite3
# import dateutil.parser
#
# from srs_sqlite import db
# from srs_sqlite.databases import SrsRecord, KeywordRecord, TagRecord
# from srs_sqlite.util import get_url_images_in_text
# from srs_sqlite.tags import tag_reader
#
#
# def get_data(database_path='../user/PathoKnowledge.db'):
#     conn = sqlite3.connect(database_path)
#     conn.row_factory = sqlite3.Row
#     c = conn.cursor()
#
#     return c.execute('SELECT * FROM srs')
#
#
# def create_new():
#     db.create_all()
#
#     for row in get_data():
#         next_review = None
#         if row['next_review']:
#             next_review = dateutil.parser.parse(row['next_review'])
#
#         srs_record = SrsRecord(
#             id=row['id'],
#             front=row['front'],
#             back=row['back'],
#             data=row['data'],
#             created=dateutil.parser.parse(row['created']),
#             modified=dateutil.parser.parse(row['modified']),
#             srs_level=row['srs_level'],
#             next_review=next_review
#         )
#         db.session.add(srs_record)
#
#         keywords = tag_reader(row['keywords'])
#         front = row['front']
#         for url in get_url_images_in_text(front):
#             front = front.replace(url, '')
#         if front:
#             keywords.add(front)
#         for keyword in keywords:
#             keyword_record = KeywordRecord(
#                 keyword=keyword,
#                 srs_id=row['id']
#             )
#             db.session.add(keyword_record)
#
#         tags = tag_reader(row['tags'])
#         for tag in tags:
#             tag_record = TagRecord(
#                 tag=tag,
#                 srs_id=row['id']
#             )
#             db.session.add(tag_record)
#
#     db.session.commit()
#
#
# if __name__ == '__main__':
#     create_new()
