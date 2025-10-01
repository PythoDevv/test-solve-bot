from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Botni ishga tushurish"),
#            types.BotCommand("dasturchi", "Coder"),
            types.BotCommand("admin", "Faqat Adminlar uchun"),
            # types.BotCommand("darslar", "Faqat Adminlar uchun"),
        ]
    )
