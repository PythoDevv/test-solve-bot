from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.rekKeyboards import link_button, back
from loader import db, dp
from states.rekStates import TugmaData


@dp.message_handler(commands=['tugma'])
async def tugma(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer(text='Tugma qo`shish panel',
                             reply_markup=link_button)


@dp.message_handler(text='Tugma ➕')
async def button_plus(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer(text='Malumotlarni kiriting\n'
                                  'Masalan : "&&& belgi bilan ajratib\n'
                                  ' link&&&Tugma nomi"\n\n'
                                  'https://t.me/+52bZMKjCR1jY2Qy&&&Referral link - Ko`rinishida',
                             reply_markup=back)
        await TugmaData.tugma_plus.set()


@dp.message_handler(state=TugmaData.tugma_plus)
async def add_link_button(message: types.Message, state: FSMContext):
    text = message.text
    if text == '🔙️ Orqaga':
        await message.answer('Tugma panel', reply_markup=link_button)
        await state.finish()
    elif text[0] == 'h':
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

        split_chanel = message.text.split('&&&')
        await db.add_tugma(link=split_chanel[0], link_name=split_chanel[1], order_button=max_number + 1)
        await message.answer("Qo'shildi", reply_markup=link_button)
        await state.finish()

    else:
        await message.answer(text='Malumotlarni kiriting \n'
                                  'Masalan : "&&& belgi bilan ajratib\n'
                                  ' link&&&Tugma nomi"\n\n'
                                  'https://t.me/+52bZMKjCR1jY2Qy&&&Referral link - Ko`rinishida')


@dp.message_handler(text='Tugma ➖')
async def remove_button(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer(text='Linkni kiriting\n\n'
                                  'Masalan: https://t.me/+52bZMKjCR1jY2Qy - Ko`rinishida',
                             reply_markup=back)
        await TugmaData.tugma_minus.set()


@dp.message_handler(state=TugmaData.tugma_minus)
async def del_button(message: types.Message, state: FSMContext):
    txt = message.text
    if txt[0] == 'h':
        channel = await db.get_tugma(link=txt)
        if not channel:
            await message.answer("Tugma topilmadi\n"
                                 "Qaytadan urinib ko'ring")

        else:
            await db.delete_tugma(link=txt)
            await message.answer('Tugma o"chirildi', reply_markup=link_button)
            await state.finish()
    elif txt == '🔙️ Orqaga':
        await message.answer('Tugma panel', reply_markup=link_button)
        await state.finish()


@dp.message_handler(text="Tugmalar ro'yxati")
async def list_buttons(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        tugmalar = await db.select_tugma()
        text = ''
        for tugma in tugmalar:
            text += f"{tugma['link']}\n"
        try:
            await message.answer(f"{text}", reply_markup=link_button)
        except:
            await message.answer(f"Tugmalar mavjud emas")
