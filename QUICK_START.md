# 🚀 Быстрый старт (Quick Start Guide)

## ⚡ 5 минут до тестирования

### Шаг 1️⃣: Активируем виртуальное окружение
```bash
.\.venv\Scripts\activate
```

### Шаг 2️⃣: Проверяем что всё готово
```bash
python manage.py check
```
✅ Должно вывести: "System check identified no issues (0 silenced)."

### Шаг 3️⃣: Применяем миграции (если не было)
```bash
python manage.py migrate
```

### Шаг 4️⃣: Загружаем тестовые данные
```bash
python load_data.py
```
✅ Должны создаться: 3 курса, 9 уроков, 2 пользователя

### Шаг 5️⃣: Запускаем сервер
```bash
python manage.py runserver
```
✅ Сервер запустится на: **http://localhost:8000/api/**

---

## 🧪 Тестирование в Postman

### Способ 1️⃣: Импорт коллекции (Рекомендуется)
1. Откройте Postman
2. **File** → **Import**
3. Выберите файл: `LMS_API_Postman_Collection.json`
4. Начните тестировать готовые примеры

### Способ 2️⃣: Ручное тестирование
Следуйте инструкциям в `POSTMAN_TESTING.md`

---

## 📋 Основные эндпоинты для быстрого теста

```bash
# Получить все курсы
curl http://localhost:8000/api/courses/

# Получить все уроки
curl http://localhost:8000/api/lessons/

# Получить всех пользователей
curl http://localhost:8000/api/users/
```

---

## 👤 Учетные данные для входа (если потребуется)

```
Email: admin@test.com
Password: admin123
```

---

## 📚 Дополнительная информация

| Файл | Описание |
|------|---------|
| `README.md` | Полная документация проекта |
| `CHECKLIST.md` | Проверка соответствия требованиям |
| `POSTMAN_TESTING.md` | Подробное описание всех эндпоинтов |
| `LMS_API_Postman_Collection.json` | Готовая Postman коллекция |

---

## ✅ Готово к оценке!

**Все требования выполнены:**
- ✅ Django проект
- ✅ DRF интегрирован
- ✅ Модели User, Course, Lesson
- ✅ Полный CRUD
- ✅ Тестовые данные
- ✅ Postman коллекция
- ✅ Документация

**Сервер готов на:** http://localhost:8000/api/
