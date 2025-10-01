import asyncio
from aiogram import types

from handlers.users.main import create_link
from loader import dp, db, bot
from aiogram.dispatcher import FSMContext
from keyboards.default.rekKeyboards import back, admin_key
from states.rekStates import RekData, AllState, Lesson, Number
from utils.misc import subscription


@dp.message_handler(text='Admin ➕')
async def add_channel(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer('Id ni kiriting', reply_markup=back)
        await AllState.env.set()


@dp.message_handler(state=AllState.env)
async def env_change(message: types.Message, state: FSMContext):
    if message.text == '🔙️ Orqaga':
        await message.answer('Admin panel', reply_markup=admin_key)
        await state.finish()
    else:
        try:
            int(message.text)
        except ValueError:
            await message.answer('Faqat son qabul qilinadi\n\n'
                                 'Qaytadan kiriting')
        admins = await db.select_all_admins()
        admins_list = []
        for i in admins:
            admins_list.append(i[1])
        if int(message.text) in admins_list:
            await message.answer('Bunday admin mavjud')
        else:
            await db.add_admin(telegram_id=int(message.text))

            await message.answer(f"Qo'shildi\n\n", reply_markup=admin_key)
            await state.finish()


@dp.message_handler(text='Admin ➖')
async def add_channel(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer('Id ni kiriting', reply_markup=back)
        await AllState.env_remove.set()


@dp.message_handler(state=AllState.env_remove)
async def env_change(message: types.Message, state: FSMContext):
    if message.text == '🔙️ Orqaga':
        await message.answer('Admin panel', reply_markup=admin_key)
        await state.finish()
    else:
        try:
            admins = await db.select_all_admins()
            admins_list = []
            for i in admins:
                admins_list.append(i[1])
            if int(message.text) in admins_list:
                await db.delete_admins(telegram_id=int(message.text))
                admins2 = await db.select_all_admins()
                admins_list2 = []
                for i in admins2:
                    admins_list2.append(i[1])

                await message.answer(f'O"chirildi\n\n'
                                     f'Hozirgi adminlar {admins_list2}', reply_markup=admin_key)
                await state.finish()
            else:
                await message.answer('Bunday admin mavjud emas\n\n'
                                     'Faqat admin id sini qabul qilamiz')
        except Exception as err:
            await message.answer(f'{err}')
            await message.answer('Faqat son qabul qilinadi\n\n'
                                 'Qaytadan kiriting')


@dp.message_handler(text='Barcha Adminlar')
async def add_channel(message: types.Message):
    admins = await db.select_all_admins()
    lst = []
    for admin in admins:
        lst.append(admin[1])
    await message.answer(f'Adminlar - {lst}', reply_markup=admin_key)


@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer(text='Admin panel',
                             reply_markup=admin_key)


@dp.message_handler(commands=['bal'])
async def update_scoreee(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer('bal va idni kiriting')
        await Number.add_user.set()


@dp.message_handler(state=Number.add_user)
async def fixx(message: types.Message, state: FSMContext):
    user_text = message.text.split(',')
    await db.update_user_score(score=int(user_text[0]), telegram_id=int(user_text[1]))
    await message.answer('Yangilandi')
    await state.finish()


@dp.message_handler(commands=['name'])
async def update_scoreee(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer('name va balni kiriting')
        await Number.name.set()


@dp.message_handler(state=Number.name)
async def fixx(message: types.Message, state: FSMContext):
    user_text = message.text.split(',')
    await db.update_user_name(name=user_text[0], telegram_id=int(user_text[1]))
    await message.answer('Yangilandi')
    await state.finish()


@dp.message_handler(commands=['username'])
async def update_username(message: types.Message):
    global admins
    if message.from_user.id in admins:
        await message.answer('username va balni kiriting')
        await Number.username.set()


@dp.message_handler(state=Number.username)
async def fixx(message: types.Message, state: FSMContext):
    user_text = message.text.split(',')
    await db.update_user_username(username=user_text[0], telegram_id=int(user_text[1]))
    await message.answer('Yangilandi')
    await state.finish()


@dp.message_handler(text='Kanal ➕')
async def add_channel(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer(text='Kanalni kiriting\n\n'
                                  'Masalan : "https://t.me/texnohelpuz ,Texno Help (Kanal Nomi)"\n\n',
                             reply_markup=back)
        await RekData.add.set()
    else:
        await message.answer("Xato\n\n" "https://t.me/ bilan kiriting")


@dp.message_handler(state=RekData.add)
async def add_username(message: types.Message, state: FSMContext):
    text = message.text
    if text[:13] == "https://t.me/":
        add_lists = await db.select_add_list()
        private_channels = await db.select_req_j_chanel()
        public_channels = await db.select_chanel()
        tugma = await db.select_tugma()
        button_numbers = []
        for i in add_lists:
            button_numbers.append(i['order_button'])
        for i in private_channels:
            button_numbers.append(i['order_button'])
        for i in public_channels:
            button_numbers.append(i['order_button'])
        for i in tugma:
            button_numbers.append(i['order_button'])
        max_number = max(button_numbers) if button_numbers else 0
        text_split = text.split(',')
        cleaned_text = text_split[0].rstrip()
        await db.add_chanell(chanelll=f"{cleaned_text[13:]}",
                             channel_name=f"{text_split[1]}", url=f"{cleaned_text}",
                             order_button=max_number + 1)
        await message.answer("Qo'shildi", reply_markup=admin_key)
        await state.finish()
    elif text == '🔙️ Orqaga':
        await message.answer('Admin panel', reply_markup=admin_key)
        await state.finish()
    else:
        await message.answer('Xato\n'
                             'https://t.me/ bilan boshlansin\n\nMasalan:\n "https://t.me/texnohelpuz ,Texno Help"')


@dp.message_handler(text='Kanal ➖')
async def add_channel(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer(text='Kanalni kiriting @ belgi bilan\n\n'
                                  'Masalan : "Kanal zayavkada bo`lsa chanel_id(-123123213),chanel_url"\n\n',
                             reply_markup=back)
        await RekData.delete.set()


@dp.message_handler(state=RekData.delete)
async def del_username(message: types.Message, state: FSMContext):
    text = message.text
    if text[:13] == "https://t.me/":
        chanel = await db.get_chanel(channel=f"{text[13:]}")
        if not chanel:
            await message.answer("Kanal topilmadi\n"
                                 "Qaytadan urinib ko'ring")

        else:
            await db.delete_channel(chanel=text[13:])
            await message.answer('Kanal o"chirildi', reply_markup=admin_key)
            await state.finish()
    elif text == '🔙️ Orqaga':
        await message.answer('Admin panel', reply_markup=admin_key)
        await state.finish()


# @dp.message_handler(text='Statistika 📊')
# async def show_users(message: types.Message):
#     all_users_count = await db.count_users()
#     in_active_users = await db.count_block_users()

#     await message.answer(f'<b>🔵 Jami obunachilar: {all_users_count} ta\n\n'
#                          f'🟡 Active: {all_users_count - in_active_users}\n'
#                          f'⚫️ Block : {in_active_users}</b>')


@dp.message_handler(text='🏘 Bosh menu')
async def menuu(message: types.Message):
    button_score = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_score.add(types.KeyboardButton(text="🎗 Ballarim"))
    await message.answer('Ballaringizni ko`rish uchun "🎗 Ballarim" tugmasini bosing',
                              reply_markup=button_score)


@dp.message_handler(text='Kanallar 📈')
async def channels(message: types.Message):
    channels = await db.select_chanel()
    text = ''
    for channel in channels:
        text += f"{channel['url']}\n"
    try:
        await message.answer(f"{text}", reply_markup=admin_key)
    except:
        await message.answer(f"Kanallar mavjud emas")


@dp.message_handler(text='Rasmni almashtirish 🖼')
async def change_picture(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer('Rasmni kiriting', reply_markup=back)
        await RekData.picture.set()


@dp.message_handler(content_types=['photo', 'text', 'video'], state=RekData.picture)
async def change_picture_(message: types.Message, state: FSMContext):
    global admins
    if message.from_user.id in admins:
        if message.photo:
            photo = message.photo[-1].file_id
            elements = await db.get_elements()
            if elements:
                await db.update_photo(photo=photo)
                await message.answer('Yangilandi', reply_markup=admin_key)
                await state.finish()

            else:
                await db.add_photo(photo=photo)
                await message.answer('Qo`shildi', reply_markup=admin_key)
                await state.finish()

        elif message.text == '🔙️ Orqaga':
            await message.answer('Bosh menu')
            await state.finish()
        elif message.text == '/start':
            await message.answer('Bosh menu')
            await state.finish()

        else:
            await message.answer('Faqat rasm qabul qilamiz')


@dp.message_handler(text="O'yin haqida matn 🎮")
async def change_picture(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer('Textni kiriting', reply_markup=back)
        await RekData.text.set()


@dp.message_handler(state=RekData.text)
async def change_picture_(message: types.Message, state: FSMContext):
    if message.text:
        elements = await db.get_elements()
        if elements:
            await db.update_game_text(game_text=message.text)
            await message.answer('Yangilandi', reply_markup=admin_key)
            await state.finish()
        elif message.text == '/start':
            await message.answer('Bosh menu')
            await state.finish()

        elif message.text == '🔙️ Orqaga':
            await message.answer('Bosh menu')
            await state.finish()

        else:
            await db.add_text(game_text=message.text)
            await message.answer('Qo`shildi', reply_markup=admin_key)
            await state.finish()
    else:
        await message.answer('Faqat Text qabul qilamiz')


@dp.message_handler(text="G'oliblarga")
async def to_winners(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer('Yuboring', reply_markup=back)
        await RekData.to_winners.set()


@dp.message_handler(state=RekData.to_winners, content_types=[
    'video', 'audio', 'voice', 'photo', 'document', 'text', 'animation', 'video_note', 'venue'])
async def to_winners_content(message: types.Message, state: FSMContext):
    if message.video:
        file_id = message.video.file_id
        file_unique_id = message.video.file_unique_id
        caption = ''
        if message.caption is not None:
            caption += message.caption
        a = await db.add_lesson(
            button_name="G'oliblarga",
            type='video',
            file_id=file_id,
            file_unique_id=file_unique_id,
            description=caption
        )
        await message.answer_video(
            video=file_id,
            caption=f"{caption}\n\n" \
                    f'🗑 o`chirish uchun mahsus code - <code>{a["id"]}</code>'
                    f' (faqat adminlarga ko`rinadi)'
        )

        await message.answer("Qo'shildi\n\n"
                             "Yana ma'lumot kiritishingiz mumkin")
    elif message.voice:
        file_id = message.voice.file_id
        file_unique_id = message.voice.file_unique_id
        caption = message.caption
        a = await db.add_lesson(
            button_name="G'oliblarga",
            type='video',
            file_id=file_id,
            file_unique_id=file_unique_id,
            description=caption
        )
        await message.answer_voice(
            voice=file_id,
            caption=f"{caption}\n\n" \
                    f'🗑 o`chirish uchun mahsus code - <code>{a["id"]}</code>'
                    f' (faqat adminlarga ko`rinadi)'
        )

        await message.answer("Qo'shildi\n\n"
                             "Yana ma'lumot kiritishingiz mumkin")
    elif message.document:
        file_id = message.document.file_id
        file_unique_id = message.document.file_unique_id
        caption = ''
        if message.caption is not None:
            caption += message.caption
        a = await db.add_lesson(
            button_name="G'oliblarga",
            type='video',
            file_id=file_id,
            file_unique_id=file_unique_id,
            description=caption
        )
        await message.answer_document(
            document=file_id,
            caption=f"{caption}\n\n" \
                    f'🗑 o`chirish uchun mahsus code - <code>{a["id"]}</code>'
                    f' (faqat adminlarga ko`rinadi)'
        )

        await message.answer("Qo'shildi\n\n"
                             "Yana ma'lumot kiritishingiz mumkin")

    elif message.photo:
        file_id = message.photo[-1].file_id
        file_unique_id = message.photo[-1].file_unique_id
        caption = ''
        if message.caption is not None:
            caption += message.caption
        a = await db.add_lesson(
            button_name="G'oliblarga",
            type='video',
            file_id=file_id,
            file_unique_id=file_unique_id,
            description=caption
        )
        await message.answer_photo(
            photo=file_id,
            caption=f"{caption}\n\n" \
                    f'🗑 o`chirish uchun mahsus code - <code>{a["id"]}</code>'
                    f' (faqat adminlarga ko`rinadi)'
        )

        await message.answer("Qo'shildi\n\n"
                             "Yana ma'lumot kiritishingiz mumkin")

    elif message.audio:
        file_id = message.audio.file_id
        file_unique_id = message.audio.file_unique_id
        caption = ''
        if message.caption is not None:
            caption += message.caption
        a = await db.add_lesson(
            button_name="G'oliblarga",
            type='video',
            file_id=file_id,
            file_unique_id=file_unique_id,
            description=caption
        )
        await message.answer_audio(
            audio=file_id,
            caption=f"{caption}\n\n" \
                    f'🗑 o`chirish uchun mahsus code - <code>{a["id"]}</code>'
                    f' (faqat adminlarga ko`rinadi)'
        )

        await message.answer("Qo'shildi\n\n"
                             "Yana ma'lumot kiritishingiz mumkin")
    elif message.text == '🔙️ Orqaga':
        await message.answer('Admin panel', reply_markup=admin_key)
        await state.finish()
    elif message.text:
        a = await db.add_lesson_text(
            button_name="G'oliblarga",
            type='text',
            file_unique_id=f'{message.message_id}',
            description=f'{message.text}'
        )
        await message.answer(f'{message.text}\n\n' \
                             f'🗑 o`chirish uchun mahsus code - <code>{a["id"]}</code>'
                             f' (faqat adminlarga ko`rinadi)')
        await message.answer("Qo'shildi\n\n"
                             "Yana ma'lumot kiritishingiz mumkin")


@dp.message_handler(text="Majburiy obuna")
async def required_subscribe(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer('Yuboring', reply_markup=back)
        await RekData.required_subscribe.set()


@dp.message_handler(state=RekData.required_subscribe, content_types=[
    'video', 'audio', 'voice', 'photo', 'document', 'text', 'animation', 'video_note', 'venue'])
async def required_subscribe_content(message: types.Message, state: FSMContext):
    if message.video:
        file_id = message.video.file_id
        file_unique_id = message.video.file_unique_id
        caption = ''
        if message.caption is not None:
            caption += message.caption
        a = await db.add_lesson(
            button_name="G'oliblarga",
            type='video',
            file_id=file_id,
            file_unique_id=file_unique_id,
            description=caption
        )
        await message.answer_video(
            video=file_id,
            caption=f"{caption}\n\n" \
                    f'🗑 o`chirish uchun mahsus code - <code>{a["id"]}</code>'
                    f' (faqat adminlarga ko`rinadi)'
        )

        await message.answer("Qo'shildi\n\n"
                             "Yana ma'lumot kiritishingiz mumkin")
    elif message.voice:
        file_id = message.voice.file_id
        file_unique_id = message.voice.file_unique_id
        caption = message.caption
        a = await db.add_lesson(
            button_name="G'oliblarga",
            type='video',
            file_id=file_id,
            file_unique_id=file_unique_id,
            description=caption
        )
        await message.answer_voice(
            voice=file_id,
            caption=f"{caption}\n\n" \
                    f'🗑 o`chirish uchun mahsus code - <code>{a["id"]}</code>'
                    f' (faqat adminlarga ko`rinadi)'
        )

        await message.answer("Qo'shildi\n\n"
                             "Yana ma'lumot kiritishingiz mumkin")
    elif message.document:
        file_id = message.document.file_id
        file_unique_id = message.document.file_unique_id
        caption = ''
        if message.caption is not None:
            caption += message.caption
        a = await db.add_lesson(
            button_name="G'oliblarga",
            type='video',
            file_id=file_id,
            file_unique_id=file_unique_id,
            description=caption
        )
        await message.answer_document(
            document=file_id,
            caption=f"{caption}\n\n" \
                    f'🗑 o`chirish uchun mahsus code - <code>{a["id"]}</code>'
                    f' (faqat adminlarga ko`rinadi)'
        )

        await message.answer("Qo'shildi\n\n"
                             "Yana ma'lumot kiritishingiz mumkin")

    elif message.photo:
        file_id = message.photo[-1].file_id
        file_unique_id = message.photo[-1].file_unique_id
        caption = ''
        if message.caption is not None:
            caption += message.caption
        a = await db.add_lesson(
            button_name="Majburiy obuna",
            type='photo',
            file_id=file_id,
            file_unique_id=file_unique_id,
            description=caption
        )
        await message.answer_photo(
            photo=file_id,
            caption=f"{caption}\n\n" \
                    f'🗑 o`chirish uchun mahsus code - <code>{a["id"]}</code>'
                    f' (faqat adminlarga ko`rinadi)'
        )

        await message.answer("Qo'shildi\n\n"
                             "Yana ma'lumot kiritishingiz mumkin")

    elif message.audio:
        file_id = message.audio.file_id
        file_unique_id = message.audio.file_unique_id
        caption = ''
        if message.caption is not None:
            caption += message.caption
        a = await db.add_lesson(
            button_name="Majburiy obuna",
            type='audio',
            file_id=file_id,
            file_unique_id=file_unique_id,
            description=caption
        )
        await message.answer_audio(
            audio=file_id,
            caption=f"{caption}\n\n" \
                    f'🗑 o`chirish uchun mahsus code - <code>{a["id"]}</code>'
                    f' (faqat adminlarga ko`rinadi)'
        )

        await message.answer("Qo'shildi\n\n"
                             "Yana ma'lumot kiritishingiz mumkin")
    elif message.text == '🔙️ Orqaga':
        await message.answer('Admin panel', reply_markup=admin_key)
        await state.finish()
    elif message.text:
        a = await db.add_lesson_text(
            button_name="Majburiy obuna",
            type='text',
            file_unique_id=f'{message.message_id}',
            description=f'{message.text}'
        )
        await message.answer(f'{message.text}\n\n' \
                             f'🗑 o`chirish uchun mahsus code - <code>{a["id"]}</code>'
                             f' (faqat adminlarga ko`rinadi)')
        await message.answer("Qo'shildi\n\n"
                             "Yana ma'lumot kiritishingiz mumkin")

@dp.message_handler(text="Obunadan so'ng")
async def alter_sub(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer('Yuboring', reply_markup=back)
        await RekData.after_sub.set()


@dp.message_handler(state=RekData.after_sub, content_types=[
    'video', 'audio', 'voice', 'photo', 'document', 'text', 'animation', 'video_note', 'venue'])
async def after_sub_content(message: types.Message, state: FSMContext):
    if message.video:
        file_id = message.video.file_id
        file_unique_id = message.video.file_unique_id
        caption = ''
        if message.caption is not None:
            caption += message.caption
        a = await db.add_lesson(
            button_name="Obunadan so'ng",
            type='video',
            file_id=file_id,
            file_unique_id=file_unique_id,
            description=caption
        )
        await message.answer_video(
            video=file_id,
            caption=f"{caption}\n\n" \
                    f'🗑 o`chirish uchun mahsus code - <code>{a["id"]}</code>'
                    f' (faqat adminlarga ko`rinadi)'
        )

        await message.answer("Qo'shildi\n\n"
                             "Yana ma'lumot kiritishingiz mumkin")
    elif message.voice:
        file_id = message.voice.file_id
        file_unique_id = message.voice.file_unique_id
        caption = message.caption
        a = await db.add_lesson(
            button_name="Obunadan so'ng",
            type='voice',
            file_id=file_id,
            file_unique_id=file_unique_id,
            description=caption
        )
        await message.answer_voice(
            voice=file_id,
            caption=f"{caption}\n\n" \
                    f'🗑 o`chirish uchun mahsus code - <code>{a["id"]}</code>'
                    f' (faqat adminlarga ko`rinadi)'
        )

        await message.answer("Qo'shildi\n\n"
                             "Yana ma'lumot kiritishingiz mumkin")
    elif message.document:
        file_id = message.document.file_id
        file_unique_id = message.document.file_unique_id
        caption = ''
        if message.caption is not None:
            caption += message.caption
        a = await db.add_lesson(
            button_name="Obunadan so'ng",
            type='document',
            file_id=file_id,
            file_unique_id=file_unique_id,
            description=caption
        )
        await message.answer_document(
            document=file_id,
            caption=f"{caption}\n\n" \
                    f'🗑 o`chirish uchun mahsus code - <code>{a["id"]}</code>'
                    f' (faqat adminlarga ko`rinadi)'
        )

        await message.answer("Qo'shildi\n\n"
                             "Yana ma'lumot kiritishingiz mumkin")

    elif message.photo:
        file_id = message.photo[-1].file_id
        file_unique_id = message.photo[-1].file_unique_id
        caption = ''
        if message.caption is not None:
            caption += message.caption
        a = await db.add_lesson(
            button_name="Obunadan so'ng",
            type='photo',
            file_id=file_id,
            file_unique_id=file_unique_id,
            description=caption
        )
        await message.answer_photo(
            photo=file_id,
            caption=f"{caption}\n\n" \
                    f'🗑 o`chirish uchun mahsus code - <code>{a["id"]}</code>'
                    f' (faqat adminlarga ko`rinadi)'
        )

        await message.answer("Qo'shildi\n\n"
                             "Yana ma'lumot kiritishingiz mumkin")

    elif message.audio:
        file_id = message.audio.file_id
        file_unique_id = message.audio.file_unique_id
        caption = ''
        if message.caption is not None:
            caption += message.caption
        a = await db.add_lesson(
            button_name="Obunadan so'ng",
            type='audio',
            file_id=file_id,
            file_unique_id=file_unique_id,
            description=caption
        )
        await message.answer_audio(
            audio=file_id,
            caption=f"{caption}\n\n" \
                    f'🗑 o`chirish uchun mahsus code - <code>{a["id"]}</code>'
                    f' (faqat adminlarga ko`rinadi)'
        )

        await message.answer("Qo'shildi\n\n"
                             "Yana ma'lumot kiritishingiz mumkin")
    elif message.text == '🔙️ Orqaga':
        await message.answer('Admin panel', reply_markup=admin_key)
        await state.finish()
    elif message.text:
        a = await db.add_lesson_text(
            button_name="Obunadan so'ng",
            type='text',
            file_unique_id=f'{message.message_id}',
            description=f'{message.text}'
        )
        await message.answer(f'{message.text}\n\n' \
                             f'🗑 o`chirish uchun mahsus code - <code>{a["id"]}</code>'
                             f' (faqat adminlarga ko`rinadi)')
        await message.answer("Qo'shildi\n\n"
                             "Yana ma'lumot kiritishingiz mumkin")


@dp.message_handler(text="Asosiy qism")
async def change_picture(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer('Yuboring', reply_markup=back)
        await RekData.main_content.set()


@dp.message_handler(state=RekData.main_content, content_types=[
    'video', 'audio', 'voice', 'photo', 'document', 'text', 'animation', 'video_note', 'venue'])
async def add_lesson(message: types.Message, state: FSMContext):
    if message.video:
        file_id = message.video.file_id
        file_unique_id = message.video.file_unique_id
        caption = ''
        if message.caption is not None:
            caption += message.caption
        await message.answer_video(
            video=file_id,
            caption=f"{caption}\n\n" \
                    f'🗑 o`chirish uchun mahsus code - <code>{file_unique_id}</code>'
                    f' (faqat adminlarga ko`rinadi)'
        )
        await db.add_lesson(
            button_name="Asosiy qism",
            type='video',
            file_id=file_id,
            file_unique_id=file_unique_id,
            description=caption
        )

        await message.answer("Qo'shildi\n\n"
                             "Yana ma'lumot kiritishingiz mumkin")
    elif message.voice:
        file_id = message.voice.file_id
        file_unique_id = message.voice.file_unique_id
        caption = message.caption
        await message.answer_voice(
            voice=file_id,
            caption=f"{caption}\n\n" \
                    f'🗑 o`chirish uchun mahsus code - <code>{file_unique_id}</code>'
                    f' (faqat adminlarga ko`rinadi)'
        )
        await db.add_lesson(
            button_name="Asosiy qism",
            type='voice',
            file_id=file_id,
            file_unique_id=file_unique_id,
            description=caption
        )

        await message.answer("Qo'shildi\n\n"
                             "Yana ma'lumot kiritishingiz mumkin")
    elif message.document:
        file_id = message.document.file_id
        file_unique_id = message.document.file_unique_id
        caption = ''
        if message.caption is not None:
            caption += message.caption
        await message.answer_document(
            document=file_id,
            caption=f"{caption}\n\n" \
                    f'🗑 o`chirish uchun mahsus code - <code>{file_unique_id}</code>'
                    f' (faqat adminlarga ko`rinadi)'
        )
        await db.add_lesson(
            button_name="Asosiy qism",
            type='document',
            file_id=file_id,
            file_unique_id=file_unique_id,
            description=caption
        )

        await message.answer("Qo'shildi\n\n"
                             "Yana ma'lumot kiritishingiz mumkin")

    elif message.photo:
        file_id = message.photo[-1].file_id
        file_unique_id = message.photo[-1].file_unique_id
        caption = ''
        if message.caption is not None:
            caption += message.caption
        await message.answer_photo(
            photo=file_id,
            caption=f"{caption}\n\n" \
                    f'🗑 o`chirish uchun mahsus code - <code>{file_unique_id}</code>'
                    f' (faqat adminlarga ko`rinadi)'
        )
        await db.add_lesson(
            button_name="Asosiy qism",
            type='photo',
            file_id=file_id,
            file_unique_id=file_unique_id,
            description=caption
        )

        await message.answer("Qo'shildi\n\n"
                             "Yana ma'lumot kiritishingiz mumkin")

    elif message.audio:
        file_id = message.audio.file_id
        file_unique_id = message.audio.file_unique_id
        caption = ''
        if message.caption is not None:
            caption += message.caption
        await message.answer_audio(
            audio=file_id,
            caption=f"{caption}\n\n" \
                    f'🗑 o`chirish uchun mahsus code - <code>{file_unique_id}</code>'
                    f' (faqat adminlarga ko`rinadi)'
        )
        await db.add_lesson(
            button_name="Asosiy qism",
            type='audio',
            file_id=file_id,
            file_unique_id=file_unique_id,
            description=caption
        )

        await message.answer("Qo'shildi\n\n"
                             "Yana ma'lumot kiritishingiz mumkin")
    elif message.text == '🔙️ Orqaga':
        await message.answer('Admin panel', reply_markup=admin_key)
        await state.finish()
    elif message.text:
        a = await db.add_lesson_text(
            button_name="Asosiy qism",
            type='text',
            file_unique_id=f'{message.message_id}',
            description=f'{message.text}'
        )
        await message.answer(f'{message.text}\n\n' \
                             f'🗑 o`chirish uchun mahsus code - <code>{message.message_id}</code>'
                             f' (faqat adminlarga ko`rinadi)')
        await message.answer("Qo'shildi\n\n"
                             "Yana ma'lumot kiritishingiz mumkin")

@dp.message_handler(text="Asosiy qism 2")
async def main_content_2_checker(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer('Yuboring', reply_markup=back)
        await RekData.main_content_2.set()


@dp.message_handler(state=RekData.main_content_2, content_types=[
    'video', 'audio', 'voice', 'photo', 'document', 'text', 'animation', 'video_note', 'venue'])
async def main_content_2_data(message: types.Message, state: FSMContext):
    if message.video:
        file_id = message.video.file_id
        file_unique_id = message.video.file_unique_id
        caption = ''
        if message.caption is not None:
            caption += message.caption
        await message.answer_video(
            video=file_id,
            caption=f"{caption}\n\n" \
                    f'🗑 o`chirish uchun mahsus code - <code>{file_unique_id}</code>'
                    f' (faqat adminlarga ko`rinadi)'
        )
        await db.add_lesson(
            button_name="Asosiy qism 2",
            type='video',
            file_id=file_id,
            file_unique_id=file_unique_id,
            description=caption
        )

        await message.answer("Qo'shildi\n\n"
                             "Yana ma'lumot kiritishingiz mumkin")
    elif message.voice:
        file_id = message.voice.file_id
        file_unique_id = message.voice.file_unique_id
        caption = message.caption
        await message.answer_voice(
            voice=file_id,
            caption=f"{caption}\n\n" \
                    f'🗑 o`chirish uchun mahsus code - <code>{file_unique_id}</code>'
                    f' (faqat adminlarga ko`rinadi)'
        )
        await db.add_lesson(
            button_name="Asosiy qism 2",
            type='voice',
            file_id=file_id,
            file_unique_id=file_unique_id,
            description=caption
        )

        await message.answer("Qo'shildi\n\n"
                             "Yana ma'lumot kiritishingiz mumkin")
    elif message.document:
        file_id = message.document.file_id
        file_unique_id = message.document.file_unique_id
        caption = ''
        if message.caption is not None:
            caption += message.caption
        await message.answer_document(
            document=file_id,
            caption=f"{caption}\n\n" \
                    f'🗑 o`chirish uchun mahsus code - <code>{file_unique_id}</code>'
                    f' (faqat adminlarga ko`rinadi)'
        )
        await db.add_lesson(
            button_name="Asosiy qism 2",
            type='document',
            file_id=file_id,
            file_unique_id=file_unique_id,
            description=caption
        )

        await message.answer("Qo'shildi\n\n"
                             "Yana ma'lumot kiritishingiz mumkin")

    elif message.photo:
        file_id = message.photo[-1].file_id
        file_unique_id = message.photo[-1].file_unique_id
        caption = ''
        if message.caption is not None:
            caption += message.caption
        await message.answer_photo(
            photo=file_id,
            caption=f"{caption}\n\n" \
                    f'🗑 o`chirish uchun mahsus code - <code>{file_unique_id}</code>'
                    f' (faqat adminlarga ko`rinadi)'
        )
        await db.add_lesson(
            button_name="Asosiy qism 2",
            type='photo',
            file_id=file_id,
            file_unique_id=file_unique_id,
            description=caption
        )

        await message.answer("Qo'shildi\n\n"
                             "Yana ma'lumot kiritishingiz mumkin")

    elif message.audio:
        file_id = message.audio.file_id
        file_unique_id = message.audio.file_unique_id
        caption = ''
        if message.caption is not None:
            caption += message.caption
        await message.answer_audio(
            audio=file_id,
            caption=f"{caption}\n\n" \
                    f'🗑 o`chirish uchun mahsus code - <code>{file_unique_id}</code>'
                    f' (faqat adminlarga ko`rinadi)'
        )
        await db.add_lesson(
            button_name="Asosiy qism 2",
            type='audio',
            file_id=file_id,
            file_unique_id=file_unique_id,
            description=caption
        )

        await message.answer("Qo'shildi\n\n"
                             "Yana ma'lumot kiritishingiz mumkin")
    elif message.text == '🔙️ Orqaga':
        await message.answer('Admin panel', reply_markup=admin_key)
        await state.finish()
    elif message.text:
        a = await db.add_lesson_text(
            button_name="Asosiy qism 2",
            type='text',
            file_unique_id=f'{message.message_id}',
            description=f'{message.text}'
        )
        await message.answer(f'{message.text}\n\n' \
                             f'🗑 o`chirish uchun mahsus code - <code>{message.message_id}</code>'
                             f' (faqat adminlarga ko`rinadi)')
        await message.answer("Qo'shildi\n\n"
                             "Yana ma'lumot kiritishingiz mumkin")

@dp.message_handler(text="Birinchi Sovg'a")
async def change_first_gift(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer('Yuboring', reply_markup=back)
        await RekData.first_gift.set()


@dp.message_handler(state=RekData.first_gift, content_types=[
    'video', 'audio', 'voice', 'photo', 'document', 'text', 'animation', 'video_note', 'venue'])
async def add_first_gift_data(message: types.Message, state: FSMContext):
    if message.video:
        file_id = message.video.file_id
        file_unique_id = message.video.file_unique_id
        caption = ''
        if message.caption is not None:
            caption += message.caption
        await message.answer_video(
            video=file_id,
            caption=f"{caption}\n\n" \
                    f'🗑 o`chirish uchun mahsus code - <code>{file_unique_id}</code>'
                    f' (faqat adminlarga ko`rinadi)'
        )
        await db.add_lesson(
            button_name="Birinchi Sovg'a",
            type='video',
            file_id=file_id,
            file_unique_id=file_unique_id,
            description=caption
        )

        await message.answer("Qo'shildi\n\n"
                             "Yana ma'lumot kiritishingiz mumkin")
    elif message.voice:
        file_id = message.voice.file_id
        file_unique_id = message.voice.file_unique_id
        caption = message.caption
        await message.answer_voice(
            voice=file_id,
            caption=f"{caption}\n\n" \
                    f'🗑 o`chirish uchun mahsus code - <code>{file_unique_id}</code>'
                    f' (faqat adminlarga ko`rinadi)'
        )
        await db.add_lesson(
            button_name="Birinchi Sovg'a",
            type='voice',
            file_id=file_id,
            file_unique_id=file_unique_id,
            description=caption
        )

        await message.answer("Qo'shildi\n\n"
                             "Yana ma'lumot kiritishingiz mumkin")
    elif message.document:
        file_id = message.document.file_id
        file_unique_id = message.document.file_unique_id
        caption = ''
        if message.caption is not None:
            caption += message.caption
        await message.answer_document(
            document=file_id,
            caption=f"{caption}\n\n" \
                    f'🗑 o`chirish uchun mahsus code - <code>{file_unique_id}</code>'
                    f' (faqat adminlarga ko`rinadi)'
        )
        await db.add_lesson(
            button_name="Birinchi Sovg'a",
            type='document',
            file_id=file_id,
            file_unique_id=file_unique_id,
            description=caption
        )

        await message.answer("Qo'shildi\n\n"
                             "Yana ma'lumot kiritishingiz mumkin")

    elif message.photo:
        file_id = message.photo[-1].file_id
        file_unique_id = message.photo[-1].file_unique_id
        caption = ''
        if message.caption is not None:
            caption += message.caption
        await message.answer_photo(
            photo=file_id,
            caption=f"{caption}\n\n" \
                    f'🗑 o`chirish uchun mahsus code - <code>{file_unique_id}</code>'
                    f' (faqat adminlarga ko`rinadi)'
        )
        await db.add_lesson(
            button_name="Birinchi Sovg'a",
            type='photo',
            file_id=file_id,
            file_unique_id=file_unique_id,
            description=caption
        )

        await message.answer("Qo'shildi\n\n"
                             "Yana ma'lumot kiritishingiz mumkin")

    elif message.audio:
        file_id = message.audio.file_id
        file_unique_id = message.audio.file_unique_id
        caption = ''
        if message.caption is not None:
            caption += message.caption
        await message.answer_audio(
            audio=file_id,
            caption=f"{caption}\n\n" \
                    f'🗑 o`chirish uchun mahsus code - <code>{file_unique_id}</code>'
                    f' (faqat adminlarga ko`rinadi)'
        )
        await db.add_lesson(
            button_name="Birinchi Sovg'a",
            type='audio',
            file_id=file_id,
            file_unique_id=file_unique_id,
            description=caption
        )

        await message.answer("Qo'shildi\n\n"
                             "Yana ma'lumot kiritishingiz mumkin")
    elif message.text == '🔙️ Orqaga':
        await message.answer('Admin panel', reply_markup=admin_key)
        await state.finish()
    elif message.text:
        a = await db.add_lesson_text(
            button_name="Birinchi Sovg'a",
            type='text',
            file_unique_id=f'{message.message_id}',
            description=f'{message.text}'
        )
        await message.answer(f'{message.text}\n\n' \
                             f'🗑 o`chirish uchun mahsus code - <code>{message.message_id}</code>'
                             f' (faqat adminlarga ko`rinadi)')
        await message.answer("Qo'shildi\n\n"
                             "Yana ma'lumot kiritishingiz mumkin")


@dp.message_handler(text="Bot havolasi")
async def change_picture(message: types.Message):
    global admins
    if message.from_user.id == admins[0]:
        await message.answer('Textni kiriting', reply_markup=back)
        await RekData.url.set()
    else:
        await message.answer('Bu tugma siz uchun emas 😉')


@dp.message_handler(state=RekData.url)
async def url(message: types.Message, state: FSMContext):
    global admins
    if message.from_user.id in admins:
        if message.text:
            elements = await db.get_elements()
            if message.text == '/start':
                await message.answer('Bosh menu')
                await state.finish()

            elif message.text == '🔙️ Orqaga':
                await message.answer('Admin qism', reply_markup=admin_key)
                await state.finish()
            elif elements:
                await db.bot_url(bot_url=message.text)
                await message.answer('Yangilandi', reply_markup=admin_key)
                await state.finish()

            else:
                await db.add_bot_url(bot_url=message.text)
                await message.answer('Qo`shildi', reply_markup=admin_key)
                await state.finish()
        else:
            await message.answer('Faqat Text qabul qilamiz')


@dp.message_handler(text="Yopiq kanal idsini kiriting")
async def change_picture(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer('Id kiriting', reply_markup=back)
        await RekData.channel_id.set()


@dp.message_handler(state=RekData.channel_id)
async def change_picture_(message: types.Message, state: FSMContext):
    if message.text:
        elements = await db.get_elements()
        if message.text == '🔙️ Orqaga':
            await message.answer('Bosh menu', reply_markup=admin_key)
            await state.finish()
        elif message.text == '/start':
            await message.answer('Bosh menu')
            await state.finish()

        elif elements and message.text.startswith('-'):

            try:
                id = int(message.text[1:])
                await db.update_channel_id(channel_id=message.text)
                await message.answer('Kanal id Yangilandi', reply_markup=admin_key)
                await state.finish()
            except Exception as err:
                await message.answer(f'Faqat -12312332 ko`rinishida kiriting')

        elif message.text.startswith('-'):
            try:
                id = int(message.text[1:])
                await db.add_channel_id(channel_id=message.text)
                await message.answer('Kanal id Qo`shildi', reply_markup=admin_key)
                await state.finish()
            except Exception as err:
                await message.answer(f'Faqat -12312332 ko`rinishida kiriting')
        else:
            await message.answer(f'Faqat -12312332 ko`rinishida kiriting')

    elif message.text == '🔙️ Orqaga':
        await message.answer('Bosh menu')
        await state.finish()
    else:
        await message.answer(f'Faqat -12312332 ko`rinishida kiriting')


@dp.message_handler(text="Obuna bo'lish so'rovi teksti")
async def req_text(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer('Yuboring', reply_markup=back)
        await RekData.req_text.set()


@dp.message_handler(state=RekData.req_text)
async def change_req_text(message: types.Message, state: FSMContext):
    if message.text:
        elements = await db.get_elements()
        if message.text == '🔙️ Orqaga':
            await message.answer('Bosh menu', reply_markup=admin_key)
            await state.finish()
        elif message.text == '/start':
            await message.answer('Bosh menu')
            await state.finish()

        elif elements and message.text:

            try:
                await db.update_main_req_text(main_req_text=message.text)
                await message.answer('Yangilandi', reply_markup=admin_key)
                await state.finish()
            except Exception as err:
                await message.answer(f'Faqat text ko`rinishida kiriting')

        elif message.text:
            try:
                await db.add_main_req_text(main_req_text=message.text)
                await message.answer('Qo`shildi', reply_markup=admin_key)
                await state.finish()
            except Exception as err:
                await message.answer(f'Faqat text ko`rinishida kiriting')
        else:
            await message.answer(f'Faqat text ko`rinishida kiriting')

    elif message.text == '🔙️ Orqaga':
        await message.answer('Bosh menu')
        await state.finish()
    else:
        await message.answer(f'Faqat text ko`rinishida kiriting')


@dp.message_handler(text="Taklif miqdorini kiritish")
async def change_picture(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer('Faqat son kiriting', reply_markup=back)
        await RekData.score.set()


@dp.message_handler(state=RekData.score)
async def change_picture_(message: types.Message, state: FSMContext):
    try:
        text = int(message.text)

        if text:
            elements = await db.get_elements()
            if elements:
                await db.update_limit_score(limit_score=text)
                await message.answer('Yangilandi', reply_markup=admin_key)
                await state.finish()
        elif message.text == '/start':
            await message.answer('Bosh menu')
            await state.finish()

    except Exception as err:
        if message.text == '/start':
            await message.answer('Bosh menu')
            await state.finish()

        if message.text == '🔙️ Orqaga':
            await message.answer('Bosh menu', reply_markup=admin_key)
            await state.finish()
        else:
            await message.answer('Faqat Son qabul qilamiz')


@dp.message_handler(text="Taklif chegarasini kiritish")
async def limit_count(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer('Faqat son kiriting', reply_markup=back)
        await RekData.limit.set()


@dp.message_handler(state=RekData.limit)
async def limit(message: types.Message, state: FSMContext):
    try:
        if message.text != '/start' or message.text != '🔙️ Orqaga':
            elements = await db.get_elements()
            limit = int(message.text)
            if elements:
                await db.update_limit_require(limit_require=limit)
                await message.answer('Yangilandi', reply_markup=admin_key)
                await state.finish()
            else:
                await db.add_limit_require(limit_score=limit)
                await message.answer('Qo`shildi', reply_markup=admin_key)
                await state.finish()
        elif message.text == '/start':
            await message.answer('Bosh menu')
            await state.finish()

        elif message.text == '🔙️ Orqaga':
            await message.answer('Bosh menu')
            await state.finish()
    except Exception as err:
        print(err)
        await message.answer('Faqat Son qabul qilamiz')


@dp.message_handler(text='Faqat Hisobni 0 ga tushirish')
async def channels(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer('Aniqmi\n\n'
                             'yes or no', reply_markup=types.ReplyKeyboardMarkup())
        await RekData.score_0.set()


@dp.message_handler(state=RekData.score_0)
async def channels(message: types.Message, state: FSMContext):
    if message.text == 'yes':
        try:
            await db.update_users_all_score()
            await db.update_users_all_args()
            await message.answer(f"Hisoblar 0 ga tushirildi", reply_markup=admin_key)
            await state.finish()
        except Exception as err:
            await message.answer(f"Muammo yuzaga keldi\n\n{err}")
    else:
        await state.finish()
        await message.answer('Bosh menu', reply_markup=admin_key)


@dp.message_handler(text='link berish')
async def show_channels(message: types.Message, state: FSMContext):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer('boshlandi')
        elements = await db.get_elements()
        chat_id = ''
        for element in elements:
            chat_id += f"{element['channel_id']}"
        select_all_users = await db.select_all_users()
        for i in select_all_users:
            if i['score'] > 9:
                is_sub = await subscription.check(user_id=message.from_user.id,
                                                  channel=f'{chat_id}')
                if is_sub is False:
                    try:
                        one_time_link = await create_link()
                        create_invite_link = one_time_link["invite_link"]

                        await bot.send_message(chat_id=i['telegram_id'], text=f'Birmarttalik link:\n'
                                                                              f'{create_invite_link}',
                                               protect_content=True)
                    except Exception as err:
                        one_time_link = await create_link()
                        create_invite_link = one_time_link["invite_link"]

                        await bot.send_message(chat_id=i['telegram_id'], text=f'Birmarttalik link:\n'
                                                                              f'{create_invite_link}',
                                               protect_content=True)
            await asyncio.sleep(1)
        await message.answer('tugadi')


@dp.message_handler(text="Barcha ma'lumotlarni tozalash")
async def drop_lessons_db(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await db.drop_lessons()
        await db.create_table_lessons()
        await message.answer("Tozalandi")


@dp.message_handler(text='Remove File')
async def add_channel(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer(
            text="Barcha ma'lumotlar o'chadi\n\nBarchasiga rozimisiz\n\nHa bo'lsa file_unique_id ni kiriting",
            reply_markup=back
        )
        await Lesson.les_del.set()


@dp.message_handler(state=Lesson.les_del)
async def del_button(message: types.Message, state: FSMContext):
    txt = message.text
    unique_id = []

    lessons = await db.select_lessons()
    for i in lessons:
        unique_id.append(i['id'])
    if txt == '🔙️ Orqaga':
        await message.answer('Admin panel', reply_markup=admin_key)
        await state.finish()
    elif int(message.text) in unique_id:
        try:
            await db.delete_lesson(id=int(message.text))
            await message.answer("O'chirildi", reply_markup=admin_key)
            await state.finish()
        except Exception as err:
            await message.answer('Bunday ma`lumot topilmadi')
    else:
        await message.answer('Xato\n\nBunday id yo`q\n\nChiqish uchun orqaga tugmasini bosing')
        

# Excel File Handler
# @dp.message_handler(text='Excel File')
# async def excel_file_handler(message: types.Message):
#     """Handle Excel file generation"""
#     try:
#         users = await db.select_all_users()
        
#         if not users:
#             await message.answer("❌ Foydalanuvchilar topilmadi!")
#             return
        
#         # Create Excel file content
#         excel_content = "ID,Full Name,Username,Phone,Score,Status,Created At\n"
        
#         for user in users:
#             excel_content += f"{user[0]},{user[1]},{user[2] or 'N/A'},{user[3] or 'N/A'},{user[4]},{user[8] or 'N/A'},{user[9] or 'N/A'}\n"
        
#         # Save to file
#         filename = f"users_export_{message.from_user.id}.csv"
#         with open(filename, 'w', encoding='utf-8') as f:
#             f.write(excel_content)
        
#         # Send file
#         with open(filename, 'rb') as f:
#             await message.answer_document(
#                 document=f,
#                 caption=f"📊 <b>Foydalanuvchilar ro'yxati</b>\n\n"
#                         f"Jami foydalanuvchilar: <b>{len(users)}</b> ta\n"
#                         f"Fayl formati: CSV"
#             )
        
#         # Clean up
#         import os
#         os.remove(filename)
        
#     except Exception as e:
#         await message.answer(f"❌ Xatolik yuz berdi: {str(e)}")


# Raqamlar soni Handler
@dp.message_handler(text='Statistika 📊')
async def numbers_count_handler(message: types.Message):
    """Show numbers count statistics"""
    try:
        
        # Get all users count
        all_users_count = await db.count_users()
        active_users_count = await db.count_active_users()
        block_users_count = await db.count_block_users()
        
        # Get test statistics
        tests = await db.get_all_tests()
        total_tests = len(tests) if tests else 0
        
        # Get total test attempts
        total_attempts = 0
        if tests:
            for test in tests:
                stats = await db.get_test_statistics(test['id'])
                total_attempts += stats['total_attempts'] if stats['total_attempts'] else 0
        
        text = f"📊 <b>Bot statistikasi</b>\n\n"
        text += f"👥 <b>Foydalanuvchilar:</b>\n"
        text += f"• Jami: <b>{all_users_count}</b> ta\n"
        text += f"• Faol: <b>{active_users_count}</b> ta\n"
        text += f"• Bloklangan: <b>{block_users_count}</b> ta\n\n"
        text += f"📝 <b>Testlar:</b>\n"
        text += f"• Jami testlar: <b>{total_tests}</b> ta\n"
        text += f"• Jami urinishlar: <b>{total_attempts}</b> ta\n\n"
        text += f"📅 <b>Oxirgi yangilanish:</b> {message.date.strftime('%d.%m.%Y %H:%M')}"
        
        await message.answer(text, reply_markup=admin_key)
        
    except Exception as e:
        await message.answer(f"❌ Xatolik yuz berdi: {str(e)}")


# G'olibni topish Handler
@dp.message_handler(text="🏆 G'olibni topish")
async def find_winner_handler(message: types.Message):
    """Find and display winner"""
    try:
        # Get elements to determine winner criteria
        elements = await db.get_elements()
        winner_ball = 0
        for i in elements:
            winner_ball += int(i["winners"])
        
        # Get top users
        top_users = await db.select_top_users(winner_ball)
        
        if not top_users:
            await message.answer("❌ G'olib topilmadi! Hech qanday foydalanuvchi topilmadi.")
            return
        
        text = f"🏆 <b>G'oliblar ro'yxati</b>\n\n"
        text += f"G'olib bo'lish uchun minimum ball: <b>{winner_ball}</b>\n\n"
        
        for i, user in enumerate(top_users, 1):
            text += f"{i}. <b>{user[1]}</b>\n"
            text += f"   Username: @{user[2] or 'N/A'}\n"
            text += f"   Ball: <b>{user[4]}</b>\n"
            text += f"   ID: <code>{user[6]}</code>\n\n"
        
        await message.answer(text, reply_markup=admin_key)
        
    except Exception as e:
        await message.answer(f"❌ Xatolik yuz berdi: {str(e)}")


