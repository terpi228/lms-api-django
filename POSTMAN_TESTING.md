# LMS API - Инструкция для тестирования в Postman

## Базовый URL
```
http://localhost:8000/api/
```

## Данные для входа (если потребуется)
- **Email:** admin@test.com
- **Password:** admin123
- **Тестовый пользователь:** user@test.com / test123

---

## CRUD КУРСОВ (Courses)

### 1. Получить список всех курсов [GET]
```
GET http://localhost:8000/api/courses/
```
**Ожидаемый результат:** 200 OK, JSON массив с 3 курсами

### 2. Создать новый курс [POST]
```
POST http://localhost:8000/api/courses/
```
**Headers:**
```
Content-Type: application/json
```
**Body (raw JSON):**
```json
{
  "title": "Python для веб-разработки",
  "description": "Изучение Python для создания веб-приложений"
}
```
**Ожидаемый результат:** 201 Created, новый курс с id

### 3. Получить конкретный курс [GET]
```
GET http://localhost:8000/api/courses/1/
```
**Ожидаемый результат:** 200 OK, данные курса с id=1

### 4. Обновить курс [PUT]
```
PUT http://localhost:8000/api/courses/1/
```
**Headers:**
```
Content-Type: application/json
```
**Body (raw JSON):**
```json
{
  "title": "Django для начинающих (обновлено)",
  "description": "Обновленное описание курса"
}
```
**Ожидаемый результат:** 200 OK, обновленные данные

### 5. Частичное обновление курса [PATCH]
```
PATCH http://localhost:8000/api/courses/1/
```
**Headers:**
```
Content-Type: application/json
```
**Body (raw JSON):**
```json
{
  "title": "Django для новичков"
}
```
**Ожидаемый результат:** 200 OK, обновленное значение title

### 6. Удалить курс [DELETE]
```
DELETE http://localhost:8000/api/courses/1/
```
**Ожидаемый результат:** 204 No Content

---

## CRUD УРОКОВ (Lessons)

### 1. Получить список всех уроков [GET]
```
GET http://localhost:8000/api/lessons/
```
**Ожидаемый результат:** 200 OK, JSON массив со всеми уроками (9 шт)

### 2. Создать новый урок [POST]
```
POST http://localhost:8000/api/lessons/create/
```
**Headers:**
```
Content-Type: application/json
```
**Body (raw JSON):**
```json
{
  "title": "Новый урок",
  "description": "Описание урока",
  "course": 1
}
```
**Ожидаемый результат:** 201 Created, новый урок с id

### 3. Получить конкретный урок [GET]
```
GET http://localhost:8000/api/lessons/1/
```
**Ожидаемый результат:** 200 OK, данные урока с id=1

### 4. Обновить урок полностью [PUT]
```
PUT http://localhost:8000/api/lessons/1/update/
```
**Headers:**
```
Content-Type: application/json
```
**Body (raw JSON):**
```json
{
  "title": "Введение в Django (обновлено)",
  "description": "Обновленное описание",
  "course": 1
}
```
**Ожидаемый результат:** 200 OK, обновленные данные

### 5. Частичное обновление урока [PATCH]
```
PATCH http://localhost:8000/api/lessons/1/update/
```
**Headers:**
```
Content-Type: application/json
```
**Body (raw JSON):**
```json
{
  "title": "Введение в Django (новое название)"
}
```
**Ожидаемый результат:** 200 OK, обновленное значение

### 6. Удалить урок [DELETE]
```
DELETE http://localhost:8000/api/lessons/1/delete/
```
**Ожидаемый результат:** 204 No Content

---

## CRUD ПОЛЬЗОВАТЕЛЕЙ (Users)

### 1. Получить список всех пользователей [GET]
```
GET http://localhost:8000/api/users/
```
**Ожидаемый результат:** 200 OK, JSON массив пользователей

### 2. Создать нового пользователя [POST]
```
POST http://localhost:8000/api/users/
```
**Headers:**
```
Content-Type: application/json
```
**Body (raw JSON):**
```json
{
  "email": "newuser@test.com",
  "username": "newuser",
  "first_name": "Новый",
  "last_name": "Пользователь",
  "password": "password123"
}
```
**Ожидаемый результат:** 201 Created, новый пользователь с id

### 3. Получить профиль пользователя [GET]
```
GET http://localhost:8000/api/users/1/
```
**Ожидаемый результат:** 200 OK, данные пользователя

### 4. Обновить профиль пользователя (Полное обновление) [PUT]
```
PUT http://localhost:8000/api/users/1/
```
**Headers:**
```
Content-Type: application/json
```
**Body (raw JSON):**
```json
{
  "email": "updated@test.com",
  "username": "updateduser",
  "first_name": "Обновленное",
  "last_name": "Имя",
  "phone": "+7-999-123-45-67",
  "city": "Москва"
}
```
**Ожидаемый результат:** 200 OK, обновленные данные

### 5. Частичное обновление профиля пользователя [PATCH]
```
PATCH http://localhost:8000/api/users/1/
```
**Headers:**
```
Content-Type: application/json
```
**Body (raw JSON):**
```json
{
  "first_name": "Иван",
  "city": "Санкт-Петербург",
  "phone": "+7-800-555-35-35"
}
```
**Ожидаемый результат:** 200 OK, обновленные поля

### 6. Удалить пользователя [DELETE]
```
DELETE http://localhost:8000/api/users/1/
```
**Ожидаемый результат:** 204 No Content

---

## Тестовые сценарии

### Сценарий 1: Создание и управление курсом
1. Создать новый курс (POST /api/courses/)
2. Получить список курсов (GET /api/courses/)
3. Получить конкретный курс (GET /api/courses/{id}/)
4. Обновить курс (PUT/PATCH /api/courses/{id}/)
5. Удалить курс (DELETE /api/courses/{id}/)

### Сценарий 2: Работа с уроками
1. Создать урок (POST /api/lessons/create/)
2. Получить список уроков (GET /api/lessons/)
3. Получить урок (GET /api/lessons/{id}/)
4. Обновить урок (PUT/PATCH /api/lessons/{id}/update/)
5. Удалить урок (DELETE /api/lessons/{id}/delete/)

### Сценарий 3: Редактирование профиля пользователя
1. Создать пользователя (POST /api/users/)
2. Получить профиль (GET /api/users/{id}/)
3. Обновить профиль ЧАСТИЧНО (PATCH /api/users/{id}/)
4. Проверить обновление (GET /api/users/{id}/)

---

## Коды ответов (HTTP Status Codes)

- **200 OK** - Успешный GET/PUT/PATCH
- **201 Created** - Успешное создание (POST)
- **204 No Content** - Успешное удаление (DELETE)
- **400 Bad Request** - Ошибка в запросе
- **404 Not Found** - Ресурс не найден
- **500 Internal Server Error** - Ошибка на сервере

---

## Заметки

1. Все эндпоинты возвращают JSON формат
2. Необходимо указывать `Content-Type: application/json` для POST/PUT/PATCH запросов
3. Для создания пользователя нужно указать пароль (будет захеширован)
4. Курс должен существовать перед созданием урока (используйте реальный `course` id)
5. Тестовые данные загружены в БД, используйте их id (1, 2, 3, и т.д.)
