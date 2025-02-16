import ollama
from chunking import get_chunks
from connection import get_connection, close_connection

def insert_docs(cursor, urls):
    cursor.execute("DELETE FROM documents")
    count = 0
    for url in urls:
        chunks = get_chunks(url)
        for chunk in chunks:
            if chunk.text:
                count += 1
                embedding = get_embedding(chunk.text)
                cursor.execute("""INSERT INTO documents (text, embeddings) VALUES (%s, %s)""", (chunk.text, embedding))
                connection.commit()
    print("Documents stored successfully! Total: ", count)

# Function to generate embeddings using Ollama
def get_embedding(text):
    response = ollama.embeddings(model="nomic-embed-text", prompt=text)
    return response["embedding"]  # Returns a list of floats (vector)

# Function to search for similar documents
def search_similar_documents(query_text, cursor, top_k=3):
    query_embedding = get_embedding(query_text)
    # Query the database for similar documents
    cursor.execute(f"""SELECT text , embeddings <-> '{query_embedding}' as distance FROM documents
                    WHERE embeddings <-> '{query_embedding}' < 30
                    ORDER BY distance  LIMIT 2""")
    response = cursor.fetchall()
    return response

if __name__ == "__main__":
    urls = [
        'https://docs.pydantic.dev/latest/examples/files/',
        'https://docs.pydantic.dev/latest/examples/requests/',
        'https://docs.pydantic.dev/latest/examples/queues/',
        'https://docs.pydantic.dev/latest/examples/orms/',
        'https://docs.pydantic.dev/latest/examples/custom_validators/'
    ]
    connection = get_connection()
    cursor = connection.cursor()
    # insert_docs(cursor, urls)
    # Querying the database
    query = "what is httpx"
    results = search_similar_documents(query, cursor)
    if (connection):
        close_connection(connection)

    print("Top matching documents:")
    for result in results:
        print("--------------------------------------------")
        print(result)
        print("--------------------------------------------")
        # print(f"Text: {result['text']}, Similarity Score: {result['similarity']}")