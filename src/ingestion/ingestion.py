# from dotenv import load_dotenv
# import os
# import sys
# from docling.document_converter import DocumentConverter
# from langchain_core.documents import Document
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from core.db import get_vector_store

# load_dotenv()
# PG_CONNECTION = os.getenv("PG_CONNECTION_STRING")

# def ingest_file(file_path: str):
#     """Ingest a file (PDF/txt) using docling and save it in vector database"""

#     # 1. Load Document
#     print(f"Processing document: {file_path}")
#     if file_path.lower().endswith(".txt"):
#         with open(file_path, "r", encoding="utf-8") as f:
#             markdown_content = f.read()
#     else:
#         # Load Document using Docling for PDFs and others
#         converter = DocumentConverter()
#         result = converter.convert(file_path)
#         # Export to markdown text
#         markdown_content = result.document.export_to_markdown()
    
#     # Create Langchain Document
#     ext = os.path.splitext(file_path)[1].lower().strip('.')
#     metadata_base = {
#         "source": file_path,
#         "document_extension": ext,
#         "category": "Personalized Retail Banking & Wealth Advisory System",
#         "last_updated": os.path.getmtime(file_path)
#     }
    
#     doc = Document(page_content=markdown_content, metadata=metadata_base)

#     # 3. Chunking
#     splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
#         chunk_size=512,
#         chunk_overlap=100
#     )

#     chunks = splitter.split_documents([doc])
#     print("Total Chunks:", len(chunks))

#     # 4 + 5. Embeddings + Store
#     vector_store = get_vector_store(collection_name="retail_banking")
  
#     vector_store.add_documents(chunks)

#     print("Ingestion completed successfully!")

# if __name__ == "__main__":
#     test_file = "Retail_banking.pdf"
#     if os.path.exists(test_file):
#         ingest_file(test_file)
#     else:
#         print(f"Test file {test_file} not found.")


from dotenv import load_dotenv
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Adjusted import path as per your structure
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.db import get_vector_store

load_dotenv()
PG_CONNECTION = os.getenv("PG_CONNECTION_STRING")


def ingest_pdf(file_path: str):
    """Ingest a PDF file and save it in vector database"""

    print(f"Processing document: {file_path}")

    # 1. Load PDF
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    print("Pages:", len(docs))

    # 2. Metadata enrichment
    for doc in docs:
        doc.metadata.update({
            "source": file_path,
            "document_extension": "pdf",
            "page": doc.metadata.get("page"),
            "category": "retail_banking",  # kept from your original code
            "last_updated": os.path.getmtime(file_path)
        })

    # 3. Chunking
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=512,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(docs)
    print("Total Chunks:", len(chunks))

    # 4 + 5. Embeddings + Store
    vector_store = get_vector_store(collection_name="retail_banking")

    vector_store.add_documents(chunks)

    print("Ingestion completed successfully!")


if __name__ == "__main__":
    test_file = "Retail_banking.pdf"

    if os.path.exists(test_file):
        ingest_pdf(test_file)
    else:
        print(f"Test file {test_file} not found.")