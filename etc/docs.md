## Docs | Документация

<details>
    <summary>Русский</summary>

### Введение

В этой документации будет описан процесс *работы и управления* ботом KeepInventory. Если вам нужна помощь в установке, перейдите на основную страницу [проекта](https://github.com/hiimluck3r/KeepInventory).


***
***Функция поиска по аудитории неактуальна и была вырезана из дальнейших билдов.***
***

Итак, вы установили, настроили и запустили бота, однако он не отвечает на все ваши действия?

Первым делом необходимо использовать команду `/initroot`, чтобы ваш ID внесли в базу данных как ROOT-пользователя.
![Инициализация root пользователя](/etc/images/initroot.png)

После этого можно использовать бота самостоятельно, например, открыть его меню (если вы этого не сделали при первом запуске) при помощи команды `/start`:
![/start](/etc/images/start_registered.png)

Стоит заметить, что незарегистрированные пользователи получат другое меню, отличающееся от вашего:
![/start not registered](/etc/images/start_not_registered.png)

### Регистрация пользователей
Если вы хотите зарегистрировать пользователя, то вы можете выдать ему одну из ролей:

- Spectator - read-only роль, позволяющая просматривать список устройств (как обычных, так и проблемных)
- Worker - роль, имеющая владеющая правами spectator, правом на изменение и создание новых записей, в том числе и в разделах "Заметки" и "Программное обеспечение".
- Admin - роль, владеющая правами worker, а также правами на:
    * Изменение приветственных текстов для пользователей
    * Перезагрузку бота
    * Загрузка резервных копий из бота и в бота
    * Чтение и удаление лог-файлов
    * Редактирование нижестоящих ролей
- ROOT - роль, владеющая правами admin, а также способная редактировать группу admin.

Для выдачи роли используйте команду `/make` в формате `/make id.role`, например:

![Выдать роль наблюдателя](/etc/images/make_spectator.png)

Узнать свой id пользователь может при помощи команды `/id`:

![Узнать свой id](/etc/images/myid.png)

Для проверки результата можно воспользоваться командой `/users`, которая позволяет вывести список всех зарегистрированных пользователей вместе с их Telegram ID, ролью и Telegram-ником (если таковой имеется, иначе - 404NotFound)
![/users](/etc/images/users.png)

Все команды для манипуляции с ролями:
- `/make id.role` - выдача роли пользователю. Доступные роли: spectator, worker
- `/rm id` - удаление пользователя из списка зарегистрированных
- `/makeadmin id` - выдача пользователю прав администратора
- `/rmadmin id` - удаление пользователя из списка администраторов

![Команды для манипуляции с ролями](/etc/images/all_role_commands.png)

### Начало работы
![Главное меню](/etc/images/main_menu.png)

Очевидно, что с самого начала у нас нет устройств. Обратимся через главное меню к разделу "Новое устройство" для создания нового.

![Новое устройство](/etc/images/create_new_device_start.png)

Если устройство не было найдено, то пользователям с ролью WORKER и выше будет предложено создать новую запись.

![Создать новую запись 1](/etc/images/create_new_device_process_first.png)

При возможности мы можем приложить фотографию:

![Создать новую запись 2](/etc/images/create_new_device_process_second.png)

**Фотографии хранятся на серверах Telegram, а в нашей базе хранятся лишь fileid этих фотографий.**

Давайте подтвердим запись и попробуем ее найти по ***последним символам артикула***:

![Поиск по артикулу 1](/etc/images/find_by_article_start.png)

![Поиск по артикулу 2](/etc/images/information_by_article.png)
***
>***P.S: В дальнейших сборках "артикул" будет заменён на "инвентарный номер", однако смысл заключается тот же.***
***


Однако не всегда удобно вписывать артикул самому, поэтому в боте есть функция распознавания штрих-кодов (рекомендованы к использованию CODE-128, QR-коды не поддерживаются, однако переписать логику под них несложно).

![Поиск по штрих-коду 1](/etc/images/search_by_barcode.png)

Как мы можем заметить, такого штрих-кода у нас нет, поэтому бот предлагает нам его записать. Процесс записи аналогичен:

![Создание новой записи по штрих-коду](/etc/images/create_device_by_barcode.png)

![Информация по штрих-коду](/etc/images/info_by_barcode.png)

### Редактирование данных
![Редактирование данных](/etc/images/information_by_article.png)

Вернемся к нашим устройствам. Как вы могли заметить, под описанием имеется много кнопок, каждая из которых отвечает за редактирование определенного параметра. Доступ к ним есть только у пользователей с ролью WORKER и старше.

Помимо возможностей редактирования и удаления устройств, у нас есть возможность объявить устройство ***проблемным***.

### Проблемные устройства
> ***Проблемным называется то устройство, которое по каким-либо причинам не выполняет требуемые функции в должном виде.***

Короче говоря, проблемное устройство - это такое устройство, которое нужно привести в рабочую норму: исправить локализацию, обновить драйвера, ОС, либо вовсе устранить физическую неисправность.

Когда мы объявляем устройство *проблемным*, мы указываем причину, а само устройство добавляется в специальную таблицу для работы над ним.

![Добавить проблемное устройство](/etc/images/make_problematic.png)

Так обозначаются проблемные устройства при их сканировании:

![Проблемное устройство](/etc/images/info_if_in_problematic.png)

А в меню "проблемные устройства" это выглядит так:

![Проблемное устройство в отдельном меню](/etc/images/problematicdevices.png)

Spectator-ы видят это меню следующим образом:

![Spectators see like this](/etc/images/spectator_problematic_devices.png)

По окончании работ устройство можно объявить исправным, а также приложить описание решения (либо поправить описание проблемы):

![Исправленное проблемное устройство](/etc/images/solved_problematic_devices.png)

![Добавить решение](/etc/images/redact_solution.png)

### Программное обеспечение и Заметки
> В версии без локального Telegram API передача файлов ограничена 20МБ на скачивание и 50 на отправку, поэтому хранение файлов осуществляется в виде ссылок на внешние ресурсы.
***
Эти два пункта в меню работают схожим образом, поэтому принцип работы будем объяснять на примере Программного обеспечения (в дальнейшем ПО).

![ПО](/etc/images/software_menu.png)

Предположим, мы хотим посмотреть доступное ПО, опубликованное другими пользователями:

![ПО отсутствует](/etc/images/software_menu_no_software.png)

Если его нет, нам попросту не на что смотреть, поэтому давайте просто создадим новое ПО с ссылкой на этот репозиторий:

![Добавление нового ПО](/etc/images/software_upload.png)

И попробуем посмотреть на наше ПО теперь:

![ПО 2](/etc/images/available_software.png)

***Заметки работают идентично***

### Админ-меню
Раз мы упомянули администраторов, то пора показать их специальный инструмент - админ-меню/панель или admin-dashboard (называйте как хотите):

![admin-dashboard](/etc/images/admin_dashboard.png)

Здесь мы можем изменить стандартные приветственные сообщения для зарегистрированных и незарегистрированных пользователей, а также много других интересных вещей, например ***бэкапы***.

### Бэкапы
Бэкапы, или же резервное копирование, производятся в формате .csv таблиц ***БЕЗ ЗАГОЛОВКОВ И С РАЗДЕЛИТЕЛЕМ-ЗАПЯТОЙ***.

Если таблицы не пусты, то Telegram отправит их без проблем, в ином случае он отправит предупредительную ошибку (не стоит ее бояться).

![Скачивание бэкапов](/etc/images/backup.png)

С загрузкой бэкапов чуть сложнее:

***Все данные, которые были в боте до момента загрузки бэкапа стираются и заменяются на представленные.***

Для вашей же безопасности мы делаем отдельный бэкап существующей таблицы, чтобы в случае чего вы могли "откатиться" до последнего сохранения.

![Сохранение при загрузке бэкапа на сервер](/etc/images/upload_backup_1.png)

![Предупредительное сообщение перед загрузкой бэкапа](/etc/images/backup_upload_2.png)

### Перезагрузка бота
Перезагрузка бота производится посредством завершения процесса контейнера, после чего он вновь загружается. Перезагружать контейнер необходимо, например, когда вы меняете приветственные сообщения.

### Просмотр log-файлов
Просмотр логов доступен в админ-меню по нажатии на соответствующую кнопку:

![Просмотр логов 1](/etc/images/logs_check_1.png)

![Просмотр логов 2](/etc/images/logs_check_2.png)

Обычно сообщения log-файлов ОЧЕНЬ большие, поэтому их приходится разбивать на несколько сообщений, поэтому не удивляйтесь, если бот вам чуть-чуть поспамит.

Удалить можно читаемый лог-файл или все сразу.

![Удалить текущий лог](/etc/images/delete_log_message.png)
</details>

<details>
    <summary>English</summary>

### Introduction

This documentation will describe the process of *working and managing* the KeepInventory bot. If you need help with the installation, go to the main page of the [project](https://github.com/hiimluck3r/KeepInventory).


***
***The audience search function is irrelevant and has been cut out of further builds.***
***

So, you have installed, configured and launched a bot, but it does not respond to all your actions?

The first step is to use the `/initroot` command so that your ID is entered into the database as the ROOT user.

![Initializing the root user](/etc/images/initroot.png)

After that, you can use the bot yourself, for example, open its menu (if you did not do this at the first launch) using the command `/start`:

![/start](/etc/images/start_registered.png)

It is worth noting that unregistered users will receive a different menu from yours:

![/start not registered](/etc/images/start_not_registered.png)

### User Registration
If you want to register a user, then you can give him one of the roles:

- Spectator - read-only role that allows you to view a list of devices (both normal and problematic)
- Worker - a role that has spectator rights, the right to change and create new records, including in the "Notes" and "Software" sections.
- Admin - a role that owns worker rights, as well as rights to:
    * Changing welcome texts for users
    * Reboot the bot
    * Uploading backups from and to the bot
    * Reading and deleting log files
    * Editing lower-level roles
- ROOT - a role that owns admin rights and is also able to edit the admin group.

To issue a role, use the command `/make` in the format `/make id.role`, for example:

![Assign observer role](/etc/images/make_spectator.png)

The user can find out his id using the `/id` command:

![Find out your id](/etc/images/myid.png)

To check the result, you can use the `/users` command, which allows you to display a list of all registered users along with their Telegram ID, role and Telegram nickname (if any, otherwise - 404NotFound)

![/users](/etc/images/users.png)

All commands for manipulating roles:
- `/make id.role` - assigning a role to a user. Available roles: spectator, worker
- `/rm id` - removing a user from the list of registered
users 
- `/makeadmin id` - granting administrator rights to the user
- `/rmadmin id` - removing a user from the list of administrators

![Commands for manipulating roles](/etc/images/all_role_commands.png)

### Getting started

![Main Menu](/etc/images/main_menu.png)

Obviously, from the very beginning we have no devices. Let's go through the main menu to the "New device" section to create a new one.

![New Device](/etc/images/create_new_device_start.png)

If the device was not found, then users with the WORKER role and above will be prompted to create a new record.

![Create a new entry 1](/etc/images/create_new_device_process_first.png)

If possible, we can attach a photo:

![Create New Entry 2](/etc/images/create_new_device_process_second.png)

**Photos are stored on Telegram servers, and only the fileid of these photos are stored in our database.**

Let's confirm the entry and try to find it by ***the last characters of the article***:

![Search by article 1](/etc/images/find_by_article_start.png)

![Search by article 2](/etc/images/information_by_article.png)
***
>***P.S: In future builds, the "article" will be replaced by the "inventory number", but the meaning is the same.***
***


However, it is not always convenient to enter the article yourself, so the bot has a barcode recognition function (CODE-128 is recommended for use, QR codes are not supported, but it is not difficult to rewrite the logic for them).

![Barcode Search 1](/etc/images/search_by_barcode.png)

As we can see, we don't have such a barcode, so the bot offers us to write it down. The recording process is similar:

![Creating a new entry by barcode](/etc/images/create_device_by_barcode.png)

![Barcode Information](/etc/images/info_by_barcode.png)

### Data editing

![Data Editing](/etc/images/information_by_article.png)

Back to our devices. As you may have noticed, there are many buttons under the description, each of which is responsible for editing a certain parameter. Only users with the WORKER role and older have access to them.

In addition to the ability to edit and delete devices, we have the ability to declare the device ***problematic***.

### Problematic devices
> ***A problematic device is one that, for some reason, does not perform the required functions in the proper way.***

In short, a problematic device is a device that needs to be brought into working order: correct localization, update drivers, OS, or eliminate a physical malfunction altogether.

When we declare a device *problematic*, we indicate the reason, and the device itself is added to a special table to work on it.

![Add Problematic device](/etc/images/make_problematic.png)

This is how problematic devices are designated when they are scanned:

![Problematic device](/etc/images/info_if_in_problematic.png)

And in the "problematic devices" menu it looks like this:

![Problematic device in a separate menu](/etc/images/problematicdevices.png)

Spectators can see this menu like this:

![Spectators see like this](/etc/images/spectator_problematic_devices.png)

At the end of the work, the device can be declared serviceable, and also attach a description of the solution (or correct the description of the problem):

![Fixed problematic device](/etc/images/solved_problematic_devices.png)

![Add Solution](/etc/images/redact_solution.png)

### Software and Notes
> In the version without the local Telegram API, file transfer is limited to 20 MB for downloading and 50 for sending, so files are stored as links to external resources.
***
These two menu items work in a similar way, so we will explain the principle of operation using the example of Software (hereinafter software).

![Software](/etc/images/software_menu.png)

Suppose we want to see the available software published by other users:

![Software is missing](/etc/images/software_menu_no_software.png)

If it's not there, we simply have nothing to look at, so let's just create a new software with a link to this repository:

![Adding new software](/etc/images/software_upload.png)

And let's try to look at our software now:

![Software 2](/etc/images/available_software.png)

***Notes work identically***

### Admin menu
Since we mentioned administrators, it's time to show their special tool - admin menu/panel or admin dashboard (call it what you want):

![admin-dashboard](/etc/images/admin_dashboard.png)

Here we can change the standard welcome messages for registered and unregistered users, as well as many other interesting things, for example ***backups***.

### Backups
Backups are made in the format of .csv tables ***WITHOUT HEADERS AND WITH A COMMA SEPARATOR***.

If the tables are not empty, then Telegram will send them without problems, otherwise it will send a warning error (do not be afraid of it).

![Downloading backups](/etc/images/backup.png)

Uploading backups is a little more difficult:

***All data that was in the bot before the backup was loaded is erased and replaced with the submitted data.***

For your own safety, we are making a separate backup of the existing table, so that if anything happens, you can "roll back" to the last save.

![Saving when uploading a backup to the server](/etc/images/upload_backup_1.png)

![Warning message before uploading backup](/etc/images/backup_upload_2.png)

### Reboot the bot
The bot is rebooted by completing the container process, after which it is loaded again. It is necessary to reload the container, for example, when you change the welcome messages.

### Viewing log files
Viewing logs is available in the admin menu by clicking on the corresponding button:

![Viewing logs 1](/etc/images/logs_check_1.png)

![Viewing logs 2](/etc/images/logs_check_2.png)

Log file messages are usually VERY large, so they have to be split into several messages, so don't be surprised if the bot spams you a little.

You can delete a readable log file or all at once.

![Delete current log](/etc/images/delete_log_message.png)

</details>
