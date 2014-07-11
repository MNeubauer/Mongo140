import os
import twitter as tw
from . import app
import threading
import mongo_parser
from pprint import pprint

# implementation of a background thread that just listens for tweets on
# the global mongodb channel and calls a function from TwitterShell
# whenever something is detected.

class TwitterListener (threading.Thread):
    stream = None

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        MY_TWITTER_CREDS = os.path.expanduser('~/.my_app_credentials')
        if not os.path.exists(MY_TWITTER_CREDS):
            tw.oauth_dance("SkunkWorks140", 
                        app.config['TWITTER_CONSUMER_KEY'], 
                        app.config['TWITTER_CONSUMER_SECRET'],
                        MY_TWITTER_CREDS)

        oauth_token, oauth_secret = tw.read_token_file(MY_TWITTER_CREDS)

        self.stream = tw.TwitterStream( auth=tw.OAuth(
            oauth_token, oauth_secret,           
            app.config['TWITTER_CONSUMER_KEY'], app.config['TWITTER_CONSUMER_SECRET']),
            domain='userstream.twitter.com'
        )

        iterator = self.stream.user()
        for tweet in iterator:
            if 'text' in tweet:
                pprint(tweet)
                mongo_parser.MongoParser.processTwitter(tweet['text'],
                                                        tweet['id'],
                                                        tweet['user']['screen_name'])
        # finished authentication, now start listening for twitter feed.

