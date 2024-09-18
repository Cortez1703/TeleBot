from aiogram import types, Router
from aiogram.filters.command import Command

from aiogram import F
import logging
from DB.DB_connection import connection
from aiogram.fsm.context import FSMContext

logging.basicConfig(level=logging.INFO)
from Buttons.buttons import Start_menu_buttons, admin_main_buttons, admin_add_buttons, admin_info_buttons, \
    admin_update_buttons

router = Router()
user = dict(())


@router.message(Command('start'))
async def start_menu(message: types.Message, state: FSMContext):
    await state.set_state(None)
    buttons = Start_menu_buttons()
    cur, conn = connection()
    user['id'] = message.from_user.id

    buttons_new_person = [[types.InlineKeyboardButton(text="Создать юзера", callback_data="Add_user")]]
    buttons_new_person = types.InlineKeyboardMarkup(inline_keyboard=buttons_new_person)
    cur.execute(f"""Select Person_name from persons where Person_tg_id='{user["id"]}'""")

    if cur.fetchall():
        await message.answer('Выберете необходимое действие', reply_markup=buttons)
    else:
        await message.answer(
            'Привет! Твоего аккаунта нет в базе данных пользователей, давай создадим нового пользователя',
            reply_markup=buttons_new_person)


@router.callback_query(F.data == 'Start_menu')
async def start_menu(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(None)
    buttons = Start_menu_buttons()

    await call.message.answer('Выберете необходимое действие', reply_markup=buttons)


@router.callback_query(F.data == 'Admin_main')
async def get_build(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(None)
    buttons = admin_main_buttons()
    await call.message.answer("Выберете необходимое действие", reply_markup=buttons)


@router.callback_query(F.data == 'Admin_add')
async def get_build(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(None)
    buttons = admin_add_buttons()
    await call.message.answer("Выберете необходимое действие", reply_markup=buttons)


@router.callback_query(F.data == 'Admin_info')
async def get_build(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(None)
    buttons = admin_info_buttons()
    await call.message.answer("Выберете необходимое действие", reply_markup=buttons)


@router.callback_query(F.data == 'Admin_update')
async def get_build(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(None)
    buttons = admin_update_buttons()
    await call.message.answer("Выберете необходимое действие", reply_markup=buttons)
