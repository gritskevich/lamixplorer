from datetime import datetime

from crawler.reddit import Reddit
from model.Base import Session, Comment, SubmissionStatus

session = Session()
reddit = Reddit


def remove_prefix(id_with_prefix):
    before, sep, after = id_with_prefix.partition('_')
    if len(after) > 0:
        return after
    return id_with_prefix


def format_comment(comment):
    comment['created_utc'] = datetime.utcfromtimestamp(comment['created_utc'])


def get_comments_by_parent_id(parent_id):
    return session.query(Comment).filter(Comment.parent_id == parent_id)


def store_comments(submission_id):
    # Retrieve submission
    submission = reddit.submission(id=submission_id)
    submission.comments.replace_more(limit=None)

    # Retrieve comments and store in database
    for praw_comment in submission.comments.list():
        if praw_comment.body == '[deleted]':
            continue
        try:
            comment = Comment(id=remove_prefix(praw_comment.name),
                              submission_id=submission.id,
                              redditor_id=remove_prefix(
                                  praw_comment.author_fullname) if praw_comment.author_fullname else "",
                              parent_id=praw_comment.parent_id.split("_")[1] if praw_comment.parent_id else "",
                              body=praw_comment.body,
                              score=praw_comment.score,
                              created_utc=datetime.utcfromtimestamp(praw_comment.created_utc)
                              )
            session.merge(comment)

        except AttributeError:
            continue

    # Update submission status to "done"
    session.query(SubmissionStatus). \
        filter(SubmissionStatus.id == submission_id). \
        update({SubmissionStatus.status: SubmissionStatus.DONE})
    session.commit()
