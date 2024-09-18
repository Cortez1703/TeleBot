from DB.DB_connection import connection
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter
from Buttons.buttons import admin_update_buttons

cur, conn = connection()

router = Router()


class OrderUpdateSubproject(StatesGroup):
    getName = State()
    getUrName = State()
    getDateStart = State()
    getComment = State()
    END = State()


@router.callback_query(StateFilter(None), F.data == 'Update_subproject')
async def update_contragent(call: types.CallbackQuery, state: FSMContext):
    cur.execute("""SELECT Subproject_name from subproject""")
    info = cur.fetchall()
    if info:
        buttons = []
        for i in info:
            buttons.append([types.InlineKeyboardButton(text=f'{i[0]}', callback_data=f'{i[0]}')])
        buttons.append([types.InlineKeyboardButton(text=f'Отменить изменение', callback_data=f'Admin_main')])
        buttons = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        await call.message.answer("Выберете проект, данные по которому хотите изменить", reply_markup=buttons)
        await state.set_state(OrderUpdateSubproject.getName)
    else:
        await call.message.answer("На данный момент в базе данных нет проектов")


@router.callback_query(StateFilter(OrderUpdateSubproject.getName))
async def get_new(call: types.CallbackQuery, state: FSMContext):
    cur.execute(f"""SELECT * from subproject where Subproject_name='{call.data}'""")
    user_data = cur.fetchall()
    await state.update_data(project_id=user_data[0][0])
    await state.update_data(new_project_name=user_data[0][2])
    await state.update_data(new_date_start_name=user_data[0][3])
    await state.update_data(new_date_end_name=user_data[0][4])
    await state.update_data(new_comment_name=user_data[0][5])
    button = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='Оставить старое',
                                                                                     callback_data="Get_old")]])
    await call.message.answer('Введите новое наименование подпроекта или нажмите "Оставить старое"',
                              reply_markup=button)
    await state.set_state(OrderUpdateSubproject.getUrName)


@router.message(StateFilter(OrderUpdateSubproject.getUrName))
async def get_ur_name(message: types.Message, state: FSMContext):
    await state.update_data(new_project_name=message.text)
    button = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='Оставить старое',
                                                                                     callback_data="Get_old")]])
    await message.answer('Введите новую дату начала подпроекта или нажмите "Оставить старое"',
                         reply_markup=button)
    await state.set_state(OrderUpdateSubproject.getDateStart)


@router.callback_query(StateFilter(OrderUpdateSubproject.getUrName))
async def get_new(call: types.CallbackQuery, state: FSMContext):
    button = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='Оставить старое',
                                                                                     callback_data="Get_old")]])
    await call.message.answer('Введите новую дату начала подпроекта или нажмите "Оставить старое"',
                              reply_markup=button)
    await state.set_state(OrderUpdateSubproject.getDateStart)


@router.message(StateFilter(OrderUpdateSubproject.getDateStart))
async def get_ur_name(message: types.Message, state: FSMContext):
    await state.update_data(new_date_start_name=message.text)
    button = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='Оставить старое',
                                                                                     callback_data="Get_old")]])
    await message.answer('Введите новую дату конца подпроекта или нажмите "Оставить старое"',
                         reply_markup=button)
    await state.set_state(OrderUpdateSubproject.getComment)


@router.callback_query(StateFilter(OrderUpdateSubproject.getDateStart))
async def get_new(call: types.CallbackQuery, state: FSMContext):
    button = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='Оставить старое',
                                                                                     callback_data="Get_old")]])
    await call.message.answer('Введите новую дату конца подпроекта или нажмите "Оставить старое"',
                              reply_markup=button)
    await state.set_state(OrderUpdateSubproject.getComment)


@router.message(StateFilter(OrderUpdateSubproject.getComment))
async def get_ur_name(message: types.Message, state: FSMContext):
    await state.update_data(new_date_end_name=message.text)
    button = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='Оставить старое',
                                                                                     callback_data="Get_old")]])
    await message.answer('Введите новый комментарий или нажмите "Оставить старое"',
                         reply_markup=button)
    await state.set_state(OrderUpdateSubproject.END)


@router.callback_query(StateFilter(OrderUpdateSubproject.getComment))
async def get_new(call: types.CallbackQuery, state: FSMContext):
    button = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='Оставить старое',
                                                                                     callback_data="Get_old")]])
    await call.message.answer('Введите новый комментарий или нажмите "Оставить старое"',
                              reply_markup=button)
    await state.set_state(OrderUpdateSubproject.END)


@router.message(StateFilter(OrderUpdateSubproject.END))
async def get_ur_name(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    cur.execute(
        f"""UPDATE subproject SET Subproject_name='{user_data['new_project_name']}',Subproject_date_start='{user_data['new_date_start_name']}',
            Subproject_date_end='{user_data['new_date_end_name']}',Subproject_comment='{user_data['new_comment_name']}' where ID_subproject={int(user_data['project_id'])}""")
    conn.commit()
    button = admin_update_buttons()
    await message.answer('Данные обновлены')
    await message.answer('Выберете необходимое действие',
                         reply_markup=button)
    await state.set_state(None)


@router.callback_query(StateFilter(OrderUpdateSubproject.END))
async def get_new(call: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    cur.execute(
        f"""UPDATE subproject SET Subproject_name='{user_data['new_project_name']}',Subproject_date_start='{user_data['new_date_start_name']}',
            Subproject_date_end='{user_data['new_date_end_name']}',Subproject_comment='{user_data['new_comment_name']}' where ID_subproject={int(user_data['project_id'])}""")
    conn.commit()
    button = admin_update_buttons()
    await call.message.answer('Данные обновлены')
    await call.message.answer('Выберете необходимое действие',
                              reply_markup=button)
    await state.set_state(None)
