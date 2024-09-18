from aiogram import types, Router, F


from aiogram.fsm.context import FSMContext
from DB.DB_connection import connection
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter
from DB_admin_add import add_functions
router = Router()


class UserAdd(StatesGroup):
    userName = State()
    userSurname = State()
    userThirdname = State()
    userPosition = State()
    userStartWork = State()
    userEndWork = State()
    userAdd = State()


@router.callback_query(StateFilter(None), F.data == 'Add_user')
async def get_user_name(call: types.CallbackQuery, state: FSMContext):
    print()
    await call.message.answer("Введите ваше имя")
    await state.set_state(UserAdd.userName)


@router.message(UserAdd.userName)
async def get_user_surname(message: types.Message, state: FSMContext):
    await state.update_data(user_name=message.text.capitalize())
    await state.update_data(user_tg_id=message.from_user.id)
    await message.answer("Введите вашу фамилию")
    await state.set_state(UserAdd.userSurname)


@router.message(UserAdd.userSurname)
async def get_user_Thirdname(message: types.Message, state: FSMContext):
    await state.update_data(user_surname=message.text.capitalize())
    await message.answer("Введите ваше отчество")
    await state.set_state(UserAdd.userThirdname)


@router.message(UserAdd.userThirdname)
async def get_user_position(message: types.Message, state: FSMContext):
    await state.update_data(user_thirdname=message.text.capitalize())
    await message.answer("Введите вашу должность")
    await state.set_state(UserAdd.userPosition)


@router.message(UserAdd.userPosition)
async def get_user_startwork(message: types.Message, state: FSMContext):
    await state.update_data(user_position=message.text.capitalize())
    await message.answer("Введите дату начала вашей работы в формате ДД.ММ.ГГГГ")
    await state.set_state(UserAdd.userStartWork)


@router.message(UserAdd.userStartWork)
async def get_user_endwork(message: types.Message, state: FSMContext):
    await state.update_data(user_startwork=message.text.capitalize())
    await message.answer("Введите дату конца вашей работы в формате ДД.ММ.ГГГГ(Если вы работает, введите -")
    await state.set_state(UserAdd.userEndWork)


@router.message(UserAdd.userEndWork)
async def add_user(message: types.Message, state: FSMContext):
    await state.update_data(user_endwork=message.text.capitalize())
    user_data = await state.get_data()
    buttons = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text='Добавить в базу данных', callback_data="User_Added")]

    ])
    await message.answer(f"""Вы ввели
    Имя: {user_data['user_name']}
    Фамилия:{user_data['user_surname']}
    Отчество:{user_data['user_thirdname']}
    Должность:{user_data['user_position']}
    Начало работы:{user_data['user_startwork']}
    Конец работы:{user_data['user_endwork']}""", reply_markup=buttons)
    await state.set_state(UserAdd.userAdd)


@router.callback_query(UserAdd.userAdd, F.data == 'User_Added')
async def go_to_start_menu(call: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    cur, conn = connection()
    cur.execute(f"""INSERT INTO persons (
                Person_name ,
                Person_surname ,
                Person_thirdname ,
                Person_position ,
                Person_tg_id ,
                Date_of_start_work ,
                Date_of_end_work ) VALUES ('{user_data['user_name']}','{user_data['user_surname']}',
'{user_data['user_thirdname']}','{user_data['user_position']}','{call.from_user.id}',
'{user_data['user_startwork']}','{user_data['user_endwork']}')""")
    user_name = user_data['user_surname']+' '+user_data['user_name']
    cur.execute(add_functions.add_place_user(user_name))
    buttons = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text='Перейти к работе', callback_data="Start_menu")]

    ])
    conn.commit()
    cur.close()
    conn.close()
    await call.message.answer(text=f'Данные добавлены', reply_markup=buttons)
    await state.set_state(None)
