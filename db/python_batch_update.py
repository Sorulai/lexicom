import os
import time
import psycopg2


def python_batch_update(cursor, connection):
    start_time = time.time()

    cursor.execute("SELECT name, status FROM short_names")
    short_names = cursor.fetchall()

    cursor.execute("SELECT name FROM full_names")
    full_names = cursor.fetchall()

    status_dict = {name: status for name, status in short_names}
    update_query = "UPDATE full_names SET status = %s WHERE name = %s"
    update_data = []
    batch_size = 10000

    for full_name, in full_names:
        short_name = full_name.split('.')[0]
        if short_name in status_dict:
            update_data.append((status_dict[short_name], full_name))
            if len(update_data) >= batch_size:
                cursor.executemany(update_query, update_data)
                update_data.clear()

    connection.commit()
    end_time = time.time()
    print(f"Python batch update завершен за {end_time - start_time} секунд.")


if __name__ == "__main__":
    connection = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
    )
    cursor = connection.cursor()

    python_batch_update(cursor, connection)

    cursor.close()
    connection.close()
