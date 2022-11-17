from django.test import TestCase
from vincent.models import User, Form, FormField

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

    def test_create_and_update_fields(self) -> None:
        form = Form.objects.create(
            name='My New Form',
            created_by=self.user,
            status=Form.Statuses.PUBLISHED
        )

        self.assertIsNotNone(form.created_at)
        self.assertIsNotNone(form.updated_at)


class FormFieldsTest(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            username='dgaitan',
            password='secret'
        )
        self.form = Form.objects.create(
            name='My New Form',
            created_by=self.user,
            status=Form.Statuses.PUBLISHED
        )

    def test_adding_a_field_to_form(self) -> None:
        field = self.form.fields.create(label='Name')

        self.assertEqual('Name', field.label)
        self.assertEqual('name', field.name)
        self.assertEqual(FormField.FieldTypes.TEXT, field.field_type)
        self.assertFalse(field.required)
        self.assertIsNone(field.placeholder)
        self.assertEqual('My New Form', field.form.name)

    def test_adding_a_field_with_all_values_defined(self) -> None:
        field = self.form.fields.create(
            label='First Name',
            placeholder='John Doe',
            required=True,
            field_type=FormField.FieldTypes.TEXT
        )

        self.assertEqual('First Name', field.label)
        self.assertEqual('first_name', field.name)
        self.assertEqual(FormField.FieldTypes.TEXT, field.field_type)
        self.assertTrue(field.required)
        self.assertIsNotNone(field.placeholder)
        self.assertEqual('John Doe', field.placeholder)
        self.assertEqual('My New Form', field.form.name)

    def test_adding_various_fields_to_form(self) -> None:
        self.form.fields.create(label='First Name', required=True)
        self.form.fields.create(label='Email', required=True, field_type=FormField.FieldTypes.EMAIL)
        self.form.fields.create(label='Message', required=True, field_type=FormField.FieldTypes.TEXTAREA)

        self.assertEqual(3, self.form.fields.count())

    def test_adding_field_with_options(self) -> None:
        select = self.form.fields.create(
            label='Programming Language',
            field_type=FormField.FieldTypes.SELECT
        )

        select.options.create(name='Python', order=1)
        select.options.create(name='PHP', order=2)
        select.options.create(name='JavaScript', order=3)

        self.assertEqual(3, select.options.count())
