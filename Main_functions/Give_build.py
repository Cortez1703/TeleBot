from DB.DB_connection import connection


cur, conn = connection()

from aiogram import Router, F, types

from aiogram.fsm.state import StatesGroup, State

from Buttons.buttons import Start_menu_buttons


class OrderGiveInventory(StatesGroup):
    GiveName = State()
    GiveInventory = State()
    GiveAmount = State()


router = Router()


@router.callback_query(F.data == 'Give_build')
async def get_build(call: types.CallbackQuery):
    buttons = Start_menu_buttons()
    await call.message.answer("Эта кнопка еще не работает")
    await call.message.answer("Выберете необходимое действие",reply_markup=buttons)