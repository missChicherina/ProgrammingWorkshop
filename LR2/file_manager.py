import os
import shutil
import json

class FileManager:
    def __init__(self, current_directory):
        self.current_directory = current_directory
        with open(r"settings.json", "r") as settings_file:
            settings = json.load(settings_file)
        self.users = settings["users"]  # Словарь пользователей
        self.load_users_data()  # Загрузка данных о пользователях
    
    # # # # # # # ОСНОВНЫЕ ЗАДАНИЯ # # # # # # # 
    
    # Создание папки (с указанием имени);
    def create_directory(self, directory_name):
        new_directory_path = os.path.join(self.current_directory, directory_name)
        if not os.path.exists(new_directory_path):
            os.mkdir(new_directory_path)
            print(f"Папка '{directory_name}' успешно создана.")
        else:
            print(f"Папка с именем '{directory_name}' уже существует.")

    # Удаление папки по имени;
    def delete_directory(self, directory_name):
        directory_to_delete = os.path.join(self.current_directory, directory_name)
        if os.path.exists(directory_to_delete):
            shutil.rmtree(directory_to_delete)
            print(f"Папка '{directory_name}' успешно удалена.")
        else:
            print(f"Папки с именем '{directory_name}' не существует.")
    
    # Перемещение между папками (в пределах рабочей папки) - заход в папку по имени, выход на уровень вверх;
    def change_directory(self, directory_name):
        target_directory = os.path.join(self.current_directory, directory_name)
        if os.path.exists(target_directory) and os.path.isdir(target_directory):
            # Проверяем, является ли целевая папка папкой пользователя
            for user, user_dir in self.users.items():
                if user_dir == target_directory:
                    self.current_directory = target_directory
                    print(f"Перешли в папку '{directory_name}'.")
                    return

            self.current_directory = os.path.dirname(self.current_directory)
            print(f"Выйдено из папки '{directory_name}'.")
        else:
            print(f"Папки с именем '{directory_name}' не существует или это не папка.")

    # Создание пустых файлов с указанием имени;
    def create_file(self, file_name):
        new_file_path = os.path.join(self.current_directory, file_name)
        if not os.path.exists(new_file_path):
            open(new_file_path, 'w').close()
            print(f"Файл '{file_name}' успешно создан.")
        else:
            print(f"Файл с именем '{file_name}' уже существует.")

    # Запись текста в файл; 
    def write_to_file(self, file_name, text):
        file_path = os.path.join(self.current_directory, file_name)
        with open(file_path, 'w') as file:
            file.write(text)
        print(f"Текст успешно записан в файл '{file_name}'.")

    # Просмотр содержимого текстового файла;
    def read_file(self, file_name):
        file_path = os.path.join(self.current_directory, file_name)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                content = file.read()
            print(f"Содержимое файла '{file_name}':")
            print(content)
        else:
            print(f"Файл с именем '{file_name}' не существует или это не файл.")

    # Удаление файлов по имени;
    def delete_file(self, file_name):
        file_path = os.path.join(self.current_directory, file_name)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Файл '{file_name}' успешно удален.")
        else:
            print(f"Файл с именем '{file_name}' не существует или это не файл.")

    # Копирование файлов из одной папки в другую;
    def copy_file(self, source_file, destination_directory):
        source_file_path = os.path.join(self.current_directory, source_file)
        destination_directory_path = os.path.join(self.current_directory, destination_directory)
        if os.path.exists(source_file_path) and os.path.isfile(source_file_path) and os.path.exists(destination_directory_path) and os.path.isdir(destination_directory_path):
            shutil.copy(source_file_path, destination_directory_path)
            print(f"Файл '{source_file}' успешно скопирован в папку '{destination_directory}'.")
        else:
            print(f"Исходный файл '{source_file}' не существует или это не файл, либо целевая папка '{destination_directory}' не существует или это не папка.")

    # # # # # # # ДОПОЛНИТЕЛЬНЫЕ ЗАДАНИЯ # # # # # # # 

    # Архивация и разархивация файлов и папок;     
    def archive_folder(self, folder_name):
        folder_path = os.path.join(self.current_directory, folder_name)
        shutil.make_archive(folder_path, 'zip', root_dir=folder_path)
        print(f"Папка '{folder_name}' успешно архивирована.")

    def quota_status(self):
        total_space = shutil.disk_usage(self.current_directory).total
        used_space = sum(os.path.getsize(os.path.join(self.current_directory, file)) for file in os.listdir(self.current_directory) if os.path.isfile(os.path.join(self.current_directory, file)))
        remaining_space = total_space - used_space
        print(f"Total space: {total_space} bytes")
        print(f"Used space: {used_space} bytes")
        print(f"Remaining space: {remaining_space} bytes")
