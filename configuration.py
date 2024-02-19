import configparser
import platform
import os
import sys
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Settings:
    """
    Класс для хранения настроек
    """
    ServerAddress: str
    CopyPath: str
    UserName: str
    Password: str
    ServerFolder: str


class Configuration:
    """
    Класс для чтения конфигурации
    """

    def __init__(self, config_file):
        #  self.config = _readConfigFile("testLab\config.ini")
        print(f"Инициализация класса чтения конфигурации {config_file}")

    @staticmethod
    def create_config(path_file: str):
        """
        Create a config file
        """
        config = configparser.ConfigParser()
        config.add_section("FTP")
        config.set("FTP", "server_address", "address")
        config.set("FTP", "copy_path", "path")
        config.set("FTP", "username", "username")
        config.set("FTP", "password", "pass")
        config.set("FTP", "server_folder", "folder")

        # сохранение конфигурации в файл
        with open(path_file, "w") as config_file:
            config.write(config_file)

    @staticmethod
    def read_config_file(file_path: str) -> Settings:
        try:
            """
            Чтение конфигурации
            """
            config = configparser.ConfigParser()
            config.read(file_path)
            config.sections()

            server_address = config.get('FTP', 'server_address')
            copy_path = config.get('FTP', 'copy_path')
            username = config.get('FTP', 'username')
            password = config.get('FTP', 'password')
            server_folder = config.get('FTP', 'server_folder')

            config = Settings(server_address, copy_path,
                              username, password, server_folder)
            return config
        except Exception as e:
            Configuration.write_file(
                f"Метод чтения конфигурации: Обработка исключения {e}")
            raise

    @staticmethod
    def check_os():
        system = platform.system()
        if system == 'Windows':
            print("Вы используете операционную систему Windows.")
        elif system == 'Linux':
            print("Вы используете операционную систему Linux.")
        elif system == 'Darwin':
            print("Вы используете операционную систему macOS.")
        else:
            print(
                f"Не удалось определить операционную систему. Система: {system}")

    if __name__ == "__main__":
        print(os.name)
        print(os.getlogin())
        check_os()
        config = configparser.ConfigParser()
        config.read('config.ini')
        config.sections()

        server_address = config.get('FTP', 'server_address')
        copy_path = config.get('FTP', 'copy_path')
        username = config.get('FTP', 'username')
        password = config.get('FTP', 'password')
        server_folder = config.get('FTP', 'server_folder')

        # Для создания файла конфигурации вдруг
        # path = "settings.ini"
        # createConfig(path)

    @classmethod
    def write_file(cls, msg: str):
        current_dir = os.path.dirname(sys.argv[0])
        file_name = "Error.txt"
        file_path = os.path.join(current_dir, file_name)
        # Если файл не существует, создаем его и записываем сообщение об ошибке
        with open(file_path, "a") as f:
            now = datetime.now()
            f.write(f"{now} \t {msg}.\n")
