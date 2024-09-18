from DB.DB_connection import connection
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter
from Buttons.buttons import admin_update_buttons

cur, conn = connection()

router = Router()


class OrderUpdateProject(StatesGroup):
    getName = State()
    getUrName = State()
    getDateStart = State()
    getComment = State()
    END = State()


@router.callback_query(StateFilter(None), F.data == 'Update_project')
async def update_contragent(call: types.CallbackQuery, state: FSMContext):
    cur.execute("""SELECT Project_name from project""")
    info = cur.fetchall()
    if info:
        buttons = []
        for i in info:
            buttons.append([types.InlineKeyboardButton(text=f'{i[0]}', callback_data=f'{i[0]}')])
        buttons.append([types.InlineKeyboardButton(text=f'Отменить изменение', callback_data=f'Admin_main')])
        buttons = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        await call.message.answer("Выберете подпроект, данные по которому хотите изменить", reply_markup=buttons)
        await state.set_state(OrderUpdateProject.getName)
    else:
        await call.message.answer("На данный момент в базе данных нет проектов")


@router.callback_query(StateFilter(OrderUpdateProject.getName))
async def get_new(call: types.CallbackQuery, state: FSMContext):
    print(call.data)
    cur.execute(f"""SELECT * from project where Project_name='{call.data}'""")
    user_data = cur.fetchall()
    await state.update_data(project_id=user_data[0][0])
    await state.update_data(new_project_name=user_data[0][1])
    await state.update_data(new_date_start_name=user_data[0][2])
    await state.update_data(new_date_end_name=user_data[0][3])
    await state.update_data(new_comment_name=user_data[0][4])
    button = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='Оставить старое',
                                                                                     callback_data="Get_old")]])
    await call.message.answer('Введите новое наименование проекта или нажмите "Оставить старое"',
                              reply_markup=button)
    await state.set_state(OrderUpdateProject.getUrName)


@router.message(StateFilter(OrderUpdateProject.getUrName))
async def get_ur_name(message: types.Message, state: FSMContext):
    await state.update_data(new_project_name=message.text)
    button = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='Оставить старое',
                                                                                     callback_data="Get_old")]])
    await message.answer('Введите новую дату начала проекта или нажмите "Оставить старое"',
                         reply_markup=button)
    await state.set_state(OrderUpdateProject.getDateStart)


@router.callback_query(StateFilter(OrderUpdateProject.getUrName))
async def get_new(call: types.CallbackQuery, state: FSMContext):
    button = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='Оставить старое',
                                                                                     callback_data="Get_old")]])
    await call.message.answer('Введите новую дату начала проекта или нажмите "Оставить старое"',
                              reply_markup=button)
    await state.set_state(OrderUpdateProject.getDateStart)


@router.message(StateFilter(OrderUpdateProject.getDateStart))
async def get_ur_name(message: types.Message, state: FSMContext):
    await state.update_data(new_date_start_name=message.text)
    button = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='Оставить старое',
                                                                                     callback_data="Get_old")]])
    await message.answer('Введите новую дату конца проекта или нажмите "Оставить старое"',
                         reply_markup=button)
    await state.set_state(OrderUpdateProject.getComment)


@router.callback_query(StateFilter(OrderUpdateProject.getDateStart))
async def get_new(call: types.CallbackQuery, state: FSMContext):
    button = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='Оставить старое',
                                                                                     callback_data="Get_old")]])
    await call.message.answer('Введите новую дату конца проекта или нажмите "Оставить старое"',
                              reply_markup=button)
    await state.set_state(OrderUpdateProject.getComment)


@router.message(StateFilter(OrderUpdateProject.getComment))
async def get_ur_name(message: types.Message, state: FSMContext):
    await state.update_data(new_date_end_name=message.text)
    button = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='Оставить старое',
                                                                                     callback_data="Get_old")]])
    await message.answer('Введите новый комментарий или нажмите "Оставить старое"',
                         reply_markup=button)
    await state.set_state(OrderUpdateProject.END)


@router.callback_query(StateFilter(OrderUpdateProject.getComment))
async def get_new(call: types.CallbackQuery, state: FSMContext):
    button = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='Оставить старое',
                                                                                     callback_data="Get_old")]])
    await call.message.answer('Введите новый комментарий или нажмите "Оставить старое"',
                              reply_markup=button)
    await state.set_state(OrderUpdateProject.END)


@router.message(StateFilter(OrderUpdateProject.END))
async def get_ur_name(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    cur.execute(
        f"""UPDATE project SET Project_name='{user_data['new_project_name']}',Project_date_start='{user_data['new_date_start_name']}',
            Project_date_end='{user_data['new_date_end_name']}',Project_comment='{user_data['new_comment_name']}' where ID_project={int(user_data['project_id'])}""")
    conn.commit()
    button = admin_update_buttons()
    await message.answer('Данные обновлены')
    await message.answer('Выберете необходимое действие',
                         reply_markup=button)
    await state.set_state(None)


@router.callback_query(StateFilter(OrderUpdateProject.END))
async def get_new(call: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    cur.execute(
        f"""UPDATE project SET Project_name='{user_data['new_project_name']}',Project_date_start='{user_data['new_date_start_name']}',
        Project_date_end='{user_data['new_date_end_name']}',Project_comment='{user_data['new_comment_name']}' 
        where ID_project={int(user_data['project_id'])}""")
    conn.commit()
    button = admin_update_buttons()
    await call.message.answer('Данные обновлены')
    await call.message.answer('Выберете необходимое действие',
                              reply_markup=button)
    await state.set_state(None)
