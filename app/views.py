from flask import  request, redirect, render_template, url_for
from flask.views import MethodView
import models
from . import app
import json
from bson import json_util
import logging
import urllib

logger = logging.getLogger('views')
logging.basicConfig(level=logging.DEBUG)
