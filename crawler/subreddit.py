from datetime import datetime

from model.Base import Session, Subreddit
from crawler.reddit import Reddit

session = Session()
reddit = Reddit


def get_subreddit_details(subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)
    return Subreddit(id=subreddit.id, display_name=subreddit.display_name, title=subreddit.title,
                     description=subreddit.description, subscribers=subreddit.subscribers,
                     created_utc=datetime.utcfromtimestamp(subreddit.created_utc))


def update_subreddit_details(subreddit_name):
    # Get subreddit details
    subreddit = get_subreddit_details(subreddit_name)
    session.merge(subreddit)
    session.commit()
    return subreddit


def get_all_subreddits():
    return session.query(Subreddit).all()
