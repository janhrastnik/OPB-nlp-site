import psycopg2, psycopg2.extras, psycopg2.extensions
from Data.auth import auth
from Data.models import Sighting
from typing import List

# the Repo class contains methods that will fetch data from the database

class Repo:
    def __init__(self):
        self.conn = psycopg2.connect(dbname=auth['db'], user=auth['user'], password=auth['password'], host = auth['host'], port=auth['port']) 
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def get_all_sightings(self) -> List[Sighting]:
        self.cur.execute("""
            SELECT * FROM sightings
            """)

        # TODO: have this data typed and send it to the Service and Presentation layers 
        res = self.cur.fetchall()

        #print(type(res))
        #print(type(res[0]))
        #print(dict(res[0]))
        sightings = [Sighting.from_dict(x) for x in res]

        #print(res)

        return sightings

    def get_all_users(self):
        self.cur.execute("""
            SELECT * FROM users
            """)

        # TODO: have this data typed and send it to the Service and Presentation layers 
        res = self.cur.fetchall()

        print(res)

    def add_new_user(self, email, nickname, hashed_password):
        self.cur.execute(f"""
            INSERT INTO users (username, email, password) VALUES (
                '{nickname}',
                '{email}',
                '{hashed_password}'
            );""")

    # TODO: we will need methods that get users, comments etc.
        
