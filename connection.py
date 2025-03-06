import psycopg2
from psycopg2 import Error # type: ignore

def create_tables(cursor):
    # SQL commands to create tables
    commands = [
        """
        -- Drop tables if they exist
        DROP TABLE IF EXISTS users, movies, ratings, recommendations, movies_to_rate CASCADE;
        """,
        """
        -- Users Table
        CREATE TABLE users (
            user_guid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            last_login TIMESTAMP DEFAULT NOW()
        );
        """,
        """
        -- Movies Table
        CREATE TABLE movies (
            movie_guid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            movie_title VARCHAR(255) NOT NULL,
            release_year INT,
            genre VARCHAR(100),
            description TEXT
        );
        """,
        """
        -- Ratings Table
        CREATE TABLE ratings (
            rating_id SERIAL PRIMARY KEY,
            user_guid UUID REFERENCES users(user_guid) ON DELETE CASCADE,
            movie_guid UUID REFERENCES movies(movie_guid) ON DELETE CASCADE,
            rating INT CHECK (rating BETWEEN 1 AND 5),
            rated_at TIMESTAMP DEFAULT NOW(),
            UNIQUE(user_guid, movie_guid)
        );
        """,
        """
        -- Recommendations Table
        CREATE TABLE recommendations (
            recommendation_id SERIAL PRIMARY KEY,
            user_guid UUID REFERENCES users(user_guid) ON DELETE CASCADE,
            movie_guid UUID REFERENCES movies(movie_guid) ON DELETE CASCADE,
            recommendation_score FLOAT DEFAULT 0.0,
            recommended_at TIMESTAMP DEFAULT NOW()
        );
        """,
        """
        -- Movies to Rate Table
        CREATE TABLE movies_to_rate (
            id SERIAL PRIMARY KEY,
            user_guid UUID REFERENCES users(user_guid) ON DELETE CASCADE,
            movie_guid UUID REFERENCES movies(movie_guid) ON DELETE CASCADE
        );
        """
    ]
    
    # Execute each command
    for command in commands:
        cursor.execute(command)

try:
    # Connect to an existing database
    connection = psycopg2.connect(
        user="postgres.dzuucaxeisqdgiubozve", 
        password="Chocolate@09", 
        host="aws-0-us-west-1.pooler.supabase.com",
        port="6543",
        dbname="postgres"
    )

    # Create a cursor to perform database operations
    cursor = connection.cursor()
    
    # Create tables
    create_tables(cursor)
    
    # Commit the changes
    connection.commit()
    
    print("Tables created successfully!")

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
