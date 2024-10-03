from Buttons.buttons import Start_menu_buttons

from DB.DB_connection import connection
from DB_admin_add import get_functions
from DB_admin_add import add_functions
from DB_admin_add import update_functions

cur, conn = connection()
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter


class OrderGetInventory(StatesGroup):
    GetName = State()
    GetInventory = State()


router = Router()


@router.callback_query(StateFilter(None), F.data == 'Get_inventory')
async def get_name(call: types.CallbackQuery, state: FSMContext):
    """Стартовая функция для процесса взятия какого-либо объекта
    После её начала у пользователя 2 варианта:
    - Отменить поиск, нажав на кнопку
    - Ввести полное или часть названия.
    Если предмет найден - пользователю будет предложен набор inline-кнопок"""

    button_cancel = types.InlineKeyboardMarkup(
        inline_keyboard=[[types.InlineKeyboardButton(text="Отменить поиск", callback_data="Start_menu")]])
    await state.set_state(OrderGetInventory.GetName)
    await call.message.answer('Введите название инвентаря, который ищете', reply_markup=button_cancel)


@router.message(StateFilter(OrderGetInventory.GetName))
async def create_inventory_buttons(message: types.Message, state: FSMContext):
    """Создание inline-кнопок имеющегося оборудования.
    Для взятия какого-либо оборудования - нажать на соответствующее название"""

    list_of_classes_objects = [i[0] for i in set(get_functions.get_inventory_name_regexp(message.text, cur))]
    buttons = [[types.InlineKeyboardButton(text=f'{str(i)}', callback_data=f'{str(i)}')] for i in
               list_of_classes_objects]
    buttons.append([types.InlineKeyboardButton(text="Отменить поиск", callback_data="Start_menu")])
    buttons = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer(f'Выберете нужный предмет или введите новое название', reply_markup=buttons)
    await state.set_state(OrderGetInventory.GetName)


@router.callback_query(StateFilter(OrderGetInventory.GetName))
async def get_inventory(call: types.CallbackQuery, state: FSMContext):
    """Вывод информации по местоположению и количеству инвентаря.
    В ответ нужно отправить количество инвентаря, которой берете"""

    button_cancel = types.InlineKeyboardMarkup(
        inline_keyboard=[[types.InlineKeyboardButton(text="Отменить поиск", callback_data="Start_menu")]])
    await state.update_data(inventory_name=f'{call.data}')
    # Вывод нужной информации по объекту
    inventory_info = get_functions.get_inventory_id_amount_place(call.data, cur)
    # Вывод местоположения объекта (Место-стол/стеллаж-ряд-полка) по найденному ID_place
    inventory_place = get_functions.get_all_from_place(inventory_info[0][2], cur)
    await state.update_data(id_inventory=f'{inventory_info[0][0]}')
    await state.update_data(id_place=f'{inventory_place[0][0]}')

    await call.message.answer(f"""{call.data} находится в следующем месте:
Комната или сотрудник: {inventory_place[0][1]},
Стол/стеллаж: {inventory_place[0][2]},
Ряд: {inventory_place[0][3]},
Полка: {inventory_place[0][4]}.\n
Количество: {inventory_info[0][1]}
Сколько берете?""", reply_markup=button_cancel)
    await state.set_state(OrderGetInventory.GetInventory)


@router.message(StateFilter(OrderGetInventory.GetInventory))
async def get_amount(message: types.Message, state: FSMContext):
    """Обработка введенного числа оборудования на взятие.
    Проверка на правильность введенных данных"""

    inventory_info = await state.get_data()
    place_class = tuple([i[0] for i in get_functions.get_place_class()])
    Inventory_ID, Inventory_amount = get_functions.get_inventory_id_amount(cur, inventory_info['inventory_name'],
                                                                           place_class)[0]
    button_cancel = types.InlineKeyboardMarkup(
        inline_keyboard=[[types.InlineKeyboardButton(text='Отменить ввод', callback_data='Start_menu')]])
    try:

        new_inventory_info = [i for i in get_functions.get_inventory_full(inventory_info['inventory_name'], cur)[0]]

        user_name_surname = get_functions.get_user_place(cur, message.from_user.id)[0]
        print(1)
        user_place_id = get_functions.get_place_main(cur, get_functions.concatinate(user_name_surname))[0]

        if len(user_place_id) < 2:
            user_place_id = user_place_id[0]
        # Замена в массиве данных по инвентарю позиций ID_place(часть инвентаря теперь у пользователя) и Amount
        new_inventory_info[5] = user_place_id
        new_inventory_info[6] = int(message.text)
        new_inventory_info.pop(0)
        user_get_amount = message.text
        if int(user_get_amount) <= 0:
            if int(user_get_amount) < 0:
                await message.answer("""Вы ввели отрицательное число. Пожалуйста, введите корректное число 
или нажмите 'Отменить ввод'""", reply_markup=button_cancel)
            else:
                await message.answer("""Вы ввели 0. Пожалуйста, введите корректное число 
или нажмите 'Отменить ввод'""", reply_markup=button_cancel)


        elif int(user_get_amount) <= int(Inventory_amount):
            # Обновления данных по объекту. Изменяется количество инвентаря на полке
            update_functions.update_inventory_main_minus(cur, conn, Inventory_amount, user_get_amount,
                                                         inventory_info['inventory_name'], Inventory_ID)
            user_id = get_functions.get_user_id(cur, message.from_user.id)[0][0]

            # Поиск в таблице строки данных, которая относится к данному пользователю
            person_exists_info = get_functions.get_inventory_id_amount(cur, inventory_info['inventory_name'],
                                                                       user_place_id)
            print(person_exists_info)
            # Проверка на наличия данных
            # Если предмет уже брался человеком, добавление новых взятых объектов.Если нет - создание новой ячейки данных

            if person_exists_info:

                update_functions.update_inventory_person_plus(cur, conn, person_exists_info[0][1], user_get_amount,
                                                              person_exists_info[0][0])
            else:
                print(new_inventory_info)
                add_functions.add_inventory_2(cur, conn, new_inventory_info)
                print(1)
            event_list = [inventory_info['id_inventory'], user_id, user_place_id, 'Забрал', message.text]

            add_functions.add_inventory_event(event_list, cur, conn)

            buttons = Start_menu_buttons()

            await message.answer(f'''Вы забрали {inventory_info['inventory_name']} в количестве {message.text}
Осталось {int(Inventory_amount) - int(message.text)}''', reply_markup=buttons)
            await state.set_state(None)
            conn.commit()
        else:
            await message.answer(
                '''Введено количество, превышающее то, что записано в базе. Повторите выбор пожалуйста, 
или нажмите кнопку "Отменить ввод"''',
                reply_markup=button_cancel)
    except Exception as e:
        print(e)
        await message.answer("Введены некорректные данные, повторите выбор пожалуйста")
