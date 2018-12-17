import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [

    """CREATE TABLE IF NOT EXISTS university_photos(
        id SERIAL PRIMARY KEY NOT NULL,
        logo BYTEA,
        background BYTEA 
    )""",
                   
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

    """CREATE TABLE IF NOT EXISTS events(
        id SERIAL NOT NULL PRIMARY KEY,
        title VARCHAR(50),
        description VARCHAR(200) NOT NULL,
        price INT DEFAULT 0,
        place VARCHAR(80),  
        event_date DATE,
        event_time TIME,
        duration INT,
        club_id INT,
        puan NUMERIC(2,1) DEFAULT 0,
        number_of_evaluation INT DEFAULT 0,
        user_id INT NOT NULL,
        FOREIGN KEY (club_id) REFERENCES clubs ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users ON DELETE SET NULL ON UPDATE CASCADE
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
    )""",
    



    """INSERT INTO universities (name, city, country, address, phone_no, website) VALUES(
        'Istanbul Technical University',
        'Istanbul',
        'Turkey',
        'Maslak 34467',
        '+902165234527',
        'wwww.itu.edu.tr'
    )""",

    """INSERT INTO universities (name, city, country, address, phone_no, website) VALUES(
        'Bogazici University',
        'Istanbul',
        'Turkey',
        'Hisarustu 34467',
        '+903425236787',
        'wwww.bogazici.edu.tr'
    )""",

    """INSERT INTO universities (name, city, country, address, phone_no, website) VALUES(
        'Middle East Technical University',
        'Ankara',
        'Turkey',
        '100. yil No:245 34563',
        '+904525234527',
        'wwww.metu.edu.tr'
    )""",
    
    """INSERT INTO universities (name, city, country, address, phone_no, website) VALUES(
       'Yildiz Teknik Universitesi',
       'Istanbul',
       'Turkey',
       'Davutpasa 34467',
       '+9034738959034',
       'wwww.ytu.edu.tr'
    )""",
   
   """INSERT INTO universities (name, city, country, address, phone_no, website) VALUES(
       'Ege University',
       'Izmir',
       'Turkey',
       'Bornova 34563',
       '+904525833527',
       'wwww.eu.edu.tr'
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
