import asyncio
from aiogram import types
from states.rekStates import RekData, AllState, Lesson, Number
from loader import dp, db, bot
from handlers.users.main import create_link
from loader import dp, db, bot
from aiogram.dispatcher import FSMContext
from keyboards.default.rekKeyboards import back, admin_key
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.misc.check_html import is_html_valid
cancel_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            # KeyboardButton(text='Orqaga qaytish'),
            KeyboardButton(text='Bekor qilish')
        ]
    ],
    resize_keyboard=True
)


@dp.message_handler(text="Go'libga")
async def gift_for_winner_selecter(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        linl_or_post_button = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='Link'),
                    KeyboardButton(text='Post'),
                ],
                [
                    KeyboardButton(text='Bekor qilish')
                ]
            ],
            resize_keyboard=True
        )

        await message.answer("Link yoki Post Jo'natasizmi", reply_markup=linl_or_post_button)
        await RekData.gift_for_winner.set()


@dp.message_handler(state=RekData.gift_for_winner)
async def gift_for_winner_selector(message: types.Message, state: FSMContext):
    if message.text == 'Link':
        await state.update_data(link_or_post='link')
        await message.answer("Nechchi ball bo'lganda berilsin?")
        await RekData.for_winner_score.set()
    elif message.text == 'Post':
        await state.update_data(link_or_post='post')
        await message.answer("Nechchi ball bo'lganda berilsin?")
        await RekData.for_winner_score.set()
    elif message.text == 'Bekor qilish':
        await message.answer("Bekor qilindi", reply_markup=admin_key)
        await state.finish()
    else:
        await message.answer('Iltimos Tugmalardan birini tanlang')


@dp.message_handler(state=RekData.for_winner_score)
async def gift_for_winner_selecter(message: types.Message, state: FSMContext):
    try:
        score = int(message.text)
        if score > 0:
            await state.update_data({'score': score})
            user_selection = await state.get_data()
            if user_selection.get('link_or_post') == 'link':
                await message.answer("Yopiq kanal ID ni yuboring\n\n"
                                     "ID -10 bilan boshlanishi shart", reply_markup=cancel_button)
                await RekData.gift_for_winner_link.set()
            elif user_selection.get('link_or_post') == 'post':
                await state.update_data(link_or_post='post')
                await message.answer("Postni yuboring", reply_markup=cancel_button)
                await RekData.gift_for_winner_post.set()
        else:
            await message.answer("Musbat son kiriting")
    except:
        await message.answer("Musbat son kiriting")


@dp.message_handler(state=RekData.gift_for_winner_link)
async def for_private_channel(message: types.Message, state: FSMContext):
    if message.text.startswith('-10'):
        try:
            bot_member = await bot.get_chat_member(message.text, bot.id)
            if bot_member.is_chat_admin():
                await state.update_data({'private_channel_id': message.text})
                await message.answer("Kanal ID Qabul qilindi\n\n"
                                     "Link bilan yuboriladigan postni yuboring!Postni istalgan shaklda yuborish mumkin(text,rasmli text yoki video formatda)\n\n"
                                     "Pastda misol keltirilgan 👇", reply_markup=cancel_button)
                await message.answer(text='Tabriklaymi Siz Barcha Shartlarni Bajardingiz\n'
                                          'Yopiq Kanal uchun link 👇\n\n'
                                          '{link}')
                await RekData.gift_for_winner_post.set()
            else:
                await message.answer(
                    '❌ Bot Kanalda admin emas ekan.Iltimos Botni kanalda admin qiling va Kanalga birorta post '
                    'tashlab o`chirib yuboring!Bu juda zarur.\n\n'
                    'Bot Yopiq kanalda admin bo`masa yopiq kanal idni qo`sholmaysiz')

        except:
            await message.answer(
                '❌ Bot Kanalda admin emas ekan.Iltimos Botni kanalda admin qiling va Kanalga birorta post '
                'tashlab o`chirib yuboring!Bu juda zarur.\n\n'
                'Bot Yopiq kanalda admin bo`masa yopiq kanal idni qo`sholmaysiz')

    elif message.text == 'Bekor qilish':
        await message.answer("Bekor qilindi", reply_markup=admin_key)
        await state.finish()
    else:
        await message.answer('Xato\n\nID -10 bilan boshlanishi shart')


@dp.message_handler(state=RekData.gift_for_winner_post, content_types=[
    'video', 'audio', 'voice', 'photo', 'document', 'text', 'animation', 'video_note', 'venue'])
async def gift_for_winner_content(message: types.Message, state: FSMContext):
    data = await state.get_data()
    is_link = True if data.get('link_or_post') == 'link' else False
    private_channel_id = data.get('private_channel_id', '')
    score = data.get('score')
    if message.video:
        file_id = message.video.file_id
        file_unique_id = message.video.file_unique_id
        caption = ''
        if message.caption is not None:
            if is_html_valid(message.caption):
                caption += message.caption
            else:
                await message.answer(
                    "Xatolik! HTML kodlarini to'g'ri kiriting\nMasalan :\n\n"
                    "&lt;b&gt; Text &lt;/b&gt; ko'rinishida bo'lishi kerak",
                    parse_mode="HTML"
                )
                return
        await message.answer_video(
            video=file_id,
            caption=f"{caption}\n\n" \
                    f'🗑 o`chirish uchun mahsus code - <code>{file_unique_id}</code>'
                    f' (faqat adminlarga ko`rinadi)'
        )
        await db.add_lesson(
            button_name="G'olibga",
            type='video',
            file_id=file_id,
            file_unique_id=file_unique_id,
            description=caption,
            score=score,
            is_link=is_link,
            private_channel_id=private_channel_id
        )
        await message.answer("Qo'shildi.Yana post qo'shasizmi?")

    elif message.voice:
        file_id = message.voice.file_id
        file_unique_id = message.voice.file_unique_id
        caption = ''
        if message.caption is not None:
            if is_html_valid(message.caption):
                caption += message.caption
            else:
                await message.answer(
                    "Xatolik! HTML kodlarini to'g'ri kiriting\nMasalan :\n\n"
                    "&lt;b&gt; Text &lt;/b&gt; ko'rinishida bo'lishi kerak",
                    parse_mode="HTML"
                )
                return
        await message.answer_voice(
            voice=file_id,
            caption=f"{caption}\n\n" \
                    f'🗑 o`chirish uchun mahsus code - <code>{file_unique_id}</code>'
                    f' (faqat adminlarga ko`rinadi)'
        )
        await db.add_lesson(
            button_name="G'olibga",
            type='voice',
            file_id=file_id,
            file_unique_id=file_unique_id,
            description=caption,
            score=score,
            is_link=is_link,
            private_channel_id=private_channel_id
        )
        await message.answer("Qo'shildi.Yana post qo'shasizmi?")

    elif message.document:
        file_id = message.document.file_id
        file_unique_id = message.document.file_unique_id
        caption = ''
        if message.caption is not None:
            if is_html_valid(message.caption):
                caption += message.caption
            else:
                await message.answer(
                    "Xatolik! HTML kodlarini to'g'ri kiriting\nMasalan :\n\n"
                    "&lt;b&gt; Text &lt;/b&gt; ko'rinishida bo'lishi kerak",
                    parse_mode="HTML"
                )
                return
        await message.answer_document(
            document=file_id,
            caption=f"{caption}\n\n" \
                    f'🗑 o`chirish uchun mahsus code - <code>{file_unique_id}</code>'
                    f' (faqat adminlarga ko`rinadi)'
        )
        await db.add_lesson(
            button_name="G'olibga",
            type='document',
            file_id=file_id,
            file_unique_id=file_unique_id,
            description=caption,
            score=score,
            is_link=is_link,
            private_channel_id=private_channel_id
        )
        await message.answer("Qo'shildi.Yana post qo'shasizmi?")

    elif message.photo:
        file_id = message.photo[-1].file_id
        file_unique_id = message.photo[-1].file_unique_id
        caption = ''
        if message.caption is not None:
            if is_html_valid(message.caption):
                caption += message.caption
            else:
                await message.answer(
                    "Xatolik! HTML kodlarini to'g'ri kiriting\nMasalan :\n\n"
                    "&lt;b&gt; Text &lt;/b&gt; ko'rinishida bo'lishi kerak",
                    parse_mode="HTML"
                )
                return
        await message.answer_photo(
            photo=file_id,
            caption=f"{caption}\n\n" \
                    f'🗑 o`chirish uchun mahsus code - <code>{file_unique_id}</code>'
                    f' (faqat adminlarga ko`rinadi)'
        )
        await db.add_lesson(
            button_name="G'olibga",
            type='photo',
            file_id=file_id,
            file_unique_id=file_unique_id,
            description=caption,
            score=score,
            is_link=is_link,
            private_channel_id=private_channel_id
        )
        await message.answer("Qo'shildi.Yana post qo'shasizmi?")


    elif message.audio:
        file_id = message.audio.file_id
        file_unique_id = message.audio.file_unique_id
        caption = ''
        if message.caption is not None:
            if is_html_valid(message.caption):
                caption += message.caption
            else:
                await message.answer(
                    "Xatolik! HTML kodlarini to'g'ri kiriting\nMasalan :\n\n"
                    "&lt;b&gt; Text &lt;/b&gt; ko'rinishida bo'lishi kerak",
                    parse_mode="HTML"
                )
                return
        await message.answer_audio(
            audio=file_id,
            caption=f"{caption}\n\n" \
                    f'🗑 o`chirish uchun mahsus code - <code>{file_unique_id}</code>'
                    f' (faqat adminlarga ko`rinadi)'
        )
        await db.add_lesson(
            button_name="G'olibga",
            type='audio',
            file_id=file_id,
            file_unique_id=file_unique_id,
            description=caption,
            score=score,
            is_link=is_link,
            private_channel_id=private_channel_id
        )
        await message.answer("Qo'shildi.Yana post qo'shasizmi?")
    elif message.text == 'Bekor qilish':
        await message.answer("Bekor qilindi", reply_markup=admin_key)
        await state.finish()
    
    elif message.text:
        if is_html_valid(message.text):
            pass
        else:
            await message.answer(
                "Xatolik! HTML kodlarini to'g'ri kiriting\nMasalan :\n\n"
                "&lt;b&gt; Text &lt;/b&gt; ko'rinishida bo'lishi kerak",
                parse_mode="HTML"
            )
            return 
        await db.add_lesson_text(
            button_name="G'olibga",
            type='text',
            file_unique_id=f'{message.message_id}',
            description=f'{message.text}',
            score=score,
            is_link=is_link,
            private_channel_id=private_channel_id
        )
        await message.answer(f'{message.text}\n\n' \
                             f'🗑 o`chirish uchun mahsus code - <code>{message.message_id}</code>'
                             f' (faqat adminlarga ko`rinadi)')
        await message.answer("Qo'shildi.Yana post qo'shasizmi?")
    select_is_have_link_db = await db.select_one_time_link(private_channel_id=private_channel_id)
    if is_link and private_channel_id and not select_is_have_link_db:
        asyncio.create_task(create_link_in_background(private_channel_id, message, bot))

async def create_link_in_background(private_channel_id, message, bot):
    for i in range(1000):
        create_invite_link = await bot.create_chat_invite_link(chat_id=private_channel_id, member_limit=1)
        await db.add_one_time_link(create_invite_link['invite_link'], private_channel_id=private_channel_id)
        await asyncio.sleep(30)



@dp.message_handler(text="Yangi Loyiha Boshlash")
async def new_projectt(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer("Aniqmi\n\n" "yes or no", reply_markup=back)
        await RekData.new_project.set()

@dp.message_handler(state=RekData.new_project)
async def new_project_checker(message: types.Message, state: FSMContext):
    if message.text == "yes":
        await db.update_all_users_data(args="000", oldd="new")
        await db.drop_requested_users()
        await db.create_table_requested_users()
        await message.answer("Barcha ballar tozalandi")
    else:
        await state.finish()
        await message.answer("Bosh menu", reply_markup=admin_key)
