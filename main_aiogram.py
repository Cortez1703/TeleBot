import logging
from aiogram import Bot, Dispatcher
import asyncio
from Start_menu_handlers import Menu_handlers

from DB.DB_connection import connection
from Admin_functions.add_admin_functions import add_person, add_project, add_place, add_inventory, add_contagent
from Main_functions import Get_inventory, Give_inventory, Info_inventory, Get_build, Give_build, Info_build
from Admin_functions.Info_admin_functions import info_contragent
from Admin_functions.update_admin_functions import update_contragent,update_project,update_subproject

logging.basicConfig(level=logging.INFO)
bot = Bot('TOKEN')
dp = Dispatcher()

a = {}

cur, conn = connection()


async def main():
    dp.include_router(Menu_handlers.router)
    dp.include_router(add_person.router)
    dp.include_router(add_place.router)
    dp.include_router(add_contagent.router)
    dp.include_router(add_inventory.router)
    dp.include_router(add_project.router)
    dp.include_router(Get_inventory.router)
    dp.include_router(Give_inventory.router)
    dp.include_router(Info_inventory.router)
    dp.include_router(Get_build.router)
    dp.include_router(Give_build.router)
    dp.include_router(Info_build.router)
    dp.include_router(info_contragent.router)
    dp.include_router(update_contragent.router)
    dp.include_router(update_project.router)
    dp.include_router(update_subproject.router)
    await dp.start_polling(bot, cur=cur, conn=conn)


if __name__ == "__main__":
    asyncio.run(main())
