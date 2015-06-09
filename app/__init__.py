from flask import Flask
import logging
import config
from datetime import timedelta
from flask.ext.sqlalchemy import SQLAlchemy

log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

from app import routes


