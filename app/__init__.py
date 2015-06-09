from flask import Flask
import logging
import config
from datetime import timedelta

log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)

app = Flask(__name__)
app.config.from_object('config')
from app import routes


