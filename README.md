<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/hiimluck3r/KeepInventory">
    <img src="etc/images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">KeepInventory</h3>

  <p align="center">
    Telegram bot for inventory of tech, software, and notes.
    <br />
    Телеграм-бот для инвентаризации техники, ПО и заметок.
    <br />
    <a href="https://github.com/hiimluck3r/KeepInventory/blob/master/etc/docs.md"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/hiimluck3r/KeepInventory/issues">Report Bug</a>
    ·
    <a href="https://github.com/hiimluck3r/KeepInventory/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents | Быстрая навигация</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project | О проекте</a>
      <ul>
        <li><a href="#built-with">Built With | Стек технологий</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started | Начало работы</a>
      <ul>
        <li><a href="#prerequisites">Requirements | Зависимости</a></li>
        <li><a href="#installation">Installation | Установка</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage | Использование</a></li>
    <li><a href="#contributing">Contributing | Сотрудничество</a></li>
    <li><a href="#license">License | Лицензия</a></li>
    <li><a href="#contact">Contact | Контакты</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project | О проекте
<a name="about-the-project"></a>
The project arose as an urgent need to find a toolkit for a quick inventory of technology in an educational institution. The bot was also created for educational purposes and was submitted as a course project.

Проект возник из-за острой необходимости найти инструментарий для быстрой инвентаризации технологий в образовательном учреждении. Бот также был создан в образовательных целях и был представлен в качестве курсового проекта.


### Built With | Стек технологий
<a name="built-with"></a>
* Python (OpenCV, pyzbar, aiogram, asyncpg)
* PostgreSQL
* Docker



<!-- GETTING STARTED -->
## Getting Started | Начало работы
<a name="getting-started"></a>
The project is designed to run inside containers, so make sure you have a container engine installed (Docker is recommended).
(Проект предназначен для работы в контейнерах, поэтому убедитесь, что у вас установлен контейнерный движок, рекомендуется Docker).

### Prerequisites | Зависимости
<a name="prerequisites"></a>
Make sure you have Docker installed.
(Убедитесь, что у вас установлен Docker).
  
  ```sh
  docker -v
  ```

### Installation
<a name="installation"></a>
1. Clone the repo (Клонируйте репозиторий).
   ```sh
   git clone https://github.com/hiimluck3r/KeepInventory.git
   ```
2. Change the settings in the docker-compose.yml and .env file (Измените настройки в файле docker-compose.yml и .env):
   ```sh
   cd KeepInventory

   nano .env
   vi docker-compose.yml
   ```
   
   ```sh
   #.env file example
   API_TOKEN = your_api_token
   HOST = db
   DB = postgres
   DBUSER = root
   PASSWORD = password
   ROOT = 1111111
   PORT = 5432
   ```

   ```yml
   version: '3.9'
   services:
    db:
        container_name: db
        image: luck3rinc/keepinventory_db:latest
        build: ./postgresql
        restart: always
        environment:
            POSTGRES_USER: $DBUSER
            POSTGRES_PASSWORD: $PASSWORD
            POSTGRES_DB: $DB
        ports:
        - "5432:5432"
        volumes:
        - ./postgresql:/docker-entrypoint-initdb.d
        - ./postgresql/data:/var/lib/postgresql/data

    pgadmin:
        container_name: pgadmin4_container
        image: dpage/pgadmin4
        restart: always
        environment:
            PGADMIN_DEFAULT_EMAIL: example@example.com
            PGADMIN_DEFAULT_PASSWORD: 123456
        ports:
        - "80:80"

    main:
        container_name: keepinventory_main
        image: luck3rinc/keepinventory:latest
        build: ./app
        restart: always
        environment:
            API_TOKEN: $API_TOKEN
            HOST: $HOST
            DB: $DB
            DBUSER: $DBUSER
            PASSWORD: $PASSWORD
            ROOT: $ROOT
            PORT: $PORT
        volumes:
        - ./app:/~/KeepInventory/app
        - ./logs:/~/KeepInventory/logs
        depends_on:
        - db

    volumes:
    logs:
   ```
3. Start the project using (Запустите проект при помощи) `docker-compose up`:
   ```sh
   docker-compose up
   ```
4. Use `/initroot` command as a ROOT user inside a bot to initialize your role entry.
(Используйте команду `/initroot` от имени ROOT пользователя внутри бота, чтобы инициализировать запись вашей роли).

Detailed instructions for using the bot can be found in separate documentation. (Подробное руководство по использованию бота вы можете найти в отдельной документации.)

<a href="https://github.com/hiimluck3r/KeepInventory/blob/master/etc/docs.md"><strong>Docs | Документация »</strong></a>


<!-- USAGE EXAMPLES -->
## Usage | Использование
<a name="usage"></a>
<details>
<summary>English</summary>
KeepInventory was made to efficiently manage technical equipment with predefined attributes. It offers a range of features to streamline inventory management:

* Role System: The system supports a hierarchical role system, allowing different levels of access such as read-only, worker, admin, and root.

* Barcode Recognition: KeepInventory can recognize articles through barcodes, enabling easy searching and retrieval of information from the database.

* Article Recognition: The system also provides the ability to identify articles based on their last characters, simplifying the search process.

* Software Register: KeepInventory includes a software register feature, allowing users to keep track of shared software.

* User Notes: Users can add notes, providing additional information or reminders.

* Backups: The system facilitates downloading and uploading backups in .csv table format, ensuring data integrity and availability.

In the future, an enhancement is planned to incorporate a separate container with Telegram Local API. This addition will significantly increase the capacity for transferring data volumes, up to 2GB. Consequently, it will simplify the process of downloading and uploading data, particularly for full PostgreSQL backups and software storage on the server.
</details>

<details>
<summary>Русский</summary>
KeepInventory создан для эффективного управления техническим оборудованием с заранее заданными атрибутами. Она предлагает ряд функций для оптимизации управления запасами:

* Система ролей: Система поддерживает иерархическую систему ролей, предоставляя различные уровни доступа, такие как "read-only", "worker", "admin" и "root".

* Распознавание штрих-кодов: KeepInventory может распознавать артикулы по штрих-кодам, что позволяет легко искать и извлекать информацию из базы данных.

* Распознавание артикулов: Система также позволяет идентифицировать артикулы по их последним символам, что упрощает процесс поиска.

* Реестр программного обеспечения: KeepInventory включает в себя функцию регистрации программного обеспечения, позволяющую пользователям отслеживать программное обеспечение, которым поделились другие пользователи.

* Заметки пользователя: Пользователи могут добавлять примечения, предоставляя дополнительную информацию или напоминания.

* Резервное копирование: Система позволяет загружать и выгружать резервные копии в формате таблиц .csv, обеспечивая целостность и доступность данных.

В будущем планируется расширение системы до отдельного контейнера с локальным API Telegram. Это дополнение значительно увеличит возможности по передаче объемов данных - до 2 ГБ. Соответственно, это упростит процесс загрузки и выгрузки данных, особенно при полном резервном копировании PostgreSQL и хранении программного обеспечения на сервере.
</details>


<!-- CONTRIBUTING -->
## Contributing | Сотрудничество
<a name="contributing"></a>
Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

Взаимопомощь - это то, что делает open source сообщество таким удивительным местом для обучения, вдохновения и творчества. Любой ваш вклад будет **очень высоко оценен**.

Если у вас есть предложение, которое позволит сделать это лучше, пожалуйста, сделайте fork репозитория и создайте запрос на исправление. Вы также можете просто открыть проблему с тегом "enhancement".
Не забудьте поставить проекту звезду!
Ещё раз спасибо!

1. Fork the Project (Fork проекта)
2. Create your Feature Branch (Создайте свою ветку Feature) (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (Зафиксируйте свои изменения) (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (Переместите изменения в ветку) (`git push origin feature/AmazingFeature`)
5. Open a Pull Request (Откройте Pull Request)




<!-- LICENSE -->
## License | Лицензия
<a name="license"></a>
Distributed under the MIT License. See `LICENSE.txt` for more information.

Распространяется под лицензией MIT. Дополнительную информацию см. в файле `LICENSE.txt`.




<!-- CONTACT -->
## Contact | Контакты
<a name="contact"></a>
* Telegram: https://t.me/hiimluck3r
* Telegram Channel: https://t.me/imluck3r
* VK: https://vk.com/hiimluck3r



<!--MARKDOWN ANCHORS -->
