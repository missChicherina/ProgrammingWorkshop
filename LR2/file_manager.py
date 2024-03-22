import json
import os
import shutil

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

    
    # # # # # # # ДОПОЛНИТЕЛЬНЫЕ ЗАДАНИЯ # # # # # # # 

    # Архивация и разархивация файлов и папок;        
    def archive_folder(self, folder_name):
        folder_path = os.path.join(self.current_directory, folder_name)
        shutil.make_archive(folder_path, 'zip', root_dir=folder_path)
        print(f"Папка '{folder_name}' успешно архивирована.")

    #  Квотирование дискового пространства и отображение занятого оставшегося места;
    def quota_status(self):
        total_space = shutil.disk_usage(self.current_directory).total
        used_space = sum(os.path.getsize(os.path.join(self.current_directory, file)) for file in os.listdir(self.current_directory) if os.path.isfile(os.path.join(self.current_directory, file)))
        remaining_space = total_space - used_space
        print(f"Total space: {total_space} bytes")
        print(f"Used space: {used_space} bytes")
        print(f"Remaining space: {remaining_space} bytes")