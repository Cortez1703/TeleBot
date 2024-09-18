from DB.DB_connection import connection
from DB_admin_add import get_functions
from DB_admin_add.get_functions import full_inventory_info

from Buttons.buttons import Start_menu_buttons

cur, conn = connection()

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter

router = Router()


class OrderInfoInventory(StatesGroup):
    InfoName = State()



@router.callback_query(StateFilter(None), F.data == 'Info_inventory')
async def get_inventory(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(message_id=call.message.message_id)
    await state.update_data(chat_id=call.message.chat.id)
    user_data = await state.get_data()
    await call.message.bot.delete_message(chat_id=user_data['chat_id'], message_id=user_data['message_id'])
    await state.set_state(OrderInfoInventory.InfoName)
    await call.message.answer('Введите часть или полное название инвентаря, информацию о котором хотите получить')


@router.message(StateFilter(OrderInfoInventory.InfoName))
async def give_inventory(message: types.Message, state: FSMContext):
    await state.update_data(message_id=message.message_id)
    await state.update_data(chat_id=message.chat.id)
    user_data = await state.get_data()
    await message.bot.delete_message(chat_id=user_data['chat_id'], message_id=user_data['message_id'])
    list_of_classes_objects = [i[0] for i in set(get_functions.get_inventory_name_regexp(message.text,cur))]
    buttons = [[types.InlineKeyboardButton(text=f'{str(i)}', callback_data=f'{str(i)}')] for i in
               list_of_classes_objects]
    buttons = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    buttons_2 = types.InlineKeyboardMarkup(inline_keyboard=[[
        types.InlineKeyboardButton(text='Отменить поиск', callback_data='Start_menu')]])
    await message.answer(f'Вот, что удалось найти:', reply_markup=buttons)
    await message.answer(f'''Если найти нужный предмет не удалось, введите новое название или отмените поиск
    ''', reply_markup=buttons_2)
    await state.set_state(OrderInfoInventory.InfoName)


@router.callback_query(StateFilter(OrderInfoInventory.InfoName))
async def get_info(call: types.CallbackQuery, state: FSMContext):
    cur.execute(f"Select * from inventory where Inventory_name='{call.data}'")
    info = full_inventory_info(cur.fetchall())
    print(info)
    buttons = Start_menu_buttons()
    await call.message.answer(f'{info}\n')
    await call.message.answer(f'Выберете необходимое действие', reply_markup=buttons)
    await state.set_state(None)
