import os
from dotenv import load_dotenv
import psycopg2

# Load environment variables from .env file
load_dotenv()

# Connect to the PostgreSQL server
conn = psycopg2.connect(
    user=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    host=os.getenv("DATABASE_HOST"),
    port=os.getenv("DATABASE_PORT"),
)

# Set autocommit to True
conn.autocommit = True

# Create a cursor object
cursor = conn.cursor()

# Define the SQL command to create the database
sql = "CREATE DATABASE " + os.getenv("DATABASE_NAME")

# Execute the SQL command
cursor.execute(sql)

print(f"database {os.getenv('DATABASE_NAME')} created")

# Close the connection
conn.close()
