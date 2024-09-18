from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
import psycopg2
from aiogram import F
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter
from DB_admin_add.add_functions import add_contragent



conn = psycopg2.connect(dbname='test', user='postgres', password='leolab12', host='127.0.0.1')
cur = conn.cursor()

router = Router()


class OrderPlace(StatesGroup):
    Sale_name = State()
    Ur_name = State()
    Date_of_document = State()
    Comment = State()
    END = State()

@router.message(StateFilter(None), Command('add_contragent'))
async def add_place(message: types.Message, state: FSMContext):
    await message.answer("Введите торговое название контрагента")
    await state.set_state(OrderPlace.Sale_name)

@router.callback_query(StateFilter(None), F.data=='Get_contragent')
async def add_place(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Введите торговое название контрагента")
    await state.set_state(OrderPlace.Sale_name)


@router.message(StateFilter(OrderPlace.Sale_name))
async def add_place(message: types.Message, state: FSMContext):
    await state.update_data(Sale=message.text.capitalize())
    await message.answer("Введите юридическое название")
    await state.set_state(OrderPlace.Ur_name)


@router.message(StateFilter(OrderPlace.Ur_name))
async def add_place(message: types.Message, state: FSMContext):
    await state.update_data(ur_name=message.text)
    await message.answer("Введите дату оформления договора с контрагентом")
    await state.set_state(OrderPlace.Date_of_document)


@router.message(StateFilter(OrderPlace.Date_of_document))
async def add_place(message: types.Message, state: FSMContext):
    await state.update_data(date_of_document=message.text)
    await message.answer("Комментарий")
    await state.set_state(OrderPlace.Comment)


@router.message(StateFilter(OrderPlace.Comment))
async def add_place(message: types.Message, state: FSMContext):
    await state.update_data(comment=message.text.capitalize())
    user_data = await state.get_data()
    buttons = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text='Добавить в базу данных', callback_data="Contragent_add")],
        [types.InlineKeyboardButton(text='Изменить', callback_data="Contragent_change")]

    ])
    await message.answer(f"""Вы ввели
Торговое название:   {user_data['Sale']}
Юридическое:   {user_data['ur_name']}
Дата оформления договора с контрагентом:   {user_data['date_of_document']}
Комментарий:   {user_data['comment']}
""",reply_markup=buttons)
    await state.set_state(OrderPlace.END)


@router.callback_query(OrderPlace.END, F.data == 'Contragent_change')
async def add_place(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Введите торговое название контрагента")
    await state.set_state(OrderPlace.Sale_name)

@router.callback_query(OrderPlace.END,F.data=='Contragent_add')
async def add_place(call: types.CallbackQuery, state: FSMContext):
    print(await state.get_data())
    cur.execute(add_contragent(await state.get_data()))
    conn.commit()
    await call.message.answer("Данные добавлены")
    await state.set_state(None)