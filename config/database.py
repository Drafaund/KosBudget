# config/database.py - Pastikan method execute_query seperti ini
import psycopg2
from psycopg2.extras import RealDictCursor
import os

class DatabaseManager:
    @staticmethod
    def get_connection():
        """Get database connection"""
        try:
            connection = psycopg2.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                database=os.getenv('DB_NAME', 'kosbudget'),
                user=os.getenv('DB_USER', 'postgres'),
                password=os.getenv('DB_PASSWORD', ''),
                port=os.getenv('DB_PORT', '5432')
            )
            return connection
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return None
    
    @staticmethod
    def execute_query(query, params=None, fetch=False):
        """Execute database query with optional fetch"""
        connection = None
        cursor = None
        try:
            connection = DatabaseManager.get_connection()
            if not connection:
                return False, []
            cursor = connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, params)
            if fetch:
                result = cursor.fetchall()
                connection.commit()
                return True, result
            else:
                connection.commit()
                return True, None
        except Exception as e:
            print(f"[DB ERROR] {e}")
            return False, []
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    @staticmethod
    def test_connection():
        """Test database connection"""
        try:
            connection = DatabaseManager.get_connection()
            if connection:
                cursor = connection.cursor()
                cursor.execute("SELECT 1;")
                result = cursor.fetchone()
                cursor.close()
                connection.close()
                return True, "Database connection successful"
            else:
                return False, "Failed to connect to database"
        except Exception as e:
            return False, f"Database connection error: {str(e)}"