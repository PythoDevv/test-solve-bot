from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, db
from states.rekStates import UserData
from keyboards.default.rekKeyboards import admin_key


@dp.message_handler(state=UserData.custom_fullname)
async def process_custom_fullname(message: types.Message, state: FSMContext):
    """Process custom fullname input"""
    if message.text == '🔙️ Orqaga':
        await message.answer('Bekor qilindi', reply_markup=admin_key)
        await state.finish()
        return
    
    custom_fullname = message.text.strip()
    
    # Save custom fullname to database
    await db.update_user_custom_fullname(custom_fullname, message.from_user.id)
    
    # Get user's total score
    user_total_score = await db.calculate_user_total_score(message.from_user.id)
    
    lessons = await db.select_related_lessons(button_name="Obunadan so'ng")
    button_score = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_score.add(types.KeyboardButton(text="📝 Testlarga Javob Berish"))
    button_score.add(types.KeyboardButton(text="❓ Test Yordam"))
    button_score.add(types.KeyboardButton(text="📋 Topshirgan testlarim"))

    await message.answer(
        f"✅ <b>Ismingiz saqlandi!</b>")
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
    
    await state.finish()
