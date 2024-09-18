import psycopg2

conn = psycopg2.connect(dbname='test', user='postgres', password='leolab12', host='127.0.0.1')
cur = conn.cursor()

cur.execute(f"""Select * FROM place WHERE Place_second ~* 'Стол' """)
a = cur.fetchall()
print(a)

cur.execute(f"""Select * from place""")

print(cur.fetchall())

print(1/0)