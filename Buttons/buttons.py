"""Блок функций, который возращают типовые значения кнопок
Используется для уменьшение количества строк кода в других файлах"""

from aiogram import types


def Start_menu_buttons():
    button_get_inventory = types.InlineKeyboardButton(text='Взять инвентарь', callback_data='Get_inventory')
    button_give_inventory = types.InlineKeyboardButton(text='Положить инвентарь', callback_data='Give_inventory')
    button_info_inventory = types.InlineKeyboardButton(text='Информация по инвентарю', callback_data='Info_inventory')

    button_get_build = types.InlineKeyboardButton(text='Взять деталь', callback_data='Get_build')
    button_give_build = types.InlineKeyboardButton(text='Положить деталь', callback_data='Give_build')
    button_info_build = types.InlineKeyboardButton(text='Информация по детали', callback_data='Info_build')

    button_admin = types.InlineKeyboardButton(text='Панель администратора', callback_data='Admin_main')
    buttons = [
        [button_get_inventory, button_get_build],
        [button_give_inventory, button_give_build],
        [button_info_inventory, button_info_build],
        [button_admin]
    ]
    a = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return a


def admin_main_buttons():
    button_give_object = types.InlineKeyboardButton(text='Добавить информацию по чему-либо', callback_data='Admin_add')
    button_get_info = types.InlineKeyboardButton(text='Получить информацию по чему-либо', callback_data='Admin_info')
    button_update_info = types.InlineKeyboardButton(text='Обновить данные по чему-либо', callback_data='Admin_update')
    button_cancel = types.InlineKeyboardButton(text='Вернуться на главное меню', callback_data='Start_menu')

    buttons = types.InlineKeyboardMarkup(
        inline_keyboard=[[button_give_object, button_get_info], [button_update_info], [button_cancel]])
    return buttons


def admin_add_buttons():
    button_get_contragent = types.InlineKeyboardButton(text='Добавить контрагента', callback_data='Get_contragent')
    button_get_project = types.InlineKeyboardButton(text='Добавить проект', callback_data='Get_project')
    button_get_subproject = types.InlineKeyboardButton(text='Добавить подпроект', callback_data='Get_subproject')
    button_get_place = types.InlineKeyboardButton(text='Добавить место хранения', callback_data='Get_Place')
    button_cancel = types.InlineKeyboardButton(text='Вернуться назад', callback_data='Start_menu')

    buttons = types.InlineKeyboardMarkup(inline_keyboard=[
        [button_get_contragent, button_get_project],
        [button_get_subproject, button_get_place],
        [button_cancel]
    ])
    return buttons


def admin_info_buttons():
    button_info_contragent = types.InlineKeyboardButton(text='Информация по всем контрагентам',
                                                        callback_data='Info_contragent')
    button_info_project = types.InlineKeyboardButton(text='Информация по всем проектам', callback_data='Info_project')
    button_info_subproject = types.InlineKeyboardButton(text='Информация по всем подпроектам',
                                                        callback_data='Info_subproject')
    button_info_place = types.InlineKeyboardButton(text='Информация по местам хранения', callback_data='Info_Place')
    button_info_persons = types.InlineKeyboardButton(text='Информация по пользователям', callback_data='Info_persons')
    button_back = types.InlineKeyboardButton(text='Вернуться назад', callback_data='Admin_main')
    button_cancel = types.InlineKeyboardButton(text='Вернуться на главное меню', callback_data='Start_menu')

    buttons = types.InlineKeyboardMarkup(inline_keyboard=[
        [button_info_contragent, button_info_project],
        [button_info_subproject, button_info_place],
        [button_info_persons],
        [button_back],
        [button_cancel]
    ])
    return buttons


def admin_update_buttons():
    button_update_contragent = types.InlineKeyboardButton(text='Обновить информацию по всем контрагентам',
                                                          callback_data='Update_contragent')
    button_update_project = types.InlineKeyboardButton(text='Обновить информацию по всем проектам',
                                                       callback_data='Update_project')
    button_update_subproject = types.InlineKeyboardButton(text='Обновить информацию по всем подпроектам',
                                                          callback_data='Update_subproject')
    button_update_persons = types.InlineKeyboardButton(text='Информация по пользователям',
                                                       callback_data='Update_persons')
    button_back = types.InlineKeyboardButton(text='Вернуться назад', callback_data='Admin_main')
    button_cancel = types.InlineKeyboardButton(text='Вернуться на главное меню', callback_data='Start_menu')

    buttons = types.InlineKeyboardMarkup(inline_keyboard=[
        [button_update_contragent],
        [button_update_project],
        [button_update_subproject],
        [button_update_persons],
        [button_back],
        [button_cancel]
    ])
    return buttons
