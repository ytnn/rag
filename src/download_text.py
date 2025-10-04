import requests
from bs4 import BeautifulSoup
import os
import json
import re

lotr_links = [
    
    # "Мир"
    
        "https://lotr.fandom.com/ru/wiki/Арда",
        "https://lotr.fandom.com/ru/wiki/Средиземье",

    # --- Расы ---
        "https://lotr.fandom.com/ru/wiki/Эльфы",
        "https://lotr.fandom.com/ru/wiki/Люди",
        "https://lotr.fandom.com/ru/wiki/Гномы",
        "https://lotr.fandom.com/ru/wiki/Хоббиты",
        "https://lotr.fandom.com/ru/wiki/Орки",
    
    # --- Локации ---
        "https://lotr.fandom.com/ru/wiki/Гондор",
        "https://lotr.fandom.com/ru/wiki/Рохан",
        "https://lotr.fandom.com/ru/wiki/Мордор",
        "https://lotr.fandom.com/ru/wiki/Лориэн",
        "https://lotr.fandom.com/ru/wiki/Ривенделл",
        "https://lotr.fandom.com/ru/wiki/Шир",
    
    # --- События ---
        "https://lotr.fandom.com/ru/wiki/Война_Кольца",
    
    # --- Персонажи ---
        "https://lotr.fandom.com/ru/wiki/Фродо_Бэггинс",
        "https://lotr.fandom.com/ru/wiki/Сэмвайз_Гэмджи",
        "https://lotr.fandom.com/ru/wiki/Мериадок_Брэндибак",
        "https://lotr.fandom.com/ru/wiki/Перегрин_Тук",
        "https://lotr.fandom.com/ru/wiki/Гэндальф",
        "https://lotr.fandom.com/ru/wiki/Арагорн",
        "https://lotr.fandom.com/ru/wiki/Леголас",
        "https://lotr.fandom.com/ru/wiki/Гимли",
        "https://lotr.fandom.com/ru/wiki/Боромир",
        "https://lotr.fandom.com/ru/wiki/Голлум",
        "https://lotr.fandom.com/ru/wiki/Валар",
        "https://lotr.fandom.com/ru/wiki/Майар",
        "https://lotr.fandom.com/ru/wiki/Мелькор",
        "https://lotr.fandom.com/ru/wiki/Саурон",

     # --- Артефакты ---
        "https://lotr.fandom.com/ru/wiki/Кольцо_Всевластия"
    ]

SOURCE_DIR = "knowledge_base/downloads"
TARGET_DIR = "knowledge_base"
MAP_FILE = os.path.join(TARGET_DIR, "terms_map.json")

def download():
    clean_dir(SOURCE_DIR)

    for url in lotr_links:
        name = url.split("/")[-1]
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")

        paragraphs = [p.get_text() for p in soup.find_all("p")]
        text = "\n".join(paragraphs)

        with open(f"{SOURCE_DIR}/{name}.txt", "w", encoding="utf-8") as f:
            f.write(text)

def load_terms_map():
    with open(MAP_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def apply_replacements(text, terms_map):
    for old, new in terms_map.items():
        pattern = re.compile(re.escape(old), re.IGNORECASE)
        text = pattern.sub(new, text)
    return text

def clean_dir(dir):
    os.makedirs(dir, exist_ok=True)
    
    for fname in os.listdir(dir):
        if fname != "terms_map.json" and fname != "downloads" and fname != "malicious.txt":
            os.remove(os.path.join(dir, fname))

def process_files():
    terms_map = load_terms_map()
    clean_dir(TARGET_DIR)

    for fname in os.listdir(SOURCE_DIR):
        src_path = os.path.join(SOURCE_DIR, fname)
        dst_path = os.path.join(TARGET_DIR, fname)

        if not os.path.isfile(src_path):
            continue

        root, ext = os.path.splitext(fname)

        if root in terms_map:
            new_root = terms_map[root]
            new_fname = new_root + ext
        else:
            new_fname = fname

        dst_path = os.path.join(TARGET_DIR, new_fname)

        with open(src_path, "r", encoding="utf-8") as f:
            content = f.read()

        new_content = apply_replacements(content, terms_map)

        with open(dst_path, "w", encoding="utf-8") as f:
            f.write(new_content)
            
if __name__ == "__main__":
    download()
    process_files()