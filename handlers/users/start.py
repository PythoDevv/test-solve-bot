import asyncio
import json
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import bot, dp, db
from states.rekStates import DelState
from utils.misc import subscription


@dp.message_handler(text='111')
async def delete_user_me2(message: types.Message):
    await db.delete_users(telegram_id=6610230337)
    await message.answer("Chopildi")

@dp.message_handler(text='222')
async def delete_user_me(message: types.Message):
    await db.delete_users(telegram_id=935795577)
    await message.answer("Chopildi")

@dp.message_handler(text='dell')
async def delete_user(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer('Id ni kiriting')
        await DelState.del_user.set()


@dp.message_handler(state=DelState.del_user)
async def del_user(message: types.Message, state: FSMContext):
    await db.delete_users(telegram_id=int(message.text))
    await message.answer("O'chirildi")
    await state.finish()


@dp.message_handler(text="🎗 Ballarim")
async def get_user_score(message: types.Message, state: FSMContext):
    try:
        user_score = await db.select_user(telegram_id=message.from_user.id)
        await message.answer(f'👤 Sizda {user_score["score"]} ball mavjud')
    except:
        await message.answer("Iltimos /start buyrug'ini bering")


@dp.callback_query_handler(text='link')
async def tanlov(call: types.CallbackQuery):
    # status = True
    # all = await db.select_chanel()
    # chanels = []
    # url = []
    # channel_names = []
    # # score = 0
    # # limit_require = 0
    # # elements = await db.get_elements()

    # # for element in elements:
    #     # score += element['limit_score']
    #     # limit_require += element['limit_require']

    # for i in all:
    #     chanels.append(i['chanelll'])
    #     url.append(i['url'])
    #     channel_names.append(i['channel_name'])

    # for channel in chanels:
    #     status *= await subscription.check(user_id=call.from_user.id,
    #                                        channel=f'{channel}')
    # if status:
    bot_username = (await bot.get_me()).username

    url_link = f'https://t.me/{bot_username}?start={call.from_user.id}'
    # text_link = f"<a href='{url_link}'>👉🏻 Havola ustiga bosing 👈🏻</a>"
    lessons = await db.select_related_lessons(button_name="Asosiy qism")
    share_button = InlineKeyboardMarkup(row_width=1)
    share_button.add(InlineKeyboardButton(text="🔥 Ishtirok etish 🔥", url=f"{url_link}"))
    if lessons:
        for i in lessons:
            if i[2] == 'video':
                await call.message.answer_video(video=f"{i[3]}", caption=f'{i[5]}\n{url_link}',
                                                reply_markup=share_button)
            elif i[2] == 'document':
                await call.message.answer_document(
                    document=f"{i[3]}", caption=f'{i[5]}\n{url_link}', reply_markup=share_button
                )
            elif i[2] == 'audio':
                await call.message.answer_audio(audio=f"{i[3]}", caption=f"{i[5]}\n{url_link}",
                                                reply_markup=share_button)
            elif i[2] == 'photo':
                await call.message.answer_photo(photo=f"{i[3]}", caption=f"{i[5]}\n{url_link}",
                                                reply_markup=share_button)
            elif i[2] == 'text':
                await call.message.answer(f"{i[5]}\n{url_link}", reply_markup=share_button)

    lessons_2 = await db.select_related_lessons(button_name="Asosiy qism 2")
    if lessons_2:
        for i in lessons_2:
            if i[2] == 'video':
                await call.message.answer_video(video=f"{i[3]}", caption=f'{i[5]}')
            elif i[2] == 'document':
                await call.message.answer_document(
                    document=f"{i[3]}", caption=f'{i[5]}'
                )
            elif i[2] == 'audio':
                await call.message.answer_audio(audio=f"{i[3]}", caption=f"{i[5]}")
            elif i[2] == 'photo':
                await call.message.answer_photo(photo=f"{i[3]}", caption=f"{i[5]}")
            elif i[2] == 'text':
                await call.message.answer(f"{i[5]}")

    # else:
    #     button = types.InlineKeyboardMarkup(row_width=1, )
    #     counter = 0
    #     for i in url:
    #         button.add(types.InlineKeyboardButton(f"{channel_names[counter]}", url=f'https://t.me/{i}'))
    #         counter += 1
    #     button.add(types.InlineKeyboardButton(text="✅ А'zo boʼldim", callback_data="check_subs"))


@dp.message_handler(Command('jsonFile'))
async def jsonnn(message: types.Message):
    user_list = []
    userss = await db.select_all_users()
    for user in userss:
        user_dict = {}
        user_dict['full_name'] = user[1]
        user_dict['username'] = user[2]
        user_dict['phone'] = user[3]
        user_dict['score'] = user[4]
        user_dict['tg_id'] = user[6]
        user_list.append(user_dict)
        await asyncio.sleep(0.05)
    with open("users.json", "w") as outfile:
        json.dump(user_list, outfile)
    document = open('users.json')
    await bot.send_document(message.from_user.id, document=document)


async def send_json():
    user_list = []
    userss = await db.select_all_users()
    for user in userss:
        user_dict = {}
        user_dict['full_name'] = user[1]
        user_dict['username'] = user[2]
        user_dict['phone'] = user[3]
        user_dict['score'] = user[4]
        user_dict['tg_id'] = user[6]
        user_list.append(user_dict)
        await asyncio.sleep(0.05)
    with open("users.json", "w") as outfile:
        json.dump(user_list, outfile)
    document = open('users.json')
    await bot.send_document(935795577, document=document)


@dp.message_handler(Command('read_file'))
async def json_reader(message: types.Message):
    f = open('users.json', 'r')
    data = json.loads(f.read())
    for user in data:
        try:
            await db.add_json_file_user(
                telegram_id=user['tg_id'],
                username=user['username'],
                full_name=user['full_name'],
                phone=user['phone'],
                score=user['score']
            )
        except Exception as e:
            print(e)
    f.close()

# @dp.message_handler(text="Excel File")
# async def marathon(message: types.Message):
#     try:
#         wb = Workbook()
#         ws = wb.active
#         ws['A1'] = "№"
#         ws['B1'] = "To'liq ismi"
#         ws['C1'] = "Telegram Username"
#         ws['D1'] = "Telefon raqami"
#         ws['E1'] = "Telegram Id"
#         ws['F1'] = "From user Telegram Id"
#         userss = await db.select_top_users_list()
#         counter = 0
#         for user in userss:
#             counter += 1
#
#             ws.append([f"{counter}", f"{user[8]}", f"{user[2]}", f"{user[3]}", f"{user[6]}", f"{user[7]}"])
#         n = random.sample(range(1, 100), 1)
#         m = random.sample(range(100, 1000), 1)
#
#         wb.save(f"Excel.xlsx")
#         file = InputFile(path_or_bytesio=f'Excel.xlsx')
#         await message.answer_document(document=file)
#         os.remove(f"Excel_{n}_{m}.xlsx")
#     except Exception as e:
#         print(e)
