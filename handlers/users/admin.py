import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from handlers.users.main import create_link
from data.config import ADMINS
from keyboards.default.rekKeyboards import back, admin_key
from loader import dp, db, bot
from states.rekStates import RekData


@dp.message_handler(text="O'chirish uchun mahsus kodlar")
async def bot_start(message: types.Message, state: FSMContext):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        for_winner_gifts = await db.select_lessons()
        if for_winner_gifts:
            for winner_gift in for_winner_gifts:
                unique = winner_gift['id']
                text = winner_gift[5] + '\n\no`chirish uchun mahsus kodlar --- <code>' + str(unique) + '</code>\n\n'
                if winner_gift[6]:
                    try:
                        one_time_link = await create_link(private_channel_id=winner_gift[8])
                        create_invite_link = one_time_link["invite_link"]
                    except Exception as err:
                        one_time_link = await db.select_one_time_link()
                        create_invite_link = one_time_link[0][3]

                        await db.update_one_time_link_column(telegram_id=message.from_user.id,
                                                             link=create_invite_link)
                    text = text.replace('{link}', create_invite_link)
                if winner_gift[2] == 'video':
                    await bot.send_video(chat_id=message.from_user.id, video=f"{winner_gift[3]}", caption=text)
                elif winner_gift[2] == 'document':
                    await bot.send_document(chat_id=message.from_user.id, document=f"{winner_gift[3]}", caption=text)
                elif winner_gift[2] == 'audio':
                    await bot.send_audio(chat_id=message.from_user.id, audio=f"{winner_gift[3]}", caption=text)
                elif winner_gift[2] == 'photo':
                    await bot.send_photo(chat_id=message.from_user.id, photo=f"{winner_gift[3]}", caption=text)
                elif winner_gift[2] == 'text':
                    await bot.send_message(chat_id=message.from_user.id, text=text)
                await asyncio.sleep(0.05)


@dp.message_handler(text='Post Yuborish 🗒')
async def bot_start(msg: types.Message, state: FSMContext):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if msg.from_user.id in admins_list:
        await msg.answer("<b>Xabarni ni yuboring</b>", reply_markup=back)
        await RekData.choice.set()


@dp.message_handler(content_types=['video', 'audio', 'voice', 'photo', 'document', 'text'],
                    state=RekData.choice)
async def contumum(msg: types.Message, state: FSMContext):
    if msg.text == '🔙️ Orqaga':
        await msg.answer('Bekor qilindi', reply_markup=admin_key)
        await state.finish()

    elif msg.video or msg.audio or msg.voice or msg.document or msg.photo or msg.text:
        if msg.text == 'Barchaga Xabar Yuborish 🗒':
            await msg.answer('Adashdingiz Shekilli\n\n'
                             'To`g`ri ma`lumot kirting')
        else:
            await state.finish()

            in_active_users = await db.count_block_users()
            active_users = await db.select_all_active_users()
            count_baza = await db.count_users()
            await msg.answer('Xabar yuborish boshlandi.')
            extra_block_users = 0
            message_sended_users = 0
            for user in active_users:
                try:
                    await msg.send_copy(chat_id=user[0])
                    message_sended_users +=1
                except Exception as err:
                    await db.update_user_status("block", user[0])
                    extra_block_users +=1
                await asyncio.sleep(0.04)
            await msg.answer(f"Yuborilganlar: <b>{message_sended_users}</b> та."
                             f"\n\nYuborilmaganlar: <b>{in_active_users + extra_block_users}</b> та."
                             f"\n\nBazada jami: <b>{count_baza}</b> та"
                             f" foydalanuvchi mavjud.", reply_markup=admin_key
                             )


@dp.message_handler(text='Mahsus Xabarni Yuborish 🗒', user_id=ADMINS)
async def bot_start(msg: types.Message, state: FSMContext):
    await msg.answer("<b>Xabarni yuboring</b>", reply_markup=back)
    await RekData.special.set()


@dp.message_handler(content_types=['video', 'audio', 'voice', 'photo', 'document', 'text'], user_id=ADMINS,
                    state=RekData.special)
async def contumum(msg: types.Message, state: FSMContext):
    elements = await db.get_elements()

    winner_ball = 0
    for i in elements:
        winner_ball += int(i["winners"])

    if msg.text == '🔙️ Orqaga':
        await msg.answer('Bekor qilindi', reply_markup=admin_key)
        await state.finish()

    elif msg.video or msg.audio or msg.voice or msg.document or msg.photo or msg.text:
        if msg.text == 'Mahsus Xabarni Yuborish 🗒':
            await msg.answer('Adashdingiz Shekilli\n\n'
                             'To`g`ri ma`lumot kirting')
        else:
            await state.finish()

            users = await db.select_all_users()
            count_baza = await db.count_users()
            count_err = 0
            count = 0
            for user in users:
                if user[4] <= winner_ball:
                    continue
                    # print('aaa')
                else:
                    try:
                        await msg.send_copy(chat_id=user[6])
                        count += 1
                        await asyncio.sleep(0.05)

                    except Exception as err:
                        count_err += 1
                        await asyncio.sleep(0.05)

            await msg.answer(f"Ҳабар юборилганлар: <b>{count}</b> та.", reply_markup=admin_key
                             )


