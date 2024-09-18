import psycopg2

conn = psycopg2.connect(dbname='test', user='postgres', password='leolab12', host='127.0.0.1')
cur = conn.cursor()
test_place = """('Склад','Второй',2,2,'В помещении'),('Склад','Второй',3,1,'В помещении'),
('Принтачная','Первый',1,1,'В помещении')"""
test_contragent = """('Все инструменты','Все инструменты','22-02-2022','-'),
('Амперкин','Амперкин','22-02-2022','-'),
('ОЗОН','ОЗОН','22-02-2022','-')"""

test_inventory = """('Винт М5','Метиз','Винт','УПД',1,100,'22-02-2022','22-02-2022','22-02-2022',100,1,'-','-'),
                    ('Винт М3','Метиз','Винт','УПД',1,100,'22-02-2022','22-02-2022','22-02-2022',100,1,'-','-'),
                    ('Винт М1','Метиз','Винт','УПД',1,100,'22-02-2022','22-02-2022','22-02-2022',100,1,'-','-'),
                    ('Молоток','Инструмент','Слесарка','УПД',1,100,'22-02-2022','22-02-2022','22-02-2022',100,1,'-','-'),
                    ('Гвоздодер','Инструмент','Слесарка','УПД',1,100,'22-02-2022','22-02-2022','22-02-2022',100,1,'-','-'),
                    ('Молоко','Продукты','Молочка','УПД',1,100,'22-02-2022','22-02-2022','22-02-2022',100,1,'-','-'),
                    ('Гайка М11','Метиз','Гайка','УПД',1,100,'22-02-2022','22-02-2022','22-02-2022',100,1,'-','-'),
                    ('Метла','Инструмент','Уборка','УПД',1,100,'22-02-2022','22-02-2022','22-02-2022',100,1,'-','-'),
                    ('Пластик','Печать','оборудование','УПД',1,100,'22-02-2022','22-02-2022','22-02-2022',100,1,'-','-'),
                    ('Отвертка','Инструмент','Слесарка','УПД',1,100,'22-02-2022','22-02-2022','22-02-2022',100,1,'-','-')"""

test_project = """('РОБОТ','22-02-2022','22-02-2022','-'),
('Аналитика','22-02-2022','22-02-2022','-'),('Нейронка','22-02-2022','22-02-2022','-')"""

test_subproject = """('РАМ3',1,'22-02-2022','22-02-2022','-'),
('РАМ2',1,'22-02-2022','22-02-2022','-'),('Ярославль',2,'22-02-2022','22-02-2022','-')"""

cur.execute("""CREATE TABLE IF NOT EXISTS persons (
                Person_ID Serial primary key,
                Person_name text,
                Person_surname text,
                Person_thirdname text,
                Person_position text,
                Person_tg_id text,
                Date_of_start_work text,
                Date_of_end_work text)""")

cur.execute("""CREATE TABLE IF NOT EXISTS contragent (
                ID_contragent serial primary key,
                Sale_name text,
                Ur_name text,
                Date_of_document date,
                Comment text)""")

cur.execute("""CREATE TABLE IF NOT EXISTS place (
                ID_place serial primary key,
                Place_main text,
                Place_second text,
                Place_third int,
                Place_last int,
                Place_class text)""")

cur.execute("""CREATE TABLE IF NOT EXISTS inventory (
                Inventory_ID serial primary key,
                Inventory_name text,
                Inventory_class text,
                Inventory_subclass text,
                Inventory_upd_name text,
                ID_place int references place (ID_place),
                Inventory_amount real,
                Inventory_date_choose date,
                Inventory_date_sale date,
                Invetory_date_of_break date,
                Invetory_price real,
                ID_saler int references contragent (ID_contragent),
                Inventory_url text,
                Inventory_comment text)
                """)

cur.execute("""CREATE TABLE IF NOT EXISTS build (
                Inventory_ID serial primary key,
                Inventory_name text,
                Inventory_class text,
                Inventory_subclass text,
                Inventory_upd_name text,
                ID_place int references place (ID_place),
                Inventory_amount real,
                Inventory_date_choose date,
                Inventory_date_sale date,
                Invetory_date_of_break date,
                Invetory_price real,
                ID_saler int references contragent (ID_contragent),
                Inventory_url text,
                Inventory_comment text)
                """)

cur.execute("""CREATE TABLE IF NOT EXISTS project (
                ID_project serial primary key,
                Project_name text,
                Project_date_start date,
                Project_date_end date,
                Project_comment text)""")

cur.execute("""CREATE TABLE IF NOT EXISTS subproject (
                ID_subproject serial primary key,
                ID_mainproject smallint references project (ID_project),
                Subproject_name text,
                Subproject_date_start date,
                Subproject_date_end date,
                Subproject_comment text)""")

cur.execute("""CREATE TABLE IF NOT EXISTS event_build (
                ID_event serial primary key,
                Event_date date,
                ID_build smallint references build (Inventory_ID),
                Ivent_amount_using smallint,
                ID_subproject smallint references subproject (ID_Subproject),
                ID_person smallint references persons (Person_ID),
                Event_comment text)""")

cur.execute("""CREATE TABLE IF NOT EXISTS event_inventory (
                ID_event serial primary key,
                Event_date date,
                ID_inventory smallint references inventory (Inventory_ID),
                ID_person smallint references persons (Person_ID),
                ID_place int references place (ID_place),
                Event_class text,
                Amount_inventory smallint,
                Event_comment text)""")

cur.execute(f"""INSERT INTO  place (Place_main,Place_second,Place_third,Place_last,Place_class)  VALUES {test_place}""")
cur.execute(f"""INSERT INTO  contragent (Sale_name,Ur_name,Date_of_document,Comment)  VALUES {test_contragent}""")
conn.commit()
cur.execute(f"""INSERT INTO  inventory (
                Inventory_name,
                Inventory_class,
                Inventory_subclass,
                Inventory_upd_name,
                ID_place,
                Inventory_amount,
                Inventory_date_choose,
                Inventory_date_sale,
                Invetory_date_of_break,
                Invetory_price,
                ID_saler,
                Inventory_url,
                Inventory_comment)
                  VALUES {test_inventory}""")
cur.execute(
    f"""INSERT INTO  project (Project_name,Project_date_start,Project_date_end,Project_comment)  VALUES {test_project}""")
conn.commit()
cur.execute(
    f"""INSERT INTO  subproject (Subproject_name,ID_mainproject,Subproject_date_start,Subproject_date_end,Subproject_comment)  VALUES {test_subproject}""")
conn.commit()
cur.close()
conn.close()
