"""В данном блоке прописаны функции добавления данных в базу данных по переданным внутрь параметрам"""
from datetime import datetime


def add_project(args):
    '''Функция добавления проекта компании в бащу данных
    Если дата окончания проекта не прописана - вводить Null, для пустого поля'''
    if args["project_end_work_date"].capitalize() == "Null":
        ans = f"""INSERT INTO project (
                Project_name,
                Project_date_start,
                Project_date_end,
                Project_comment) VALUES (
                '{args["project_name"]}','{args["project_start_work_date"]}',
                NULL,'{args["project_comment"]}')
"""
    else:
        ans = f"""INSERT INTO project (
                        Project_name,
                        Project_date_start,
                        Project_date_end,
                        Project_comment) VALUES (
                        '{args["project_name"]}','{args["project_start_work_date"]}',
                        '{args["project_end_work_date"]}','{args["project_comment"]}')"""

    return ans


def add_contragent(args):
    '''Функция добавления контрагента компании в базу данных'''
    ans = f"""INSERT INTO contragent (Sale_name ,
                Ur_name ,
                Date_of_document ,
                Comment) VALUES 
        ('{args['Sale']}', '{args['ur_name']}', '{args['date_of_document']}', '{args['comment']}')  """

    return ans


def add_placE(args):
    """Функция добавления места нахождения в лабе. Обычно работает до времени использования самого кода,
    т.к. все пространства заполняются заранее"""
    ans = f"""INSERT INTO place (Place_main,Place_second ,Place_third ,Place_last,Place_class) VALUES 
        ('{args['first_level']}', '{args['second_level']}', {args['third_level']}, {args['last_level']},'В помещении')  """

    return ans


def add_place_user(user_name):
    return f"""INSERT INTO place (
                Place_main ,
                Place_second,
                Place_third,
                Place_last,Place_class) VALUES ('{user_name}',Null,Null,Null,'У человека')"""


def add_inventory(cur,conn,args):
    """Функция возвращает текстовую переменную, используемую для добавления данных по инвентарю в БД"""
    if args['inventory_date_break'] == '-':
        ans = f"""INSERT INTO inventory (Inventory_name,
                    Inventory_class,
                    Inventory_subclass,
                    Inventory_upd_name,
                    ID_place ,
                    Inventory_amount,
                    Inventory_date_choose,
                    Inventory_date_sale,
                    Invetory_date_of_break,
                    Invetory_price,
                    ID_saler,
                    Inventory_url,
                    Inventory_comment) VALUES 
            ('{args['inventory_name']}', 
            '{args['inventory_class']}', 
            '{args['inventory_subclass']}', 
            '{args['inventory_upd']}',
            {args['ID_place']},
            {args['inventory_amount']},
            '{args['inventory_date_choose']}',
            '{args['inventory_date_sale']}',
            NULL,
            {args['inventory_price']},
            '{args['ID_contragent']}','{args['inventory_url']}','{args['inventory_comment']}')  """
    else:
        ans = f"""INSERT INTO inventory (Inventory_name,
                            Inventory_class,
                            Inventory_subclass,
                            Inventory_upd_name,
                            ID_place ,
                            Inventory_amount,
                            Inventory_date_choose,
                            Inventory_date_sale,
                            Invetory_date_of_break,
                            Invetory_price,
                            ID_saler,
                            Inventory_url,
                            Inventory_comment) VALUES 
                    ('{args['inventory_name']}', 
                    '{args['inventory_class']}', 
                    '{args['inventory_subclass']}', 
                    '{args['inventory_upd']}',
                    {args['ID_place']},
                    {args['inventory_amount']},
                    '{args['inventory_date_choose']}',
                    '{args['inventory_date_sale']}',
                    '{args['inventory_date_break']}',
                    {args['inventory_price']},
                    '{args['ID_contragent']}','{args['inventory_url']}','{args['inventory_comment']}')  """
    cur.execute(ans)
    conn.commit()

def add_inventory_2(cur,conn,args):
    if args[8]:
        ans = """INSERT INTO inventory (Inventory_name,
                        Inventory_class,
                        Inventory_subclass,
                        Inventory_upd_name,
                        ID_place ,
                        Inventory_amount,
                        Inventory_date_choose,
                        Inventory_date_sale,
                        Invetory_date_of_break,
                        Invetory_price,
                        ID_saler,
                        Inventory_url,
                        Inventory_comment) VALUES ('{0}','{1}','{2}','{3}',{4},{5},'{6}','{7}','{8}',{9},{10},
                '{11}','{12}')""".format(*args)
    else:
        ans = """INSERT INTO inventory (Inventory_name,
                                Inventory_class,
                                Inventory_subclass,
                                Inventory_upd_name,
                                ID_place ,
                                Inventory_amount,
                                Inventory_date_choose,
                                Inventory_date_sale,
                                Invetory_date_of_break,
                                Invetory_price,
                                ID_saler,
                                Inventory_url,
                                Inventory_comment) VALUES ('{0}','{1}','{2}','{3}',{4},{5},'{6}','{7}',NULL,{9},{10},
                        '{11}','{12}')""".format(*args)
    cur.execute(ans)
    conn.commit()



def add_inventory_event(args, cur, conn):
    command = f"""INSERT INTO event_inventory (Event_date ,ID_inventory ,
                ID_person ,ID_place,Event_class ,Amount_inventory ,
                Event_comment) VALUES ('{datetime.now().replace(microsecond=0)}',{args[0]},{args[1]},{args[2]},
                '{args[3]}',{int(args[4])},'-')"""
    cur.execute(command)
    conn.commit()
