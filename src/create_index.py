import os
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

SOURCE_DIR = "knowledge_base"
INDEX_DIR = "index"
os.makedirs(INDEX_DIR, exist_ok=True)

CHUNK_SIZE = 300   
CHUNK_OVERLAP = 50 

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
EMBEDDING_DIM = embedding_model.get_sentence_embedding_dimension()
print(f"Используемая модель: {EMBEDDING_MODEL_NAME}, размер эмбеддингов: {EMBEDDING_DIM}")

index = faiss.IndexFlatL2(EMBEDDING_DIM)
metadata_list = []

def split_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_text(text)
    return chunks

chunk_id = 0
for fname in os.listdir(SOURCE_DIR):
    if not fname.endswith(".txt"):
        continue
        
    file_path = os.path.join(SOURCE_DIR, fname)
    chunks = split_text(file_path)
    
    print(f"{fname}: {len(chunks)} чанков")
    
    for i, chunk in enumerate(chunks):
        emb = embedding_model.encode(chunk)
        emb = np.array([emb], dtype='float32')
        index.add(emb)
        metadata_list.append({
            "file": fname,
            "chunk_id": i,
            "text": chunk
        })
        chunk_id += 1

faiss.write_index(index, os.path.join(INDEX_DIR, "faiss.index"))
print(f"FAISS индекс сохранён: {os.path.join(INDEX_DIR, 'faiss.index')}")

with open(os.path.join(INDEX_DIR, "metadata.json"), "w", encoding="utf-8") as f:
    json.dump(metadata_list, f, ensure_ascii=False, indent=2)

print(f"Всего чанков в индексе: {chunk_id}")

query = "Кто такой дурислав?"
query_vector = embedding_model.encode([query])
D, I = index.search(np.array(query_vector, dtype=np.float32), k=3)
for idx in I[0]:
    print(metadata_list[idx]["file"], metadata_list[idx]["text"][:200])

