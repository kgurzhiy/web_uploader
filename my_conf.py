import os

from celery import Celery
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(
    basedir, 'data.sqlite'
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_ENABLED'] = False

app.config['CELERY_BROKER_URL'] = 'amqp://localhost/'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

db = SQLAlchemy(app)

