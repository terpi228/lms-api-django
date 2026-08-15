import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from materials.models import User

# Проверяем, есть ли суперпользователь
admin_exists = User.objects.filter(is_superuser=True).exists()

if admin_exists:
    admin = User.objects.filter(is_superuser=True).first()
    print(f"✅ Суперпользователь уже существует: {admin.email}")
else:
    print("⚠️  Суперпользователя нет, создаём...")
    User.objects.create_superuser(
        email='admin@test.com',
        username='admin',
        password='admin123'
    )
    print("✅ Суперпользователь создан: admin@test.com / admin123")
