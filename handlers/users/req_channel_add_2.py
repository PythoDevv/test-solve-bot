from loader import dp, db
from aiogram import types
from data.config import ADMINS
from aiogram.dispatcher import FSMContext
from states.rekStates import Number, DelUser
from aiogram.dispatcher.filters import BoundFilter


class IsGroup(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return message.chat.type in (
            types.ChatType.GROUP,
            types.ChatType.SUPERGROUP,
        )


class IsPrivate(BoundFilter):
    async def check(self, message: types.Message):
        return message.chat.type == types.ChatType.PRIVATE


@dp.message_handler(commands=['del'])
async def delete_user(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer('Id ni kiriting')
        await DelUser.user.set()


@dp.message_handler(state=DelUser.user)
async def delete(message: types.Message, state: FSMContext):
    await db.delete_users(telegram_id=int(f'{message.text}'))
    await message.answer('O"chirildi')
    await state.finish()


@dp.chat_join_request_handler()
async def new_chat_member(req: types.ChatJoinRequest):
    chanel_1 = ''
    chanel_2 = ''
    chanel_3 = ''
    chanel_4 = ''
    chanel_5 = ''
    chanel_6 = ''
    chanel_7 = ''
    chanel_8 = ''
    chanel_9 = ''
    counter = 1
    requested_link = f"{req.invite_link['invite_link']}"
    requested_user = await db.get_requested_users(telegram_id=req.from_user.id)
    channels = await db.select_req_j_chanel()

    if requested_user and channels:
        for i in channels:
            channel = i['url']
            if counter == 1:
                chanel_1 = f"{channel[:22]}..."
            if counter == 2:
                chanel_2 = f"{channel[:22]}..."
            if counter == 3:
                chanel_3 = f"{channel[:22]}..."
            if counter == 4:
                chanel_4 = f"{channel[:22]}..."
            if counter == 5:
                chanel_5 = f"{channel[:22]}..."
            if counter == 6:
                chanel_6 = f"{channel[:22]}..."
            if counter == 7:
                chanel_7 = f"{channel[:22]}..."
            if counter == 8:
                chanel_7 = f"{channel[:22]}..."
            if counter == 9:
                chanel_9 = f"{channel[:22]}..."
            counter += 1
    if requested_link == chanel_1:
        await db.update_url_1(url_1='yes', telegram_id=req.from_user.id)
    elif requested_link == chanel_2:
        await db.update_url_2(url_2='yes', telegram_id=req.from_user.id)
    elif requested_link == chanel_3:
        await db.update_url_3(url_3='yes', telegram_id=req.from_user.id)
    elif requested_link == chanel_4:
        await db.update_url_4(url_4='yes', telegram_id=req.from_user.id)
    elif requested_link == chanel_5:
        await db.update_url_5(url_5='yes', telegram_id=req.from_user.id)
    elif requested_link == chanel_6:
        await db.update_url_6(url_6='yes', telegram_id=req.from_user.id)
    elif requested_link == chanel_7:
        await db.update_url_7(url_7='yes', telegram_id=req.from_user.id)
    elif requested_link == chanel_8:
        await db.update_url_8(url_8='yes', telegram_id=req.from_user.id)
    elif requested_link == chanel_9:
        await db.update_url_9(url_9='yes', telegram_id=req.from_user.id)

    elif not requested_user and channels:
        for i in channels:
            channel = i['url']
            if counter == 1:
                chanel_1 = f"{channel[:22]}..."
            if counter == 2:
                chanel_2 = f"{channel[:22]}..."
            if counter == 3:
                chanel_3 = f"{channel[:22]}..."
            if counter == 4:
                chanel_4 = f"{channel[:22]}..."
            if counter == 5:
                chanel_5 = f"{channel[:22]}..."
            if counter == 6:
                chanel_6 = f"{channel[:22]}..."
            if counter == 7:
                chanel_7 = f"{channel[:22]}..."
            if counter == 8:
                chanel_8 = f"{channel[:22]}..."
            if counter == 9:
                chanel_9 = f"{channel[:22]}..."
            counter += 1

        if requested_link == chanel_1:
            await db.update_url_1(url_1='yes', telegram_id=req.from_user.id)
        elif requested_link == chanel_2:
            await db.update_url_2(url_2='yes', telegram_id=req.from_user.id)
        elif requested_link == chanel_3:
            await db.update_url_3(url_3='yes', telegram_id=req.from_user.id)
        elif requested_link == chanel_4:
            await db.update_url_4(url_4='yes', telegram_id=req.from_user.id)
        elif requested_link == chanel_5:
            await db.update_url_5(url_5='yes', telegram_id=req.from_user.id)
        elif requested_link == chanel_6:
            await db.update_url_6(url_6='yes', telegram_id=req.from_user.id)
        elif requested_link == chanel_7:
            await db.update_url_7(url_7='yes', telegram_id=req.from_user.id)
        elif requested_link == chanel_8:
            await db.update_url_8(url_8='yes', telegram_id=req.from_user.id)
        elif requested_link == chanel_9:
            await db.update_url_9(url_9='yes', telegram_id=req.from_user.id)


@dp.message_handler(text='fix', user_id=ADMINS)
async def update_scoreee(message: types.Message):
    await message.answer('id va balni kiriting')
    await Number.add_user.set()


@dp.message_handler(state=Number.add_user)
async def fixx(message: types.Message, state: FSMContext):
    user_text = message.text.split(',')
    await db.update_user_score(score=int(user_text[0]), telegram_id=int(user_text[1]))
    await message.answer('bo`ldi')
    await state.finish()


@dp.message_handler(commands=['upscore'])
async def delete_user(message: types.Message, state: FSMContext):
    await db.update_user_score(score=0, telegram_id=message.from_user.id)
    await message.answer('0')
