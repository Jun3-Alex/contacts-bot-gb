import json
import os
from aiogram import Dispatcher, types
from aiogram import Bot
# from aiogram import executor


TOKEN = os.environ.get('gb_bot_token')


dp = Dispatcher()

phone_book = {}

async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

async def menu(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text="/menu. Меню")
    await bot.send_message(chat_id=message.chat.id, text="/create. Создать телефонный справочник")
    await bot.send_message(chat_id=message.chat.id, text="/show. Показать все контакты")
    await bot.send_message(chat_id=message.chat.id, text="/find. Найти контакт")
    await bot.send_message(chat_id=message.chat.id, text="/add. Добавить контакт")
    await bot.send_message(chat_id=message.chat.id, text="/del. Удалить контакт")
    await bot.send_message(chat_id=message.chat.id, text="/save. Сохранить")
    await bot.send_message(chat_id=message.chat.id, text="/load. Загрузить")
    await bot.send_message(chat_id=message.chat.id, text="/exit. Выход")


@dp.message(CommandStart())
async def start(message: types.Message):
    await menu(message)


@dp.message(commands=['menu'])
async def show_menu(message: types.Message):
    await menu(message)


@dp.message_handler(commands=['show'])
async def show_contacts(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=str(phone_book))


@dp.message_handler(commands=['create'])
async def create_phone_book(message: types.Message):
    with open('phone_book.json', "w", encoding='utf-8') as file:
        file.write(json.dumps(phone_book, ensure_ascii=False))
    await bot.send_message(chat_id=message.chat.id, text="Телефонная книга создана")


@dp.message_handler(commands=['load'])
async def load_phone_book(message: types.Message):
    global phone_book
    with open('phone_book.json', "r", encoding='utf-8') as file:
        phone_book = json.loads(file.read())
    await bot.send_message(chat_id=message.chat.id, text="Данные загружены")


@dp.message_handler(commands=['find'])
async def find_contact(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text="Введите имя:")
    contact_name = (await dp.wait_for(types.Message)).text
    await bot.send_message(chat_id=message.chat.id, text=str(phone_book.get(contact_name, "Контакт не найден")))


@dp.message_handler(commands=['del'])
async def delete_contact(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text="Введите имя:")
    contact_name = (await dp.wait_for(types.Message)).text
    del phone_book[contact_name]
    await bot.send_message(chat_id=message.chat.id, text="Запись успешно удалена")


@dp.message_handler(commands=['save'])
async def save_data(message: types.Message):
    with open('phone_book.json', "a", encoding='utf-8') as file:
        file.write(json.dumps(phone_book, ensure_ascii=False))
    await bot.send_message(chat_id=message.chat.id, text="Данные сохранены")


@dp.message_handler(commands=['add'])
async def add_contact(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text="Введите имя:")
    name = (await dp.wait_for(types.Message)).text
    await bot.send_message(chat_id=message.chat.id, text="Введите номера телефонов через запятую:")
    phones = (await dp.wait_for(types.Message)).text.split(",")
    await bot.send_message(chat_id=message.chat.id, text="Введите email через запятую:")
    email = (await dp.wait_for(types.Message)).text.split(",")
    contact = {
        'phones': phones,
        'email': email,
        'birthday': (await bot.send_message(chat_id=message.chat.id, text="Введите день рождения:")).text
    }
    phone_book[name] = contact
    await save()
    await bot.send_message(chat_id=message.chat.id, text="Контакт успешно добавлен")


@dp.message_handler(commands=['exit'])
async def exit_program(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text="Программа завершена")


if __name__ == '__main__':
    asyncio.run(main())
