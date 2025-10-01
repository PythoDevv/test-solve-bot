from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.default.rekKeyboards import admin_key_2, back
from loader import db, dp
from states.rekStates import RekData


@dp.message_handler(commands=["admin2"], user_id=ADMINS)
async def admin(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer(text="Admin panel", reply_markup=admin_key_2)


@dp.message_handler(text="Add List Kanal ➕")
async def add_channel(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer(
            text="Add List uchun Kanalni kiriting\n\n" 'Masalan : "@Chanel Ko`rinishida', reply_markup=back
        )
        await RekData.add_list_plus_channel.set()


@dp.message_handler(state=RekData.add_list_plus_channel)
async def add_username(message: types.Message, state: FSMContext):
    text = message.text
    if text[0] == "@":

        await db.add_channel_for_add_list(url=message.text)
        await message.answer("Qo'shildi", reply_markup=admin_key_2)
        await state.finish()
    elif text == "🔙️ Orqaga":
        await message.answer("Admin panel", reply_markup=admin_key_2)
        await state.finish()

    else:
        await message.answer(
            "Xato\n\n" "@ belgi bilan yoki kanal id(-11001835334270andLink) sini link bilan birga kiriting kiriting"
        )


@dp.message_handler(text="Add List Kanal ➖")
async def add_channel(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer(text="Kanalni kiriting @ belgi bilan\n\n" "Masalan : @username\n\n", reply_markup=back)
        await RekData.add_list_minus_channel.set()


@dp.message_handler(state=RekData.add_list_minus_channel)
async def del_username(message: types.Message, state: FSMContext):
    text = message.text
    if text[0] == "@":
        chanel = await db.get_add_list_chanel(url=f"{text}")
        if not chanel:
            await message.answer("Kanal topilmadi\n" "Qaytadan urinib ko'ring")

        else:
            await db.delete_add_list_channel(url=text)
            await message.answer('Kanal o"chirildi', reply_markup=admin_key_2)
            await state.finish()
    elif text == "🔙️ Orqaga":
        await message.answer("Admin panel", reply_markup=admin_key_2)
        await state.finish()


@dp.message_handler(text="Add List ➕", user_id=ADMINS)
async def add_channel(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer(
            text="Add List ni kiriting\n\n" 'Masalan : "https://t.me/+QweRew2112WE@# Ko`rinishida', reply_markup=back
        )
        await RekData.add_list_plus.set()


@dp.message_handler(state=RekData.add_list_plus)
async def add_add_list_db(message: types.Message, state: FSMContext):
    text = message.text
    if text[:13] == "https://t.me/":
        add_list = text.split("&&&")
        await db.add_add_list(url=add_list[0], button_name=add_list[1])
        await message.answer("Qo'shildi", reply_markup=admin_key_2)
        await state.finish()
    elif text == "🔙️ Orqaga":
        await message.answer("Admin panel", reply_markup=admin_key_2)
        await state.finish()

    else:
        await message.answer("Xato\n\n" "https://t.me/ bilan kiriting")


@dp.message_handler(text="Add List ➖", user_id=ADMINS)
async def del_add_list(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer(
            text="Add List Url ni kiriting\n\n" "Masalan : https://t.me/+QweRew2112WE@#\n\n", reply_markup=back
        )
        await RekData.add_list_minus.set()


@dp.message_handler(state=RekData.add_list_minus)
async def del_add_list_db(message: types.Message, state: FSMContext):
    text = message.text
    if text[:13] == "https://t.me/":
        chanel = await db.get_add_list(url=f"{text}")
        if not chanel:
            await message.answer("Kanal topilmadi\n" "Qaytadan urinib ko'ring")

        else:
            await db.delete_add_list(url=text)
            await message.answer('Kanal o"chirildi', reply_markup=admin_key_2)
            await state.finish()
    elif text == "🔙️ Orqaga":
        await message.answer("Admin panel", reply_markup=admin_key_2)
        await state.finish()


@dp.message_handler(text="Add List 📈")
async def channels(message: types.Message):
    channels = await db.select_add_list()
    text = ""
    for channel in channels:
        text += f"{channel['url']}\n"
    try:
        await message.answer(f"{text}", reply_markup=admin_key_2)
    except:
        await message.answer(f"Add List mavjud emas")


@dp.message_handler(text="Add List Kanallar 📈")
async def channels(message: types.Message):
    channels = await db.select_chanel_add_list()
    text = ""
    for channel in channels:
        text += f"{channel['url']}\n"
    try:
        await message.answer(f"{text}", reply_markup=admin_key_2)
    except:
        await message.answer(f"Kanallar mavjud emas")
