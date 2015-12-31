import json
import re
import tweepy

from twitter_model import TwitterData


class StreamWatcherListener(tweepy.StreamListener):
    db = None
    regex_list = None
    db_name = "twitter_stream"

    def __init__(self, db, queries):
        super(StreamWatcherListener, self).__init__()
        self.regex_list = [re.compile('(?:^|\s|$)('+q+')(?:^|\s|$)', re.IGNORECASE) for q in queries]
        self.db = db

    def on_data(self, data):
        obj = json.loads(data)
        if "text" in obj and self.find(obj["text"]):
            self.db.insert(TwitterData(obj))

    def find(self, content):
        for regex in self.regex_list:
            if regex.search(content):
                return True
        return False

    def on_error(self, status_code):
        print 'An error has occured! Status code = %s' % status_code
        return True

    def on_timeout(self):
        print 'Timeout...'


def init_crawler(consumer_key, consumer_secret, access_token, access_token_secret, db, titles):
    auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    track = [prepare_phrase(t) for t in titles] + ['#'+remove_special_chars(t) for t in titles]
    print(track)

    stream = tweepy.Stream(auth, StreamWatcherListener(db, track))
    stream.filter(track=track, languages=['en'])


def prepare_phrase(string):
    pattern = re.compile("[^\w'\- ]")
    return pattern.sub('', string)


def remove_special_chars(string):
    pattern = re.compile("[^\w]")
    return pattern.sub('', string)

