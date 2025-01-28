import psycopg2


def connect_to_db():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="PASS",
        host="localhost",
        port="5432"
    )
    return conn


def create_table():
    conn = connect_to_db()
    with conn.cursor() as cur:
        cur.execute('''
        CREATE TABLE IF NOT EXISTS users(
        id VARCHAR(100) PRIMARY KEY,
        count_pass INT);
        ''')

    conn.commit()
    cur.close()
    conn.close()


def user_exists(user_id):
    conn = connect_to_db()
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT COUNT(*) FROM users WHERE id = %s;', (user_id,))
            count = cur.fetchone()[0]
            return count > 0
    except Exception as e:
        return False
    finally:
        conn.close()


def add_user(user_id):
    user_id = str(user_id)
    if user_exists(user_id):
        return

    conn = connect_to_db()
    with conn.cursor() as cur:
        cur.execute('''
        INSERT INTO users(id, count_pass)
        VALUES (%s, %s);
        ''', (user_id, 0))
    conn.commit()
    cur.close()
    conn.close()


def update_count(user_id):
    user_id = str(user_id)
    if not user_exists(user_id):
        add_user(user_id)
    conn = connect_to_db()

    with conn.cursor() as cur:
        cur.execute('''
        UPDATE users
        SET count_pass = count_pass + 1
        WHERE id = %s;
        ''', (user_id,))
    conn.commit()
    cur.close()
    conn.close()


def get_count(user_id):
    user_id = str(user_id)
    if not user_exists(user_id):
        add_user(user_id)
    conn = connect_to_db()

    with conn.cursor() as cur:
        cur.execute('''
        SELECT count_pass
        FROM users
        WHERE id = %s;
        ''', (user_id, ))
        result = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return result
