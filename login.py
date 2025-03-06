import streamlit as st
import hashlib
from app import init_connection, run_query

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def check_user_credentials(username, password):
    """Verify user credentials against the database"""
    hashed_password = hash_password(password)
    query = """
        SELECT * FROM users 
        WHERE username = %s AND password_hash = %s
    """
    result = run_query(query, (username, hashed_password))
    return bool(result)

def login_page():
    """Display and handle the login page"""
    st.title("Login")
    
    # Initialize session state for login status
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    # Login form
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")

        if submit_button:
            if check_user_credentials(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password")

def logout():
    """Handle user logout"""
    st.session_state.logged_in = False
    st.session_state.username = None
    st.rerun()

def create_users_table():
    """Create the users table if it doesn't exist"""
    query = """
    CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password_hash VARCHAR(64) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    conn = init_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()

if __name__ == "__main__":
    create_users_table()
    login_page() 