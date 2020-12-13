# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
songplay_id int PRIMARY KEY,
start_time timestamp NOT NULL,
user_id integer NOT NULL,
level text NOT NULL,
song_id text NOT NULL,
artist_id text NOT NULL,
session_id integer NOT NULL,
location text,
user_agent text NOT NULL
)
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
user_id integer PRIMARY KEY,
first_name text NOT NULL,
last_name text NOT NULL,
gender text NOT NULL,
level text NOT NULL
)
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
song_id text PRIMARY KEY,
title text NOT NULL,
artist_id text NOT NULL,
year integer NOT NULL,
duration numeric NOT NULL
)
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
artist_id text PRIMARY KEY,
name text NOT NULL,
location text,
latitude numeric,
longitude numeric
)
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (
start_time timestamp PRIMARY KEY,
hour integer NOT NULL,
day integer NOT NULL,
weekofyear integer NOT NULL,
year integer NOT NULL,
month integer NOT NULL,
dayofweek integer NOT NULL
)
""")

# INSERT RECORDS

songplay_table_insert = ("""
INSERT INTO songplays
VALUES (%s, %s, %s, %s, %s, %s, %s, %s ,%s)
ON CONFLICT (songplay_id)
DO NOTHING
""")

user_table_insert = ("""
INSERT INTO users
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (user_id)
DO NOTHING
""")

song_table_insert = ("""
INSERT INTO songs
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (song_id)
DO NOTHING
""")

artist_table_insert = ("""
INSERT INTO artists 
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (artist_id)
DO NOTHING
""")


time_table_insert = ("""
INSERT INTO time 
VALUES (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (start_time)
DO NOTHING
""")

# FIND SONGS
song_select = ("""
SELECT s.song_id, a.artist_id
FROM songs s
JOIN artists a ON s.artist_id = a.artist_id
AND s.title = %s
AND a.name = %s
AND s.duration = %s
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]