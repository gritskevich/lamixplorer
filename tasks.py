import subprocess

from invoke import task

from crawler import subreddit, submission, redditor, queue, comment
import os
from dotenv import load_dotenv

load_dotenv()

@task
def upgrade_db(ctx):
    """
    Upgrade the database to the latest migration.
    """
    cmd = "alembic upgrade head"
    subprocess.run(cmd, shell=True, check=True)


@task
def update_subreddit_details(ctx, subreddit_name=os.environ.get('DEFAULT_SUBREDDIT_NAME')):
    """Update subreddit details"""
    subreddit.update_subreddit_details(subreddit_name)


@task
def update_submissions(ctx, subreddit_name=os.environ.get('DEFAULT_SUBREDDIT_NAME')):
    """Update submissions"""
    submission.store_submissions(subreddit_name)


@task
def update_redditors(ctx):
    """Update redditors"""
    redditor.update_redditors()


@task
def update_submission_queue(ctx):
    id_list_from_subreddit = submission.get_submission_id_list_to_add_to_queue()
    queue.populate_submission_status_table(id_list_from_subreddit)


@task
def update_comments(ctx):
    from_queue = submission.get_pending_submission_id_list_from_queue()
    for submission_id in from_queue:
        comment.store_comments(submission_id)

@task
def crawl_subreddit(ctx, subreddit_name=os.environ.get('DEFAULT_SUBREDDIT_NAME')):
    upgrade_db(ctx)
    update_subreddit_details(ctx, subreddit_name)
    update_submissions(ctx, subreddit_name)
    update_redditors(ctx)
    update_submission_queue(ctx)
    update_comments(ctx)
