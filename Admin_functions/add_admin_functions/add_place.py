from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
import psycopg2
from aiogram import F
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter
from DB_admin_add.add_functions import add_placE


conn = psycopg2.connect(dbname='test', user='postgres', password='leolab12', host='127.0.0.1')
cur = conn.cursor()

router = Router()


class OrderPlace(StatesGroup):
    first_level = State()
    second_level = State()
    third_level = State()
    last_level = State()
    END = State()

@router.message(StateFilter(None), Command('add_place'))
async def add_place(message: types.Message, state: FSMContext):
    await message.answer("Введите комнату помещения")
    await state.set_state(OrderPlace.first_level)

@router.callback_query(StateFilter(None), F.data=='Get_place')
async def add_place(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Введите комнату помещения")
    await state.set_state(OrderPlace.first_level)



@router.message(StateFilter(OrderPlace.first_level))
async def add_place(message: types.Message, state: FSMContext):
    await state.update_data(first_level=message.text.capitalize())
    await message.answer("Введите стол/стеллаж")
    await state.set_state(OrderPlace.second_level)


@router.message(StateFilter(OrderPlace.second_level))
async def add_place(message: types.Message, state: FSMContext):
    await state.update_data(second_level=message.text.capitalize())
    await message.answer("Введите ряд (целое число)")
    await state.set_state(OrderPlace.third_level)


@router.message(StateFilter(OrderPlace.third_level))
async def add_place(message: types.Message, state: FSMContext):
    await state.update_data(third_level=message.text.capitalize())
    await message.answer("Введите полку (целое число)")
    await state.set_state(OrderPlace.last_level)


@router.message(StateFilter(OrderPlace.last_level))
async def add_place(message: types.Message, state: FSMContext):
    await state.update_data(last_level=message.text.capitalize())
    user_data = await state.get_data()
    buttons = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text='Добавить в базу данных', callback_data="Place_add")],
        [types.InlineKeyboardButton(text='Изменить', callback_data="Place_change")]

    ])
    await message.answer(f"""Вы ввели
Комната:   {user_data['first_level']}
Стол:   {user_data['second_level']}
Ряд:   {user_data['third_level']}
Полка:   {user_data['last_level']}
""",reply_markup=buttons)
    await state.set_state(OrderPlace.END)


@router.callback_query(OrderPlace.END, F.data == 'Place_change')
async def add_place(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Введите комнату помещения")
    await state.set_state(OrderPlace.first_level)

@router.callback_query(OrderPlace.END,F.data=='Place_add')
async def add_place(call: types.CallbackQuery, state: FSMContext):
    print(await state.get_data())
    cur.execute(add_placE(await state.get_data()))
    conn.commit()
    await call.message.answer("Данные добавлены")
    await state.set_state(None)