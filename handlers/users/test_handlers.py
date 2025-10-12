import re
import pytz
import asyncio
from aiogram import types
from datetime import datetime
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
            f"Test uchun nechta ball berish kerak? (masalan: 5):",
            reply_markup=back
        )
        await TestData.test_score.set()
        
    except ValueError:
        await message.answer(
            "❌ <b>Xato!</b>\n\n"
            "Faqat raqam kiriting!\n"
            "Qayta kiriting:",
            reply_markup=back
        )


@dp.message_handler(state=TestData.test_score)
async def process_test_score(message: types.Message, state: FSMContext):
    """Process test score input"""
    if message.text == '🔙️ Orqaga':
        await message.answer('Bekor qilindi', reply_markup=admin_key)
        await state.finish()
        return
    
    try:
        test_score = int(message.text.strip())
        if test_score <= 0:
            await message.answer(
                "❌ <b>Xato!</b>\n\n"
                "Test balli 0 dan katta bo'lishi kerak.\n"
                "Qayta kiriting:",
                reply_markup=back
            )
            return
        
        await state.update_data(test_score=test_score)
        user_data = await state.get_data()
        await message.answer(
            f"✅ Test balli qabul qilindi: {test_score}\n\n"
            f"To'g'ri javoblarni kiriting (masalan: abcccbaccbbbaccaabb):\n"
            f"<i>Javoblar {user_data['test_questions_count']} ta bo'lishi kerak</i>",
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
        test_score=user_data['test_score'],
        created_by=message.from_user.id
    )
    
    await message.answer(
        f"✅ <b>Test muvaffaqiyatli yaratildi!</b>\n\n"
        f"📝 <b>Test kodi:</b> {test['test_code']}\n"
        f"📋 <b>Test nomi:</b> {test['test_name']}\n"
        f"📊 <b>Savollar soni:</b> {test['total_questions']}\n"
        f"🏆 <b>Test balli:</b> {test['test_score']}\n"
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
    
    # Split tests into chunks to avoid message length limit
    chunk_size = 15  # Number of tests per message
    total_tests = len(tests)
    
    for chunk_start in range(0, total_tests, chunk_size):
        chunk_end = min(chunk_start + chunk_size, total_tests)
        chunk_tests = tests[chunk_start:chunk_end]
        
        if chunk_start == 0:
            text = f"📋 <b>Testlar ro'yxati ({total_tests} ta):</b>\n\n"
        else:
            text = f"📋 <b>Testlar (davomi):</b>\n\n"
        
        for i, test in enumerate(chunk_tests, chunk_start + 1):
            text += f"{i}. <b>{test['test_name']}</b>\n"
            text += f"   🔢 Kodi: <code>{test['test_code']}</code>\n"
            text += f"   📊 Savollar: {test['total_questions']} ta\n"
            text += f"   🏆 Ball: {test['test_score']}\n"
            text += f"   ⏰ Vaqt: {test['time_limit']} daqiqa\n"
            text += f"   🆔 ID: {test['id']}\n\n"
        
        # Check if message is too long (Telegram limit is ~4096 characters)
        if len(text) > 4000:
            # Split further if still too long
            lines = text.split('\n')
            current_chunk = ""
            for line in lines:
                if len(current_chunk + line + '\n') > 4000:
                    await message.answer(current_chunk)
                    current_chunk = line + '\n'
                else:
                    current_chunk += line + '\n'
            if current_chunk:
                await message.answer(current_chunk)
        else:
            await message.answer(text)
    
    await message.answer("✅ Barcha testlar ko'rsatildi", reply_markup=admin_key)


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
        
        # Header message
        header_text = f"📊 <b>Test natijalari</b>\n\n"
        header_text += f"📝 <b>Test:</b> {test['test_name']}\n"
        header_text += f"🔢 <b>Kod:</b> {test['test_code']}\n"
        header_text += f"🏆 <b>Test balli:</b> {test['test_score']}\n"
        header_text += f"📈 <b>Jami urinishlar:</b> {stats['total_attempts']}\n"
        header_text += f"📊 <b>O'rtacha ball:</b> {stats['average_score']:.1f}%\n"
        header_text += f"🏆 <b>Eng yuqori ball:</b> {stats['highest_score']:.1f}%\n"
        header_text += f"📉 <b>Eng past ball:</b> {stats['lowest_score']:.1f}%\n\n"
        
        await message.answer(header_text, reply_markup=admin_key)
        
        if attempts:
            # Sort attempts by percentage (highest first)
            attempts_sorted = sorted(attempts, key=lambda x: x['percentage'], reverse=True)
            
            # Split attempts into chunks to avoid message length limit
            chunk_size = 20  # Number of attempts per message
            total_attempts = len(attempts_sorted)
            
            for chunk_start in range(0, total_attempts, chunk_size):
                chunk_end = min(chunk_start + chunk_size, total_attempts)
                chunk_attempts = attempts_sorted[chunk_start:chunk_end]
                
                if chunk_start == 0:
                    attempts_text = f"📋 <b>Barcha urinishlar ({total_attempts} ta):</b>\n\n"
                else:
                    attempts_text = f"📋 <b>Urinishlar (davomi):</b>\n\n"
                
                for i, attempt in enumerate(chunk_attempts, chunk_start + 1):
                    tashkent_tz = pytz.timezone('Asia/Tashkent')
                    completed_at_tashkent = attempt['completed_at'].astimezone(tashkent_tz)
                    attempts_text += f"{i}. <b>{attempt['full_name']}</b>\n"
                    attempts_text += f"   📊 Natija: {attempt['correct_answers']}/{attempt['total_questions']}\n"
                    attempts_text += f"   📈 Foiz: {attempt['percentage']:.1f}%\n"
                    attempts_text += f"   🏆 Ball: {attempt['score']}\n"
                    attempts_text += f"   📅 Sana: {completed_at_tashkent.strftime('%d.%m.%Y %H:%M')}\n\n"
                
                # Check if message is too long (Telegram limit is ~4096 characters)
                if len(attempts_text) > 4000:
                    # Split further if still too long
                    lines = attempts_text.split('\n')
                    current_chunk = ""
                    for line in lines:
                        if len(current_chunk + line + '\n') > 4000:
                            await message.answer(current_chunk)
                            await asyncio.sleep(0.04)
                            current_chunk = line + '\n'
                        else:
                            current_chunk += line + '\n'
                    if current_chunk:
                        await message.answer(current_chunk)
                        await asyncio.sleep(0.04)
                else:
                    await message.answer(attempts_text)
                    await asyncio.sleep(0.04)
        else:
            await message.answer("📋 Hozircha hech kim bu testni topshirmagan.")
        
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
