import streamlit as st
import psycopg2
from psycopg2 import Error
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

# Database connection configuration
DB_CONFIG = {
    "user": "postgres.dzuucaxeisqdgiubozve",
    "password": "Chocolate@09",
    "host": "aws-0-us-west-1.pooler.supabase.com",
    "port": "6543",
    "dbname": "postgres"
}

# Initialize database connection
@st.cache_resource
def init_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except (Exception, Error) as error:
        st.error(f"Error connecting to PostgreSQL: {error}")
        return None

# Execute query with caching
@st.cache_data
def run_query(query, params=None):
    conn = init_connection()
    if conn is None:
        return None
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            if params:
                cur.execute(query, params)
            else:
                cur.execute(query)
            return cur.fetchall()
    except (Exception, Error) as error:
        st.error(f"Error executing query: {error}")
        return None

# Streamlit app
def main():
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        from login import login_page
        login_page()
    else:
        st.title("Movie Recommendation System")
        
        # Add logout button in sidebar
        if st.sidebar.button("Logout"):
            from login import logout
            logout()
        
        # Display welcome message
        st.write(f"Welcome, {st.session_state.username}!")
        
        # Example: Display movies
        st.subheader("Available Movies")
        movies = run_query("""
            SELECT movie_title, release_year, genre 
            FROM movies 
            ORDER BY release_year DESC
            LIMIT 10
        """)
        
        if movies:
            for movie in movies:
                st.write(f"🎬 {movie['movie_title']} ({movie['release_year']}) - {movie['genre']}")
        else:
            st.write("No movies found in the database.")

if __name__ == "__main__":
    main()
