## Работа с ботом

**Для запуска в докере** сначала сбилдить образ:


``docker compose build``

Потом запустить:


``docker compose run --rm -it rag-bot``

**Для запуска вручную** зайти в папку src, выбрать соответствующий файл и запустить его, установив зависимости.

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

<img width="1644" height="363" alt="image" src="https://github.com/user-attachments/assets/ba5135c3-e0d5-4292-9f90-5948ffc8c004" />
<img width="1629" height="397" alt="image" src="https://github.com/user-attachments/assets/a936bf8d-644a-44ae-a3f4-0ae32c1e84f8" />
<img width="1638" height="392" alt="image" src="https://github.com/user-attachments/assets/68e43a17-b771-483a-8fb0-64f67e103e70" />
<img width="1656" height="225" alt="image" src="https://github.com/user-attachments/assets/d36cb09d-a16d-44f9-9f61-9d08ac3bce81" />
<img width="1654" height="380" alt="image" src="https://github.com/user-attachments/assets/7a6eab5f-87e9-4e76-bab3-409aba87312c" />

## Задание 5. Запуск и демонстрация работы бота

### Результат
Без фильтрации:
<img width="1638" height="349" alt="image" src="https://github.com/user-attachments/assets/f75e25ae-5c8c-4f83-897d-e7c4379eba13" />

Добавил пре-промпт - не помогло:

<img width="848" height="329" alt="image" src="https://github.com/user-attachments/assets/3fa8c2b0-0c50-419b-9cd0-56202adca413" />

Добавил функцию фильтрации запрещенных слов в чанках - сработало

<img width="838" height="422" alt="image" src="https://github.com/user-attachments/assets/556a7044-115d-4f00-a996-bd361f497ed6" />

Вывод: пре-промпт фильтрация не обеспечивает желаемый уровень защиты, т.к. по сути явлется скорее рекомендацией модели, а не жестким правилом. Для обеспечения зажиты секретов необходимо реализовывать фильтрующие функции для очистки чанков от чувствительных данных.




