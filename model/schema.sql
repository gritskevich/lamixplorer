CREATE TABLE subreddit (
    id VARCHAR(20) PRIMARY KEY,
    display_name VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    subscribers INTEGER,
    created_utc DATETIME
);

CREATE TABLE submission (
    id VARCHAR(20) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    redditor_id VARCHAR(20) NOT NULL REFERENCES redditor(id),
    score INTEGER NOT NULL,
    num_comments INTEGER NOT NULL,
    subreddit_id VARCHAR(20) NOT NULL REFERENCES subreddit(id),
    url TEXT,
    created_utc DATETIME,
    selftext TEXT
);

CREATE TABLE redditor (
    id VARCHAR(20) PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
);

CREATE TABLE comment (
    id VARCHAR(20) PRIMARY KEY,
    submission_id VARCHAR(20) NOT NULL REFERENCES submission(id),
    redditor_id VARCHAR(20) NOT NULL REFERENCES redditor(id),
    parent_id VARCHAR(20),
    body TEXT,
    score INTEGER,
    created_utc DATETIME
);

CREATE TABLE submission_status (
    id TEXT PRIMARY KEY,
    status TEXT
);