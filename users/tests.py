from django.conf import settings
from django.test import SimpleTestCase
from rest_framework.test import APITestCase

from materials.models import Course, Lesson

from .models import Payment, Subscription, User


class UserAppConfigurationTest(SimpleTestCase):
    def test_custom_user_model_is_configured_in_users_app(self):
        self.assertEqual(settings.AUTH_USER_MODEL, 'users.User')


class PaymentAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='user@example.com', username='user', password='password')
        self.course = Course.objects.create(title='Django')
        self.lesson = Lesson.objects.create(course=self.course, title='Serializers')
        Payment.objects.create(user=self.user, paid_course=self.course, amount='1000.00', payment_method='transfer')
        Payment.objects.create(user=self.user, paid_lesson=self.lesson, amount='300.00', payment_method='cash')

    def test_payment_list_supports_filtering_and_ordering(self):
        response = self.client.get('/api/payments/', {'paid_course': self.course.id, 'ordering': 'payment_date'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['paid_course'], self.course.id)

    def test_user_detail_returns_payment_history(self):
        response = self.client.get(f'/api/users/{self.user.id}/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['payments']), 2)

    def test_login_with_email_returns_tokens(self):
        response = self.client.post('/api/login/', {'email': 'user@example.com', 'password': 'password'}, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_create_payment_requires_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/payments/', {'paid_course': self.course.id, 'amount': '150.00', 'payment_method': 'transfer'}, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user'], self.user.id)


class SubscriptionAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='subscriber@example.com',
            username='subscriber',
            password='password',
        )
        self.course = Course.objects.create(title='Django', owner=self.user)

    def test_subscription_toggles_and_is_returned_for_course(self):
        self.client.force_authenticate(user=self.user)

        add_response = self.client.post(
            '/api/subscription/',
            {'course': self.course.id},
            format='json',
        )
        self.assertEqual(add_response.status_code, 200)
        self.assertEqual(add_response.data['message'], 'Подписка добавлена')
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

        detail_response = self.client.get(f'/api/courses/{self.course.id}/')
        self.assertTrue(detail_response.data['is_subscribed'])

        remove_response = self.client.post(
            '/api/subscription/',
            {'course': self.course.id},
            format='json',
        )
        self.assertEqual(remove_response.status_code, 200)
        self.assertEqual(remove_response.data['message'], 'Подписка удалена')
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_anonymous_course_response_is_not_subscribed(self):
        response = self.client.get(f'/api/courses/{self.course.id}/')

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data['is_subscribed'])
