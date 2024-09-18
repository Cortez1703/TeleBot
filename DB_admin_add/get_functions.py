from DB.DB_connection import connection

cur, conn = connection()


def get_inventory_name_regexp(word, cur):
    cur.execute(f"""SELECT Inventory_name from inventory where inventory_name ~* '{word}' and Inventory_amount > 0 
    and ID_place IN (SELECT ID_place from place where Place_class = 'В помещении') """)
    return cur.fetchall()


def get_give_inventory_name(word):
    return f"SELECT Inventory_name from inventory where inventory_name ~* '{word}' and Inventory_amount > 0"


def get_inventory_id_amount_place(word, cur):
    cur.execute(f"Select Inventory_ID,Inventory_amount,ID_place from inventory where Inventory_name='{word}'")
    return cur.fetchall()


def get_inventory_id_amount(cur, *args):
    if isinstance(args[1],int):
        cur.execute(
            f"""SELECT Inventory_ID,Inventory_amount FROM inventory 
                WHERE Inventory_name='{args[0]}' and ID_place = {args[1]}""")
    else:
        cur.execute(
            f"""SELECT Inventory_ID,Inventory_amount FROM inventory 
                    WHERE Inventory_name='{args[0]}' and ID_place IN {args[1]}""")
    return cur.fetchall()

def get_inventory_name_where_id(cur,word):
    cur.execute(f"SELECT Inventory_name FROM inventory WHERE ID_place={word}")
    return cur.fetchall()
def get_inventory_full(word, cur):
    cur.execute(f"SELECT * from inventory where inventory_name = '{word}'")
    return cur.fetchall()


def get_all_from_place(word, cur):
    cur.execute(f"SELECT * from place where ID_place={word}")
    return cur.fetchall()


def get_user_id(cur, tg_id):
    cur.execute(f"SELECT Person_ID from persons where Person_tg_id='{tg_id}'")
    return cur.fetchall()


def get_inventory_amount(word):
    return f"SELECT Inventory_amount from inventory where inventory_name = '{word}' "


def give_inventory_amount(cur,word):
    cur.execute(f"SELECT Inventory_amount from inventory where inventory_name = '{word}'")
    return cur.fetchall()

def get_inventory_place(word):
    return f"select ID_place from inventory where inventory_name='{word}'"


def get_user_place(cur,word):
    cur.execute(f"""SELECT Person_name,Person_surname from persons where Person_tg_id='{word}'""")
    return cur.fetchall()


def concatinate(listi):
    listi = [i for i in listi]
    return str(listi[1] + ' ' + listi[0])


def get_place(word):
    return f"Select Place_main,Place_second,Place_third,Place_last from place where ID_place={word}"


def get_place_class():
    cur.execute(f"SELECT ID_place from place where Place_class='В помещении'")
    return cur.fetchall()


def get_place_main(cur,word):
    cur.execute(f"Select ID_place from place where Place_main='{word}'")
    return cur.fetchall()


def full_inventory_info(args):
    return f"""ID инвентаря:  {args[0][0]}
Название инвентаря:  {args[0][1]}
Класс инвентаря:  {args[0][2]}
Подкласс инвентаря:  {args[0][3]}
Название по УПД:  {args[0][4]}
ID места назначения:  {args[0][5]}
Количество инвентаря:  {args[0][6]}
Дата выбора:  {args[0][7]}
Дата покупки: {args[0][8]}
Дата списания: {args[0][9]}
Цена за штуку:  {args[0][10]}
ID поставщика:  {args[0][11]}
Ссылка на товар:  {args[0][12]}
Комментарий:  {args[0][13]}
"""
