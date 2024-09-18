from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter
from DB.DB_connection import connection
from Buttons.buttons import admin_info_buttons

cur, conn = connection()

router = Router()


@router.callback_query(F.data == 'Info_contragent')
async def info_contragent(call: types.CallbackQuery):
    cur.execute("""SELECT * FROM contragent""")

    buttons = admin_info_buttons()
    info = cur.fetchall()
    print(info)
    print(bool(info))
    if info:
        ans = ''
        for i in info:
            print(i)
            ans += f"""ID контрагента: {i[0]},
    Наименование контрагента: {i[1]},
    Юридическое название: {i[2]},
    Дата оформления договора: {i[3]},
    Комментарий: {i[4]} \n\n\n"""

        await call.message.answer(f"""{ans}""", reply_markup=buttons)
    else:
        await call.message.answer("На данный момент нет контрагентов в базе данных")
        await call.message.answer("Выберете необходимое действие", reply_markup=buttons)


@router.callback_query(F.data == 'Info_project')
async def info_contragent(call: types.CallbackQuery):
    cur.execute("""SELECT * FROM project""")
    ans = ''
    info = cur.fetchall()
    buttons = admin_info_buttons()
    if info:
        for i in info:
            ans += f"""ID проекта: {i[0]},
    Наименование проекта: {i[1]},
    Дата начала работ над проектом: {i[2]},
    Дата конца работ над проектом: {i[3]},
    Комментарий: {i[4]} \n\n\n"""

        await call.message.answer(f"""КУКУ 
        {ans}"""
                                  , reply_markup=buttons)
    else:
        await call.message.answer("На данный момент нет активных проектов")
        await call.message.answer("Выберете необходимое действие", reply_markup=buttons)


@router.callback_query(F.data == 'Info_subproject')
async def info_contragent(call: types.CallbackQuery):
    cur.execute("""SELECT * FROM subproject""")
    ans = ''
    info = cur.fetchall()
    buttons = admin_info_buttons()
    if info:
        for i in info:
            ans += f"""ID проекта: {i[0]},
        ID родительского проекта: {i[1]},
        Наименование подпроекта: {i[2]},
        Дата начала работ над проектом: {i[3]},
        Дата конца работ над проектом: {i[4]},
        Комментарий: {i[5]} \n\n\n"""

        await call.message.answer(f"{ans}", reply_markup=buttons)
    else:
        await call.message.answer("На данный момент нет активных подпроектом")
        await call.message.answer("Выберете необходимое действие", reply_markup=buttons)


@router.callback_query(F.data == 'Info_persons')
async def info_contragent(call: types.CallbackQuery):
    cur.execute("""SELECT * FROM persons""")
    ans = ''
    info = cur.fetchall()
    buttons = admin_info_buttons()
    if info:
        for i in info:
            cur.execute(f"""SELECT ID_place from place where Place_main='{i[2] + " " + i[1]}'""")
            ans += f"""ID пользователя: {i[0]},
        Имя пользователя: {i[1]},
        Фамилия пользователя: {i[2]},
        Отчество пользователя: {i[3]},
        Должность пользователя: {i[4]},
        ID места хранения пользователя: {cur.fetchall()[0][0]},
        Дата приёма на работу: {i[6]},
        Дата увольнения : {i[7]}\n\n\n"""

        await call.message.answer(f"{ans}", reply_markup=buttons)
    else:
        await call.message.answer("На данный момент нет активных пользователей")
        await call.message.answer("Выберете необходимое действие", reply_markup=buttons)
