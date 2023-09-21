from aiogram import Bot, Dispatcher
from aiogram import filters
from aiogram.filters import Command, CommandStart, StateFilter, Text
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import (Message, InlineKeyboardMarkup, InlineKeyboardButton,CallbackQuery, FSInputFile)
from config import *
from Buttons import *
import html
base = {}
bot: Bot = Bot(token=token)
dp: Dispatcher = Dispatcher(bot=bot)


# app = FastAPI()
#
#
# @app.get("/")
# def root():
#     return "Hello from Space! 🚀"


class FSMFillForm(StatesGroup):
    zakaz = State()
    name = State()
    age = State()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Добро пожаловать👋, {message.from_user.first_name}!\n\nЯ - 🤖, бот Kosher Moscow Devilery "
                 "создан для того, "
                 "чтобы помочь Вам сделать заказ нашей продукции!"
                 "\n\n"
                 "<i>Выберите один из пунктов меню 👇</i>", parse_mode='html', reply_markup=keyb1)


@dp.message(lambda x: x.text == '📔 Прайс-Лист')
async def list(message: Message):
    Fyle = FSInputFile(path='price.pdf')
    await bot.send_document(message.chat.id, document=Fyle)

@dp.message(lambda x: x.text == '📥 Оформить заказ')
async def register(message: Message, state: FSMContext):
    base[message.from_user.id] = {}
    await message.answer('Укажите Ваши имя и фамилию 👇')
    await state.set_state(FSMFillForm.name)


@dp.message(StateFilter(FSMFillForm.name), lambda x: len(x.text.split()) == 2)
async def register_name(message: Message, state: FSMContext):
    base[message.chat.id]['ФИО клиента'] = message.text
    await message.answer('Введите номер телефона(введите только цифры в формате - 89999999999)👇')
    await state.set_state(FSMFillForm.age)


@dp.message(StateFilter(FSMFillForm.name))
async def warning_register_name(message: Message):
    await message.answer('Пожалуйста, проверьте, правильно ли заполнены данные')


@dp.message(StateFilter(FSMFillForm.age),lambda x:x.text.isdigit())
async def register_age1(message: Message, state:FSMContext):
    base[message.chat.id]['Номер телефона'] = message.text
    await message.answer('Введите продукцию и ее количество для заказа 👇')
    await state.set_state(FSMFillForm.zakaz)


@dp.message(StateFilter(FSMFillForm.age))
async def warning_register_age(message: Message):
    await message.answer('Пожалуйста, проверьте, правильно ли заполнены данные')


@dp.message(StateFilter(FSMFillForm.zakaz), lambda x: len(x.text) >= 1)
async def zakaz2(message: Message, state:FSMContext):
    messagetext = message.text
    base[message.from_user.id]['Заказ'] = messagetext
    await bot.send_message(channel_id, f'{base[message.from_user.id]}')
    await message.answer('Благодарим Вас за оформленный заказ🙂! В ближайшее время мы с Вами свяжемся!')
    base[message.from_user.id] = {}
    await state.clear()

@dp.message(lambda x: x.text == '☎ Контакты')
async def contact1(message: Message):
    await message.answer(f'{message.from_user.first_name}, Выберите один из предложенных каналов связи😌\n 👇👇👇'
                         , reply_markup= keyb2)


@dp.message(lambda x: x.text == '📩 Telegram')
async def contact1(message: Message):
    await message.answer('@lansky_770'
                         , reply_markup= keyb1)


@dp.message(lambda x: x.text == '📩 WhatsApp')
async def contact1(message: Message):
    await message.answer('https://wa.link/z8gdav>'
                         , reply_markup= keyb1)


if __name__ == '__main__':
    dp.run_polling(bot)
