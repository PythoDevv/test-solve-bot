from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

button_scorelink = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔗 Taklif posti", callback_data="link")
        ]

    ]
)

invite_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="👤 Одам таклиф қилиб балларни тўплаш", callback_data="invite")
        ]

    ]
)
