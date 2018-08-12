from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os

from .util import open_browser_tab
from .config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

from .views import *
from .api import *


def load_srs(filename, host='localhost', port=8000, debug=False):
    os.environ['DATABASE_URI'] = filename
    if not os.path.exists(filename):
        db.create_all()

    open_browser_tab('http://{}:{}'.format(host, port))

    app.run(
        host=host,
        port=port,
        debug=debug
    )
