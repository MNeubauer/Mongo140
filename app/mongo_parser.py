import os
import twitter as tw
from . import app
from pprint import pprint
import pymongo
import re
import demjson

# some python code to manage the twitter engine.  Defines a class that 
# contains information about the twitter state and the conection.

class MongoParser:
   
    # post a message to the authenticated twitter stream
    @staticmethod
    def postTwitter(msg, tweetId, username): 
        MY_TWITTER_CREDS = os.path.expanduser('~/.my_app_credentials')
        if not os.path.exists(MY_TWITTER_CREDS):
            tw.oauth_dance("SkunkWorks140", 
                        app.config['TWITTER_CONSUMER_KEY'], 
                        app.config['TWITTER_CONSUMER_SECRET'],
                        MY_TWITTER_CREDS)

        # authenticate twitter session
        oauth_token, oauth_secret = tw.read_token_file(MY_TWITTER_CREDS) 
        
        twitter = tw.Twitter(auth=tw.OAuth(
        oauth_token, 
        oauth_secret, 
        app.config['TWITTER_CONSUMER_KEY'], 
        app.config['TWITTER_CONSUMER_SECRET']))
        

        twitter.statuses.update(status="@{} {}".format(username, msg))

        print "@{} {}".format(username, msg)

    @staticmethod
    def processTwitter(msg, tweetId, username):
        regex = r'^(?P<mention>\S+)\s+(?P<prunedData>.+)'
        stripper = re.compile(regex)
        m = stripper.match(msg)
        if m is None:
            return;

        response = MongoParser.process(m.groupdict()['prunedData'])
        # get back a string to respond with
        MongoParser.postTwitter(response, tweetId, username)

    # parses and validates a command from twitter into a standard canonical command
    @staticmethod
    def process(msg):
        # strip the initial mention 
        regex = r'\s*db\.(?P<coll>\w+)\.(?P<func>\w+)\((?P<data>.+)\)'
        twitter_matcher = re.compile(regex)
        m = twitter_matcher.match(msg)
        
        if m is None:
            return "invalid command string passed";

        print "============ MAPPING DATA INTO NATIVE FORMAT ============"
        data_parsed = demjson.decode(m.groupdict()['data'])
        pprint(data_parsed)
        
        print "============ FULL OUTPUT ============"
        parsed = m.groupdict()
        
        client = pymongo.MongoClient()
        if parsed['func'] == 'find':
            cur = client.db[parsed['coll']].find(data_parsed)
            ld = list(cur)
            msg = ''
            for item in ld:
                msg += ('{' + ', '.join('{} : {}'.format(key, val) for key, val in sorted(item.items())) + '}' + '\n')
            return msg
    
        elif parsed['func'] == 'insert':
            cur = client.db[parsed['coll']].insert(data_parsed)
            return "{} successfully inserted".format(cur)














