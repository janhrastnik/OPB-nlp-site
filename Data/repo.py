import psycopg2, psycopg2.extras, psycopg2.extensions
from Data.auth import auth
from Data.models import Sighting, User
from typing import List

# the Repo class contains methods that will fetch data from the database

class Repo:
    def __init__(self):
        self.conn = psycopg2.connect(dbname=auth['db'], user=auth['user'], password=auth['password'], host = auth['host'], port=auth['port']) 
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def get_all_sightings(self) -> List[Sighting]:
        self.cur.execute("""
            SELECT * FROM sightings;
            """)

        res = self.cur.fetchall()

        sightings = [Sighting.from_dict(x) for x in res]

        return sightings

    def get_sightings_paginated(self, page: int) -> List[Sighting]:
        self.cur.execute(f"""
            SELECT * FROM sightings LIMIT 10 OFFSET {10*(page-1)};
            """)

        res = self.cur.fetchall()

        sightings = [Sighting.from_dict(x) for x in res]

        return sightings

    def get_all_users(self):
        self.cur.execute("""
            SELECT * FROM users;
            """)

        # TODO: have this data typed and send it to the Service and Presentation layers 
        res = self.cur.fetchall()

        print(res)

    def add_new_user(self, email: str, nickname: str, hashed_password: str):
        self.cur.execute(f"""
            INSERT INTO users (username, email, password) VALUES (
                '{nickname}',
                '{email}',
                '{hashed_password}'
            );""")

        self.conn.commit()

    def user_exists(self, email: str) -> bool:

        user_exists_flag = False

        self.cur.execute(f"""
            SELECT 1 FROM users WHERE email = '{email}';
            """)

        if self.cur.fetchone():
            user_exists_flag = True

        return user_exists_flag;

    def get_user(self, email: str) -> User:

        self.cur.execute(f"""
            SELECT * FROM users WHERE email = '{email}';
            """)

        user = User.from_dict(self.cur.fetchone())

        return user
    
    # TODO: we will need methods that get users, comments etc.
        


    def add_sighting(date, location, description, witness):
        self.cur.execute("""
            INSERT INTO sightings (date, location, description, witness)
            VALUES (?, ?, ?, ?)
        """, (date, location, description, witness))
        self.conn.commit()
