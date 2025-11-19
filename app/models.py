import sqlite3
import csv
import os

DB_PATH = "instance/movie.db"

#Database Connection Helper
def get_db_connection():
    '''Creates a SQLite connection with row access by column name'''
    con_nect = sqlite3.connect(DB_PATH) #Opens SQLite file.Flask(create one by default) if file == None
    con_nect.row_factory = sqlite3.Row #row["title"] instead of row[1]
    return con_nect #Returns the database connection for use elsewhere

#Create tables for your Database
def create_tables():
    '''Helper tht creates our tables if they don't exist'''
    con_nect = get_db_connection() #Gets new SQLite connection using your helper function
    cursor = con_nect.cursor() #Creates a cursor object. A cursor executes SQL queries "SQL command tool"

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            genre TEXT,
            year INTEGER,
            description TEXT, 
            rating REAL       
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            movie_id INTEGER,
            rating REAL,
            FOREIGN KEY (movie_id) REFERENCES movies(id)
        );
    """)

    con_nect.commit() #Saves(writes) the table creation changes to the database
    con_nect.close() #Closes the connection - important for avoiding memory leaks or locked DS files

#Insert Movie into DATABASE
def insert_movie(movie):
    """Insert a movie Dict {"title": "...", "genre": "..."}"""
    #Each time(function) you need to connect to the database
    con_nect = get_db_connection()
    cursor = con_nect.cursor()

    cursor.execute("""
        INSERT INTO movies (title, genre, year, description, rating)
        VALUES (?, ?, ?, ?, ?)
    """), (
        movie.get("title"),
        movie.get("genre"),
        movie.get("year"),
        movie.get("desciption"),
        movie.get("rating")
    )

    con_nect.commit()
    con_nect.close()


#Load CSV
def load_movies_from_csv(csv_path):
    """Load movies from CSV into SQLite DB"""
    if not os.path.exists(csv_path):
        print(f"CSV not found: {csv_path}")
        return
    
    con_nect = get_db_connection()
    cursor = con_nect.cursor()

    with open(csv_path, encoding='UTF-8') as file:
        reader = csv.DictReader(file) #row["key"]

        for row in reader:
            cursor.execute("""
                INSERT INTO movies (title, genre, year, description, rating)
                VALUES (?, ?, ?, ?, ?)
            """), (
                row.get("title"),
                row.get("genre"),
                row.get("year"),
                row.get("description"),
                float(row["rating"] if row.get(["rating"]) else None) #Our datatype for rating needs to be REAL
                )
    
    con_nect.commit()
    con_nect.close()
    #Print success message
    print("Movies loades to database successfully")
    
#Movie Query Functions
def get_movie_by_title(title: str):
    '''Quering our database for movies using movie title'''
    con_nect = get_db_connection()
    cursor = con_nect.cursor()

    cursor.execute("SELECT * FROM movies WHERE title = ?", (title,))
    movie = cursor.fetchone() #Python DB API:Used to retrieve data after a query
    #fetchone() fetches the very next available row from the result set of the lsast executed query

    con_nect.close() #Close since we are quering we do not need to commit
    return movie

def get_movie_by_genre(genre: str, exclude_title=None) -> list:
    '''Quering our database for movies based of genre'''
    con_nect = get_db_connection()
    cursor = con_nect.cursor()

    if exclude_title:
        cursor.execute("""
            SELECT * FROM movies
            WHERE genre = ?
            LIMIT 5
            """, (genre, exclude_title))
    else:
        cursor.execute("""
            SELECT * FROM movieS
            WHERE genre = ?
            LIMIT 5
        """, (genre,))
    
    movies = cursor.fetchall()
    con_nect.close()

    return movies

#Creted self
def get_all_movies(exclude_title=None) -> list:
    '''Retrieves alll movies from the Database'''
    con_nect = get_db_connection()
    cursor = con_nect.cursor()

    if exclude_title:
        cursor.execute("SELECT * FROM movies WHERE title = ?", (exclude_title,))
    else:
        cursor.execute("SELECT * FROM movies")
    
    movies = cursor.fetchall()
    con_nect.close()

    return movies

def find_index_of_movie(title: str, all_movies: list, exclude_title=None):
    '''Retrieves the index of a number'''
    title = title.lower()

    for idx, movie in enumerate(all_movies):
        if movie["title"].lower() == title:
            return idx
    return None # or -1





        

    



#Dev post






#Your database stores things that your web app needs during runtime, such as; 
    #Users: user_id, username, their preferences, watch history
    #User ratings: collaborative filtering, AI training, improving recommendations
    #Searchable movie table(even if the main dataset is CSV-derived, you put "clean" datainto SQLite for effecient quering)
    #If you compute recommendations once, you can stre them for faster response.
#DATABASE = Fast, Persistent, Queryable Storage
    #fast SELECT queries, indexes for search, transactions(safe writes), persistence(data isn't lost when server stops)
    #This is necessary for: search functionality, user login + profiles, rating movies, saving past recommendation, caching results

#MODERN AI Recommendations Still Need A Database
    #vector embeddings may be stored in a DB, user beghaviour needs to be saved, may store similar scores, cching improves performance
    #NB: An AI system is not a replacement for a database. AI needs structured data to work with