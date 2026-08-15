import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from materials.models import User, Course, Lesson

# Создаём тестового пользователя если его нет
user, created = User.objects.get_or_create(
    email='user@test.com',
    defaults={
        'username': 'testuser',
        'first_name': 'Тест',
        'last_name': 'Пользователь',
    }
)
if created:
    user.set_password('test123')
    user.save()
    print(f"✅ Создан пользователь: {user.email}")
else:
    print(f"✅ Пользователь уже существует: {user.email}")

# Создаём тестовые курсы
courses_data = [
    {
        'title': 'Django для начинающих',
        'description': 'Полный курс Django с нуля. Изучите основы фреймворка, создавайте веб-приложения.'
    },
    {
        'title': 'REST API с Django',
        'description': 'Создание REST API с помощью Django Rest Framework. Практические примеры и лучшие практики.'
    },
    {
        'title': 'Продвинутый Django',
        'description': 'Углублённое изучение Django. Оптимизация, безопасность, масштабирование приложений.'
    }
]

courses = []
for course_data in courses_data:
    course, created = Course.objects.get_or_create(
        title=course_data['title'],
        defaults={'description': course_data['description']}
    )
    courses.append(course)
    status = "✅ Создан" if created else "✅ Уже существует"
    print(f"{status} курс: {course.title}")

# Создаём уроки для каждого курса
lessons_data = {
    0: [
        {'title': 'Введение в Django', 'description': 'Что такое Django и зачем он нужен'},
        {'title': 'Установка и настройка', 'description': 'Установка Django и создание первого проекта'},
        {'title': 'Модели и БД', 'description': 'Работа с моделями данных и базами данных'},
    ],
    1: [
        {'title': 'Основы REST', 'description': 'Принципы REST архитектуры'},
        {'title': 'Django REST Framework', 'description': 'Установка и первая API'},
        {'title': 'Сериализаторы', 'description': 'Работа с сериализаторами в DRF'},
    ],
    2: [
        {'title': 'Оптимизация запросов', 'description': 'Оптимизация БД запросов с select_related и prefetch_related'},
        {'title': 'Кэширование', 'description': 'Использование Redis для кэширования'},
        {'title': 'Развёртывание', 'description': 'Развёртывание Django приложений на сервер'},
    ]
}

for course_idx, course in enumerate(courses):
    for lesson_data in lessons_data.get(course_idx, []):
        lesson, created = Lesson.objects.get_or_create(
            course=course,
            title=lesson_data['title'],
            defaults={'description': lesson_data['description']}
        )
        status = "✅ Создан" if created else "✅ Уже существует"
        print(f"  {status} урок: {lesson.title}")

print("\n✅ Тестовые данные готовы!")
