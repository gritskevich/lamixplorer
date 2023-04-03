from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create a database connection
engine = create_engine("sqlite:///lamictal.sqlite")
Session = sessionmaker(bind=engine)

# Define a base class for all models
Base = declarative_base()
metadata = Base.metadata


class Subreddit(Base):
    __tablename__ = 'subreddit'
    id = Column(String(20), primary_key=True)
    display_name = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    subscribers = Column(Integer)
    created_utc = Column(DateTime)


class Submission(Base):
    __tablename__ = 'submission'
    id = Column(String(20), primary_key=True)
    title = Column(String(255), nullable=False)
    redditor_id = Column(String(20), ForeignKey('redditor.id'), nullable=False)
    score = Column(Integer, nullable=False)
    num_comments = Column(Integer, nullable=False)
    subreddit_id = Column(String(20), ForeignKey('subreddit.id'), nullable=False)
    url = Column(Text)
    created_utc = Column(DateTime)
    selftext = Column(Text)


class Redditor(Base):
    __tablename__ = 'redditor'
    id = Column(String(20), primary_key=True)
    username = Column(String(50), nullable=False)


class Comment(Base):
    __tablename__ = 'comment'
    id = Column(String(20), primary_key=True)
    submission_id = Column(String(20), ForeignKey('submission.id'), nullable=False)
    redditor_id = Column(String(20), ForeignKey('redditor.id'), nullable=False)
    parent_id = Column(String(20))
    body = Column(Text)
    score = Column(Integer)
    created_utc = Column(DateTime)


class SubmissionStatus(Base):
    PENDING = 'pending'
    DONE = 'done'
    __tablename__ = 'submission_status'
    id = Column(Text, primary_key=True)
    status = Column(Text)
