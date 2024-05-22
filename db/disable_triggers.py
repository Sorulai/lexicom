import os
import time
import psycopg2


def disable_triggers(cursor, connection):
    start_time = time.time()
    cursor.execute("ALTER TABLE full_names DISABLE TRIGGER ALL")
    cursor.execute("""
        UPDATE full_names fn
        SET status = sn.status
        FROM short_names sn
        WHERE SPLIT_PART(fn.name, '.', 1) = sn.name
        """)
    cursor.execute("ALTER TABLE full_names ENABLE TRIGGER ALL")
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
    disable_triggers(cursor, connection)

    cursor.close()
    connection.close()
