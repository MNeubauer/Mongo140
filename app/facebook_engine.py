#import facebook
from . import app
from flask import request
import requests 

@app.route('/')
def index():
    return 'Hello World'


@app.route('/subscribe')
def subscribe():
    FB_APP_ID = app.config['FB_APP_ID']
    # access_token is sent as a query string parameter
    FB_APP_ACCESS_TOKEN = app.config['FB_APP_ACCESS_TOKEN']
    FB_VERIFY_TOKEN = app.config['FB_VERIFY_TOKEN']
    # object, fields, callback_url, and verify_token are sent as urllib.urlencode([('param','val')])
    CALLBACK_URL = 'http://skunk.ngrok.com/fb'

    payload_url = "https://graph.facebook.com/{0}/subscriptions".format(FB_APP_ID)
    payload = {"access_token": FB_APP_ACCESS_TOKEN, "object": "user", "fields": "feed", "verify_token": FB_VERIFY_TOKEN, "callback_url": CALLBACK_URL}   
    r = requests.post(payload_url, data=payload)
    return r.text


@app.route('/fb', methods=['GET','POST'])
def handle_requests():
    if request.method == 'GET':
        FB_VERIFY_TOKEN = app.config['FB_VERIFY_TOKEN']
        mode = request.args.get('hub.mode')
        challenge = request.args.get('hub.challenge')
        verification = request.args.get('hub.verify_token')

        # if we have our verification token back echo the challenge back to facebook
        if verification == FB_VERIFY_TOKEN:
            return challenge
        else:
            return "FAILED"

    elif request.method == 'POST':
        # do some stuff with the updates
        print (request)
        return "Hello World"