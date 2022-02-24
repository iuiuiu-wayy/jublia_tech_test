from flask import Flask, request, jsonify, make_response
from flask_mail import Mail, Message
from celery import Celery
import sys
import os
sys.path.append(os.getcwd())
from config import Config
import models, view, control
import time
import datetime
import pytz

LOCAL_TIMEZONE = pytz.timezone('Singapore')
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)
mail = Mail(app)
#celery -A run.celery worker --pool=gevent --concurreny=500 --loglevel=info
celery = Celery(
    'run',
    backend=app.config['CELERY_RESULT_BACKEND'],
    broker=app.config['CELERY_BROKER_URL'],
    CELERY_IMPORTS=("run")
)
class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)
celery.Task = ContextTask

models.init_app(app)
view.init_app(app)
control.init_app(app, mail, celery)

if __name__ == '__main__':
    app.run(debug=True)