import asyncio
from aiogram import executor

from loader import dp, db, bot
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await db.create()
    await db.create_table_tugma()
    await db.create_table_chanel()
    await db.create_table_admins()
    await db.create_table_users()
    await db.create_table_lessons()
    await db.create_table_buttons()
    await db.create_table_add_list()
    await db.create_table_one_time_link()
    await db.create_table_add_list_chanel()
    await db.create_table_chanel_element()
    await db.create_table_requested_users()
    await db.create_table_request_join_chanel()
    await db.create_table_user_number()
    await db.create_table_tests()
    await db.create_table_test_attempts()
    await set_default_commands(dispatcher)

    admins = await db.select_all_admins()
    try:
        if 935795577 == admins[0][1]:
            print('>>> qo`shilgan')
            print(f'>>> Hozirgi adminlar - {admins}')
    except Exception as err:
        print(err)
        await db.add_admin(telegram_id=935795577)

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)

    asyncio.create_task(check_users())


async def check_users():
    while True:
        users = await db.select_all_users()
        for user in users:
            try:
                await bot.send_chat_action(user[6], "typing")
                await db.update_user_status("active", user[6])
            except Exception as err:
                await db.update_user_status("block", user[6])
            await asyncio.sleep(0.04)
        await asyncio.sleep(86400)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
