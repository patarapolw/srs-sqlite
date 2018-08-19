from flask import request, jsonify, Response, send_from_directory
from werkzeug.utils import secure_filename

import math
from datetime import datetime
import os
import re
import sqlalchemy.exc

from . import app, db, Config
from .databases import SrsRecord, SrsTuple
from .util import get_url_images_in_text


# @app.route('/api/all/<page_number>')
# def all_records(page_number, page_size=10):
#     page_number = int(page_number)
#
#     query = SrsRecord.query.order_by(SrsRecord.modified.desc())
#     total = query.count()
#     if page_number < 0:
#         page_number = math.ceil(total/page_size) + page_number + 1
#
#     offset = (page_number - 1) * page_size
#
#     records = query\
#         .offset(offset)\
#         .limit(page_size)\
#         .all()
#
#     data = [dict(SrsTuple().from_db(record)) for record in records]
#
#     return jsonify({
#         'data': data,
#         'pages': {
#             'from': offset + 1 if total > 0 else 0,
#             'to': total if offset + page_size > total else offset + page_size,
#             'number': page_number,
#             'total': total
#         }
#     })


@app.route('/api/all/<page_number>')
def all_records(page_number, page_size=10):
    def _filter():
        for srs_record in SrsRecord.query.order_by(SrsRecord.modified.desc()):
                yield srs_record

    page_number = int(page_number)

    query = list(_filter())
    total = len(query)

    if page_number < 0:
        page_number = math.ceil(total / page_size) + page_number + 1

    offset = (page_number - 1) * page_size

    records = query[offset:offset + page_size]

    data = [dict(SrsTuple().from_db(record)) for record in records]

    return jsonify({
        'data': data,
        'pages': {
            'from': offset + 1 if total > 0 else 0,
            'to': total if offset + page_size > total else offset + page_size,
            'number': page_number,
            'total': total
        }
    })


@app.route('/api/search/<page_number>', methods=['POST'])
def search(page_number, page_size=10):
    def _search():
        query_string = request.get_json()['q'].lower()

        for srs_record in SrsRecord.query.order_by(SrsRecord.modified.desc()):
            front = srs_record.front
            if front:
                for url in get_url_images_in_text(front):
                    front = front.replace(url, ' ')

            back = srs_record.back
            if back:
                for url in get_url_images_in_text(back):
                    back = back.replace(url, ' ')

            if any([query_string in cell.lower()
                    for cell in (front, back, srs_record.tags, srs_record.keywords) if cell]):
                yield srs_record

    page_number = int(page_number)

    query = list(_search())
    total = len(query)

    if page_number < 0:
        page_number = math.ceil(total / page_size) + page_number + 1

    offset = (page_number - 1) * page_size

    records = query[offset:offset + page_size]

    data = [dict(SrsTuple().from_db(record)) for record in records]

    return jsonify({
        'data': data,
        'pages': {
            'from': offset + 1 if total > 0 else 0,
            'to': total if offset + page_size > total else offset + page_size,
            'number': page_number,
            'total': total
        }
    })


@app.route('/api/edit', methods=['POST'])
def edit_record():
    record = request.get_json()
    old_record = SrsRecord.query.filter_by(id=record['id']).first()
    if old_record is None:
        srs_tuple = SrsTuple()
        setattr(srs_tuple, record['fieldName'], record['data'])

        new_record = SrsRecord(**srs_tuple.to_db())

        try:
            db.session.add(new_record)
            db.session.commit()
            record_id = new_record.id
        except sqlalchemy.exc.IntegrityError:
            return Response(status=400)
    else:
        setattr(old_record, record['fieldName'], record['data'])
        old_record.modified = datetime.now()

        db.session.commit()
        record_id = old_record.id

    return jsonify({
        'id': record_id
    }), 201


@app.route('/api/delete/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    srs_record = SrsRecord.query.filter_by(id=record_id).first()
    front = srs_record.front

    db.session.delete(srs_record)
    db.session.commit()

    return jsonify({
        'id': record_id,
        'front': front
    }), 303


@app.route('/api/images/create', methods=['POST'])
def create_image():
    if not os.path.exists(Config.IMAGE_DATABASE_FOLDER):
        os.mkdir(Config.IMAGE_DATABASE_FOLDER)

    if 'file' in request.files:
        file = request.files['file']
        filename = secure_filename(file.filename)
        while os.path.exists(os.path.join(Config.IMAGE_DATABASE_FOLDER, filename)):
            filename_stem, filename_ext = os.path.splitext(filename)
            match_obj = re.search(r'(.*)(\d+)$',filename_stem)
            if match_obj is not None:
                filename = match_obj.group(1) + str(int(match_obj.group(2)) + 1) + filename_ext
            else:
                filename = filename_stem + '0' + filename_ext

        file.save(os.path.join(Config.IMAGE_DATABASE_FOLDER, filename))

        return jsonify({
            'filename': filename
        }), 201

    # image.get('filename', uuid1().hex + '.png')
    # with open(os.path.join(Config.IMAGE_DATABASE_FOLDER, filename), 'wb') as f:
    #     f.write(b64decode(image['data']))
    #
    # return filename
    return Response(status=304)
