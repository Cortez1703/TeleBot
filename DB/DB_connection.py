import psycopg2

def connection():
    """Функция инициализации коннекта и курсора к базе данных"""
    conn = psycopg2.connect(dbname='test', user='postgres', password='leolab12', host='127.0.0.1')
    cur = conn.cursor()
    return cur, conn
