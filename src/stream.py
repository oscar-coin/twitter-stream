import re
import tweepy
from twitter_model import TwitterData


class StreamWatcherListener(tweepy.StreamListener):

    db = None
    track = None

    def __init__(self, db, track):
        super(StreamWatcherListener, self).__init__()
        self.track = track
        self.db = db

    def on_status(self, status):
        if status.text and self.find(status.text):
            data = TwitterData(status)
            self.db.insert(data)

    def find(self, content):
        for obj in self.track:
            pattern = re.compile("\b#?"+obj+"\b")
            if pattern.match(content):
                return True
        return False

    def on_error(self, status_code):
        print 'An error has occured! Status code = %s' % status_code
        return True

    def on_timeout(self):
        print 'Timeout...'


def init_crawler(consumer_key, consumer_secret, access_token, access_token_secret, db, phrases):
    auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = tweepy.Stream(auth, StreamWatcherListener(db, phrases), timeout=None)
    stream.filter(track=phrases, languages=['en'], async=True)
