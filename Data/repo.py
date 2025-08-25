import psycopg2
import psycopg2.extras
import psycopg2.extensions
from datetime import datetime
from Data.auth import auth
from Data.models import Sighting, User, Comment
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

    def get_user_sightings(self, user_id: int) -> List[Sighting]:
        self.cur.execute(f"""
            SELECT * FROM sightings WHERE user_id = {user_id};
            """)

        res = self.cur.fetchall()

        sightings = [Sighting.from_dict(x) for x in res]

        return sightings

    def get_all_users(self):
        self.cur.execute("""
            SELECT * FROM users;
            """)

        res = self.cur.fetchall()

        users = [User.from_dict(x) for x in res]

        print(users)

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

        return user_exists_flag

    def get_user(self, email: str) -> User:

        self.cur.execute(f"""
            SELECT * FROM users WHERE email = '{email}';
            """)

        user = User.from_dict(self.cur.fetchone())

        return user
    
    def add_sighting(self, sighting: Sighting):
        coords = f"{sighting.coords}"  # coords should already be in "lat, long" format
        self.cur.execute("""
            INSERT INTO sightings (title, sighting_date, description, coords, duration, user_id, creation_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (
            sighting.title,
            sighting.sighting_date.strftime("%Y-%m-%d %H:%M:%S"),
            sighting.description,
            coords,
            sighting.duration,
            sighting.user_id,
            sighting.creation_date.strftime("%Y-%m-%d %H:%M:%S")
        ))
        self.conn.commit()

    def get_sighting_by_id(self, sighting_id: int) -> Sighting:
        self.cur.execute("""
            SELECT * FROM sightings WHERE id = %s;
        """, (sighting_id,))
        row = self.cur.fetchone()
        if row:
            return Sighting.from_dict(row)
        return None

    def delete_sighting(self, sighting_id: int) -> bool:
        self.cur.execute("""
            DELETE FROM sightings WHERE id = %s;
        """, (sighting_id,))
        self.conn.commit()
        return True

    def add_comment(self, email: str, comment: str, sighting_id: int):
        # we get the user id first
        self.cur.execute(f"""
            SELECT id FROM users WHERE email = '{email}';
            """)

        user_id = self.cur.fetchone()[0]

        print("SIIEIE", user_id)
        
        # we add the comment
        self.cur.execute(f"""
            INSERT INTO comments (content, creation_date, user_id, sighting_id) VALUES (
                '{comment}',
                '{datetime.now()}',
                '{user_id}',
                '{sighting_id}'
            );""")

        self.conn.commit()

    def get_sighting_comments(self, sighting_id: int) -> List[Comment]:
        self.cur.execute(f"""
            SELECT * FROM comments WHERE sighting_id = '{sighting_id}';
            """)

        res = self.cur.fetchall()

        comments = [Comment.from_dict(x) for x in res]

        return comments

