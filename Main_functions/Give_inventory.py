from DB.DB_connection import connection
from DB_admin_add import get_functions

cur, conn = connection()

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter
from Buttons.buttons import Start_menu_buttons


class OrderGiveInventory(StatesGroup):
    GiveName = State()
    GiveInventory = State()
    GiveAmount = State()


router = Router()


@router.callback_query(StateFilter(None), F.data == 'Give_inventory')
async def give_list_of_inventory(call: types.CallbackQuery, state: FSMContext):
    """Стартовая функция для процесса возврата какого-либо объекта
        Проверяется наличие какого-либо инвентаря у человека и есть 2 варианта:
        -Ничего нет. Пользователю предлагается добавить НОВЫЙ объект в базу
        -Какие-то предметы находятся у пользователя.Предлагается список предметов на возврат."""

    # Поиск ID_place ориентируясь на Telegram_ID и поиск всех предметов, которые находятся у данного человека

    list_names = [i for i in get_functions.get_user_place(cur,call.from_user.id)[0]]
    place_id = get_functions.get_place_main(cur,get_functions.concatinate(list_names))[0][0]
    await state.update_data(place_id=place_id)
    inventory = [i[0] for i in get_functions.get_inventory_name_where_id(cur,place_id)]
    # Проверка на наличие каких-либо предметов у человека
    if inventory:
        buttons = [[types.InlineKeyboardButton(text=f"{i}", callback_data=f"{i}")] for i in inventory]
        buttons.append([types.InlineKeyboardButton(text=f"Отмена", callback_data="Start_menu")])
        buttons = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        await state.set_state(OrderGiveInventory.GiveName)
        await call.message.answer('''Выберете, что хотите вернуть.Если хотите внести новое оборудование - 
        нажмите кнопку "Внести новое оборудование"''',
                                  reply_markup=buttons)
    else:
        buttons = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text=f"Внести новое оборудование", callback_data="add_inventory")],
            [types.InlineKeyboardButton(text=f"Отмена", callback_data="Start_menu")]])
        await call.message.answer(
            '''Вы ничего не брали. Внесите новый предмет, нажав на соответствующую кнопку или 
            вернитесь на стартовое меню, нажам "Отмена"''',
            reply_markup=buttons)


@router.callback_query(StateFilter(OrderGiveInventory.GiveName), F.data != 'add_inventory')
async def return_inventory(call: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    await state.update_data(inventory_name=call.data)
    button = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="Вернуть все",
                                                                                     callback_data="give_all")]])

    inventory_id,inventory_amount = get_functions.get_inventory_id_amount(cur,call.data,user_data['place_id'])[0]
    await call.message.answer(f"""Вы брали {call.data}
    в количестве {inventory_amount}.Введите число инвентаря, которое возвращаете или нажмите кнопку 'Вернуть всё'""",
                              reply_markup=button)
    await state.set_state(OrderGiveInventory.GiveInventory)


@router.callback_query(StateFilter(OrderGiveInventory.GiveInventory), F.data == 'give_all')
async def return_all_inventory(call: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    cur.execute(f"""SELECT Inventory_ID FROM inventory WHERE Inventory_name='{user_data['inventory_name']}' AND 
           ID_place NOT IN (SELECT ID_place FROM place WHERE Place_class='У человека')""")
    inventory_id = cur.fetchall()[0][0]
    cur.execute(f"""SELECT Inventory_amount from inventory where Inventory_name='{user_data['inventory_name']}' 
           and ID_place= {user_data['place_id']}""")
    user_amount = cur.fetchall()[0][0]
    cur.execute(
        f"""UPDATE inventory SET Inventory_amount=Inventory_amount+{int(user_amount)} WHERE
         Inventory_ID = {inventory_id}""")
    cur.execute(f"""DELETE FROM inventory WHERE Inventory_name='{user_data['inventory_name']}' 
           AND ID_place= {user_data['place_id']}""")
    conn.commit()
    amount = get_functions.give_inventory_amount(cur,user_data['inventory_name'])[0][0]
    buttons = Start_menu_buttons()
    await call.message.answer(f"""Данные обновлены.Теперь {user_data['inventory_name']} в количестве {amount}  """)
    await call.message.answer(f"""Выберете необходимое действие""",
                              reply_markup=buttons)
    await state.set_state(None)


@router.message(StateFilter(OrderGiveInventory.GiveInventory))
async def get_some_inventory(message: types.Message, state: FSMContext):
    await state.update_data(message_id=message.message_id)
    await state.update_data(chat_id=message.chat.id)
    user_data = await state.get_data()
    await message.bot.delete_message(chat_id=user_data['chat_id'], message_id=user_data['message_id'])
    user_data = await state.get_data()
    cur.execute(
        f"""SELECT Inventory_ID,Inventory_amount from inventory where Inventory_name='{user_data['inventory_name']}' and 
        ID_place NOT IN (SELECT ID_place from place where Place_class='У человека')""")
    inv_id, inv_amount = cur.fetchall()[0]
    cur.execute(f"""SELECT Inventory_amount from inventory where Inventory_name='{user_data['inventory_name']}' 
        and ID_place= {user_data['place_id']}""")
    user_amount = cur.fetchall()[0][0]
    if int(user_amount) > int(message.text):
        cur.execute(
            f"""UPDATE inventory SET Inventory_amount=Inventory_amount+{int(message.text)} where 
            Inventory_ID = {inv_id}""")
        conn.commit()

        cur.execute(
            f"""UPDATE inventory SET Inventory_amount=Inventory_amount-{int(message.text)} 
            where ID_place = {user_data['place_id']} and Inventory_name='{user_data['inventory_name']}'
""")
        conn.commit()

        cur.execute(f"""SELECT Inventory_amount from inventory where Inventory_name='{user_data["inventory_name"]}' 
                       and Inventory_ID = {inv_id}""")
        amount = cur.fetchall()[0][0]
        buttons = Start_menu_buttons()
        await message.answer(f"""Данные обновлены.Теперь {user_data['inventory_name']} в количестве {amount} на месте.
У вас осталось {int(user_amount) - int(message.text)}""")
        await message.answer(f"""Выберете необходимое действие""",
                             reply_markup=buttons)
        await state.set_state(None)

    elif int(user_amount) == int(message.text):
        cur.execute(
            f"""UPDATE inventory SET Inventory_amount=Inventory_amount+{int(message.text)} 
            where Inventory_ID = {inv_id}""")
        cur.execute(f"DELETE FROM inventory where ID_place = {user_data['place_id']}")
        cur.execute(f"""SELECT Inventory_amount from inventory where Inventory_name='{user_data["inventory_name"]}' 
                               and Inventory_ID = {inv_id}""")
        amount = cur.fetchall()[0][0]
        buttons = Start_menu_buttons()
        await message.answer(f"""Данные обновлены.Теперь {user_data['inventory_name']} в количестве {amount}  """)
        await message.answer(f"""Выберете необходимое действие""",
                             reply_markup=buttons)
        await state.set_state(None)
        conn.commit()
    else:
        await message.answer("Вы ввели число большее, чем вы брали. Введите данные корректно")
