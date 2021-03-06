# Methods of collecting and processing data from the Internet
Методы сбора и обработки данных из сети Интернет

## Lesson 1
### Основы клиент-серверного взаимодействия. Парсинг API
1) Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя, сохранить JSON-вывод в файле *.json.
2) Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа). Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

## Lesson 2
### Парсинг HTML. BeautifulSoup, MongoDB
Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы) с сайта superjob.ru и hh.ru. Приложение должно анализировать несколько страниц сайта(также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:

- Наименование вакансии
- Предлагаемую зарплату (отдельно мин. и и отдельно макс.)
- Ссылку на саму вакансию
- Сайт откуда собрана вакансия

## Lesson 3
### Парсинг HTML. BS, SQLAlchemy
1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, записывающую собранные вакансии в созданную БД
2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введенной суммы
3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта

## Lesson 4
### Парсинг HTML. XPath
Написать приложение, которое собирает основные новости с сайтов mail.ru, lenta.ru.
Для парсинга использовать xpath. Структура данных должна содержать:
- название источника,
- наименование новости,
- ссылку на новость,
- дата публикации

## Lesson 5
### Парсинг HTML. XPath
1. Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
2. Написать программу, которая собирает «Новинки» с сайта техники mvideo и складывает данные в БД. Сайт можно выбрать и свой. Главный критерий выбора: динамически загружаемые товары