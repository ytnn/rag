## Задание 2. Подготовка базы знаний

### По итогу задания у вас должно получиться: 
- [Папка](https://github.com/ytnn/rag/tree/dev/src/knowledge_base/downloads) с 30+ уникальными документами:
- Скрипт или описание логики подмены терминов: [download_text.py](https://raw.githubusercontent.com/ytnn/rag/refs/heads/dev/src/download_text.py)
- Словарь замен [terms_map.json](https://raw.githubusercontent.com/ytnn/rag/refs/heads/dev/src/knowledge_base/terms_map.json) и краткое пояснение к нему: Взял вселенную Властелина колец и заменил термины по словарю terms_map.json.
- Финальная база, которую невозможно «угадывать» по памяти модели: [https://github.com/ytnn/rag/tree/dev/src/knowledge_base](https://github.com/ytnn/rag/tree/dev/src/knowledge_base) .

## Задание 3. Создание векторного индекса базы знаний

### Результат
- Название модели: all-MiniLM-L6-v2
- Размер эмбеддингов: 384
- База знаний: Властелин колец
- Число чанков в индексе: 1933
- Сколько времени заняла генерация: 30 секунд
- Скрипт или описание логики подмены терминов: [create_index.py](https://raw.githubusercontent.com/ytnn/rag/refs/heads/dev/src/create_index.py)
- Созданный индекс: [faiss.index](https://github.com/ytnn/rag/tree/dev/src/index)

## Задание 4. Реализация RAG-бота с техниками промптинга
### Результат
- Запускаемый скрипт: [rag_bot.py](https://raw.githubusercontent.com/ytnn/rag/refs/heads/dev/src/rag_bot.py)
- Примеры 3–5 успешных диалогов:
- Примеры одного-двух случаев, когда бот будет отвечать: «Я не знаю»:
