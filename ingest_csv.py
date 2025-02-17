from pathlib import Path
from connection import get_connection, close_connection

# Convert CSV to Docling document
#(Path("./famous_quotes_100.csv"))
#read csv file
import csv

from embeddocs import get_embedding

def read_csv(file_path, cursor):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
           embedding = get_embedding(row[1])
           cursor.execute("INSERT INTO quotes (author, quote, embedding) VALUES (%s, %s, %s)", (row[0],row[1], embedding))


#ingest into postgres 
connection = get_connection()
cursor = connection.cursor()
read_csv(Path("./famous-quotes.csv"), cursor)
connection.commit()
if (connection):
    close_connection(connection)
