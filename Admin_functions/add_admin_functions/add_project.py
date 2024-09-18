from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
import psycopg2
from aiogram import F
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter
from DB_admin_add.add_functions import add_project




conn = psycopg2.connect(dbname='test', user='postgres', password='leolab12', host='127.0.0.1')
cur = conn.cursor()

router = Router()


class OrderProject(StatesGroup):
    Project_name = State()
    Project_start_work_date = State()
    Project_end_work_date = State()
    Project_comment = State()
    END = State()
    Add = State()
    Change = State()

@router.message(StateFilter(None), Command('add_project'))
async def add_place(message: types.Message, state: FSMContext):
    await message.answer("Введите название проекта")
    await state.set_state(OrderProject.Project_name)

@router.callback_query(StateFilter(None), F.data=='Get_project')
async def add_place(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Введите название подпроекта")
    await state.set_state(OrderProject.Project_name)


@router.message(StateFilter(OrderProject.Project_name))
async def add_place(message: types.Message, state: FSMContext):
    await state.update_data(project_name=message.text.capitalize())
    await message.answer("Введите дату начала работы над проектом")
    await state.set_state(OrderProject.Project_start_work_date)


@router.message(StateFilter(OrderProject.Project_start_work_date))
async def add_place(message: types.Message, state: FSMContext):
    await state.update_data(project_start_work_date=message.text)
    await message.answer("Введите дату конца работы над проектом")
    await state.set_state(OrderProject.Project_comment)


@router.message(StateFilter(OrderProject.Project_comment))
async def add_place(message: types.Message, state: FSMContext):
    await state.update_data(project_end_work_date=message.text.capitalize())
    await message.answer("Введите комментарий к проекту")
    await state.set_state(OrderProject.END)


@router.message(StateFilter(OrderProject.END))
async def add_place(message: types.Message, state: FSMContext):
    await state.update_data(project_comment=message.text.capitalize())
    user_data = await state.get_data()
    buttons = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text='Добавить в базу данных', callback_data="Project_add")],
        [types.InlineKeyboardButton(text='Изменить', callback_data="Project_change")]

    ])
    await message.answer(f"""Вы ввели
    Название проекта: {user_data['project_name']}
    Начало работы над проектом: {user_data['project_start_work_date']}
    Окончание работ над проектом: {user_data['project_end_work_date']}
    Комментарии: {user_data['project_comment']}
    """, reply_markup=buttons)
    await state.set_state(OrderProject.Add)


@router.callback_query(OrderProject.Add, F.data == 'Project_change')
async def add_place(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Введите название прроекта")
    await state.set_state(OrderProject.Project_name)


@router.callback_query(OrderProject.Add, F.data == 'Project_add')
async def add_place(call: types.CallbackQuery, state: FSMContext):
    print(await state.get_data())
    cur.execute(add_project(await state.get_data()))

    conn.commit()
    await call.message.answer("Данные добавлены")
    await state.set_state(None)
