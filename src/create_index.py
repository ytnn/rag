import os
import json
import time
import numpy as np
import faiss
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

SOURCE_DIR = "knowledge_base"
INDEX_DIR = "index"
os.makedirs(INDEX_DIR, exist_ok=True)

CHUNK_SIZE = 300
CHUNK_OVERLAP = 50

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
EMBEDDING_DIM = embedding_model.get_sentence_embedding_dimension()
print(f"Используемая модель: {EMBEDDING_MODEL_NAME}, размер эмбеддингов: {EMBEDDING_DIM}")

index = faiss.IndexFlatIP(EMBEDDING_DIM)
metadata_list = []

def split_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    return splitter.split_text(text)

start_time = time.time()

chunk_id = 0
for fname in os.listdir(SOURCE_DIR):
    if not fname.endswith(".txt"):
        continue
        
    file_path = os.path.join(SOURCE_DIR, fname)
    chunks = split_text(file_path)
    print(f"{fname}: {len(chunks)} чанков")

    embeddings = embedding_model.encode(chunks, show_progress_bar=True)
    embeddings = np.array(embeddings, dtype='float32')
    faiss.normalize_L2(embeddings)

    index.add(embeddings)

    for i, chunk in enumerate(chunks):
        metadata_list.append({
            "file": fname,
            "chunk_id": i,
            "text": chunk
        })
        chunk_id += 1

end_time = time.time()
print(f"\nВремя генерации эмбеддингов и индексации: {end_time - start_time:.2f} секунд")

faiss.write_index(index, os.path.join(INDEX_DIR, "faiss.index"))
print(f"FAISS индекс сохранён: {os.path.join(INDEX_DIR, 'faiss.index')}")

with open(os.path.join(INDEX_DIR, "metadata.json"), "w", encoding="utf-8") as f:
    json.dump(metadata_list, f, ensure_ascii=False, indent=2)

print(f"Всего чанков в индексе: {chunk_id}")

query = "Кто такой Логоваз?"
query_vector = embedding_model.encode([query])
query_vector = np.array(query_vector, dtype='float32')
faiss.normalize_L2(query_vector)

D, I = index.search(query_vector, k=5)

print("\n=== Результаты поиска " + query)
for idx, score in zip(I[0], D[0]):
    print(f"{metadata_list[idx]['file']} ({score:.3f})")
    print(metadata_list[idx]["text"][:200])
