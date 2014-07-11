from flask import  request, redirect, render_template, url_for
from flask.views import MethodView
import models
from . import app
import json
from bson import json_util
import logging
import urllib
import twitter_engine as twe
import twitter_listener as tl

logger = logging.getLogger('views')
logging.basicConfig(level=logging.DEBUG)

bg = None

@app.route('/')
@app.route('/index')
def index():
    return app.config['SECRET_KEY'] 

# start twitter loop running~
@app.route('/twitter')
def twitter():
    print "twitter hit"
    twt = twe.TwitterEngine()
    bg = tl.TwitterListener(twt) 
    print "successfully constructed"
    bg.start()
    print "running"
    return 'helloworld'

@app.route('/listen')
def listen():
    return 'test'

@app.route('/successauth')
def successauth():
    return 'authentication was successful'



