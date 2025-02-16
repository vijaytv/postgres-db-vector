import ollama
from connection import get_connection, close_connection



# Function to generate embeddings using Ollama
def get_embedding(text):
    response = ollama.embeddings(model="nomic-embed-text", prompt=text)
    return response["embedding"]  # Returns a list of floats (vector)


def insert_test_data(cursor):
# Example documents to store
    documents = [
        {"id": 1, "text": "Machine learning is fascinating."},
        {"id": 2, "text": "Vector databases are useful for semantic search."},
        {"id": 3, "text": "Python is a great programming language."}
    ]
    # Delete all rows from the table
    cursor.execute("DELETE FROM documents")
    # Insert embeddings into Supabase
    for doc in documents:
        embedding = get_embedding(doc["text"])
        cursor.execute("""INSERT INTO documents (text, embeddings) VALUES (%s, %s)""", (doc["text"], embedding))
        connection.commit()
    print("Documents stored successfully!")

# Function to search for similar documents
def search_similar_documents(query_text, cursor, top_k=3):
    query_embedding = get_embedding(query_text)
    # Query the database for similar documents
    cursor.execute(f"""SELECT text FROM documents ORDER BY embeddings <-> '{query_embedding}' LIMIT 5""")
    response = cursor.fetchall()
    return response

if __name__ == "__main__":
    connection = get_connection()
    cursor = connection.cursor()
    insert_test_data(cursor)

    # Querying the database
    query = "What is machine learning?"
    results = search_similar_documents(query, cursor)
    if (connection):
        close_connection(connection)

    print("Top matching documents:")
    for result in results:
        print(result[0])
        # print(f"Text: {result['text']}, Similarity Score: {result['similarity']}")