import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
    """CREATE TABLE IF NOT EXISTS universities(
        id SERIAL NOT NULL PRIMARY KEY,
        name VARCHAR(100) UNIQUE NOT NULL,
        city VARCHAR(15),
        country VARCHAR(30),
        images_id INT,
        score_id INT,
        address TEXT UNIQUE,
        phone_no VARCHAR(13) UNIQUE,
        website VARCHAR(50) UNIQUE,
        FOREIGN KEY (images_id) REFERENCES university_photos ON DELETE SET NULL ON UPDATE CASCADE,
        FOREIGN KEY (score_id) REFERENCES avg_score ON DELETE SET NULL ON UPDATE CASCADE
    )""",

    

    """CREATE TABLE IF NOT EXISTS users(
        id SERIAL NOT NULL PRIMARY KEY, 
        name VARCHAR(20) NOT NULL, 
        surname VARCHAR(20) NOT NULL, 
        nickname VARCHAR(20) UNIQUE NOT NULL,
        password VARCHAR(80) NOT NULL,
        email TEXT UNIQUE NOT NULL,
        status VARCHAR(15) NOT NULL,
        city VARCHAR(15),
        university_id INT,
        last_login TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        registration_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        avatar BYTEA DEFAULT NULL,
        FOREIGN KEY (university_id) REFERENCES universities ON DELETE SET NULL ON UPDATE CASCADE
    )""",

	"""CREATE TABLE IF NOT EXISTS comments(
        id SERIAL NOT NULL PRIMARY KEY,
        title VARCHAR(50) NOT NULL,
        body VARCHAR(200) NOT NULL,
        useful_no INT DEFAULT 0,
        useless_no INT DEFAULT 0,
        user_id INT NOT NULL,
        event_id INT NOT NULL,
        comment_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        user_nickname VARCHAR(20) NOT NULL,
        FOREIGN KEY (event_id) REFERENCES events ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users ON DELETE CASCADE ON UPDATE CASCADE
    )"""
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)

