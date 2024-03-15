## SFTPyTransfer

SFTPyTransfer это простой в использовании инструмент Python для автоматизированной передачи файлов по протоколу SFTP.

#### Для работы приложение требуется выполнение следующих действий:
#### Создайте конфигурационный файл config.ini

> [FTP] <br>
> server_address = удаленный.адрес.сервера <br>
> server_folder = /remote/path/to/folder<br>
> copy_path = /local/path/to/folder<br>
> username = User_Name<br>
> password = Pass<br><br>
> [Settings] <br>
> database = databaseType (sqlite, postgres)<br><br>
> [Sqlite]<br>
> file_path = /local/path/file.db<br><br>
> [Postgres]<br>
database=db_name<br>
user=db_user<br>
password=db_password<br>
host=db_host<br>
port=db_port<br>
> Добавление другие настроек<br>

