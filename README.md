# LamiXplorer

This project is a Python-based Reddit crawler that uses PRAW, Pushshift API, SQLite and Alembic to collect data from a specified subreddit.

## Prerequisites
Before running the crawler, you will need to obtain API keys for the OpenAI API and the Reddit API. You can get these keys by signing up for the respective services.

You will also need to create a .env file in the root directory of the project and add the following environment variables:

```
OPENAI_API_KEY=<your OpenAI API key>
REDDIT_CLIENT_ID=<your Reddit client ID>
REDDIT_CLIENT_SECRET=<your Reddit client secret>
REDDIT_USER_AGENT=<your Reddit user agent string>
```

## Installation

To install the required packages, run:

```
pip install -r requirements.txt
```

## Usage
To crawl a subreddit, run:


```
invoke crawl_subreddit --subreddit_name=<subreddit_name>
```
This will update the subreddit details, store the submissions, update the redditors, update the submission queue, and store the comments for the specified subreddit.