from model.Base import Session, SubmissionStatus

session = Session()


def populate_submission_status_table(submission_ids):
    for submission_id in submission_ids:
        if not session.query(SubmissionStatus).filter_by(id=submission_id).first():
            session.add(SubmissionStatus(id=submission_id, status=SubmissionStatus.PENDING))
            session.commit()
