## SFTPyTransfer

SFTPyTransfer это простой в использовании инструмент Python дл€ автоматизированной передачи файлов по протоколу SFTP.

#### ƒл€ работы приложение требуетс€ выполнение следующих действий:
#### —оздайте конфигурационный файл config.ini

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
> ƒобавление другие настроек<br>

