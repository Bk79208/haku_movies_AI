from pinecone import Pinecone
import fitz
import google.generativeai as genai
import os
from dotenv import load_dotenv

# pip install google-generativeai
# pip install pinecone
# pip install PyMuPDF
# # pip install tiktoken

load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# PINECONE_API_KEY = "pcsk_3T9yTU_5rgnKoTXvBJG3X4HdVXTGeQuxLf8vdLt7Daxbw7BJj6kMAGbvq6uRZxh5AD9k6R"
# GEMINI_API_KEY = "AIzaSyD9mVHd4slwaWy8LTRX_j5Wvcy7BSna0E0"

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text() + "\n"
    return text

model = "models/text-embedding-004"

genai.configure(api_key=GEMINI_API_KEY)

def embed_text(text):
    response = genai.embed_content(
        model=model,
        content=text,
        task_type="retrieval_document",
    )
    return response

pinecone_client = Pinecone(api_key=PINECONE_API_KEY)

vector_index = pinecone_client.Index("m-genre-kb")

def upsert_vectors_to_pinecone(document_text):
    upsert_data= []

    for idx, (file, text) in enumerate(document_text.items()):
        vector = embed_text(text).get("embedding", [])
        meta_data = {
            "text": text,
        }
        # upsert_data.append({f"doc-{idx}", vector, meta_data})
        upsert_data.append(("doc-" + str(idx), vector, meta_data))

    vector_index.upsert(upsert_data)
    print("vector upserted successfilly.")


if __name__ == "__main__":
    document_text = {}

    for file in os.listdir("documents"):
        text = extract_text_from_pdf("documents/" + file)
        document_text[file] = text
    upsert_vectors_to_pinecone(document_text)
    print("All documents processed and vector upserted.")