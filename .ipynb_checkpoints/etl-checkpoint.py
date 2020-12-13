import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    
    # open song file
    df_list = []

    for x in [filepath]:
        df_list.append(pd.read_json(x, lines=True))

    df = pd.concat(df_list, ignore_index=True)

    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].values.tolist()

    for x in song_data[:]:
        try:
            cur.execute(song_table_insert, x)
        except psycopg2.Error as e:
            print("Error: Inserting Rows")
            print(e)
    
    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', \
                      'artist_latitude', 'artist_longitude']].values.tolist()
    
    for x in artist_data[:]:
        try:
            cur.execute(artist_table_insert, x)
        except psycopg2.Error as e:
            print("Error: Inserting Rows")
            print(e)


def process_log_file(cur, filepath):
    
    # open log file
    df_list = []
    
    for x in [filepath]:
        df_list.append(pd.read_json(x, lines=True))

    df = pd.concat(df_list, ignore_index=True)

    # filter by NextSong action
    df = df[df['page'] == 'NextSong']
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')

    # convert timestamp column to datetime
    t = df['ts']
    
    # insert time data records
    time_data = (t, t.dt.hour, t.dt.day, t.dt.weekofyear, t.dt.year, t.dt.month, t.dt.dayofweek)
    column_labels = ('timestamp', 'hour', 'day', 'weekofyear', 'year', 'month', 'dayofweek')
    time_df = pd.DataFrame(
    {
        column_labels[0] : time_data[0],
        column_labels[1] : time_data[1],
        column_labels[2] : time_data[2],
        column_labels[3] : time_data[3],
        column_labels[4] : time_data[4],
        column_labels[5] : time_data[5],
        column_labels[6] : time_data[6]
    }
    ).drop_duplicates().reset_index(drop=True)

    for i, row in time_df.iterrows():
        try:
            cur.execute(time_table_insert, list(row))
        except psycopg2.Error as e:
            print("Error: Inserting Rows")
            print(e)

    # load user table
    user_df = df[['userId', 'firstName','lastName', 'gender', 'level']].drop_duplicates().dropna(axis='index').reset_index(drop=True) 

    # insert user records
    for i, row in user_df.iterrows():
        try:
            cur.execute(user_table_insert, row)
        except psycopg2.Error as e:
            print("Error: Inserting Rows")
            print(e)

    # insert songplay records
    for index, row in df.iterrows():
    
        df_row = pd.DataFrame(columns = ['ts', 'user_id', 'level', 'song_id', 'artist_id', 'session_id', 'location', 'user_agent']) 
    
        # get songid and artistid from song and artist tables
        try:
            cur.execute(song_select, (row.song, row.artist, row.length))
            results = cur.fetchone()
        except psycopg2.Error as e:
            print("Error: SELECT *")
            print(e)
    
        if results:
            songid, artistid = results
            df_row = df_row.append({'ts':row.ts, 'user_id':row.userId, 'level':row.level, 'song_id':results[0], 'artist_id':results[1], 
                      'session_id':row.sessionId, 'location':row.location, 'user_agent':row.userAgent}, ignore_index=True)
        else:
            continue

        # insert songplay record
        songplay_data = df_row.values.tolist()
        for x in songplay_data[:]:
            try:
                cur.execute(songplay_table_insert, x)
            except psycopg2.Error as e:
                print("Error: Inserting Rows")
                print(e)


def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    try:
        conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=robbie password=p@ssw0rd")
    except psycopg2.Error as e:
        print("Error: Could not make connection to the Postgres database")
        print(e)
        
    try:
        cur = conn.cursor()
    except psycopg2.Error as e:
        print("Error: Could not get cursor to the Database")
        print(e)

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()