from aiogram import types

from aiogram.dispatcher import FSMContext

from keyboards.default.rekKeyboards import back, admin_secret_button, admin_key
from loader import dp, db
from states.rekStates import RekData


@dp.message_handler(text='Yopiq Kanal ➕')
async def add_channel(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer(text='Kanalni kiriting\n\n'
                                  'Masalan : "&&& belgi bilan ajratib:'
                                  ' chanel_id(-123123213)&&&+chanel_url&&&Kanal nomi"\n\n'
                                  '-1001798189867&&&+52bZMKjCR1jY2Qy&&&asdasd - Ko`rinishida',
                             reply_markup=back)
        await RekData.add_secret.set()


@dp.message_handler(state=RekData.add_secret)
async def add_username(message: types.Message, state: FSMContext):
    text = message.text
    if text == '🔙️ Orqaga':
        await message.answer('Yopiq Admin panel', reply_markup=admin_secret_button)
        await state.finish()
    elif text[0] == '-':
        split_chanel = message.text.split(',')
        chanel_lst = []
        url_lst = []
        channel_name_lst = []
        for i in split_chanel:
            lst = i.split('&&&')
            chanel_lst.append(lst[0])
            url_lst.append(lst[1])
            channel_name_lst.append(lst[2])

        chanel = f'{chanel_lst}'
        url = f'{url_lst}'
        channel_name = f'{channel_name_lst}'
        ch_text = chanel.replace("'", '')
        ch_text2 = ch_text.replace(" ", '')
        u_text = url.replace("'", '')
        u_text2 = u_text.replace(" ", '')
        channel_name_text = channel_name.replace("'", '')
        channel_name_text2 = channel_name_text.replace(" ", '')
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

        await db.add_req_j_channel(channel_id=ch_text2[1:-1], url=u_text2[1:-1], channel_name=channel_name_text2[1:-1],
                                   order_button=max_number+1)
        await message.answer("Qo'shildi", reply_markup=admin_secret_button)
        await state.finish()

    else:
        await message.answer(text='Kanalni kiriting\n\n'
                                  'Masalan : "&&& belgi bilan ajratib:'
                                  ' chanel_id(-123123213)&&&+chanel_url&&&Kanal nomi"\n\n'
                                  '-1001798189867&&&+52bZMKjCR1jY2Qy&&&asdasd - Ko`rinishida')


@dp.message_handler(text='Yopiq Kanal ➖')
async def add_channel(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer(text='Kanalni kiriting\n\n'
                                  'Masalan : "&&& belgi bilan ajratib:'
                                  ' chanel_id(-123123213)&&&+chanel_url&&&Kanal nomi"\n\n'
                                  '-1001798189867&&&+52bZMKjCR1jY2Qy&&&asdasd - Ko`rinishida',
                             reply_markup=back)
        await RekData.delete_secret.set()


@dp.message_handler(state=RekData.delete_secret)
async def del_username(message: types.Message, state: FSMContext):
    txt = message.text
    if txt[0] == '-':
        print(1123)
        channel = await db.get_req_j_chanel(channel_id=txt)
        print(channel)
        if not channel:
            await message.answer("Kanal topilmadi\n"
                                 "Qaytadan urinib ko'ring")

        else:
            await db.delete_req_j_channel(channel_id=txt)
            await message.answer('Kanal o"chirildi', reply_markup=admin_secret_button)
            await state.finish()
    elif txt == '🔙️ Orqaga':
        await message.answer('Admin panel', reply_markup=admin_key)
        await state.finish()


@dp.message_handler(commands=['secret_admin'])
async def admin(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer(text='Yopiq Admin panel',
                             reply_markup=admin_secret_button)


@dp.message_handler(text="Yopiq Kanallar ro'yxati 😱")
async def secret_channels(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        channels = await db.select_req_j_chanel()
        text = ''
        for channel in channels:
            text += f"{channel['channel_id']}\n"
        try:
            await message.answer(f"{text}", reply_markup=admin_secret_button)
        except:
            await message.answer(f"Kanallar mavjud emas")
