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
    
    # parses and validates a command from twitter into a standard canonical command
    def process(self, msg):
        # strip the initial mention 
        regex = r'^(?P<mention>\S+)\s+db\.(?P<coll>\w+)\.(?P<func>\w+)\((?P<data>.+)\)'
        twitter_matcher = re.compile(regex)
        m = twitter_matcher.match(msg)
        print "============ MAPPING DATA INTO NATIVE FORMAT ============"
        data_full = demjson.decode(m.groupdict()['data'])
        pprint(data_full)

        print "============ FULL OUTPUT ============"
        pprint(m.groupdict())


