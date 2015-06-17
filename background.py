__author__ = 'parth'

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from sqlalchemy.orm import sessionmaker
import models
import json
import config


from sqlalchemy import create_engine
engine = create_engine(config.database_uri)

models.Base.metadata.create_all(engine)

# Creating static session for background job
Session = sessionmaker(bind=engine)
session = Session()


class StatsListener(StreamListener):

    # This function captures the tweet from twitter streaming api
    # data parameter denotes the json data we received from the api
    def on_data(self, data):
        recv = json.loads(data)

        # We need try catch here because sometimes data from api
        # is not accurate
        try:
            user = self.get_user_from_stream_data(recv)
            tweet = self.get_tweet_from_stream_data(recv)
        except KeyError:
            return True

        # Case where user's tweet is received first time
        if models.User.get_by_id(session, user.id) is None:
            session.add(user)
            # initialize the count to 1 because we discovered
            # first tweet of this user.
            session.add(models.TweetCount(user.id, 1))
            # To prevent duplicate tweets in database
            if models.Tweet.get_by_id(session, tweet.id) is None:
                session.add(tweet)
            session.commit()
            return True

        # Increment current count
        tweet_count = models.TweetCount.get_by_user_id(session, user.id)
        tweet_count.count += 1
        # To prevent duplicate tweets in database
        if models.Tweet.get_by_id(session, tweet.id) is None:
                session.add(tweet)
        session.commit()
        return True

    # Fetch user from stream data.
    @staticmethod
    def get_user_from_stream_data(data):
        user_obj = data['user']
        return models.User(user_obj['id'], user_obj['name'], user_obj['screen_name'])

    # Fetch tweet from stream data.
    @staticmethod
    def get_tweet_from_stream_data(data):
        return models.Tweet(data['id'], data['text'], data['user']['id'])

    def on_error(self, status):
        print(status)


def tweet_processor(track_keyword):
    l = StatsListener()
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_token_secret)

    stream = Stream(auth, l)
    # Track all tweets containing the keyword.
    stream.filter(track=[track_keyword])



