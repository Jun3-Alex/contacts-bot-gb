from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Создать"),
            KeyboardButton(text="Загрузить"),
            KeyboardButton(text="Сохранить")
        ],
        [
            KeyboardButton(text="Показать все"),
            KeyboardButton(text="Найти"),
            KeyboardButton(text="Добавить")
        ],
        [
            KeyboardButton(text="Удалить"),
            KeyboardButton(text="Выход")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите действие из меню",
    selective=True
)


