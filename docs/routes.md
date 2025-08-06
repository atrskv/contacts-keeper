| Метод  | Маршрут              | Шаблон               | Описание                     |
|--------|----------------------|----------------------|------------------------------|
| **GET**    | /contacts/           | contacts/index.html  | Список контактов             |
| **GET**    | /contacts/{id}       | contacts/show.html   | Информация о контакте        |
| **GET**    | /contacts/random/    | contacts/show.html   | Случайный контакт            |
| **GET**    | /contacts/new/       | contacts/new.html    | Форма создания нового контакта |
| **POST**   | /contacts/           | -                    | Создание нового контакта     |
| **GET**    | /contacts/{id}/edit/ | contacts/edit.html   | Форма редактирования контакта |
| **POST**  | /contacts/{id}/      | -                    | Обновление контакта          |
| **POST** | /contacts/{id}/delete/ | -                  | Удаление контакта            |
