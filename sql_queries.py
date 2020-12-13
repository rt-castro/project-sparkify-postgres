# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
songplay_id SERIAL PRIMARY KEY,
start_time timestamp NOT NULL REFERENCES time (start_time),
user_id integer NOT NULL REFERENCES users (user_id),
level text NOT NULL,
song_id text REFERENCES songs (song_id),
artist_id text REFERENCES artists (artist_id),
session_id integer NOT NULL,
location text,
user_agent text NOT NULL,
CONSTRAINT fk_time_songplays FOREIGN KEY (start_time) REFERENCES time (start_time) ON DELETE SET NULL,
CONSTRAINT fk_users_songplays FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE SET NULL,
CONSTRAINT fk_songs_songplays FOREIGN KEY (song_id) REFERENCES songs (song_id) ON DELETE SET NULL,
CONSTRAINT fk_artists_songplays FOREIGN KEY (artist_id) REFERENCES artists (artist_id) ON DELETE SET NULL
);
CREATE UNIQUE INDEX songplays_idx on songplays (start_time, session_id)
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
INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (start_time, session_id)
DO UPDATE SET song_id = EXCLUDED.song_id, artist_id = EXCLUDED.artist_id
""")

user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (user_id)
DO UPDATE SET level = EXCLUDED.level
""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (song_id)
DO NOTHING
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location, latitude, longitude)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (artist_id)
DO UPDATE SET name=EXCLUDED.name, location=EXCLUDED.location, latitude=EXCLUDED.latitude, longitude=EXCLUDED.longitude
""")


time_table_insert = ("""
INSERT INTO time (start_time, hour, day, weekofyear, year, month, dayofweek)
VALUES (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (start_time)
DO NOTHING
""")

# FIND SONGS
song_select = ("""
SELECT s.song_id, a.artist_id
FROM songs s
JOIN artists a ON s.artist_id = a.artist_id
WHERE s.title = %s
AND a.name = %s
AND s.duration = %s
""")

# QUERY LISTS

create_table_queries = [user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]