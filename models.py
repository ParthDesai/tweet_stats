__author__ = 'parth'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, ForeignKey, BigInteger, Integer
from sqlalchemy.orm import relationship


Base = declarative_base()

# Model representing number of tweets for
# particular user.
# Note: This is more efficient than storing count
# with user table and more normalized.
class TweetCount(Base):
    __tablename__ = 'tweet_counts'

    user_id = Column(BigInteger, ForeignKey('users.id'), primary_key=True)
    count = Column(Integer)
    user = relationship('User')

    def __init__(self, user_id, count):
        self.user_id = user_id
        self.count = count

    def __repr__(self):
        return "User id:" + self.user_id + " " + "has tweets:" + self.count

    # Get tweet count of the user
    # 0 will be returned in case of count does not found.
    @classmethod
    def get_tweet_count(cls, session, user_id):
        entity = cls.get_by_user_id(session, user_id)
        if entity is None:
            return 0
        return entity.count

    # Get count of particular user.
    @classmethod
    def get_by_user_id(cls, session, user_id):
        return session.query(cls).filter_by(user_id=user_id).first()

    # Get the user whose tweet count is maximum.
    @classmethod
    def get_max_tweet_count(cls, session):
        return session.query(cls).order_by(TweetCount.count.desc()).first()


# Model representing tweets
# Following attribute of tweet is stored:
# *tweet_id in id
# *user_id in user_id
# *tweet_text in text
class Tweet(Base):
    __tablename__ = 'tweets'

    id = Column(BigInteger, primary_key=True)
    text = Column(String, nullable=False)

    user_id = Column(BigInteger, ForeignKey('users.id'))
    user = relationship('User', back_populates='tweets')

    def __init__(self, tweet_id, text, user_id):
        self.id = tweet_id
        self.text = text
        self.user_id = user_id

    def __repr__(self):
        return self.tweet_id + " " + "tweeted by " + self.user_id + " " + "Text:" + self.text

    # Get number of tweets
    @classmethod
    def get_count(cls, session):
        return session.query(cls).count()

    # Get number of users.
    @classmethod
    def get_by_id(cls, session, tweet_id):
        return session.query(cls).filter_by(id=tweet_id).first()


# Model representing user
# Following attributes are stored:
# *user_id in id
# *user_name in name
# *user_screen_name in handle
class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    handle = Column(String, index=True, nullable=False)

    tweets = relationship('Tweet', back_populates='user')

    def __init__(self, user_id, name, handle):
        self.id = user_id
        self.name = name
        self.handle = handle

    def __repr__(self):
        return "Handle: " + self.handle + " " + "Name: " + self.name

    # Get user by id.
    @classmethod
    def get_by_id(cls, session, user_id):
        return session.query(cls).filter_by(id=user_id).first()

    # Get number of users
    @classmethod
    def get_count(cls, session):
        return session.query(cls).count()
