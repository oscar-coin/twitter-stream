import tweepy
from twitter_model import TwitterData


class StreamWatcherListener(tweepy.StreamListener):

    db = None

    def __init__(self, db):
        super(StreamWatcherListener, self).__init__()
        self.db = db

    def on_status(self, status):
        data = TwitterData(status)
        self.db.insert(data)

    def on_error(self, status_code):
        print 'An error has occured! Status code = %s' % status_code
        # keep stream alive
        return True

    def on_timeout(self):
        print 'Timeout...'


def init_crawler(consumer_key, consumer_secret, access_token, access_token_secret, db, phrases):

    auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = tweepy.Stream(auth, StreamWatcherListener(db), timeout=None)

    # if phrases:
    #     phrases = phrases.strip()
    # track_list = None
    # if phrases:
    #     track_list = [k for k in phrases.split(',')]

    stream.filter(track=phrases, languages=["en"], async=True)
