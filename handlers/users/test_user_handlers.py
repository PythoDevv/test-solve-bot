import re
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp, db, bot
from states.rekStates import TestData


# User Test Taking Handlers
@dp.message_handler(text='📝 Testlarga Javob Berish')
async def start_test_taking(message: types.Message):
    """Start test taking process"""
    await message.answer(
        "📝 Test javoblarini tekshirish uchun quyidagi formatda test javoblarini yuboring:\n\n"
        "<b>Format:</b>\n"
        "<code>TestKodi+javoblar</code>\n\n"
        "<b>Misollar:</b>\n"
        "<code>TEST001+abcccbaccbbbaccaabb</code>\n"
        "<code>TEST001+1a2b3c4c5c6b7a8c9c10b11b12b13a14c15c16a17a18b19b</code>\n\n"
        "‼️ <b>Diqqat!!</b> Testni barcha javoblarini yuboring!",
        reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton("📋 Mening Testlarim", callback_data="my_tests")
        )
    )


@dp.message_handler(regexp=r'^[A-Za-z0-9]+\+[a-d]+$')
async def process_test_answers(message: types.Message):
    """Process test answer submission"""
    try:
        # Parse test code and answers
        parts = message.text.split('+', 1)
        if len(parts) != 2:
            await message.answer(
                "❌ <b>Xato format!</b>\n\n"
                "To'g'ri format: <code>TestKodi+javoblar</code>\n"
                "Masalan: <code>TEST001+abcccbaccbbbaccaabb</code>"
            )
            return
        
        test_code = parts[0].strip().upper()
        user_answers = parts[1].strip().lower()
        
        # Get test from database
        test = await db.get_test_by_code(test_code)
        if not test:
            await message.answer(
                f"❌ <b>Test topilmadi!</b>\n\n"
                f"'{test_code}' kodi bilan test mavjud emas.\n"
                f"Test kodini tekshirib qayta urining."
            )
            return
        
        # Validate answers length
        if len(user_answers) != test['total_questions']:
            await message.answer(
                f"❌ <b>Javoblar soni mos kelmaydi!</b>\n\n"
                f"Test javoblari soni: <b>{test['total_questions']}ta</b> bo'lishi kerak\n"
                f"Sizning javoblaringiz soni esa: <b>{len(user_answers)}ta</b>\n\n"
                f"Barcha javoblarni yuboring!"
            )
            return
        
        # Validate answer format
        if not re.match(r'^[abcd]+$', user_answers):
            await message.answer(
                "❌ <b>Xato format!</b>\n\n"
                "Javoblar faqat a, b, c, d harflaridan iborat bo'lishi kerak!\n"
                "Qayta urining."
            )
            return
        
        # Check if user already took this test
        existing_attempt = await db.get_user_test_attempt(test['id'], message.from_user.id)
        
        # Calculate score
        correct_answers = test['correct_answers']
        correct_count = 0
        
        for i, (user_answer, correct_answer) in enumerate(zip(user_answers, correct_answers)):
            if user_answer == correct_answer:
                correct_count += 1
        
        score = correct_count
        percentage = (correct_count / test['total_questions']) * 100
        
        # Save test attempt
        if not existing_attempt:
            await db.add_test_attempt(
                test_id=test['id'],
                user_id=message.from_user.id,
                user_answers=user_answers,
                score=score,
                total_questions=test['total_questions'],
                correct_answers=correct_count,
                percentage=percentage
            )
        
        
        # Prepare result message
        result_text = f"✅ <b>Test yakunlandi!</b>\n\n"
        result_text += f"📝 <b>Test:</b> {test['test_name']}\n"
        result_text += f"🔢 <b>Kod:</b> {test['test_code']}\n"
        result_text += f"📊 <b>Natija:</b> {correct_count}/{test['total_questions']}\n"
        result_text += f"📈 <b>Foiz:</b> {percentage:.1f}%\n\n"
        
        # Add performance message
        if percentage >= 90:
            result_text += "🏆 <b>Ajoyib! Juda yaxshi natija!</b>"
        elif percentage >= 80:
            result_text += "👏 <b>Yaxshi! Yaxshi natija!</b>"
        elif percentage >= 70:
            result_text += "👍 <b>Yaxshi! Qoniqarli natija!</b>"
        elif percentage >= 60:
            result_text += "📚 <b>O'qish kerak! Yaxshilash uchun harakat qiling!</b>"
        else:
            result_text += "📖 <b>Qayta o'qib chiqing va qayta urining!</b>"
        
        if existing_attempt:
            result_text += f"\n\n🔄 <b>Eslatma:</b> Siz bu testni avval ham topshirgansiz. Natija yangilanmaydi.Birinchi yechgan natijangiz hisoblanadi."
        
        await message.answer(result_text)
        
    except Exception as e:
        print(f"Error processing test answers: {e}")
        await message.answer(
            "❌ <b>Xatolik yuz berdi!</b>\n\n"
            "Iltimos, qayta urining yoki admin bilan bog'laning."
        )


@dp.callback_query_handler(text="my_tests")
async def show_my_tests(call: types.CallbackQuery):
    """Show user's test history"""
    user_id = call.from_user.id
    test_history = await db.get_user_test_history(user_id)
    
    if not test_history:
        await call.message.answer(
            "📋 <b>Mening testlarim</b>\n\n"
            "Hozircha siz hech qanday test topshirmagansiz."
        )
        return
    
    text = "📋 <b>Mening testlarim:</b>\n\n"
    
    for i, attempt in enumerate(test_history, 1):
        text += f"{i}. <b>{attempt['test_name']}</b>\n"
        text += f"   Kod: <code>{attempt['test_code']}</code>\n"
        text += f"   Natija: {attempt['correct_answers']}/{attempt['total_questions']}\n"
        text += f"   Foiz: {attempt['percentage']:.1f}%\n"
        text += f"   Sana: {attempt['completed_at'].strftime('%d.%m.%Y %H:%M')}\n\n"
    
    await call.message.answer(text)
    await call.answer()


# Help handler for test format
@dp.message_handler(text='❓ Test Yordam')
async def test_help(message: types.Message):
    """Show test help information"""
    await message.answer(
        "❓ <b>Test yordam</b>\n\n"
        "<b>Test javoblarini qanday yuborish kerak?</b>\n\n"
        "1️⃣ Test kodini oling (masalan: TEST001)\n"
        "2️⃣ Javoblaringizni tayyorlang (a, b, c, d)\n"
        "3️⃣ Quyidagi formatda yuboring:\n"
        "   <code>TestKodi+javoblar</code>\n\n"
        "<b>Misollar:</b>\n"
        "• <code>TEST001+abcccbaccbbbaccaabb</code>\n"
        "• <code>TEST001+1a2b3c4c5c6b7a8c9c10b11b12b13a14c15c16a17a18b19b</code>\n\n"
        "<b>Muhim:</b>\n"
        "• Javoblar faqat a, b, c, d harflaridan iborat bo'lishi kerak\n"
        "• Barcha savollarga javob berish kerak\n"
        "• Test kodini to'g'ri kiriting\n\n"
        "Savollar bo'lsa admin bilan bog'laning!"
    )
