import random
import string
import psycopg2
import time
import os

from dotenv import load_dotenv

conn_params = {
    'host': os.getenv('DB_HOST'),
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}


def generate_random_name(length=8):
    """Функция для генерации случайного имени файла"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def generate_random_extension():
    """Функция для генерации случайного расширения"""
    extensions = ['mp3', 'wav', 'flac', 'ogg', 'aac']
    return random.choice(extensions)


connection = psycopg2.connect(**conn_params)
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS short_names")
cursor.execute("DROP TABLE IF EXISTS full_names")

cursor.execute("""
CREATE TABLE short_names (
    name VARCHAR(255) PRIMARY KEY,
    status INTEGER
);
""")

cursor.execute("""
CREATE TABLE full_names (
    name VARCHAR(255) PRIMARY KEY,
    status INTEGER
);
""")

num_short_names = 700000
num_full_names = 500000

start_time = time.time()

short_names = set()
batch_size = 10000  
short_names_data = []

for _ in range(num_short_names):
    while True:
        name = generate_random_name()
        if name not in short_names:
            break
    status = random.randint(0, 1)
    short_names.add(name)
    short_names_data.append((name, status))
    if len(short_names_data) >= batch_size:
        cursor.executemany("INSERT INTO short_names (name, status) VALUES (%s, %s)", short_names_data)
        short_names_data.clear()

if short_names_data:
    cursor.executemany("INSERT INTO short_names (name, status) VALUES (%s, %s)", short_names_data)

connection.commit()

end_time = time.time()
print(f"Вставка данных в short_names завершена за {end_time - start_time:.2f} секунд.")

start_time = time.time()


full_names_data = []
short_names_list = tuple(short_names)
used_names = set()

cursor.execute("ALTER TABLE full_names DISABLE TRIGGER ALL")

for _ in range(num_full_names):
    while True:
        short_name = random.choice(short_names_list)
        full_name = f"{short_name}.{generate_random_extension()}"
        if short_name not in used_names:
            break
    used_names.add(short_name)
    full_names_data.append((full_name,))
    if len(full_names_data) >= batch_size:
        cursor.executemany("INSERT INTO full_names (name, status) VALUES (%s, NULL)", full_names_data)
        full_names_data.clear()

if full_names_data:
    cursor.executemany("INSERT INTO full_names (name, status) VALUES (%s, NULL)", full_names_data)

cursor.execute("ALTER TABLE full_names ENABLE TRIGGER ALL")

connection.commit()

end_time = time.time()
print(f"Вставка данных в full_names завершена за {end_time - start_time:.2f} секунд.")

cursor.close()
connection.close()
