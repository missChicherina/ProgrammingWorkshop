import os
import json
from file_manager import FileManager

def login_or_register(file_manager):
    with open(r"settings.json", "r") as settings_file:
        settings = json.load(settings_file)
    
    print("Доступные пользователи:")
    for user in settings["users"]:
        print(user)

    while True:
        username = input("Введите имя пользователя: ")

        if username in settings["users"]:
            # Пытаемся войти в аккаунт пользователя
            file_manager.login_user(username)
            break
        else:
            # Предлагаем зарегистрировать нового пользователя
            choice = input("Пользователь не найден. Зарегистрировать нового пользователя? (y/n): ")
            if choice.lower() == "y":
                file_manager.register_user(username)
                break
            elif choice.lower() == "n":
                continue
            else:
                print("Некорректный ввод. Попробуйте снова.")

def main():
    file_manager = FileManager(os.getcwd())
    login_or_register(file_manager)

    while True:
        # Отображаем меню
        print("\nДобро пожаловать в файловый менеджер!")
        print("Выберите действие:")
        print("1. Создать папку")
        print("2. Удалить папку")
        print("3. Перейти в папку")
        print("4. Создать файл")
        print("5. Записать текст в файл")
        print("6. Просмотреть содержимое файла")
        print("7. Удалить файл")
        print("8. Скопировать файл")
        print("9. Переместить файл")
        print("10. Переименовать файл")
        print("11. Показать список файлов и папок")
        print("12. Архивировать папку")
        print("13. Проверить квоту дискового пространства")
        print("0. Выход")

        choice = input("Введите номер действия: ")

        if choice == "1":
            directory_name = input("Введите имя новой папки: ")
            file_manager.create_directory(directory_name)
        elif choice == "2":
            directory_name = input("Введите имя папки для удаления: ")
            file_manager.delete_directory(directory_name)
        elif choice == "3":
            directory_name = input("Введите имя папки для перехода: ")
            file_manager.change_directory(directory_name)
        elif choice == "4":
            file_name = input("Введите имя нового файла: ")
            file_manager.create_file(file_name)
        elif choice == "5":
            file_name = input("Введите имя файла для записи текста: ")
            text = input("Введите текст для записи в файл: ")
            file_manager.write_to_file(file_name, text)
        elif choice == "6":
            file_name = input("Введите имя файла для просмотра содержимого: ")
            file_manager.read_file(file_name)
        elif choice == "7":
            file_name = input("Введите имя файла для удаления: ")
            file_manager.delete_file(file_name)
        elif choice == "8":
            source_file = input("Введите имя файла для копирования: ")
            destination_directory = input("Введите имя целевой папки: ")
            file_manager.copy_file(source_file, destination_directory)
        elif choice == "9":
            source_file = input("Введите имя файла для перемещения: ")
            destination_directory = input("Введите имя целевой папки: ")
            file_manager.move_file(source_file, destination_directory)
        elif choice == "10":
            old_name = input("Введите старое имя файла: ")
            new_name = input("Введите новое имя файла: ")
            file_manager.rename_file(old_name, new_name)
        elif choice == "11":
            file_manager.list_files()
        elif choice == "12":
            folder_name = input("Введите имя папки для архивации: ")
            file_manager.archive_folder(folder_name)
        elif choice == "13":
            file_manager.quota_status()
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Некорректный ввод. Попробуйте снова.")

if __name__ == "__main__":
    main()