"""
Database setup script - Run this instead of manual MySQL commands
"""
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def setup_database():
    """Create database and tables"""
    cursor = None
    connection = None
    try:
        # Connect without specifying a database (to create the database)
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
        )
        
        cursor = connection.cursor()
        
        # Create database
        db_name = os.getenv('DB_NAME', 'todo_db')
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"✓ Database '{db_name}' created/verified")
        
        # Select database
        cursor.execute(f"USE {db_name}")
        
        # Create todos table
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
        cursor.execute(create_table_query)
        print("✓ Table 'todos' created/verified")
        
        connection.commit()
        print("\n✓ Database setup completed successfully!")
        print(f"\nYou can now run: uvicorn main:app --reload")
        
    except Error as e:
        print(f"✗ Error: {e}")
        print("\nPlease make sure:")
        print("1. MySQL Server is running")
        print("2. Database credentials in .env are correct")
        print("3. Check your username and password")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

if __name__ == "__main__":
    setup_database()
