import asyncio
import json
import os
from aiogram import Dispatcher, Bot, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


TOKEN = os.environ.get('gb_bot_token')

bot = Bot(token=TOKEN)
dp = Dispatcher()

global phone_book


class ContactData(StatesGroup):
    name = State()
    phone = State()
    email = State()
    birthday = State()


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Привет! Я твой телефонный справочник!")


async def menu(message: Message):
    await bot.send_message(chat_id=message.chat.id, text="/menu. Меню")
    await bot.send_message(chat_id=message.chat.id, text="/create. Создать телефонный справочник")
    await bot.send_message(chat_id=message.chat.id, text="/show. Показать все контакты")
    await bot.send_message(chat_id=message.chat.id, text="/find. Найти контакт")
    await bot.send_message(chat_id=message.chat.id, text="/add. Добавить контакт")
    await bot.send_message(chat_id=message.chat.id, text="/del. Удалить контакт")
    await bot.send_message(chat_id=message.chat.id, text="/save. Сохранить")
    await bot.send_message(chat_id=message.chat.id, text="/load. Загрузить")
    await bot.send_message(chat_id=message.chat.id, text="/exit. Выход")


@dp.message(Command("menu"))
async def show_menu(message: Message):
    await menu(message)


@dp.message(Command("show"))
async def show_contacts(message: Message):
    await bot.send_message(chat_id=message.chat.id, text=str(phone_book))


@dp.message(Command("create"))
async def create_phone_book(message: Message):
    with open('phone_book.json', "w", encoding='utf-8') as file:
        file.write(json.dumps(phone_book, ensure_ascii=False))
    await bot.send_message(chat_id=message.chat.id, text="Телефонная книга создана")


@dp.message(Command("load"))
async def load_phone_book(message: Message):
    global phone_book
    with open('phone_book.json', "r", encoding='utf-8') as file:
        phone_book = json.loads(file.read())
    await bot.send_message(chat_id=message.chat.id, text="Данные загружены")


@dp.message(Command("save"))
async def save_data(message: Message, contact: dict):
    with open('phone_book.json', "a", encoding='utf-8') as file:
        file.write(json.dumps(contact, ensure_ascii=False))
    await bot.send_message(chat_id=message.chat.id, text="Данные сохранены")


@dp.message(Command("find"))
async def find_contact(message: Message):
    await bot.send_message(chat_id=message.chat.id, text="Введите имя:")
    contact_name = (await dp.wait_for(Message)).text
    await bot.send_message(chat_id=message.chat.id, text=str(phone_book.get(contact_name, "Контакт не найден")))


@dp.message(Command("del"))
async def delete_contact(message: Message):
    await bot.send_message(chat_id=message.chat.id, text="Введите имя:")
    contact_name = (await dp.wait_for(Message)).text
    del phone_book[contact_name]
    await bot.send_message(chat_id=message.chat.id, text="Запись успешно удалена")


@dp.message(Command("add"))
async def add_contact(message: Message, state: FSMContext):
    await state.set_state(ContactData.name)
    await message.answer("Введите имя контакта")


@dp.message(ContactData.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(ContactData.phone)
    await message.answer("Введите номер контакта")


@dp.message(ContactData.phone)
async def process_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(ContactData.email)
    await message.answer("Введите email контакта")


@dp.message(ContactData.email)
async def process_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await state.set_state(ContactData.birthday)
    await message.answer("Введите день рождения контакта")


@dp.message(ContactData.email)
async def process_birthday(message: Message, state: FSMContext):
    await state.update_data(birthday=message.text)
    await state.set_state(ContactData.birthday)
    await message.answer("Введите день рождения контакта")
    data = await state.get_data()

    contacts = {
        'phones': data.get('phone'),
        'email': data.get('email'),
        'birthday': data.get('birthday')
    }
    phone_book[data.get('name')] = contacts

    save_data(message, phone_book)
    await message.answer("Контакт успешно добавлен!")
    await state.finish()


@dp.message(Command("exit"))
async def exit_bot(message: Message):
    await bot.send_message(chat_id=message.chat.id, text="Программа завершена")


async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
