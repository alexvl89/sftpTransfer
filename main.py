import datetime
import sys
import paramiko
from configuration import Configuration
import os
import log_entry.sqlprovider

logged_25_percent = False


class Main:
    def __init__(self, config_file):
        self.config_reader = Configuration(config_file)

    @classmethod
    def download_latest_file(cls, conf, domain='', use_ntlm_v2=True, port=22):
        try:
            local_path = conf.CopyPath
            serverpath = conf.ServerFolder

            # Создаем объект SFTPClient
            transport = paramiko.Transport(conf.ServerAddress, port)
            # Подключаемся
            transport.connect(username=conf.UserName, password=conf.Password)
            # формируем sftp канал
            sftp = paramiko.SFTPClient.from_transport(transport)
            # Переходим в каталог
            sftp.chdir(conf.ServerFolder)
            # Получаем список файлов и каталогов в текущем каталоге
            files = sftp.listdir()

            latest_file = None
            latest_m_time = 0
            file_size = 0

            print(f"Содержимое каталога {serverpath}:")
            for file in files:
                print(file)
                file_path = os.path.join(serverpath, file)
                fileinfo = sftp.file(file_path)
                print(fileinfo)
                file_stat = sftp.stat(file_path)

                last_modify = file_stat.st_mtime
                current_size = file_stat.st_size
                print(f'File: {file}')
                print(f'  Size: {current_size} bytes')
                print(f'  Permissions: {file_stat.st_mode}')
                print(f'  Last modified: {last_modify}')
                print()
                if (last_modify > latest_m_time):
                    latest_m_time = last_modify
                    latest_file = file
                    file_size = current_size

            main_file = os.path.join(serverpath, latest_file)
            local_path = os.path.join(local_path, latest_file)
            Main.write_log(f"Начало копирования {main_file} в {local_path}")

            sftp.get(main_file, local_path, callback=lambda transferred,
                     total: Main.print_progress(transferred, file_size))

            Main.write_log(f"Копирование в {local_path} завершено")

            # Закрываем соединение
            sftp.close()
            transport.close()

            if os.path.exists(local_path):
                # запускаем процедуру копирования в другое место
                Main.write_log("Запускаем процедуру копирования в новое место")

        except Exception as Ex:
            Configuration.write_file(f"file not seen {Ex}")

    @staticmethod
    def check_config_file(file_config_name: str):
        """
        Проверка конфигурационного файла
        :param file_config_name: Наименование конфигурационного файла
        :return:
        """
        try:
            # проверяем существование файла
            if not os.path.exists(file_config_name):
                Configuration.create_config(file_config_name)
                Configuration.write_file(
                    "Ошибка: отсутствует файл конфигурации.\n")
                Configuration.write_file(
                    "Необходимо заполнить файл конфигурации config.ini\n")
                Configuration.write_file(
                    "Следует указать необходимые параметры для работы программы.\n")
                return False
            else:
                # Если файл существует, возвращаем True
                return True
        except Exception as e:
            Configuration.write_file(f"Ошибка проверки файла конфигурации " +
                                     f"{file_config_name} {e}")

    @staticmethod
    def print_progress(transferred, total):
        """
        Вывод информации по загрузке файла
        Args:
           transferred (_type_): Размер загруженного файла
           total (_type_): Общий размер файла
        """

        percent = transferred / total * 100
        sys.stdout.write(f"\rProgress: {percent:.2f}%")
        sys.stdout.flush()

        # if percent >= 1 and percent < 6 and not logged_25_percent:
        #     Main.writeLog('25% of the file has been downloaded.')
        #     logged_25_percent = True

    @staticmethod
    def write_log(message: str) -> None:
        """
        Записываем лог
        Args:
            message (str): _description_
        """
        try:
            db = log_entry.sqlprovider.SqlProvider("mydb.sqlite")
            db.add_log_entry(1, f"{message}")
            db.close()
        except Exception as e:
            # Записываем в файл error лог и ошибку исключения
            dt_now = datetime.datetime.now()
            Configuration.write_file(f"{dt_now} Событие записи в лог - {message}")
            Configuration.write_file(
                f"{dt_now} Ошибка записи в базу данных - {e}")


if __name__ == "__main__":
    try:
        # смотрим текущую папку
        currentDir = os.path.dirname(sys.argv[0])
        fileConfig = "config.ini"
        file_path = os.path.join(currentDir, fileConfig)
        if not Main.check_config_file(file_path):
            msg = "Файл конфигурации отсутствует. Создан новый файл config.ini."
            Main.write_log(msg)
            Configuration.write_file(f"{msg}")
        else:
            msg = f"Файл конфигурации найден. {file_path}"
            Main.write_log(msg)
            Configuration.write_file(msg)

        mainObj = Configuration.read_config_file(file_path)

        dwnl_obj = Main(file_path)
        # загружаем файл
        dwnl_obj.download_latest_file(mainObj)
    except Exception as e:
        Main.write_log(f"Ошибка загрузки файла {e}")
        # Configuration.write_file(f"Ошибка загрузки файла {e}")

    # input("Ожидание")
