import os

import praw
from dotenv import load_dotenv

load_dotenv()

# set up the Reddit API client
Reddit = praw.Reddit(client_id=os.environ.get('REDDIT_CLIENT_ID'), client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
                     user_agent=os.environ.get('REDDIT_USER_AGENT'))
