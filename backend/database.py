import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Create and return a database connection"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'todo_db')
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def init_db():
    """Initialize the database with the todos table"""
    connection = get_db_connection()
    if connection is None:
        print("Failed to connect to database")
        return

    cursor = connection.cursor()
    
    create_table_query = """
    CREATE TABLE IF NOT EXISTS todos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        description TEXT,
        completed BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )
    """
    
    try:
        cursor.execute(create_table_query)
        connection.commit()
        print("Database initialized successfully")
    except Error as e:
        print(f"Error creating table: {e}")
    finally:
        cursor.close()
        connection.close()
