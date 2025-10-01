import asyncio
from aiogram import types

from loader import dp, db, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import BoundFilter

from states.rekStates import RekData


class IsGroup(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return message.chat.type in (
            types.ChatType.GROUP,
            types.ChatType.SUPERGROUP,
        )


class IsPrivate(BoundFilter):
    async def check(self, message: types.Message):
        return message.chat.type == types.ChatType.PRIVATE


@dp.message_handler(text='dblink')
async def create_link_manually(message: types.Message):
    if message.from_user.id == 935795577:
        for_winner_gifts = await db.select_related_lessons(button_name="""G'olibga""")
        if for_winner_gifts:
            for winner_gift in for_winner_gifts:
                if winner_gift[6]:
                    db_links = await db.select_one_time_all_links(private_channel_id=winner_gift[8])
                    safe_db_links = db_links
                    safe_winner_gift_id = str(winner_gift[8])
                    await message.answer(
                        f"Bazada - {safe_db_links}ta link bor.\nKanal id - {safe_winner_gift_id[1:]}"
                    )

@dp.message_handler(text='gogogo')
async def create_link_manually(message: types.Message):
    if message.from_user.id == 935795577:
        await bot.send_message(chat_id=935795577,text='boshlandi')
        for_winner_gifts = await db.select_related_lessons(button_name="""G'olibga""")
        if for_winner_gifts:
            for winner_gift in for_winner_gifts:
                if winner_gift[6]:
                    for i in range(1000):
                        create_invite_link = await bot.create_chat_invite_link(chat_id=winner_gift[8], member_limit=1)
                        await db.add_one_time_link(create_invite_link['invite_link'], private_channel_id=winner_gift[8])
                        await asyncio.sleep(30)


async def create_link():
    elements = await db.get_elements()
    chat_id = ''

    for element in elements:
        chat_id += f"{element['channel_id']}"

    create_invite_link = await bot.create_chat_invite_link(chat_id=chat_id, member_limit=1)
    return create_invite_link


@dp.message_handler(state=RekData.number_phone, content_types=types.ContentTypes.CONTACT)
async def show_channels(message: types.Message, state: FSMContext):
    limit_require = 0
    score = 0
    elements = await db.get_elements()
    chat_id = ''

    for element in elements:
        score += element['limit_score']
        limit_require += element['limit_require']
        chat_id += f"{element['channel_id']}"

    if state:
        await state.finish()
    user = await db.select_user(telegram_id=message.from_user.id)
    user_number = f"{message.contact.phone_number}"
    if user_number.startswith("+998") or user_number.startswith("998"):
        if user[3] == "---":
            await db.update_user_phone(
                phone=message.contact.phone_number,
                telegram_id=message.from_user.id,
            )
            if user[5] == "new":
                try:
                    args = await db.select_user(telegram_id=message.from_user.id)
                    args_user = await db.select_user(telegram_id=int(args[7]))
                    update_score = int(args_user[4]) + score
                    await db.update_user_score(score=update_score, telegram_id=int(args[7]))

                    await bot.send_message(chat_id=int(args[7]),
                                           text=f"👤 Yangi ishtirokchi qo`shildi\n"
                                                f"🎗 Siz <b>{update_score}ta</b> foydalanuvchi taklif qildingiz\n"
                                                f"🗣 Ko`proq do`stlaringizni taklif qiling!")
                    if update_score == limit_require:
                        # lessons = await db.select_related_lessons(button_name="""G'oliblarga""")
                        try:
                            one_time_link = await create_link()
                            create_invite_link = one_time_link["invite_link"]
                        except Exception as err:
                            one_time_link = await db.select_one_time_link()
                            create_invite_link = one_time_link[0][3]

                            await db.update_one_time_link_column(telegram_id=message.from_user.id,
                                                                 link=create_invite_link)
                        # for i in lessons:
                        #     if i[2] == 'video':
                        #         await bot.send_video(chat_id=int(args[7]), video=f"{i[3]}", caption=f'{i[5]}\n\n'
                        #                                                                             f'{create_invite_link}')
                        #     elif i[2] == 'document':
                        #         await bot.send_document(chat_id=int(args[7]), document=f"{i[3]}", caption=f'{i[5]}\n\n'
                        #                                                                                   f'{create_invite_link}')
                        #     elif i[2] == 'audio':
                        #         await bot.send_audio(chat_id=int(args[7]), audio=f"{i[3]}", caption=f'{i[5]}\n\n'
                        #                                                                             f'{create_invite_link}')
                        #     elif i[2] == 'photo':
                        #         await bot.send_photo(chat_id=int(args[7]), photo=f"{i[3]}", caption=f'{i[5]}\n\n'
                        #                                                                             f'{create_invite_link}')
                        #     elif i[2] == 'text':
                        await bot.send_message(chat_id=int(args[7]), text=f'Tabriklaymi Siz Barcha Shartlarni Bajardingiz\n'
                                                                          f'Yopiq Kanal uchun link 👇\n\n'
                                                                          f'{create_invite_link}',
                                               )
                    await db.update_user_oldd(oldd='not', telegram_id=message.from_user.id)
                except Exception as e:
                    print(e, 'check_sub_err')
            lessons = await db.select_related_lessons(button_name="Obunadan so'ng")
            button_score = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button_score.add(types.KeyboardButton(text="🎗 Ballarim"))
            await message.answer("🎉 Tabriklaymiz! Siz loyihamizga to'liq ro'yxatdan o'tdingiz!\n\n"
                                 "Ballaringizni ko`rish uchun '🎗 Ballarim' tugmasini bosing",
                                 reply_markup=button_score)
            if lessons:
                for i in lessons:
                    if i[2] == 'video':
                        await message.answer_video(video=f"{i[3]}", caption=f'{i[5]}', reply_markup=link)
                    elif i[2] == 'document':
                        await message.answer_document(document=f"{i[3]}", caption=f'{i[5]}', reply_markup=link)
                    elif i[2] == 'audio':
                        await message.answer_audio(audio=f"{i[3]}", caption=f'{i[5]}', reply_markup=link)
                    elif i[2] == 'photo':
                        await message.answer_photo(photo=f"{i[3]}", caption=f'{i[5]}', reply_markup=link)
                    elif i[2] == 'text':
                        await message.answer(f'{i[5]}', reply_markup=link)
