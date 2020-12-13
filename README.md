# SPARKIFY

CONTENTS OF THIS FILE
---------------------

 * Introduction
 * Requirements
 * Schema Design
 * Project Files
 * Configuration
 * Process
 * Maintainers
 

INTRODUCTION
------------

 * A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

 * They'd like to have a database with tables designed to optimize queries on song play analysis. This project aims is to create a database schema and ETL pipeline for this analysis.


REQUIREMENTS
------------

This project utilizes the following technologies:

 * **Software**
 
    - *Anaconda* (https://www.anaconda.com/products/individual)

      Used to run the .ipynb files, and also to test the validity of the ETL process 
 
   - *PostgreSQL* (https://www.postgresql.org/download/)

     The RDBMS that this project utilizes.
     
   - *Python* (https://www.python.org/downloads/)

     The main language where the project is based on.
 
 * **Python Libraries** (does not come built-in with the Python or Anaconda software download)
    
   - *psycopg2* (https://pypi.org/project/psycopg2/)

     Psycopg is the most popular PostgreSQL database adapter for the Python programming language.
     Used for developing the ETL process in python.

   - *ipython-sql* (https://pypi.org/project/ipython-sql/)

     Connect to a database, using SQLAlchemy URL connect strings, then issue SQL commands within IPython or IPython. 
     Used for running the some cells in test.ipynb to test the validity of the ETL process. 
 
 
SCHEMA DESIGN
-------------

 * Fact Table
 
    1. **songplays** - records in log data associated with song plays
    
       - *columns: songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
       
 * Dimension Tables

    2. **users** - users in the app
    
       - *columns: songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
       
    3. **songs** - songs in music database
    
       - *columns: song_id, title, artist_id, year, duration

    4. **artists** - artists in music database
    
       - *columns: artist_id, name, location, latitude, longitude

    5. **time** - timestamps of records in songplays broken down into specific units
    
       - *columns: start_time, hour, day, week, month, year, weekday


PROJECT FILES
-------------

 * Connection
    - **creds.py**: contains the connection details to be used for the connection string.
    - **conn.py**: contains the connection string with the details from the **creds.py** file.
 
 * Create Tables
    - **create.py**: It accesses the default postgres database to create the database *sparkifydb*, and drop the fact and dimension tables if they exist, and then create them.
    
 * ETL
    - **sql_queries.py**: Contains the queries that will be processed in the ETL workflow.
    - **etl.py**: Runs the whole ETL process - creating the connection to the postgres database, reading the JSON files, and then ingesting thrm to the database.
    - **etl.ipynb**: A more sequential and detailed breakdown of each of the main processes in the ETL workflow.

 * Test
    - **test.ipynb**: Tests whether the files were successfully ingested.

   
CONFIGURATION
-------------
 
 * Configure the connection credentials in the **creds.py** file to simulate your local production:

    - **hostname**: This is the hostname or the host IP of where your postgres server is located.

    - **db**: This is the database name.

    - **usr**: This will be the user that you have setup in your postgres server.
     
    - **passwd**: This will be the password of the active user.
     
 * Configure the connection credentials in the **test.ipynb** when trying to setup a connection to your local Postgres for sparkifydb:
    - [4] %sql postgresql://hostname:password@hostname/dbname
    

PROCESS
-------

 * Configure the **creds.py** to replicate the connection details of your local production.
 * Run the **create_tables.py** to drop/create the tables that will be used in the project.
 * Run the **etl.py** to extract the data from the JSON files and ingest them to the created database.
 * Run the **test.ipynb** to check whether the data ingestion was successful.


MAINTAINERS
-----------

Current maintainers:
 * Robert Carlo T. Castro (rt-castro) - https://www.github.com/rt-castro