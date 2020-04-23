import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    '''
    This procedure processes a song file whose filepath has been provided as an arugment.
    It extracts the song information in order to store it into the songs table.
    Then it extracts the artist information in order to store it into the artists table.

    INPUTS:
    * cur the cursor variable
    * filepath the file path to the song file
    '''
    # open song file
    df = pd.read_json(filepath, lines=True) 

    # insert song record
    song_data = df[['song_id','title','artist_id','year','duration']].values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id','artist_name','artist_location','artist_latitude','artist_longitude']].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    '''
    This procedure processes a log file whose filepath has been provided as an arugment.
    The data is filtered for NextSong action and timestamp used to extract required details
    The details are inserted into time table  
    Then it extracts the user information in order to store it into the users table.
    Lastly, the data from the log file, timestamp, and users table would have its extract information stored in the songplays table.

    INPUTS:
    * cur the cursor variable
    * filepath the file path to the log file
    '''

    # open log file
    df = pd.read_json(filepath, lines=True) 

    # filter by NextSong action
    df = df[df['page']=='NextSong']
    df['timestamp'] = pd.to_numeric(round(df['ts']/1000, 0), downcast='signed')
    df.loc[:, 'ts'] = df.ts.apply(lambda x: pd.datetime.fromtimestamp(x/1000))
    df['hour'] = df['ts'].dt.hour
    df['day'] = df['ts'].dt.day
    df['weekofyear'] = df['ts'].dt.weekofyear
    df['month'] = df['ts'].dt.month
    df['year'] = df['ts'].dt.year
    df['dayofweek'] = df['ts'].dt.dayofweek
    column_names = ['ts','hour','day','weekofyear','month','year','dayofweek']
    # convert timestamp column to datetime
    t = df[column_names]
    
    # insert time data records
    time_data = t.values
    column_labels = ['ts','hour','day','weekofyear','month','year','dayofweek']
    time_df = df[column_labels]

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId','firstName','lastName','gender','level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    '''
    This procedure processes files whose filepath has been captured from the directory path provided as an arugment.
    It captures the files within the path directory and loops through all the file in the directory given in path
    Then it extracts the file path and submits the filepath and other details to the function provided.

    INPUTS:
    * cur the cursor variable
    * conn the database connection variable
    * filepath the file path to the data folders and files
    * func the function that processes the file variable
    '''

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
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
