from flask import Flask, redirect

from rq import Queue
from redis import Redis
from background import tweet_processor
from flask import render_template, request
from sqlalchemy.orm import sessionmaker

import models

import config

app = Flask(__name__)

redis_conn = Redis()
# Have a timeout large enough.
q = Queue(default_timeout=9999999, connection=redis_conn)

from sqlalchemy import create_engine
engine = create_engine(config.database_uri, echo=True)

models.Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


# class to store the tweet statistics.
class TweetStats:
    def __init__(self, tweets, users, max_user):
        self.tweets = tweets
        self.users = users
        self.max_user = max_user

# Displays the page where we can see statistics.
@app.route('/')
def stats():
    session = Session()
    max_tweet_count = models.TweetCount.get_max_tweet_count(session)
    tweets = models.Tweet.get_count(session)
    users = models.User.get_count(session)
    # Handle a case where database is not populated
    if max_tweet_count is not None:
        max_tweet_user_handle = max_tweet_count.user.handle
    else:
        max_tweet_user_handle = 0
    session.close()
    return render_template("stats.html", stats=TweetStats(tweets, users, max_tweet_user_handle))


# Start the background job with the keyword
# specified as query parameter.
@app.route('/start')
def start_job():
    keyword = request.args.get('keyword')
    q.enqueue(tweet_processor, keyword)
    # Redirect to the statistics page.
    return redirect('/', code=302)


if __name__ == '__main__':
    app.run()
