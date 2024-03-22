import os
import json
from file_manager import FileManager

def main():
    # Создаем объект FileManager
    file_manager = FileManager(os.getcwd())

    while True:
        # Отображаем меню
        print("\nДобро пожаловать в файловый менеджер!")
        print("Выберите действие:")
        print("1. Создать папку")
        print("2. Удалить папку")
        print("3. Перейти в папку")
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