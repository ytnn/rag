import os
import subprocess

BASE_DIR = "/app"
KB_DIR = os.path.join(BASE_DIR, "knowledge_base")
INDEX_DIR = os.path.join(BASE_DIR, "index")
SRC_DIR = os.path.join(BASE_DIR, "src")

os.makedirs(KB_DIR, exist_ok=True)
os.makedirs(INDEX_DIR, exist_ok=True)

if not os.listdir(KB_DIR):
    print("Knowledge base пустая. Загружаем данные...")
    subprocess.run(["python", os.path.join(SRC_DIR, "download_text.py")], check=True)

if not os.listdir(INDEX_DIR):
    print("Индекс пустой. Создаём индекс...")
    subprocess.run(["python", os.path.join(SRC_DIR, "create_index.py")], check=True)

print("Запускаем RAG-бот...")
subprocess.run(["python", os.path.join(SRC_DIR, "rag_bot.py")], check=True)
