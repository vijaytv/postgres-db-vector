import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POStGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

def get_connection():
    connection = psycopg2.connect(database=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD, host=POSTGRES_HOST, port=POSTGRES_PORT)
    return connection

def close_connection(connection):
    if connection:
        connection.close()

def main():
    print("Hello from postgres-db-vector!")
    connection = psycopg2.connect(database=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD, host=POSTGRES_HOST, port=POSTGRES_PORT)
    print("Connected to postgres")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM food")
    rows = cursor.fetchall()
    for row in rows:
        print(list(row))
    connection.close()
    print("Disconnected from postgres")
if __name__ == "__main__":
    main()
