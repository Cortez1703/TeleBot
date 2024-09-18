import psycopg2

conn = psycopg2.connect(dbname='test', user='postgres', password='leolab12', host='127.0.0.1')
cur = conn.cursor()

cur.execute("DROP table event_build ")
cur.execute("DROP table event_inventory ")
cur.execute("DROP table inventory ")
cur.execute("DROP table build ")
cur.execute("DROP table contragent ")
cur.execute("DROP table subproject ")
cur.execute("DROP table project ")
cur.execute("DROP table place ")
cur.execute("DROP table persons ")
conn.commit()