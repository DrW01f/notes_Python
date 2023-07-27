# Задача №49. Решение в группах Создать телефонный справочник с
# возможностью импорта и экспорта данных в формате .txt. Фамилия, имя,
# отчество, номер телефона - данные, которые должны находиться
# в файле.
# 1. Программа должна выводить данные
# 2. Программа должна сохранять данные в текстовом файле
# 3. Пользователь может ввести одну из характеристик для поиска
# определенной записи(Например имя или фамилию человека)
# 4. Использование функций. Ваша программа не должна быть линейной

# Задача 38: Дополнить телефонный справочник возможностью изменения и
# удаления данных. Пользователь также может ввести имя или фамилию, и Вы
# должны реализовать функционал для изменения и удаления данных

import os
import json
import time

"""
данные в файле будут храниться в виде списка словарей!
os.getcwd() - текущая рабочая директория.
os.listdir(path=".") - список файлов и директорий в папке.
"""


def full_name_file(name="note", extension=".json") -> str:
    """
    Функция для возвращения имени файла (при работе в текущей директории)
    """
    return name + extension


def create_file(file_name: str) -> None:
    """
    Функция для создания файла
    """
    if file_name not in os.listdir(os.getcwd()):
        file = open(file_name, "w", encoding="UTF-8")
        file.write("[]")
        print(f'Создан файл: {file_name}')


def load_info() -> list:
    """
    Загружает данные из файла
    """
    name = full_name_file()
    with open(name, "r", encoding="UTF-8") as file:
        data = json.load(file)
    return data


def create_info(data: list) -> None:
    """
    Функция добавляет новую заметку
    """
    data.append(
            dict(
                #id=input("Введите имя контакта:\n"),
                head=input("Введите заголовок заметки:\n"),
                note_body=input("Введите текст заметки:\n"),
                last_edit_time = time.ctime(os.path.getmtime(full_name_file()))
                )
            )
    print("Заметка успешно добавлена")


def save_info(data: list) -> None:
    """
    Функция для сохранения информации в файл
    """
    name = full_name_file()
    with open(name, "w", encoding="UTF-8") as file:
        json.dump(data, file, ensure_ascii=False)


def show_info(notes: list) -> None:
    """
    Функция выводит на экран содержание заметок
    """
    if len(notes) < 1:
        print("Заметок пока нет")
    else:
        note_dict = dict(
                head = "Заголовок",
                note_body= "Содержание заметки",
                last_edit_time="Время последнего редактирования"            
                )
        info = str()
        for num, elem in enumerate(notes, 1):
            info += f"\n Заметка №{num}:\n"
            info += "\n".join(f"{note_dict[k]}:  {v}" for k, v in elem.items())
            info += "\n---------------\n"
        print(info)


def delete_info(data: list)-> None:
    """
    Функция удаляет конкретную заметку 
    """
    if len(data) > 0:
        while True:
            try:
                number = int(input("Выберите номер(id) заметки, который хотите удалить: \n(0 - показать заметки) \n-1 прервать команду\n"))
                if number == 0:
                    show_info(data)
                elif number == -1:
                    break
                elif 1 <= number < len(data) +1:
                    data.pop(number - 1)
                    print(f"\n Заметка № {number} успешно удалена")            
                    break
                else:
                    print("Такого номера(id) заметки не существует")
            except ValueError:
                print("Введено неправильное значение")
    else:
        print("Заметок пока нет")


def find_contact(data: list)->None:
    """
    Функция для поиска заметок
    """
    if len(data) > 0:
        find = input("Введите значение для поиска:  ")
        result = list(filter(lambda elem: find in elem["head"] or find in elem["note_body"] or find in elem["create_time"], data))
        if result:
            print(f"Найдено {len(result)} заметок: \n")
            show_info(result)
        else:
            print("Ничего не найдено")
    else:
        print("Заметок пока нет")


def change_info(data: list)->None:
    """
    Функция изменяет заметки по выбору параметра
    """
    if len(data) > 0:
        while True:
            try:
                number = int(input("\nВыберите номер(id) заметки, которую хотите изменить: \n(0 - показать заметки, -1 прервать команду)\n"))
                if number == 0:
                    show_info(data)
                elif number == -1:
                    break
                elif 1 <= number < len(data) +1:
                    while True:
                        elem = data[number-1]
                        change = input("Выберите параметр для изменения: З - заголовок, Т - текст заметки (-1 - прервать команду):\n")
                        if change == "-1":
                                break                            
                        elif change.lower() == "з":
                            elem["head"] = input("Введите новый заголовок:\n")
                        elif change.lower() == "т": 
                            elem["note_body"] = input("Введите новую заметку:\n")
                        else:
                            print("Введено неправильное значение")
                    
                    print(f"Заметка № {number} успешно изменена")            
                    elem["last_edit_time"] = time.ctime(os.path.getmtime(full_name_file()))
                    break
                else:
                    print("Такой заметки не существует")
            except ValueError:
                print("Введено неправильное значение")
    else:
        print("Заметок пока нет")



def menu()-> int:
    """
    Функция возвращает значение порядкого номера команды из всех возможных
    """
    command = {
        "exit" : "Закончить работу",
        "show": "Показать все заметки", 
        "add": "Добавить новую заметку", 
        "find": "Найти заметку",
        "change" : "Изменить заметку",
        "delete" : "Удалить заметку"
        }         
    
    while True:        
        choice = input("Нажмите цифру команды или введите 'help' для получения справки(0 - завершение работы): ")
        if choice.isdigit():
            if 0 <= int(choice) < len(command):
                return(int(choice))
            else:
                print("Такой команды пока нет")
        elif choice.lower() == "help":
            print("На данный момент программа обладает следующими возможностями:")        
            for num, val in enumerate(command.values()):
                print(num, val)
        else:
            print("Неизвестная команда")
         
 
def main():
    """
    Главная функция
    """
    name = full_name_file()
    create_file(name)
    data = load_info()
   
    while True:
        command = menu()    
        if command == 0:            
            print("Личинка skynet закончила свою работу")
            return
        elif command == 1:
            show_info(data)
        elif command == 2:
            create_info(data)
        elif command == 3:
            find_contact(data) 
        elif command == 4:
            change_info(data) 
        elif command == 5:
            delete_info(data)
        save_info(data)   
        
if __name__ == '__main__':
    main()
