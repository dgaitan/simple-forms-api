from django.test import TestCase

from vincent.models import User


class AuthAPITest(TestCase):

    def test_api_login(self) -> None:
        user = User.objects.create_user(username='dgaitan', email='david@mail.com', password='secret')

        request = self.client.post('/api/auth/token', {
            'username': 'dgaitan',
            'password': 'secret'
        }, 'application/json')

        self.assertEqual(200, request.status_code)

    def test_api_login_failed(self) -> None:
        user = User.objects.create_user(username='dgaitan', email='david@mail.com', password='secret')

        request = self.client.post('/api/auth/token', {
            'username': 'dgaitan',
            'password': 'secret_wrong'
        }, 'application/json')

        self.assertEqual(401, request.status_code)