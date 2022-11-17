from django.test import TestCase
from vincent.models import User

class UserModelTest(TestCase):

    def test_basic_model_creation(self) -> None:
        user = User.objects.create(
            username='dgaitan',
            password='secret'
        )

        self.assertEqual('dgaitan', user.username)
        self.assertEqual('secret', user.password)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertEqual('', user.email)

    def test_model_creation_with_names(self) -> None:
        user = User.objects.create(
            username='dgaitan',
            email='david@mail.com',
            first_name='David',
            last_name='Gaitan',
            password='secret'
        )

        self.assertEqual('dgaitan', user.username)
        self.assertEqual('secret', user.password)
        self.assertEqual('David', user.first_name)
        self.assertEqual('Gaitan', user.last_name)
        self.assertEqual('david@mail.com', user.email)
        self.assertEqual('David Gaitan', user.get_full_name())
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)
