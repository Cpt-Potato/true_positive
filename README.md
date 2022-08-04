### Telegram bot для отправки скриншотов в ответ на сообщение со ссылкой
#### Стек: Aiogram, SQLAlchemy, PostgreSQL, Docker
Статистика запросов хранится в PostgreSQL.<br>
Все вызовы неблокирующие, т.к. всё в асинхронке (в том числе и браузер, который теперь Pyppeteer, а не синхронный Selenium).<br>
Скриншоты сохраняются в папку /media (для каждого дня создаётся отдельная папка).<br>
После ввода пароля администратора можно просмотреть статистику запросов за день.
#### Запуск
* Клонировать репозиторий
```
git clone https://github.com/Cpt-Potato/true_positive.git
```
* Перейти в папку с ним
* В переменных окружения или файле .env (переименовать .env.dev) указать значения DATABASE_URL, TOKEN, ADMIN_PASSWORD
* Перейти в папку с проектом в терминале
* Построить контейнеры докера и запустить их
```
docker-compose up -d
```
* Открыть Telegram и найти там вашего бота для указанного токена
* Пользоваться :)