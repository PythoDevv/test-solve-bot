from aiogram import types

from data.config import ADMINS
from loader import dp, db


@dp.message_handler(text="dropppp_users")
async def drop_users(message: types.Message):
    await db.drop_users()
    await db.create_table_users()
    await message.answer('Done ✅')


@dp.message_handler(text="dropppp_elements")
async def dropppp_elements(message: types.Message):
    await db.drop_elements()
    await db.create_table_chanel_element()
    await message.answer('Done ✅')


@dp.message_handler(text="dropppp_req")
async def drop_req(message: types.Message):
    await db.drop_requested_users()
    await db.create_table_requested_users()
    await message.answer('Done ✅')


@dp.message_handler(text="dropppp_req_ch")
async def drop_ch(message: types.Message):
    await db.drop_req_j_Chanel()
    await db.create_table_request_join_chanel()
    await message.answer('Done ✅')

@dp.message_handler(text="dropppp_users_numbers")
async def drop_users(message: types.Message):
    await db.drop_users_number()
    await db.create_table_user_number()
    await message.answer('Done drop numbers ✅')
