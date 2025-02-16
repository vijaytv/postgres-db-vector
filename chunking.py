from transformers import AutoTokenizer
from extractusingdocling import parse2markdown
from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker


EMBED_MODEL_ID = "sentence-transformers/all-MiniLM-L6-v2"
MAX_TOKENS = 8192

tokenizer = AutoTokenizer.from_pretrained(EMBED_MODEL_ID)

chunker = HybridChunker(
    tokenizer=tokenizer,  # instance or model name, defaults to "sentence-transformers/all-MiniLM-L6-v2"
    max_tokens=MAX_TOKENS,  # optional, by default derived from `tokenizer`
    merge_peers=True,  # optional, defaults to True
)

def get_chunks(url):
    doc = DocumentConverter().convert(source=url).document
    chunk_iter = chunker.chunk(dl_doc=doc)
    chunks = list(chunk_iter)
    return chunks

if __name__ == "__main__":
    chunks = get_chunks('./output.md')
    print(chunks[2].text)