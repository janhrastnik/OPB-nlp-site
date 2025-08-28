import psycopg2
import os
import random
from datetime import datetime, timedelta
from Data.auth import auth

"""
This class sets up the database if the user doesn't have the 'nlp' 
database yet. We expect this to run when the user launches the app 
for the first time.

We create required tables and fill them with data, that
we got from https://www.kaggle.com/datasets/NUFORC/ufo-sightings/data.
"""

class DatabaseSetup:
    def __init__(self):
        self.conn = psycopg2.connect(dbname=auth['db'], user=auth['user'], password=auth['password'], host = auth['host'], port=auth['port'])
        self.cur = self.conn.cursor()

    def should_setup(self) -> bool:
        # we determine if we need to run the setup process
        # obviously we don't want to run the setup if the user already has a filled database created

        setup_flag = False

        # we know that the database already exists, that responsibility falls onto the user

        # check if sightings table exists
        self.cur.execute("""
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'public'
              AND table_name = 'sightings';
            """)

        res_1 = self.cur.fetchone()

        if res_1:
            # check if sightings table has any entries
            self.cur.execute("""
                SELECT count(*) AS exact_count FROM sightings;
                """)

            res_2 = self.cur.fetchone()

            if res_2[0] != 0:
                setup_flag = False

        return setup_flag

    def setup(self):
        self.wipe_any_old_data()
        self.setup_tables()
        self.setup_data()

    def wipe_any_old_data(self):
        self.cur.execute("""
            DROP TABLE IF EXISTS users cascade;
            DROP TABLE IF EXISTS sightings cascade;
            DROP TABLE IF EXISTS comments;
            DROP TABLE IF EXISTS locations;
            DROP TABLE IF EXISTS shapes;
            """)

        self.conn.commit()

    def setup_tables(self):
        # TABELA UPORABNIKOV
        self.cur.execute("""CREATE TABLE users (
            id serial PRIMARY KEY,
            username varchar(50) unique,
            email varchar(255) unique,
            password varchar(255)
        );""")

        # TABELA OPAŽANJ
        self.cur.execute("""CREATE TABLE sightings (
            id serial PRIMARY KEY,
            title varchar(255),
            sighting_date timestamp,
            description text,
            coords point,
            duration varchar(255),
            user_id integer not null references users(id) on delete cascade,
            creation_date timestamp default current_timestamp
        );""")

        # TABELA KOMENTARJEV
        self.cur.execute("""CREATE TABLE comments (
            id serial PRIMARY KEY,
            content text,
            creation_date timestamp default current_timestamp,
            user_id integer not null references users(id) on delete cascade,
            sighting_id integer not null references sightings(id) on delete cascade 
        );""")

        # TABELA LOKACIJ
        self.cur.execute("""CREATE TABLE locations (
            id serial PRIMARY KEY,
            city varchar(255),
            country varchar(255)
        );""")

        # TABELA OBLIK OPAŽANJ
        self.cur.execute("""CREATE TABLE shapes (
            id serial PRIMARY KEY,
            name varchar(255)   
        );""")

        self.conn.commit()

    def setup_data(self):
        # create some placeholder users
        self.cur.execute("""INSERT INTO users (username, email, password) VALUES (
            'VladimirBober',
            'vladimir-bober@fake-email',
            'bad-password'
        );""")

        self.cur.execute("""INSERT INTO users (username, email, password) VALUES (
            'JohnSmith',
            'john-smith@fake-email',
            'bad-password'
        );""")

        self.cur.execute("""INSERT INTO users (username, email, password) VALUES (
            'JaneDoe',
            'jane-doe@fake-email',
            'bad-password'
        );""")

        self.cur.execute("""INSERT INTO users (username, email, password) VALUES (
            'WillSmith',
            'will-smith@fake-email',
            'bad-password'
        );""")

        self.cur.execute("""INSERT INTO users (username, email, password) VALUES (
            'KevinBaker',
            'kevin-baker@fake-email',
            'bad-password'
        );""")

        self.conn.commit()

        # we get the absolute file path of our csv data file, otherwise relative filepath would work only from certain working directory
        # downside is that if we move any of the files, this will silently break
        dirname = os.path.dirname(__file__)
        data_filepath = os.path.join(dirname, '../podatki/complete.csv')

        # DATA COLUMNS IN ORDER
        # datetime,city,state,country,shape,duration (seconds),duration (hours/min),comments,date posted,latitude,longitude

        # here we add in our existing ufo data we got from kaggle
        # assume, we have some placeholder users already defined in the db
        # and randomly assign them the ufo sightings as if they were theirs
        # for the sake of making a demo project
        with open(data_filepath) as F:
            lines = [x.strip() for x in F.readlines()]

            queries = []

            # fixes a DatetimeFieldOverflow error (not really)
            # self.cur.execute("SET datestyle=mdy;")

            # only do 10000 entries due to fmf server limitations
            for i, line in enumerate(lines[1:10000]):
                line = line.split(",")
                # SIGHTINGS COLUMNS IN ORDER
                # title, sighting_date, description, coords, duration, user_id, creation_date 
                shape = "unknown" if line[4] == "" else line[4]
                title = f"Sighting of {shape}-shaped UFO in {line[1].capitalize()}, {line[2].capitalize()}"
                coords = f"({line[9]}, {line[10]})"

                sighting_date = ""
                creation_date = ""

                try: 
                    if line[0].endswith("24:00"):
                        # Parse just the date part
                        dt = datetime.strptime(line[0][:10].strip(), "%m/%d/%Y")
                        # Move to the next day at midnight
                        dt += timedelta(days=1)
                        sighting_date = dt.replace(hour=0, minute=0)
                    else:
                        sighting_date = datetime.strptime(line[0], "%m/%d/%Y %H:%M")

                    creation_date = datetime.strptime(line[8], "%m/%d/%Y")
                except ValueError:
                    # entry is broken and will not make it into the db
                    continue
                

                query = f"""INSERT INTO sightings (title, sighting_date, description, coords, duration, user_id, creation_date) VALUES (
                    '{title}',
                    '{sighting_date}',
                    '{line[7]}',
                    '{coords}',
                    '{line[6]}',
                    '{random.randint(1, 5)}',
                    '{creation_date}'
                )
                """

                queries.append(query)

            for query in queries:
                try:
                    self.cur.execute(query)
                except psycopg2.errors.InvalidTextRepresentation:
                    # some of the sighting entries are flawed, we should not bother rescuing all of them
                    self.conn.rollback()

        self.conn.commit()
