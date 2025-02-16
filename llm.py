import ollama
from connection import get_connection, close_connection
from embeddocs import search_similar_documents

if __name__ == "__main__":
    connection = get_connection()
    cursor = connection.cursor()
    # insert_docs(cursor, urls)
    # Querying the database
    query = "Give example code to validate data from a csv file"
    results = search_similar_documents(query, cursor)
    if (connection):
        close_connection(connection)

    # set context for the prompt
    context = ""
    for result in results:
        context += result[0] + "\n"
    
    prompt = "You are a pydantic coding assistant. You are given the following context. \n" + context + "\n" + query + "\n" + "Answer the question only based on the context provided."
    # Query against ollama
    response = ollama.generate(model="llama3.2:latest", prompt=prompt)
    print(response['response'])
