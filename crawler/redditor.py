from crawler import submission
from crawler.reddit import Reddit
from model.Base import Session, Redditor

session = Session()
reddit = Reddit


def remove_prefix(id_with_prefix):
    before, sep, after = id_with_prefix.partition('_')
    if len(after) > 0:
        return after
    return id_with_prefix


def get_redditor_by_id(redditor_id):
    redditor = reddit.redditor(redditor_id)

    return Redditor(id=redditor_id, username=redditor.name)


def store_redditor_by_id(redditor_id):
    # Get Redditor details
    redditor = get_redditor_by_id(redditor_id)

    session.merge(redditor)
    session.commit()


def update_redditors():
    for redditor_id in submission.get_redditor_id_list():
        store_redditor_by_id(redditor_id)
    return None
