import psycopg2
from Data.auth import auth

# the Repo class contains methods that will fetch data from the database

class Repo:
    def __init__(self):
        self.conn = psycopg2.connect(dbname=auth['db'], user=auth['user'], password=auth['password'], host = auth['host'], port=auth['port']) 
        self.cur = self.conn.cursor()

    def get_all_sightings(self):
        self.cur.execute("""
            SELECT * FROM sightings                 
            """)

        # TODO: have this data typed and send it to the Service and Presentation layers 
        res = self.cur.fetchall()

        print(res)

    # TODO: we will need methods that get users, comments etc.
        
