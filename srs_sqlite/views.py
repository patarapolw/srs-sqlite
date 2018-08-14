from flask import render_template, request
import os

from . import app
from .databases import SrsRecord, SrsTuple


@app.route('/')
def index():
    config = {
        'colHeaders': SrsTuple.__slots__,
        'renderers': {
            'front': 'markdownRenderer',
            'back': 'markdownRenderer'
        },
        'colWidths': [210, 381, 179, 155, 85, 220]
    }

    return render_template('index.html', title=os.getenv('DATABASE_URI', ''), config=config)


@app.route('/card/<int:card_id>')
def card(card_id):
    record = SrsRecord.query.filter_by(id=card_id).first()
    return render_template('card.html', card=dict(SrsTuple().from_db(record)), show=False)


@app.route('/card/<int:card_id>/show')
def card_show(card_id):
    record = SrsRecord.query.filter_by(id=card_id).first()
    return render_template('card.html', card=dict(SrsTuple().from_db(record)), show=True)
