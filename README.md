Tweet statistics
================================
A simple python server that uses twitter streaming api, to generate simple statistics.

It reports total number of users and tweets processed, and handle of the user who has tweeted maximum number of tweets
for the keyword.


API
---
### GET `/start`
- Description : starts the backgrond process of tweets fetching.
- Query Arguments : `keyword` (keyword to track in tweets)
- Response code : `302`


Prerequisits
------------
- `rq` [Website](http://python-rq.org)
- `Flask` [Website](http://flask.pocoo.org)
- `SqlAlchemy` [Website](http://www.sqlalchemy.org)
