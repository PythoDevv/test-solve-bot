import asyncpg
import asyncio
from aiogram import types

from keyboards.default.all import number
from loader import dp, db, bot
from states.rekStates import RekData, UserData
from utils.misc import subscription
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.filters import CommandStart


@dp.message_handler(text='link')
async def get_link(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        for_winner_gifts = await db.select_related_lessons(button_name="""G'olibga""")
        if for_winner_gifts:
            for winner_gift in for_winner_gifts:
                text = winner_gift[5]
                if winner_gift[6]:
                    try:
                        one_time_link = await create_link(private_channel_id=winner_gift[8])
                        create_invite_link = one_time_link["invite_link"]
                    except Exception as err:
                        one_time_link = await db.select_one_time_link(private_channel_id=winner_gift[8])
                        if one_time_link:
                            create_invite_link = one_time_link[0][3]

                            await db.update_one_time_link_column(telegram_id=message.from_user.id,
                                                                link=create_invite_link)
                        else:
                            create_invite_link = "Link olishda muammo yuzaga keldi.\nIltimos, admin bilan bog'laning 👇\n\nAdmin - @Ilyosbek_Kv"
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


class IsGroup(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return message.chat.type in (
            types.ChatType.GROUP,
            types.ChatType.SUPERGROUP,
        )


class IsPrivate(BoundFilter):
    async def check(self, message: types.Message):
        return message.chat.type == types.ChatType.PRIVATE


async def create_link(private_channel_id):
    create_invite_link = await bot.create_chat_invite_link(chat_id=private_channel_id, member_limit=1)
    return create_invite_link


@dp.message_handler(IsPrivate(), CommandStart(), state='*')
async def show_channels(message: types.Message, state: FSMContext):
    if state:
        await state.finish()
    requested_user_is_subscribe = await db.get_requested_users(telegram_id=message.from_user.id)
    channels = await db.select_req_j_chanel()
    if requested_user_is_subscribe:
        list_chanel_id = []
        for channel in channels:
            list_chanel_id.append(channel['channel_id'])
        is_join = {
            'chanel_1': '',
            'chanel_2': '',
            'chanel_3': '',
            'chanel_4': '',
            'chanel_5': '',
            'chanel_6': '',
            'chanel_7': '',
            'chanel_8': '',
            'chanel_9': '',

        }

        join_counter = 0
        for channel in list_chanel_id:
            check_subscription = await subscription.check(user_id=message.from_user.id,
                                                          channel=channel)
            join_counter += 1
            is_join[f'chanel_{join_counter}'] = check_subscription
        if is_join:
            if is_join[f'chanel_1'] == 1:
                await db.update_url_1(url_1='yes', telegram_id=message.from_user.id)
            if is_join[f'chanel_2'] == 1:
                await db.update_url_2(url_2='yes', telegram_id=message.from_user.id)
            if is_join[f'chanel_3'] == 1:
                await db.update_url_3(url_3='yes', telegram_id=message.from_user.id)
            if is_join[f'chanel_4'] == 1:
                await db.update_url_4(url_4='yes', telegram_id=message.from_user.id)
            if is_join[f'chanel_5'] == 1:
                await db.update_url_5(url_5='yes', telegram_id=message.from_user.id)
            if is_join[f'chanel_6'] == 1:
                await db.update_url_6(url_6='yes', telegram_id=message.from_user.id)
            if is_join[f'chanel_7'] == 1:
                await db.update_url_7(url_7='yes', telegram_id=message.from_user.id)
            if is_join[f'chanel_8'] == 1:
                await db.update_url_8(url_8='yes', telegram_id=message.from_user.id)
            if is_join[f'chanel_9'] == 1:
                await db.update_url_9(url_9='yes', telegram_id=message.from_user.id)

    else:
        try:
            await db.add_requested_users(telegram_id=message.from_user.id)
        except Exception as err:
            pass
        list_chanel_id = []
        for channel in channels:
            list_chanel_id.append(channel['channel_id'])
        is_join = {
            'chanel_1': '',
            'chanel_2': '',
            'chanel_3': '',
            'chanel_4': '',
            'chanel_5': '',
            'chanel_6': '',
            'chanel_7': '',
            'chanel_8': '',
            'chanel_9': '',

        }

        join_counter = 0
        for channel in list_chanel_id:
            check_subscription = await subscription.check(user_id=message.from_user.id,
                                                          channel=channel)
            join_counter += 1
            is_join[f'chanel_{join_counter}'] = check_subscription
        if is_join:
            if is_join[f'chanel_1'] == 1:
                await db.update_url_1(url_1='yes', telegram_id=message.from_user.id)
            if is_join[f'chanel_2'] == 1:
                await db.update_url_2(url_2='yes', telegram_id=message.from_user.id)
            if is_join[f'chanel_3'] == 1:
                await db.update_url_3(url_3='yes', telegram_id=message.from_user.id)
            if is_join[f'chanel_4'] == 1:
                await db.update_url_4(url_4='yes', telegram_id=message.from_user.id)
            if is_join[f'chanel_5'] == 1:
                await db.update_url_5(url_5='yes', telegram_id=message.from_user.id)
            if is_join[f'chanel_6'] == 1:
                await db.update_url_6(url_6='yes', telegram_id=message.from_user.id)
            if is_join[f'chanel_7'] == 1:
                await db.update_url_7(url_7='yes', telegram_id=message.from_user.id)
            if is_join[f'chanel_8'] == 1:
                await db.update_url_8(url_8='yes', telegram_id=message.from_user.id)
            if is_join[f'chanel_9'] == 1:
                await db.update_url_9(url_9='yes', telegram_id=message.from_user.id)

    args = message.get_args()
    if_old = await db.select_user(telegram_id=message.from_user.id)
    elements = await db.get_elements()
    photo = ''
    chat_id = ''
    score = 1
    for element in elements:
        photo += f"{element['photo']}"
        chat_id += f"{element['channel_id']}"
        score += element['limit_score']
    requested_user = await db.get_requested_users(telegram_id=message.from_user.id)
    buttons_list = []
    button = types.InlineKeyboardMarkup(row_width=1, )

    if requested_user:
        counter = 1
        for channel in channels:
            if requested_user[0][counter] != 'yes':
                buttons_dict = {}
                buttons_dict['button_name'] = channel['channel_name']
                buttons_dict['url'] = channel['url']
                buttons_dict['order_button'] = channel['order_button']
                buttons_list.append(buttons_dict)
            counter += 1
    else:
        for channel in channels:
            buttons_dict = {}
            buttons_dict['button_name'] = channel['channel_name']
            buttons_dict['url'] = channel['url']
            buttons_dict['order_button'] = channel['order_button']
            buttons_list.append(buttons_dict)
    button_score = types.ReplyKeyboardMarkup(resize_keyboard=True)

    len_buttons = len(buttons_list)
    try:
        user = await db.add_user(full_name=message.from_user.full_name,
                                    telegram_id=message.from_user.id,
                                    username=message.from_user.username,
                                    phone='---',
                                    oldd='new',
                                    user_args=f"{args}"
                                    )
    except asyncpg.exceptions.UniqueViolationError:
        user = await db.select_user(telegram_id=message.from_user.id)
    await db.update_user_args(user_args=f'{args}', telegram_id=message.from_user.id)

    status = True
    all = await db.select_chanel()
    chanels = []
    url = []
    channel_names = []
    add_list_channel = await db.select_add_list_channels()
    add_list = await db.select_add_list()
    for add_lst in add_list:
        url.append(add_lst["url"])
        channel_names.append(add_lst["button_name"])
    for channel in add_list_channel:
        chanels.append(channel["url"])

    for i in all:
        chanels.append({
            'chanelll': f"@{i['chanelll']}",
            'url': i['url'],
            'channel_name': i['channel_name'],
            'order_button': i['order_button']
        })

    for channel in chanels:
        is_subscribe = await subscription.check(user_id=message.from_user.id,
                                            channel=channel['chanelll'])
        if not is_subscribe:
            buttons_dict = {}
            buttons_dict['button_name'] = channel['channel_name']
            buttons_dict['url'] = channel['url']
            buttons_dict['order_button'] = channel['order_button']
            buttons_list.append(buttons_dict)
        status *= is_subscribe
    if status and len_buttons == 0:
        # Check if user needs to provide custom fullname
        user = await db.select_user(telegram_id=message.from_user.id)
        if user and not user.get('custom_fullname'):
            await message.answer(
                "Familiya va ismingizni kiriting:",
                reply_markup=types.ReplyKeyboardMarkup(
                    keyboard=[[types.KeyboardButton(text='🔙️ Orqaga')]],
                    resize_keyboard=True
                )
            )
            await UserData.custom_fullname.set()
            return
        
        button_score.add(types.KeyboardButton(text="📝 Testlarga Javob Berish"))
        button_score.add(types.KeyboardButton(text="❓ Test Yordam"))
        button_score.add(types.KeyboardButton(text="📋 Topshirgan testlarim"))

        lessons = await db.select_related_lessons(button_name="Obunadan so'ng")

        if lessons:
            for i in lessons:
                if i[2] == 'video':
                    await message.answer_video(video=f"{i[3]}", caption=f'{i[5]}', reply_markup=button_score)
                elif i[2] == 'document':
                    await message.answer_document(document=f"{i[3]}", caption=f'{i[5]}', reply_markup=button_score)
                elif i[2] == 'audio':
                    await message.answer_audio(audio=f"{i[3]}", caption=f'{i[5]}', reply_markup=button_score)
                elif i[2] == 'photo':
                    await message.answer_photo(photo=f"{i[3]}", caption=f'{i[5]}', reply_markup=button_score)
                elif i[2] == 'text':
                    await message.answer(f'{i[5]}', reply_markup=button_score)
    else:
        tugmalar = await db.select_tugma()
        if tugmalar:
            for tugma in tugmalar:
                buttons_dict = {}
                buttons_dict['button_name'] = tugma['link_name']
                buttons_dict['url'] = tugma['link']
                buttons_dict['order_button'] = tugma['order_button']
                buttons_list.append(buttons_dict)
        sorted_data = sorted(buttons_list, key=lambda x: x['order_button'])

        for i in sorted_data:
            button.add(types.InlineKeyboardButton(i['button_name'], url=i['url']))
        button.add(types.InlineKeyboardButton(text="✅ А'zo boʼldim", callback_data="check_subs"))
        lessons = await db.select_related_lessons(button_name="Majburiy obuna")

        if lessons:
            for i in lessons:
                text = i[5].replace('{ism}', f'{message.from_user.full_name}')
                if i[2] == 'video':
                    await message.answer_video(video=f"{i[3]}", caption=text, reply_markup=button)
                elif i[2] == 'document':
                    await message.answer_document(document=f"{i[3]}", caption=text, reply_markup=button)
                elif i[2] == 'audio':
                    await message.answer_audio(audio=f"{i[3]}", caption=text, reply_markup=button)
                elif i[2] == 'photo':
                    await message.answer_photo(photo=f"{i[3]}", caption=text, reply_markup=button)
                elif i[2] == 'text':
                    await message.answer(text, reply_markup=button)



@dp.callback_query_handler(text="check_subs")
async def checker(call: types.CallbackQuery, state: FSMContext):
    requested_user_is_subscribe = await db.get_requested_users(telegram_id=call.from_user.id)
    channels = await db.select_req_j_chanel()
    if requested_user_is_subscribe:
        list_chanel_id = []
        for channel in channels:
            list_chanel_id.append(channel['channel_id'])
        is_join = {
            'chanel_1': '',
            'chanel_2': '',
            'chanel_3': '',
            'chanel_4': '',
            'chanel_5': '',
            'chanel_6': '',
            'chanel_7': '',
            'chanel_8': '',
            'chanel_9': '',

        }

        join_counter = 0
        for channel in list_chanel_id:
            check_subscription = await subscription.check(user_id=call.from_user.id,
                                                          channel=channel)
            join_counter += 1
            is_join[f'chanel_{join_counter}'] = check_subscription
        if is_join[f'chanel_1'] == 1:
            await db.update_url_1(url_1='yes', telegram_id=call.from_user.id)
        if is_join[f'chanel_2'] == 1:
            await db.update_url_2(url_2='yes', telegram_id=call.from_user.id)
        if is_join[f'chanel_3'] == 1:
            await db.update_url_3(url_3='yes', telegram_id=call.from_user.id)
        if is_join[f'chanel_4'] == 1:
            await db.update_url_4(url_4='yes', telegram_id=call.from_user.id)
        if is_join[f'chanel_5'] == 1:
            await db.update_url_5(url_5='yes', telegram_id=call.from_user.id)
        if is_join[f'chanel_6'] == 1:
            await db.update_url_6(url_6='yes', telegram_id=call.from_user.id)
        if is_join[f'chanel_7'] == 1:
            await db.update_url_7(url_7='yes', telegram_id=call.from_user.id)
        if is_join[f'chanel_8'] == 1:
            await db.update_url_8(url_8='yes', telegram_id=call.from_user.id)
        if is_join[f'chanel_9'] == 1:
            await db.update_url_9(url_9='yes', telegram_id=call.from_user.id)

    else:
        try:
            await db.add_requested_users(telegram_id=call.from_user.id)
        except Exception as err:
            pass
        list_chanel_id = []
        for channel in channels:
            list_chanel_id.append(channel['channel_id'])
        is_join = {
            'chanel_1': '',
            'chanel_2': '',
            'chanel_3': '',
            'chanel_4': '',
            'chanel_5': '',
            'chanel_6': '',
            'chanel_7': '',
            'chanel_8': '',
            'chanel_9': '',
        }

        join_counter = 0
        for channel in list_chanel_id:
            check_subscription = await subscription.check(user_id=call.from_user.id,
                                                          channel=channel)
            join_counter += 1
            is_join[f'chanel_{join_counter}'] = check_subscription
        if is_join[f'chanel_1'] == 1:
            await db.update_url_1(url_1='yes', telegram_id=call.from_user.id)
        if is_join[f'chanel_2'] == 1:
            await db.update_url_2(url_2='yes', telegram_id=call.from_user.id)
        if is_join[f'chanel_3'] == 1:
            await db.update_url_3(url_3='yes', telegram_id=call.from_user.id)
        if is_join[f'chanel_4'] == 1:
            await db.update_url_4(url_4='yes', telegram_id=call.from_user.id)
        if is_join[f'chanel_5'] == 1:
            await db.update_url_5(url_5='yes', telegram_id=call.from_user.id)
        if is_join[f'chanel_6'] == 1:
            await db.update_url_6(url_6='yes', telegram_id=call.from_user.id)
        if is_join[f'chanel_7'] == 1:
            await db.update_url_7(url_7='yes', telegram_id=call.from_user.id)
        if is_join[f'chanel_8'] == 1:
            await db.update_url_8(url_8='yes', telegram_id=call.from_user.id)
        if is_join[f'chanel_9'] == 1:
            await db.update_url_9(url_9='yes', telegram_id=call.from_user.id)

    status = True
    all = await db.select_chanel()
    chanels = []
    url = []
    channel_names = []
    add_list_channel = await db.select_add_list_channels()
    add_list = await db.select_add_list()
    for add_lst in add_list:
        url.append(add_lst["url"])
        channel_names.append(add_lst["button_name"])
    for channel in add_list_channel:
        chanels.append(channel["url"])

    for i in all:
        chanels.append({
            'chanelll': f"@{i['chanelll']}",
            'url': i['url'],
            'channel_name': i['channel_name'],
            'order_button': i['order_button']
        })

    score = 1
    elements = await db.get_elements()
    photo = ''
    chat_id = ''
    for element in elements:
        score += element['limit_score']
        photo += f"{element['photo']}"
        chat_id += f"{element['channel_id']}"
    buttons_list = []

    for channel in chanels:
        is_subscribe = await subscription.check(user_id=call.from_user.id,
                                            channel=channel['chanelll'])
        if not is_subscribe:
            buttons_dict = {}
            buttons_dict['button_name'] = channel['channel_name']
            buttons_dict['url'] = channel['url']
            buttons_dict['order_button'] = channel['order_button']
            buttons_list.append(buttons_dict)
        status *= is_subscribe
    button = types.InlineKeyboardMarkup(row_width=1, )
    requested_user = await db.get_requested_users(telegram_id=call.from_user.id)
    if requested_user:
        counter = 1
        for channel in channels:
            if requested_user[0][counter] != 'yes':
                buttons_dict = {}
                buttons_dict['button_name'] = channel['channel_name']
                buttons_dict['url'] = channel['url']
                buttons_dict['order_button'] = channel['order_button']
                buttons_list.append(buttons_dict)
            counter += 1
    else:
        for channel in channels:
            buttons_dict = {}
            buttons_dict['button_name'] = channel['channel_name']
            buttons_dict['url'] = channel['url']
            buttons_dict['order_button'] = channel['order_button']
            buttons_list.append(buttons_dict)

    len_buttons = len(buttons_list)
    if status and len_buttons == 0:
        # Check if user needs to provide custom fullname
        user = await db.select_user(telegram_id=call.from_user.id)
        if user and not user.get('custom_fullname'):
            await call.message.answer(
                "Familiya va ismingizni kiriting:",
                reply_markup=types.ReplyKeyboardMarkup(
                    keyboard=[[types.KeyboardButton(text='🔙️ Orqaga')]],
                    resize_keyboard=True
                )
            )
            await UserData.custom_fullname.set()
            return
        
        lessons = await db.select_related_lessons(button_name="Obunadan so'ng")

        button_score = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_score.add(types.KeyboardButton(text="📝 Testlarga Javob Berish"))
        button_score.add(types.KeyboardButton(text="❓ Test Yordam"))
        button_score.add(types.KeyboardButton(text="📋 Topshirgan testlarim"))
        
        for i in lessons:
            if i[2] == 'video':
                await call.message.answer_video(video=f"{i[3]}", caption=f'{i[5]}', reply_markup=button_score)
            elif i[2] == 'document':
                await call.message.answer_document(document=f"{i[3]}", caption=f'{i[5]}', reply_markup=button_score)
            elif i[2] == 'audio':
                await call.message.answer_audio(audio=f"{i[3]}", caption=f'{i[5]}', reply_markup=button_score)
            elif i[2] == 'photo':
                await call.message.answer_photo(photo=f"{i[3]}", caption=f'{i[5]}', reply_markup=button_score)
            elif i[2] == 'text':
                await call.message.answer(f'{i[5]}', reply_markup=button_score)
    else:
        tugmalar = await db.select_tugma()
        if tugmalar:
            for tugma in tugmalar:
                buttons_dict = {}
                buttons_dict['button_name'] = tugma['link_name']
                buttons_dict['url'] = tugma['link']
                buttons_dict['order_button'] = tugma['order_button']
                buttons_list.append(buttons_dict)
        sorted_data = sorted(buttons_list, key=lambda x: x['order_button'])

        for i in sorted_data:
            button.add(types.InlineKeyboardButton(i['button_name'], url=i['url']))

        button.add(types.InlineKeyboardButton(text="✅ А'zo boʼldim", callback_data="check_subs"))
        lessons = await db.select_related_lessons(button_name="Majburiy obuna")

        if lessons:
            for i in lessons:
                text = i[5].replace('{ism}', f'{call.from_user.full_name}')
                if i[2] == 'video':
                    await call.message.answer_video(video=f"{i[3]}", caption=text, reply_markup=button)
                elif i[2] == 'document':
                    await call.message.answer_document(document=f"{i[3]}", caption=text, reply_markup=button)
                elif i[2] == 'audio':
                    await call.message.answer_audio(audio=f"{i[3]}", caption=text, reply_markup=button)
                elif i[2] == 'photo':
                    await call.message.answer_photo(photo=f"{i[3]}", caption=text, reply_markup=button)
                elif i[2] == 'text':
                    await call.message.answer(text, reply_markup=button)
