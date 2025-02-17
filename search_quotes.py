import ollama
import sys
from chunking import get_chunks
from connection import get_connection, close_connection

# Function to generate embeddings using Ollama
def get_embedding(text):
    response = ollama.embeddings(model="nomic-embed-text", prompt=text)
    return response["embedding"]  # Returns a list of floats (vector)

# Function to search for similar documents
def search_similar_documents(query_text, cursor, top_k=3):
    query_embedding = get_embedding(query_text)
    # Query the database for similar documents
    cursor.execute(f"""SELECT author, quote , embedding <-> '{query_embedding}' as distance FROM quotes
                    WHERE embedding <-> '{query_embedding}' < 20
                    ORDER BY distance  LIMIT 4""")
    response = cursor.fetchall()
    return response

if __name__ == "__main__":

    n = len(sys.argv)
    if (n == 1):
        print("Please provide a query")
        exit()
    query = sys.argv[1]
    connection = get_connection()
    cursor = connection.cursor()
    # Querying the database based on command line argument

    
    results = search_similar_documents(query, cursor)
    if (connection):
        close_connection(connection)

    context = ""
    for result in results:
        context += f"{result[0]} said  {result[1]}\n"
    
    print("Context-------------------------------------------")
    print(context)
    print("-------------------------------------------------")
    query = "who said the quote that has the word or words: " + query
    prompt = "you are an assistant who can reply with the authors and quotes using only the context and query which contains words from the quote. \n" + context + "\n" + query + "\n" + "Limit the answer only based on the context provided. Do Not elaborate"

    # Query against ollama
    response = ollama.generate(model="llama3.2:latest", prompt=prompt)
    print(response['response'])