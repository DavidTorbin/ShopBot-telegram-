from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


item1 = KeyboardButton(text='📔 Прайс-Лист')
item2 = KeyboardButton(text='📥 Оформить заказ')
item3 = KeyboardButton(text='☎ Контакты')
keyb1 = ReplyKeyboardMarkup(keyboard=[[item1], [item2], [item3]], resize_keyboard=True)


item3 = KeyboardButton(text='📩 Telegram')
item4 = KeyboardButton(text='📩 WhatsApp')
keyb2 = ReplyKeyboardMarkup(keyboard=[[item3], [item4]], resize_keyboard=True)
