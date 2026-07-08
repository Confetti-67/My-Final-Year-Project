# create_db.py
import psycopg2

def create_database():
    try:
        # Connect to the default 'postgres' database first
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",  # Connect to default database
            user="postgres",      # Default PostgreSQL username
            password="Peter@martin0157"  # Replace with your actual password
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if our database already exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname='forex_regime_detection'")
        exists = cursor.fetchone()
        
        if not exists:
            print("Creating 'forex_regime_detection' database...")
            cursor.execute("CREATE DATABASE forex_regime_detection")
            print("Database created successfully!")
        else:
            print("Database 'forex_regime_detection' already exists.")
            
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error creating database: {e}")
        return False

if __name__ == "__main__":
    create_database()