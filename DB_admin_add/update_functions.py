def update_inventory(old_amount,new_amount,name):
    return f"""UPDATE inventory SET Inventory_amount={old_amount+float(new_amount)} where Inventory_name='{name}'"""

def update_inventory_main_minus(cur,conn,*args):
    cur.execute(
        f"""UPDATE inventory SET Inventory_amount={int(args[0]) - int(args[1])} 
                    where Inventory_name='{args[2]}' and Inventory_ID={args[3]} """)
    conn.commit()

def update_inventory_person_plus(cur,conn,*args):
    cur.execute(f"""UPDATE inventory SET Inventory_amount={int(args[0]) + int(args[1])} 
                    where Inventory_ID='{args[2]}' """)
    conn.commit()