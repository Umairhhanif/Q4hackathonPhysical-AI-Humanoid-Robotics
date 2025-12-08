import os
import glob
from typing import List, Dict
import uuid
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from qdrant_client.http import models
from src.services.llm import get_embedding
from src.services.vector_store import VectorStore

async def load_markdown_files(directory: str) -> List[Dict]:
    """Recursively load markdown files from a directory."""
    files = []
    # Normalize path
    search_path = os.path.join(directory, "**/*.md")
    for file_path in glob.glob(search_path, recursive=True):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            # relative path for metadata
            rel_path = os.path.relpath(file_path, start=directory)
            files.append({"path": rel_path, "content": content})
    return files

def chunk_markdown(content: str) -> List[Dict]:
    """Split markdown content into chunks."""
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    md_header_splits = markdown_splitter.split_text(content)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = []
    for split in md_header_splits:
        split_chunks = text_splitter.split_text(split.page_content)
        for chunk_text in split_chunks:
            chunks.append({
                "content": chunk_text,
                "metadata": split.metadata
            })
    return chunks

async def ingest_documents(docs_dir: str):
    """Main ingestion function."""
    print(f"Scanning directory: {docs_dir}")
    files = await load_markdown_files(docs_dir)
    print(f"Found {len(files)} markdown files.")

    client = VectorStore.get_client()
    collection_name = VectorStore.get_collection_name()
    
    # Ensure collection exists
    VectorStore.ensure_collection()
    
    total_chunks = 0
    points = []
    
    for file in files:
        chunks = chunk_markdown(file["content"])
        for chunk in chunks:
            text = chunk["content"]
            metadata = chunk["metadata"]
            metadata["source_file"] = file["path"]
            
            # Generate ID deterministically from content + path
            chunk_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, text + file["path"]))
            
            # Get embedding
            embedding = await get_embedding(text)
            
            points.append(models.PointStruct(
                id=chunk_id,
                vector=embedding,
                payload={
                    "content": text,
                    "source_file": file["path"],
                    "header_path": str(metadata) # flatten for simple storage
                }
            ))
            total_chunks += 1
            
            # Batch upload (e.g. every 50)
            if len(points) >= 50:
                client.upsert(collection_name=collection_name, points=points)
                points = []

    # Upload remaining
    if points:
        client.upsert(collection_name=collection_name, points=points)

    print(f"Ingestion complete. Processed {total_chunks} chunks.")
    return total_chunks
