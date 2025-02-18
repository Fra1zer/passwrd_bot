import psycopg2
import logging
logging.basicConfig(level=logging.INFO, filename="logs_DB.log", filemode="w",
                    format="%(asctime)s - %(levelname)s - %(message)s")


def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="PASS",
            host="localhost",
            port="5432"
        )
        logging.info(f'Подключение к БД прошло')
        return conn
    except psycopg2.Error as err:
        logging.error(f'Ошибка подключения к БД: {err}')
        return None


def create_table():
    conn = connect_to_db()
    if conn is None:
        logging.error(f'Ошибка подключения к БД')
        return

    try:
        with conn.cursor() as cur:
            cur.execute('''
            CREATE TABLE IF NOT EXISTS users(
            id VARCHAR(100) PRIMARY KEY,
            count_pass INT);
            ''')

            conn.commit()
            cur.close()
            conn.close()
            logging.info(f'Таблица успешна создана/уже существует')
    except psycopg2.Error as err:
        logging.error(f"Ошибка при создании таблицы: {err}")


def user_exists(user_id):
    conn = connect_to_db()
    if conn is None:
        logging.error('Ошибка подключения к БД')
        return

    try:
        with conn.cursor() as cur:
            cur.execute('SELECT COUNT(*) FROM users WHERE id = %s;', (user_id,))
            count = cur.fetchone()[0]
            return count > 0
    except psycopg2.Error as err:
        logging.error(f'Не удалось получить информацию о наличии пользователя в БД: {err}')
        return False
    finally:
        conn.close()


def add_user(user_id):
    user_id = str(user_id)
    if user_exists(user_id):
        return

    conn = connect_to_db()
    if conn is None:
        logging.error('Ошибка подключения к БД')
        return

    try:
        with conn.cursor() as cur:
            cur.execute('''
            INSERT INTO users(id, count_pass)
            VALUES (%s, %s);
            ''', (user_id, 0))
        conn.commit()
        cur.close()
        conn.close()
        logging.info(f"Пользователь добавлен в БД")
    except psycopg2.Error as err:
        logging.error(f"Ошибка при добавления пользователя в БД: {err}")


def update_count(user_id):
    user_id = str(user_id)
    if not user_exists(user_id):
        add_user(user_id)

    conn = connect_to_db()
    if conn is None:
        logging.error('Ошибка подключения к БД')
        return

    try:
        with conn.cursor() as cur:
            cur.execute('''
            UPDATE users
            SET count_pass = count_pass + 1
            WHERE id = %s;
            ''', (user_id,))
        conn.commit()
        cur.close()
        conn.close()
        logging.info(f"Колонка count_pass обновлена у пользователя {user_id}")
    except psycopg2.Error as err:
        logging.error(f"Ошибка при изменении колонки count_pass у пользователя {user_id}: {err}")

def get_count(user_id):
    user_id = str(user_id)
    if not user_exists(user_id):
        add_user(user_id)

    conn = connect_to_db()
    if conn is None:
        logging.error('Ошибка подключения к БД')
        return

    try:
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
            logging.info(f'Успешно получены данные колонки count_pass пользователя {user_id}')
            return result
    except psycopg2.Error as err:
        logging.error(f"Не удалось получить данные колонки count_pass пользователя {user_id}: {err}")