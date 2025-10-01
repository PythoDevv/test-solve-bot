import re
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from loader import dp, db, bot
from states.rekStates import TestData
from data.config import ADMINS
from keyboards.default.rekKeyboards import admin_key, back


# Test Creation Handlers for Admins
@dp.message_handler(text='📝 Test Yaratish')
async def create_test_start(message: types.Message):
    """Start test creation process"""
    # Check if user is admin
    admins = await db.select_all_admins()
    admins_list = [admin[1] for admin in admins]
    if message.from_user.id not in admins_list:
        await message.answer("❌ Siz admin emassiz!")
        return
    
    await message.answer(
        "📝 <b>Yangi test yaratish</b>\n\n"
        "Test kodi yuboring (masalan: TEST001):",
        reply_markup=back
    )
    await TestData.test_code.set()


@dp.message_handler(state=TestData.test_code)
async def process_test_code(message: types.Message, state: FSMContext):
    """Process test code input"""
    if message.text == '🔙️ Orqaga':
        await message.answer('Bekor qilindi', reply_markup=admin_key)
        await state.finish()
        return
    
    test_code = message.text.strip().upper()
    
    # Check if test code already exists
    existing_test = await db.get_test_by_code(test_code)
    if existing_test:
        await message.answer(
            f"❌ <b>Xato!</b>\n\n"
            f"'{test_code}' kodi bilan test mavjud.\n"
            f"Boshqa kod kiriting:",
            reply_markup=back
        )
        return
    
    await state.update_data(test_code=test_code)
    await message.answer(
        "✅ Test kodi qabul qilindi!\n\n"
        "Test nomini kiriting:",
        reply_markup=back
    )
    await TestData.test_name.set()


@dp.message_handler(state=TestData.test_name)
async def process_test_name(message: types.Message, state: FSMContext):
    """Process test name input"""
    if message.text == '🔙️ Orqaga':
        await message.answer('Bekor qilindi', reply_markup=admin_key)
        await state.finish()
        return
    
    test_name = message.text.strip()
    await state.update_data(test_name=test_name)
    await message.answer(
        "✅ Test nomi qabul qilindi!\n\n"
        "Test savollar sonini kiriting (masalan: 50):",
        reply_markup=back
    )
    await TestData.test_questions_count.set()



@dp.message_handler(state=TestData.test_questions_count)
async def process_test_questions_count(message: types.Message, state: FSMContext):
    """Process test questions count input"""
    if message.text == '🔙️ Orqaga':
        await message.answer('Bekor qilindi', reply_markup=admin_key)
        await state.finish()
        return
    
    try:
        questions_count = int(message.text.strip())
        if questions_count <= 0:
            await message.answer(
                "❌ <b>Xato!</b>\n\n"
                "Savollar soni 0 dan katta bo'lishi kerak.\n"
                "Qayta kiriting:",
                reply_markup=back
            )
            return
        
        await state.update_data(test_questions_count=questions_count)
        await message.answer(
            f"✅ Savollar soni qabul qilindi: {questions_count}\n\n"
            f"To'g'ri javoblarni kiriting (masalan: abcccbaccbbbaccaabb):\n"
            f"<i>Javoblar {questions_count} ta bo'lishi kerak</i>",
            reply_markup=back
        )
        await TestData.test_correct_answers.set()
        
    except ValueError:
        await message.answer(
            "❌ <b>Xato!</b>\n\n"
            "Faqat raqam kiriting!\n"
            "Qayta kiriting:",
            reply_markup=back
        )


@dp.message_handler(state=TestData.test_correct_answers)
async def process_test_correct_answers(message: types.Message, state: FSMContext):
    """Process test correct answers input"""
    if message.text == '🔙️ Orqaga':
        await message.answer('Bekor qilindi', reply_markup=admin_key)
        await state.finish()
        return
    
    user_data = await state.get_data()
    questions_count = user_data['test_questions_count']
    correct_answers = message.text.strip().lower()
    
    # Validate answers length
    if len(correct_answers) != questions_count:
        await message.answer(
            f"❌ <b>Xato!</b>\n\n"
            f"Javoblar soni mos kelmaydi!\n"
            f"Kutilgan: {questions_count} ta\n"
            f"Kiritilgan: {len(correct_answers)} ta\n\n"
            f"Qayta kiriting:",
            reply_markup=back
        )
        return
    
    # Validate answer format (only a, b, c, d)
    if not re.match(r'^[abcd]+$', correct_answers):
        await message.answer(
            "❌ <b>Xato!</b>\n\n"
            "Javoblar faqat a, b, c, d harflaridan iborat bo'lishi kerak!\n"
            "Qayta kiriting:",
            reply_markup=back
        )
        return
    
    await state.update_data(test_correct_answers=correct_answers)
    
    user_data = await state.get_data()
    
    # Create test in database
    test = await db.add_test(
        test_code=user_data['test_code'],
        test_name=user_data['test_name'],
        description='---',
        total_questions=user_data['test_questions_count'],
        correct_answers=user_data['test_correct_answers'],
        time_limit=0,
        created_by=message.from_user.id
    )
    
    await message.answer(
        f"✅ <b>Test muvaffaqiyatli yaratildi!</b>\n\n"
        f"📝 <b>Test kodi:</b> {test['test_code']}\n"
        f"📋 <b>Test nomi:</b> {test['test_name']}\n"
        f"📊 <b>Savollar soni:</b> {test['total_questions']}\n"
        # f"⏰ <b>Vaqt chegarasi:</b> {test['time_limit']} daqiqa\n"
        f"🆔 <b>Test ID:</b> {test['id']}\n\n"
        f"Foydalanuvchilar testni quyidagi formatda yuborishlari mumkin:\n"
        f"<code>{test['test_code']}+javoblar</code>",
        reply_markup=admin_key
    )
    
    await state.finish()
        


# Test Management Handlers
@dp.message_handler(text='📋 Testlar Ro\'yxati')
async def list_tests(message: types.Message):
    """List all tests"""
    # Check if user is admin
    admins = await db.select_all_admins()
    admins_list = [admin[1] for admin in admins]
    if message.from_user.id not in admins_list:
        await message.answer("❌ Siz admin emassiz!")
        return
    
    tests = await db.get_all_tests()
    
    if not tests:
        await message.answer(
            "📋 <b>Testlar ro'yxati</b>\n\n"
            "Hozircha testlar mavjud emas.",
            reply_markup=admin_key
        )
        return
    
    text = "📋 <b>Testlar ro'yxati:</b>\n\n"
    for i, test in enumerate(tests, 1):
        text += f"{i}. <b>{test['test_name']}</b>\n"
        text += f"   Kodi: <code>{test['test_code']}</code>\n"
        text += f"   Savollar: {test['total_questions']} ta\n"
        text += f"   Vaqt: {test['time_limit']} daqiqa\n"
        text += f"   ID: {test['id']}\n\n"
    
    await message.answer(text, reply_markup=admin_key)


@dp.message_handler(text='📊 Test Natijalari')
async def test_results_start(message: types.Message):
    """Start test results viewing"""
    # Check if user is admin
    admins = await db.select_all_admins()
    admins_list = [admin[1] for admin in admins]
    if message.from_user.id not in admins_list:
        await message.answer("❌ Siz admin emassiz!")
        return
    
    tests = await db.get_all_tests()
    
    if not tests:
        await message.answer(
            "📊 <b>Test natijalari</b>\n\n"
            "Hozircha testlar mavjud emas.",
            reply_markup=admin_key
        )
        return
    
    text = "📊 <b>Test natijalarini ko'rish</b>\n\n"
    text += "Test ID sini kiriting:\n\n"
    
    for test in tests:
        text += f"<b>{test['test_name']}</b> - ID: <code>{test['id']}</code>\n"
    
    await message.answer(text, reply_markup=back)
    await TestData.test_edit_select.set()


@dp.message_handler(state=TestData.test_edit_select)
async def show_test_results(message: types.Message, state: FSMContext):
    """Show test results for specific test"""
    if message.text == '🔙️ Orqaga':
        await message.answer('Bekor qilindi', reply_markup=admin_key)
        await state.finish()
        return
    
    try:
        test_id = int(message.text.strip())
        test = await db.get_test_by_id(test_id)
        
        if not test:
            await message.answer(
                "❌ <b>Xato!</b>\n\n"
                "Bunday ID bilan test topilmadi.\n"
                "Qayta kiriting:",
                reply_markup=back
            )
            return
        
        # Get test statistics
        stats = await db.get_test_statistics(test_id)
        attempts = await db.get_test_attempts_by_test(test_id)
        
        text = f"📊 <b>Test natijalari</b>\n\n"
        text += f"📝 <b>Test:</b> {test['test_name']}\n"
        text += f"🔢 <b>Kod:</b> {test['test_code']}\n"
        text += f"📈 <b>Jami urinishlar:</b> {stats['total_attempts']}\n"
        text += f"📊 <b>O'rtacha ball:</b> {stats['average_score']:.1f}%\n"
        text += f"🏆 <b>Eng yuqori ball:</b> {stats['highest_score']:.1f}%\n"
        text += f"📉 <b>Eng past ball:</b> {stats['lowest_score']:.1f}%\n\n"
        
        if attempts:
            text += "<b>Eng yaxshi natijalar:</b>\n"
            for i, attempt in enumerate(attempts[:10], 1):  # Show top 10
                text += f"{i}. {attempt['full_name']} - {attempt['percentage']:.1f}%\n"
        
        await message.answer(text, reply_markup=admin_key)
        await state.finish()
        
    except ValueError:
        await message.answer(
            "❌ <b>Xato!</b>\n\n"
            "Faqat raqam kiriting!\n"
            "Qayta kiriting:",
            reply_markup=back
        )


@dp.message_handler(text='🗑️ Testni O\'chirish')
async def delete_test_start(message: types.Message):
    """Start test deletion process"""
    # Check if user is admin
    admins = await db.select_all_admins()
    admins_list = [admin[1] for admin in admins]
    if message.from_user.id not in admins_list:
        await message.answer("❌ Siz admin emassiz!")
        return
    
    tests = await db.get_all_tests()
    
    if not tests:
        await message.answer(
            "🗑️ <b>Testni o'chirish</b>\n\n"
            "Hozircha testlar mavjud emas.",
            reply_markup=admin_key
        )
        return
    
    text = "🗑️ <b>Testni o'chirish</b>\n\n"
    text += "O'chiriladigan test ID sini kiriting:\n\n"
    
    for test in tests:
        text += f"<b>{test['test_name']}</b> - ID: <code>{test['id']}</code>\n"
    
    await message.answer(text, reply_markup=back)
    await TestData.test_delete_confirm.set()


@dp.message_handler(state=TestData.test_delete_confirm)
async def confirm_delete_test(message: types.Message, state: FSMContext):
    """Confirm test deletion"""
    if message.text == '🔙️ Orqaga':
        await message.answer('Bekor qilindi', reply_markup=admin_key)
        await state.finish()
        return
    
    try:
        test_id = int(message.text.strip())
        test = await db.get_test_by_id(test_id)
        
        if not test:
            await message.answer(
                "❌ <b>Xato!</b>\n\n"
                "Bunday ID bilan test topilmadi.\n"
                "Qayta kiriting:",
                reply_markup=back
            )
            return
        
        # Delete test (soft delete)
        await db.delete_test(test_id)
        
        await message.answer(
            f"✅ <b>Test muvaffaqiyatli o'chirildi!</b>\n\n"
            f"📝 <b>Test:</b> {test['test_name']}\n"
            f"🔢 <b>Kod:</b> {test['test_code']}",
            reply_markup=admin_key
        )
        
        await state.finish()
        
    except ValueError:
        await message.answer(
            "❌ <b>Xato!</b>\n\n"
            "Faqat raqam kiriting!\n"
            "Qayta kiriting:",
            reply_markup=back
        )
