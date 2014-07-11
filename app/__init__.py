from flask import Flask
from flask.ext.mongoengine import MongoEngine
import config

app = Flask(__name__)
app.config.from_object(config)

from app import views
from app import filters
from app import facebook_engine



db = MongoEngine(app)
