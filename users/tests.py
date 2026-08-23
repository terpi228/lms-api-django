from django.conf import settings
from django.test import SimpleTestCase


class UserAppConfigurationTest(SimpleTestCase):
    def test_custom_user_model_is_configured_in_users_app(self):
        self.assertEqual(settings.AUTH_USER_MODEL, 'users.User')
