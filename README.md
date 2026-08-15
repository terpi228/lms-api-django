# LMS (Learning Management System) - Django + DRF

## 📋 Описание проекта

Полнофункциональная Learning Management System (LMS) на Django с Django REST Framework, включающая:
- Управление курсами (CRUD)
- Управление уроками (CRUD)
- Управление пользователями (CRUD)
- Кастомную модель пользователя на базе `AbstractBaseUser`
- REST API эндпоинты для всех операций

---

## ✅ Выполненные требования задания

### Основные требования:
- [x] Создан новый Django-проект
- [x] Подключен Django REST Framework в настройках проекта
- [x] Созданы модели: User (кастомная на AbstractBaseUser), Course, Lesson
- [x] Реализованы CRUD операции для курсов и уроков
- [x] Все эндпоинты протестированы

### Дополнительные требования:
- [x] Реализован эндпоинт для редактирования профиля пользователя (PATCH /api/users/{id}/)
- [x] Возможность частичного обновления профиля (PATCH запросы)

---

## 📦 Установленные зависимости

```
Django==6.1
djangorestframework==3.18.0
Pillow==11.2.0
psycopg2==2.9.10
python-dotenv==1.0.1
```

---

## 🗂️ Структура проекта

```
Vise-sets_generics/
├── config/                 # Основной конфиг проекта
│   ├── settings.py        # Настройки Django (DRF, БД, INSTALLED_APPS)
│   ├── urls.py            # Маршруты API
│   └── wsgi.py
├── materials/             # Основное приложение
│   ├── models.py          # Модели: User, Course, Lesson
│   ├── serializers.py     # DRF сериализаторы
│   ├── views.py           # API представления (ViewSets и APIViews)
│   ├── urls.py            # URL маршруты приложения
│   └── migrations/        # Миграции БД
├── .env                   # Переменные окружения
├── manage.py              # Django CLI
└── check_admin.py         # Скрипт для проверки админа
└── load_data.py           # Скрипт для загрузки тестовых данных
└── POSTMAN_TESTING.md     # Документация по тестированию
└── LMS_API_Postman_Collection.json  # Postman коллекция
```

---

## 🗄️ Модели данных

### User (Кастомная модель пользователя)
```python
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True)
    first_name = models.CharField()
    last_name = models.CharField()
    phone = models.CharField()
    city = models.CharField()
    avatar = models.ImageField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
```

### Course
```python
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
```

### Lesson
```python
class Lesson(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
```

---

## 🚀 Быстрый старт

### 1. Установка зависимостей
```bash
# Если виртуальное окружение ещё не создано:
python -m venv .venv

# Активация виртуального окружения:
.\.venv\Scripts\activate  # Windows
source .venv/bin/activate # Linux/Mac

# Установка зависимостей:
pip install -r requirements.txt
```

### 2. Подготовка БД
```bash
# Создание миграций
python manage.py makemigrations

# Применение миграций
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser

# Загрузка тестовых данных
python load_data.py
```

### 3. Запуск сервера
```bash
python manage.py runserver
```

Сервер будет доступен по адресу: **http://localhost:8000/api/**

---

## 📝 REST API Эндпоинты

### Курсы (Courses)
| Метод | URL | Описание |
|-------|-----|---------|
| GET | `/api/courses/` | Получить все курсы |
| POST | `/api/courses/` | Создать новый курс |
| GET | `/api/courses/{id}/` | Получить курс по ID |
| PUT | `/api/courses/{id}/` | Полное обновление курса |
| PATCH | `/api/courses/{id}/` | Частичное обновление курса |
| DELETE | `/api/courses/{id}/` | Удалить курс |

### Уроки (Lessons)
| Метод | URL | Описание |
|-------|-----|---------|
| GET | `/api/lessons/` | Получить все уроки |
| POST | `/api/lessons/create/` | Создать новый урок |
| GET | `/api/lessons/{id}/` | Получить урок по ID |
| PUT | `/api/lessons/{id}/update/` | Полное обновление урока |
| PATCH | `/api/lessons/{id}/update/` | Частичное обновление урока |
| DELETE | `/api/lessons/{id}/delete/` | Удалить урок |

### Пользователи (Users)
| Метод | URL | Описание |
|-------|-----|---------|
| GET | `/api/users/` | Получить всех пользователей |
| POST | `/api/users/` | Создать нового пользователя |
| GET | `/api/users/{id}/` | Получить профиль пользователя |
| PUT | `/api/users/{id}/` | Полное обновление профиля |
| PATCH | `/api/users/{id}/` | Частичное обновление профиля |
| DELETE | `/api/users/{id}/` | Удалить пользователя |

---

## 🧪 Тестирование в Postman

### Импорт коллекции Postman:
1. Откройте Postman
2. Нажмите **Import** → выберите файл `LMS_API_Postman_Collection.json`
3. Используйте готовые примеры для тестирования

### Альтернатива - ручное тестирование:
Подробные инструкции по всем эндпоинтам см. в файле `POSTMAN_TESTING.md`

---

## 🔑 Учетные данные для тестирования

**Администратор:**
- Email: `admin@test.com`
- Password: `admin123`

**Тестовый пользователь:**
- Email: `user@test.com`
- Password: `test123`

**Тестовые данные:**
- 3 готовых курса
- 9 готовых уроков (по 3 на каждый курс)
- 2 пользователя (admin и user)

---

## 📄 Примеры запросов

### Создание курса
```bash
curl -X POST http://localhost:8000/api/courses/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Django для начинающих",
    "description": "Полный курс Django"
  }'
```

### Обновление профиля пользователя (Частичное)
```bash
curl -X PATCH http://localhost:8000/api/users/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Иван",
    "city": "Москва"
  }'
```

### Получение всех уроков
```bash
curl http://localhost:8000/api/lessons/
```

---

## ⚙️ Конфигурация базы данных

### По умолчанию используется SQLite:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Для использования PostgreSQL:
1. Добавьте в `.env` файл:
```
USE_POSTGRES=True
DB_NAME=lms_db
DB_USER=postgres
DB_PASSWORD=ваш_пароль
DB_HOST=localhost
DB_PORT=5432
```

2. Убедитесь, что установлен `psycopg2`:
```bash
pip install psycopg2
```

---

## 🔍 Полезные команды

```bash
# Проверка конфигурации проекта
python manage.py check

# Просмотр всех URL маршрутов
python manage.py show_urls

# Вход в Django shell
python manage.py shell

# Создание резервной копии БД
python manage.py dumpdata > backup.json

# Восстановление из резервной копии
python manage.py loaddata backup.json

# Удаление всех миграций (осторожно!)
python manage.py migrate materials zero
```

---

## 📚 Документация

- **Django:** https://docs.djangoproject.com/
- **Django REST Framework:** https://www.django-rest-framework.org/
- **Postman:** https://learning.postman.com/

---

## 👤 Автор

**Разработано для:** LMS курс на SkyPro  
**Версия:** 1.0  
**Дата:** 2026-08-14

---

## 📌 Заметки

- Все эндпоинты возвращают JSON формат
- PATCH запросы позволяют обновлять только необходимые поля
- Пароли пользователей автоматически хешируются
- Для создания урока необходимо передать валидный ID курса
- Статус коды соответствуют REST стандартам (200, 201, 204, 400, 404, 500)

---

**Проект готов к использованию и оценке! ✅**
