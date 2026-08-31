from django.core.management.base import BaseCommand

from materials.models import Course, Lesson
from users.models import Payment, User


class Command(BaseCommand):
    help = 'Creates example payments for API verification.'

    def handle(self, *args, **options):
        user, _ = User.objects.get_or_create(
            email='payments@example.com',
            defaults={'username': 'payments_user'},
        )
        course, _ = Course.objects.get_or_create(
            title='Test course for payments',
            defaults={'description': 'Created by the seed_payments command.'},
        )
        lesson, _ = Lesson.objects.get_or_create(
            course=course,
            title='Test lesson for payments',
        )

        course_payment, course_created = Payment.objects.get_or_create(
            user=user,
            paid_course=course,
            paid_lesson=None,
            defaults={'amount': '1000.00', 'payment_method': 'transfer'},
        )
        lesson_payment, lesson_created = Payment.objects.get_or_create(
            user=user,
            paid_course=None,
            paid_lesson=lesson,
            defaults={'amount': '300.00', 'payment_method': 'cash'},
        )

        created_count = int(course_created) + int(lesson_created)
        self.stdout.write(self.style.SUCCESS(f'Payment records created: {created_count}.'))