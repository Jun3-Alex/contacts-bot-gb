# Задача №49. Решение в группах
# Создать телефонный справочник с
# возможностью импорта и экспорта данных в
# формате .txt. Фамилия, имя, отчество, номер
# телефона - данные, которые должны находиться
# в файле.
# 1. Программа должна выводить данные
# 2. Программа должна сохранять данные в
# текстовом файле
# 3. Пользователь может ввести одну из
# характеристик для поиска определенной
# записи(Например имя или фамилию
# человека)
# 4. Использование функций. Ваша программа
# не должна быть линейной


import json


def create():
    with open('phone_book.json', "w", encoding='utf-8') as file:
        file.write(json.dumps(phone_book, ensure_ascii=False))
    print("Телефонная книга создана")


def save():
    with open('phone_book.json', "a", encoding='utf-8') as file:
        file.write(json.dumps(phone_book, ensure_ascii=False))
    print("Данные сохранены")


def load():
    global phone_book
    with open('phone_book.json', "r", encoding='utf-8') as file:
        phone_book = json.loads(file.read())
    print("Данные загружены")


def show():
    print(phone_book)


def add():
    name = input("Введите имя: ")
    phones = input("Введите номера телефонов через запятую: ").split(",")
    email = input("Введите email через запятую: ").split(",")
    contact = {
        'phones': phones,
        'email': email,
        'birthday': input("Введите день рождения: ")
    }
    phone_book[name] = contact
    save()
    print("Контакт успешно добавлен")


def find():
    contact_name = input("Введите имя: ")
    print(phone_book[contact_name])


def del_contact():
    contact_name = input("Введите имя: ")
    del phone_book[contact_name]
    print("Запись успешно удалена")


def exit():
    print("Программа завершена")


def menu():
    print("/menu. Меню")
    print("/create. Создать телефонный справочник")
    print("/show. Показать все контакты")
    print("/find. Найти контакт")
    print("/add. Добавить контакт")
    print("/del. Удалить контакт")
    print("/save. Сохранить")
    print("/load. Загрузить")
    print("/exit. Выход")


phone_book = {}
# create()
menu()

while True:
    command = input("Введите команду: ")
    if command == "/menu":
        menu()
    elif command == "/show":
        show()
    elif command == "/create":
        create()
    elif command == "/load":
        load()
    elif command == "/find":
        find()
    elif command == "/del":
        del_contact()
    elif command == "/save":
        save()
    elif command == "/add":
        add()
    elif command == "/exit":
        exit()
        break







