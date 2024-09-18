from DB.DB_connection import connection
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter
from Buttons.buttons import admin_update_buttons

cur, conn = connection()

router = Router()


class OrderUpdateContragent(StatesGroup):
    getName = State()
    getUrName = State()
    getDateStart = State()
    getComment = State()
    END = State()


@router.callback_query(StateFilter(None), F.data == 'Update_contragent')
async def update_contragent(call: types.CallbackQuery, state: FSMContext):
    cur.execute("""SELECT Sale_name from contragent""")
    info = cur.fetchall()
    if info:
        buttons = []
        for i in info:
            buttons.append([types.InlineKeyboardButton(text=f'{i[0]}', callback_data=f'{i[0]}')])
        buttons.append([types.InlineKeyboardButton(text=f'Отменить изменение', callback_data=f'Admin_main')])
        buttons = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        await call.message.answer("Выберете контрагента, данные по которому хотите изменить", reply_markup=buttons)
        await state.set_state(OrderUpdateContragent.getName)
    else:
        await call.message.answer("На данный момент в базе данных нет контрагентов")


@router.callback_query(StateFilter(OrderUpdateContragent.getName))
async def get_new(call: types.CallbackQuery, state: FSMContext):
    cur.execute(f"""SELECT * from contragent where Sale_name='{call.data}'""")
    user_data = cur.fetchall()
    await state.update_data(sale_id=user_data[0][0])
    await state.update_data(new_sale_name=user_data[0][1])
    await state.update_data(new_ur_name=user_data[0][2])
    await state.update_data(new_date_name=user_data[0][3])
    await state.update_data(new_comment_name=user_data[0][4])
    button = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='Оставить старое',
                                                                                     callback_data="Get_old")]])
    await call.message.answer('Введите новое наименование контрагента или нажмите "Оставить старое"',
                              reply_markup=button)
    await state.set_state(OrderUpdateContragent.getUrName)


@router.message(StateFilter(OrderUpdateContragent.getUrName))
async def get_ur_name(message: types.Message, state: FSMContext):
    await state.update_data(new_sale_name=message.text)
    button = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='Оставить старое',
                                                                                     callback_data="Get_old")]])
    await message.answer('Введите новое юридическое название контрагента или нажмите "Оставить старое"',
                         reply_markup=button)
    await state.set_state(OrderUpdateContragent.getDateStart)


@router.callback_query(StateFilter(OrderUpdateContragent.getUrName))
async def get_new(call: types.CallbackQuery, state: FSMContext):
    button = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='Оставить старое',
                                                                                     callback_data="Get_old")]])
    await call.message.answer('Введите новое юридическое название контрагента или нажмите "Оставить старое"',
                              reply_markup=button)
    await state.set_state(OrderUpdateContragent.getDateStart)


@router.message(StateFilter(OrderUpdateContragent.getDateStart))
async def get_ur_name(message: types.Message, state: FSMContext):
    await state.update_data(new_ur_name=message.text)
    button = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='Оставить старое',
                                                                                     callback_data="Get_old")]])
    await message.answer('Введите новую дату договора или нажмите "Оставить старое"',
                         reply_markup=button)
    await state.set_state(OrderUpdateContragent.getComment)


@router.callback_query(StateFilter(OrderUpdateContragent.getDateStart))
async def get_new(call: types.CallbackQuery, state: FSMContext):
    button = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='Оставить старое',
                                                                                     callback_data="Get_old")]])
    await call.message.answer('Введите новую дату договора или нажмите "Оставить старое"',
                              reply_markup=button)
    await state.set_state(OrderUpdateContragent.getComment)


@router.message(StateFilter(OrderUpdateContragent.getComment))
async def get_ur_name(message: types.Message, state: FSMContext):
    await state.update_data(new_date_name=message.text)
    button = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='Оставить старое',
                                                                                     callback_data="Get_old")]])
    await message.answer('Введите новый комментарий или нажмите "Оставить старое"',
                         reply_markup=button)
    await state.set_state(OrderUpdateContragent.END)


@router.callback_query(StateFilter(OrderUpdateContragent.getComment))
async def get_new(call: types.CallbackQuery, state: FSMContext):
    button = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='Оставить старое',
                                                                                     callback_data="Get_old")]])
    await call.message.answer('Введите новый комментарий или нажмите "Оставить старое"',
                              reply_markup=button)
    await state.set_state(OrderUpdateContragent.END)


@router.message(StateFilter(OrderUpdateContragent.END))
async def get_ur_name(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    cur.execute(f"""UPDATE contragent SET Sale_name='{user_data['new_sale_name']}',Ur_name='{user_data['new_ur_name']}',
    Date_of_document='{user_data['new_date_name']}',Comment='{user_data['new_comment_name']}'""")
    conn.commit()
    button = admin_update_buttons()
    await message.answer('Данные обновлены')
    await message.answer('Выберете необходимое действие',
                         reply_markup=button)
    await state.set_state(None)


@router.callback_query(StateFilter(OrderUpdateContragent.END))
async def get_new(call: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    cur.execute(f"""UPDATE contragent SET Sale_name='{user_data['new_sale_name']}',Ur_name='{user_data['new_ur_name']}',
Date_of_document='{user_data['new_date_name']}',Comment='{user_data['new_comment_name']}' where ID_contragent={user_data['sale_id']}""")
    conn.commit()
    button = admin_update_buttons()
    await call.message.answer('Данные обновлены')
    await call.message.answer('Выберете необходимое действие',
                              reply_markup=button)
    await state.set_state(None)
