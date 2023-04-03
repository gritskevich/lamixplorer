from datetime import datetime, timedelta

import requests
from sqlalchemy import text

from model.Base import Session, Submission, SubmissionStatus, engine

session = Session()


def get_submission_with_score_higher_than(score):
    return session.query(Submission).filter(Submission.score > score)


def get_submission_by_id(submission_id):
    return session.query(Submission).filter(Submission.id == submission_id)


def get_redditor_id_list():
    return [i[0] for i in session.query(Submission.redditor_id).distinct()]


def remove_prefix(id_with_prefix):
    before, sep, after = id_with_prefix.partition('_')
    if len(after) > 0:
        return after
    return id_with_prefix


def store_submissions(subreddit):
    # Set up base URL and search parameters
    base_url = "https://api.pushshift.io/reddit/submission/search"
    size = 1000
    after = int((datetime.utcnow() - timedelta(days=10 * 365)).timestamp())  # 10 years ago
    before = int(datetime.utcnow().timestamp())

    while True:
        # Make API request
        params = {"subreddit": subreddit, "sort": "created_utc", "size": size, "after": after, "before": before}
        response = requests.get(base_url, params=params)
        data = response.json()["data"]
        num_results = len(data)

        # Stop if no more results
        if num_results == 0:
            break

        # Update 'before' parameter for next search
        before = data[-1]["created_utc"]

        # Store submissions in database
        for submission_result in data:
            if not ('author_fullname' in submission_result) or submission_result['selftext'] == '[deleted]':
                continue
            submission = Submission(id=submission_result["id"],
                                    title=submission_result['title'],
                                    redditor_id=remove_prefix(submission_result['author_fullname']),
                                    score=submission_result['score'],
                                    num_comments=submission_result['num_comments'],
                                    subreddit_id=remove_prefix(submission_result['subreddit_id']),
                                    url=submission_result['url'],
                                    created_utc=datetime.utcfromtimestamp(submission_result['created_utc']),
                                    selftext=submission_result['selftext'])
            session.merge(submission)
            session.commit()


def get_submission_id_list_to_add_to_queue():
    id_list = engine.connect().execute(text(
        "SELECT DISTINCT(id) FROM submission WHERE id NOT IN (SELECT id FROM submission_status)"
    ))
    return [i[0] for i in id_list]


def get_pending_submission_id_list_from_queue():
    return [i[0] for i in session.query(SubmissionStatus.id).filter(SubmissionStatus.status == SubmissionStatus.PENDING)]
