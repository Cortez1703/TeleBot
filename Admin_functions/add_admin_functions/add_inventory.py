from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
import psycopg2
from aiogram import F
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter
from Buttons.buttons import Start_menu_buttons
from DB_admin_add import add_functions
from DB_admin_add.get_functions import get_give_inventory_name

conn = psycopg2.connect(dbname='test', user='postgres', password='leolab12', host='127.0.0.1')
cur = conn.cursor()

router = Router()


class OrderPlace(StatesGroup):
    Inventory_name = State()
    Inventory_class = State()
    Inventory_subclass = State()
    Inventory_upd_name = State()
    Inventory_place1 = State()
    Inventory_place2 = State()
    Inventory_place3 = State()
    Inventory_place4 = State()
    ID_place = State()
    Inventory_amount = State()
    Inventory_date_choose = State()
    Inventory_date_sale = State()
    Inventory_date_of_break = State()
    Inventory_price = State()
    Id_contragent = State()
    Inventory_url = State()
    Inventory_comment = State()
    END = State()


class OrderGiveInventory(StatesGroup):
    GiveName = State()


@router.message(StateFilter(None), Command('add_inventory'))
async def add_place(message: types.Message, state: FSMContext):
    button_cancel = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="Отменить операцию",
                                                                                            callback_data="Start_menu")]])
    await message.answer("Введите название инвентаря", reply_markup=button_cancel)
    await state.set_state(OrderPlace.Inventory_name)


@router.callback_query(F.data == 'add_inventory')
async def add_place(call: types.CallbackQuery, state: FSMContext):
    button_cancel = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="Отменить операцию",
                                                                                            callback_data="Start_menu")]])
    await call.message.answer("Введите название инвентаря", reply_markup=button_cancel)
    await state.set_state(OrderPlace.Inventory_name)


@router.message(StateFilter(OrderPlace.Inventory_name))
async def add_place(message: types.Message, state: FSMContext):
    cur.execute(get_give_inventory_name(message.text))
    object_name = cur.fetchall()
    await state.update_data(inventory_name=message.text.capitalize())
    button_cancel = [types.InlineKeyboardButton(text="Отменить операцию", callback_data="Start_menu")]
    button_add = [types.InlineKeyboardButton(text="Добавить то, что ввёл", callback_data="Add_new")]
    if object_name:
        buttons = [[types.InlineKeyboardButton(text=f"{i[0]}", callback_data=f'{i[0]}')] for i in
                   object_name]
        buttons.append(button_cancel)
        buttons.append(button_add)
        buttons = types.InlineKeyboardMarkup(inline_keyboard=buttons)

        await message.answer("На данный момент есть следующие позиции", reply_markup=buttons)
        await message.answer(
            '''Выберете что-то из предложенного списка для добавления нового инвентаря 
к старому или же введите другое название''')

    else:
        buttons = types.InlineKeyboardMarkup(inline_keyboard=[button_cancel])
        await message.answer("Введите класс инвентаря", reply_markup=buttons)
        await state.set_state(OrderPlace.Inventory_class)


@router.callback_query(StateFilter(OrderPlace.Inventory_name), F.data == 'Add_new')
async def add_new(call: types.CallbackQuery, state: FSMContext):
    button_cancel = [types.InlineKeyboardButton(text="Отменить операцию", callback_data="Start_menu")]
    buttons = types.InlineKeyboardMarkup(inline_keyboard=[button_cancel])
    await call.message.answer("Введите класс инвентаря", reply_markup=buttons)
    await state.set_state(OrderPlace.Inventory_class)


@router.message(StateFilter(OrderPlace.Inventory_class))
async def add_place(message: types.Message, state: FSMContext):
    button_cancel = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="Отменить операцию",
                                                                                            callback_data="Start_menu")]])
    await state.update_data(inventory_class=message.text)
    await message.answer("Введите подкласс инвентаря", reply_markup=button_cancel)
    await state.set_state(OrderPlace.Inventory_subclass)


@router.message(StateFilter(OrderPlace.Inventory_subclass))
async def add_place(message: types.Message, state: FSMContext):
    button_cancel = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="Отменить операцию",
                                                                                            callback_data="Start_menu")]])
    await state.update_data(inventory_subclass=message.text.capitalize())
    await message.answer("Введите название по УПД", reply_markup=button_cancel)
    await state.set_state(OrderPlace.Inventory_upd_name)


@router.message(StateFilter(OrderPlace.Inventory_upd_name))
async def add_place(message: types.Message, state: FSMContext):
    await state.update_data(inventory_upd=message.text.capitalize())
    cur.execute("Select Place_main from place where Place_class='В помещении'")
    list_of = [i[0] for i in set(cur.fetchall())]
    buttons = [[types.InlineKeyboardButton(text=f'{i}', callback_data=f'{i}')] for i in list_of]
    buttons.append([types.InlineKeyboardButton(text="Отменить операцию",
                                               callback_data="Start_menu")])
    buttons = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("Выберете комнату, куда кладете инвентарь", reply_markup=buttons)
    await state.set_state(OrderPlace.Inventory_place1)


@router.callback_query(StateFilter(OrderPlace.Inventory_place1))
async def add_place(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(inventory_place1=call.data)
    user_data = await state.get_data()

    cur.execute(f"Select Place_second from place where Place_main='{user_data["inventory_place1"]}'")
    list_of = [i[0] for i in set(cur.fetchall())]
    buttons = [[types.InlineKeyboardButton(text=f'{i}', callback_data=f'{i}')] for i in list_of]
    buttons.append([types.InlineKeyboardButton(text="Отменить операцию",
                                               callback_data="Start_menu")])
    buttons = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await call.message.answer("Выберете стол/стеллаж", reply_markup=buttons)
    await state.set_state(OrderPlace.Inventory_place2)


@router.callback_query(StateFilter(OrderPlace.Inventory_place2))
async def add_place(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(inventory_place2=call.data)
    user_data = await state.get_data()
    cur.execute(f"""Select Place_third from place where Place_main='{user_data['inventory_place1']}' 
    and Place_second='{user_data['inventory_place2']}'""")
    list_of = [i[0] for i in set(cur.fetchall())]
    buttons = [[types.InlineKeyboardButton(text=f'{i}', callback_data=f'{i}')] for i in list_of]
    buttons.append([types.InlineKeyboardButton(text="Отменить операцию",
                                               callback_data="Start_menu")])
    buttons = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await call.message.answer("Выберете стол/стеллаж", reply_markup=buttons)
    await state.set_state(OrderPlace.Inventory_place3)


@router.callback_query(StateFilter(OrderPlace.Inventory_place3))
async def add_place(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(inventory_place3=call.data)
    user_data = await state.get_data()
    cur.execute(f"""Select Place_last from place where Place_main='{user_data['inventory_place1']}' 
    and Place_second='{user_data['inventory_place2']}' and Place_third={user_data['inventory_place3']}""")
    list_of = [i[0] for i in set(cur.fetchall())]
    buttons = [[types.InlineKeyboardButton(text=f'{i}', callback_data=f'{i}')] for i in list_of]
    buttons.append([types.InlineKeyboardButton(text="Отменить операцию",
                                               callback_data="Start_menu")])
    buttons = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await call.message.answer("Выберете ряд", reply_markup=buttons)
    await state.set_state(OrderPlace.Inventory_place4)


@router.callback_query(StateFilter(OrderPlace.Inventory_place4))
async def add_place(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(inventory_place4=call.data)
    user_data = await state.get_data()
    cur.execute(f"""Select ID_place from place where Place_main='{user_data["inventory_place1"]}' and
Place_second='{user_data["inventory_place2"]}' and Place_third={int(user_data['inventory_place3'])} 
and Place_last={int(user_data['inventory_place4'])}""")

    listi = cur.fetchall()

    button_cancel = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="Отменить операцию",
                                                                                            callback_data="Start_menu")]])
    await state.update_data(ID_place=listi[0][0])
    await state.set_state(OrderPlace.Inventory_amount)
    await call.message.answer("Выберете количество инвентаря", reply_markup=button_cancel)


@router.message(StateFilter(OrderPlace.Inventory_amount))
async def add_place(message: types.Message, state: FSMContext):
    button_cancel = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="Отменить операцию",
                                                                                            callback_data="Start_menu")]])
    await state.update_data(inventory_amount=message.text)
    await message.answer("Введите дату выбора инвентаря (в формате ДД-ММ-ГГГГ)", reply_markup=button_cancel)
    await state.set_state(OrderPlace.Inventory_date_choose)


@router.message(StateFilter(OrderPlace.Inventory_date_choose))
async def add_place(message: types.Message, state: FSMContext):
    button_cancel = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="Отменить операцию",
                                                                                            callback_data="Start_menu")]])
    await state.update_data(inventory_date_choose=message.text)
    await message.answer("Введите дату покупки инвентаря (в формате ДД-ММ-ГГГГ)", reply_markup=button_cancel)
    await state.set_state(OrderPlace.Inventory_date_sale)


@router.message(StateFilter(OrderPlace.Inventory_date_sale))
async def add_place(message: types.Message, state: FSMContext):
    button_cancel = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="Отменить операцию",
                                                                                            callback_data="Start_menu")]])
    await state.update_data(inventory_date_sale=message.text)
    await message.answer(
        "Введите дату списания/поломки инвентаря (в формате ДД-ММ-ГГГГ или -, если дата поломки не наступила",
        reply_markup=button_cancel)
    await state.set_state(OrderPlace.Inventory_date_of_break)


@router.message(StateFilter(OrderPlace.Inventory_date_of_break))
async def add_place(message: types.Message, state: FSMContext):
    button_cancel = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="Отменить операцию",
                                                                                            callback_data="Start_menu")]])
    await state.update_data(inventory_date_break=message.text)
    await message.answer("Введите цену инвентаря", reply_markup=button_cancel)
    await state.set_state(OrderPlace.Inventory_price)


@router.message(StateFilter(OrderPlace.Inventory_price))
async def add_place(message: types.Message, state: FSMContext):
    await state.update_data(inventory_price=message.text)
    cur.execute("Select Sale_name from contragent")
    list_of = [i[0] for i in set(cur.fetchall())]
    buttons = [[types.InlineKeyboardButton(text=f'{i}', callback_data=f'{i}')] for i in list_of]
    buttons.append([types.InlineKeyboardButton(text="Отменить операцию",
                                               callback_data="Start_menu")])
    buttons = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("Выберете Контрагента, у которого купили", reply_markup=buttons)
    await state.set_state(OrderPlace.Id_contragent)


@router.callback_query(StateFilter(OrderPlace.Id_contragent))
async def add_place(call: types.CallbackQuery, state: FSMContext):
    button_cancel = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="Отменить операцию",
                                                                                            callback_data="Start_menu")]])
    await state.update_data(saler_name=call.data)
    user_data = await state.get_data()
    cur.execute(f"""Select ID_contragent from contragent where Sale_name='{user_data["saler_name"]}'""")
    listi = cur.fetchall()
    await state.update_data(ID_contragent=listi[0][0])
    await call.message.answer("Введите ссылку на товар", reply_markup=button_cancel)
    await state.set_state(OrderPlace.Inventory_url)


@router.message(StateFilter(OrderPlace.Inventory_url))
async def add_place(message: types.Message, state: FSMContext):
    button_cancel = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="Отменить операцию",
                                                                                            callback_data="Start_menu")]])
    await state.update_data(inventory_url=message.text)

    await message.answer("Введите комментарий", reply_markup=button_cancel)
    await state.set_state(OrderPlace.Inventory_comment)


@router.message(StateFilter(OrderPlace.Inventory_comment))
async def add_place(message: types.Message, state: FSMContext):
    await state.update_data(inventory_comment=message.text.capitalize())
    user_data = await state.get_data()
    buttons = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text='Добавить в базу данных', callback_data="Inventory_add")],
        [types.InlineKeyboardButton(text='Изменить', callback_data="Inventory_change")]

    ])
    await message.answer(f"""Вы ввели
Название инвентаря {user_data['inventory_name']}
Класс инвентаря {user_data['inventory_class']}
Подкласс инвентаря {user_data['inventory_subclass']}
Название по УПД {user_data['inventory_upd']}
ID места назначения {user_data['ID_place']}
Количество инвентаря {user_data['inventory_amount']}
Дата выбора {user_data['inventory_date_choose']}
Дата покупки {user_data['inventory_date_sale']}
Дата списания{user_data['inventory_date_break']}
Цена за штуку {user_data['inventory_price']}
ID поставщика {user_data['ID_contragent']}
Ссылка на товар {user_data['inventory_url']}
Комментарий {user_data['inventory_comment']}
""", reply_markup=buttons)
    await state.set_state(OrderPlace.END)


@router.callback_query(OrderPlace.END, F.data == 'Inventory_change')
async def add_place(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Введите торговое название контрагента")
    await state.set_state(None)


@router.callback_query(OrderPlace.END, F.data == 'Inventory_add')
async def add_place(call: types.CallbackQuery, state: FSMContext):
    add_functions.add_inventory(cur, conn, await state.get_data())
    buttons = Start_menu_buttons()
    await call.message.answer("Данные добавлены")
    await call.message.answer("Выберете дальнейшее действие", reply_markup=buttons)
    await state.set_state(None)
