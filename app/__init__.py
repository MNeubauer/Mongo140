from flask import Flask
from flask.ext.mongoengine import MongoEngine
import config
from werkzeug.contrib.fixers import ProxyFix
app = Flask(__name__)
app.config.from_object(config)

from app import views
from app import filters

app.wsgi_app = ProxyFix(app.wsgi_app)

db = MongoEngine(app)
