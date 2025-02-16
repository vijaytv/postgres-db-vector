import ollama
from dotenv import load_dotenv
import os
from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker
import json

# from supabase import create_client, Client

# load_dotenv()

# # Load environment variables
# SUPABASE_URL = os.getenv("SUPABASE_URL")
# SUPABASE_KEY = os.getenv("SUPABASE_KEY")

urls = [
    'https://docs.pydantic.dev/latest/examples/files/',
    'https://docs.pydantic.dev/latest/examples/requests/',
    'https://docs.pydantic.dev/latest/examples/queues/',
    'https://docs.pydantic.dev/latest/examples/orms/',
    'https://docs.pydantic.dev/latest/examples/custom_validators/'
]


def parse_url(url):
    conv_res = DocumentConverter().convert(url)
    doc = conv_res.document

    chunker = HybridChunker(tokenizer="BAAI/bge-small-en-v1.5")  # set tokenizer as needed
    chunk_iter = chunker.chunk(doc)
    chunks = list(chunk_iter)
    print(chunks)
    print(len(chunks))
    return chunks

# parse_url(urls[0])

def parse2markdown(url):
    conv_res = DocumentConverter().convert(url)
    doc = conv_res.document
    markdown_output = doc.export_to_markdown()
    #write to file
    with open('output.md', 'w') as f:
        f.write(markdown_output)
    return markdown_output

# parse2markdown(urls[0])

def parse2json(url):
    conv_res = DocumentConverter().convert(url)
    doc = conv_res.document
    json_output = doc.export_to_dict()
    print(json_output)
    #write to file
    with open('output.json', 'w') as f:
        json.dump(json_output, f, indent=4)
    
    return json_output

# parse2json(urls[0])


