import psycopg2


def connection():
    """Функция инициализации коннекта и курсора к базе данных"""
    conn = psycopg2.connect(dbname='test', user='user', password='password', host='127.0.0.1')
    cur = conn.cursor()
    return cur, conn
