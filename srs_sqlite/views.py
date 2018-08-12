from flask import render_template
import os

from . import app
from .databases import SrsTuple


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
