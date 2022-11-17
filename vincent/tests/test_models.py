from django.test import TestCase
from vincent.models import User, Form

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


class FormModelTest(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            username='dgaitan',
            password='secret'
        )

    def test_creating_only_form(self) -> None:
        form = Form.objects.create(
            name='My New Form',
            created_by=self.user,
            status=Form.Statuses.PUBLISHED
        )

        self.assertEqual('My New Form', form.name)
        self.assertEqual(Form.Statuses.PUBLISHED, form.status)
        self.assertEqual(2, form.status)
        self.assertIsInstance(form.created_by, User)
        self.assertEqual('dgaitan', form.created_by.username)

    def test_creating_draft_form(self) -> None:
        form = Form.objects.create(
            name='My New Draft Form',
            created_by=self.user,
        )

        self.assertEqual('My New Draft Form', form.name)
        self.assertEqual(Form.Statuses.DRAFT, form.status)
        self.assertEqual(1, form.status)

    def test_trashing_a_form(self) -> None:
        form = Form.objects.create(
            name='My New Form',
            created_by=self.user,
            status=Form.Statuses.PUBLISHED
        )

        self.assertEqual('My New Form', form.name)
        self.assertEqual(Form.Statuses.PUBLISHED, form.status)
        self.assertEqual(2, form.status)

        form.status = Form.Statuses.TRASHED
        form.save()

        self.assertEqual(Form.Statuses.TRASHED, form.status)
        self.assertEqual(3, form.status)
