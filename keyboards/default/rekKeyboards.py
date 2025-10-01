from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

rekKey1 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Rasm"),
            KeyboardButton(text="Video")
        ],
        [
            KeyboardButton(text='Text'),
            KeyboardButton(text='Back')
        ]
    ],
    resize_keyboard=True
)
admin_key_2 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Add List ➕"),
            KeyboardButton(text="Add List ➖"),
        ],
        [
            KeyboardButton(text="Add List 📈"),
        ],
        [
            KeyboardButton(text="Add List Kanal ➕"),
            KeyboardButton(text="Add List Kanal ➖"),
        ],
        [
            KeyboardButton(text="Add List Kanallar 📈"),
        ],
    ]
)

back = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🔙️ Orqaga'),
        ]
    ],
    resize_keyboard=True
)

main_section = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🔝 Bosh menu'),
        ]
    ],
    resize_keyboard=True
)

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='- Tanlov'),
        ],
        [
            KeyboardButton(text="- Go School")
        ]
    ], resize_keyboard=True
)

admin_key = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Post Yuborish 🗒'),
        ],
        [
            KeyboardButton(text='Barcha Adminlar'),
            KeyboardButton(text='Admin ➕'),
            KeyboardButton(text='Admin ➖')
        ],
        [
            KeyboardButton(text='Kanal ➕'),
            KeyboardButton(text='Kanal ➖')
        ],
        [
            KeyboardButton(text="Kanallar 📈"),
            KeyboardButton(text="Statistika 📊")
        ],
        # [
        #     KeyboardButton(text="Go'libga"),
        # ],
        # [
        #     KeyboardButton(text='Asosiy qism'),
        #     KeyboardButton(text='Asosiy qism 2'),
        # ],
        # [
            # KeyboardButton(text='Taklif miqdorini kiritish'),
            # KeyboardButton(text='Taklif chegarasini kiritish'),
            # KeyboardButton(text="G'olibga")
        # ],
        [
            KeyboardButton(text="Obunadan so'ng"),
        #     KeyboardButton(text='Faqat Hisobni 0 ga tushirish'),
        ],
        [
            KeyboardButton(text="Majburiy obuna"),
            # KeyboardButton(text="Yangi Loyiha Boshlash"),
        ],
        [
            KeyboardButton(text="Remove File"),
            KeyboardButton(text="Barcha ma'lumotlarni tozalash")
        ],
        [
            # KeyboardButton(text="📊 Raqamlar soni"),
            # KeyboardButton(text="🏆 G'olibni topish"),
        ],
        [
            KeyboardButton(text="📝 Test Yaratish"),
            KeyboardButton(text="📋 Testlar Ro'yxati"),
        ],
        [
            KeyboardButton(text="📊 Test Natijalari"),
            KeyboardButton(text="🗑️ Testni O'chirish"),
        ],
        [
            KeyboardButton(text="O'chirish uchun mahsus kodlar"),
            # KeyboardButton(text="🏘 Bosh menu")
        ]
    ],
    resize_keyboard=True
)

admin_secret_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Yopiq Kanallar ro'yxati 😱"),
        ],
        [
            KeyboardButton(text='Yopiq Kanal ➕'),
            KeyboardButton(text='Yopiq Kanal ➖')
        ],
        [
            KeyboardButton(text="🏘 Bosh menu")

        ]
    ],
    resize_keyboard=True
)
link_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Tugmalar ro'yxati"),
        ],
        [
            KeyboardButton(text='Tugma ➕'),
            KeyboardButton(text='Tugma ➖')
        ],
        [
            KeyboardButton(text="🏘 Bosh menu")

        ]
    ],
    resize_keyboard=True
)
