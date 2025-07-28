import psycopg2
import sys
from auth import *

"""
This script sets up the database if the user doesn't have the 'nlp' 
database yet. We expect this to run when the user launches the app 
for the first time. 

We create required tables and fill them with data, that
we got from https://www.kaggle.com/datasets/NUFORC/ufo-sightings/data.

TODO: maybe add more placeholder data here, like other users?
"""

conn = psycopg2.connect(dbname=auth['db'], user=auth['user'], password=auth['password'], host = auth['host'], port=auth['port'])

cur = conn.cursor()

args = sys.argv
try:
    if args[1] == "--clean":
        # wipe any previous tables that might exist to do a clean setup

        cur.execute("""
            DROP TABLE IF EXISTS users cascade;
            DROP TABLE IF EXISTS sightings;
            DROP TABLE IF EXISTS comments;
            DROP TABLE IF EXISTS locations;
            DROP TABLE IF EXISTS shapes;
        """)
except IndexError:
    pass

# TABELA UPORABNIKOV
cur.execute("""CREATE TABLE users (
    id serial PRIMARY KEY,
    username varchar(50) unique,
    email varchar(255) unique,
    password varchar(255),
    salt text
);""")

# TABELA OPAŽANJ
cur.execute("""CREATE TABLE sightings (
    id serial PRIMARY KEY,
    title varchar(255),
    sighting_date timestamptz,
    description text,
    coords point,
    duration varchar(255),
    user_id integer not null references users(id) on delete cascade,
    creation_date timestamp default current_timestamp
);""")

# TABELA KOMENTARJEV
cur.execute("""CREATE TABLE comments (
    id serial PRIMARY KEY,
    content text,
    creation_date timestamp default current_timestamp,
    user_id integer not null references users(id) on delete cascade,
    sighting_id integer not null references sightings(id) on delete cascade 
);""")

# TABELA LOKACIJ
cur.execute("""CREATE TABLE locations (
    id serial PRIMARY KEY,
    city varchar(255),
    country varchar(255)
);""")

cur.execute("""CREATE TABLE shapes (
    id serial PRIMARY KEY,
    name varchar(255)   
);""")

conn.commit()

cur.close()
conn.close()
