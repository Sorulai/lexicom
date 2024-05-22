import os
import time
import psycopg2


def create_temp_table(cursor, connection):
    start_time = time.time()
    cursor.execute("""
    CREATE TEMP TABLE temp_update AS
    SELECT fn.name, sn.status
    FROM full_names fn
    JOIN short_names sn ON SPLIT_PART(fn.name, '.', 1) = sn.name
    
    """)
    cursor.execute("CREATE INDEX idx_temp_update_name ON temp_update(name)")
    cursor.execute("""
        UPDATE full_names fn
        SET status = tu.status
        FROM temp_update tu
        WHERE fn.name = tu.name
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
    create_temp_table(cursor, connection)

    cursor.close()
    connection.close()
