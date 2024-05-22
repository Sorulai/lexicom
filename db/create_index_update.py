import os
import time
import psycopg2


def create_indexes(cursor, connection):
    start_time = time.time()
    cursor.execute("CREATE INDEX idx_temp_full_names ON full_names(name)")
    cursor.execute("""
        UPDATE full_names
        SET status = short_names.status
        FROM short_names
        WHERE short_names.name = SPLIT_PART(full_names.name, '.',1)
        """)
    connection.commit()
    end_time = time.time()
    print(f"Create index completed in {end_time - start_time} seconds.")


if __name__ == "__main__":
    connection = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    cursor = connection.cursor()
    create_indexes(cursor, connection)

    cursor.close()
    connection.close()
