Перед запуском необходимо заполнить `askme_django/.env` файл.

Пример заполнения лежит в `askme_django/.env.sample`

Запуск: `docker-compose up`

Приложение будет доступно по адресу `http://127.0.0.1:8000`

База данных будет доступна к подключению по порту `5431`

Для заполнения базы данных - команда `docker-compose exec web python manage.py fill_database <ratio>`

Для остановки - `docker-compose down`. 
Если необходимо удалить все данные, связанные с images, volumes - добавить флаг `-v`
