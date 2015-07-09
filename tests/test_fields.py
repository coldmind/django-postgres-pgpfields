from __future__ import unicode_literals

import datetime

from django.test import TestCase
from django.utils import six

from django_postgres_pgpfields import proxy
from django_postgres_pgpfields import fields, managers

from .factories import EncryptedModelFactory
from .models import EncryptedModel, EncryptedModelWithoutManager


PGP_FIELDS = (
    fields.EmailPGPPublicKeyField,
    fields.IntegerPGPPublicKeyField,
    fields.TextPGPPublicKeyField,
    fields.DatePGPPublicKeyField,
)


class TestPGPMixin(TestCase):
    """Test `PGPMixin` behave properly."""

    def test_check(self):
        """Assert `max_length` check does not return any error."""
        for field in PGP_FIELDS:
            self.assertEqual(field(name='field').check(), [])

    def test_max_length(self):
        """Assert `max_length` is ignored."""
        for field in PGP_FIELDS:
            self.assertEqual(field(max_length=42).max_length, None)

    def test_db_type(self):
        """Check db_type is `bytea`."""
        for field in PGP_FIELDS:
            self.assertEqual(field().db_type(), 'bytea')


class TestEmailPGPMixin(TestCase):
    """Test emails fields behave properly."""

    def test_max_length_validator(self):
        """Check `MaxLengthValidator` is not set."""
        field_validated = fields.EmailPGPPublicKeyField().run_validators(value='value@value.com')
        self.assertEqual(field_validated, None)


class TestEncryptedTextFieldModel(TestCase):
    """Test `EncryptedTextField` can be integrated in a `Django` model."""
    model = EncryptedModel

    def test_fields(self):
        """Assert fields are representing our model."""
        fields = self.model._meta.get_all_field_names()
        expected = (
            'id',
            'email_pgp_pub_field',
            'integer_pgp_pub_field',
            'pgp_pub_field',
            'pgp_pub_date_field',
            'pgp_pub_null_boolean_field',
        )
        if six.PY2:
            self.assertItemsEqual(fields, expected)
        else:
            self.assertCountEqual(fields, expected)

    def test_value_returned_is_not_bytea(self):
        """Assert value returned is not a memoryview instance."""
        EncryptedModelFactory.create()
        instance = self.model.objects.get()
        self.assertIsInstance(instance.email_pgp_pub_field, six.text_type)
        self.assertIsInstance(instance.integer_pgp_pub_field, int)
        self.assertIsInstance(instance.pgp_pub_field, six.text_type)

    def test_fields_descriptor_is_not_instance(self):
        """`EncryptedProxyField` instance returns itself when accessed from the model."""
        self.assertIsInstance(
            self.model.pgp_pub_field,
            proxy.EncryptedProxyField,
        )

    def test_value_query(self):
        """Assert querying the field's value is making one query."""
        EncryptedModelFactory.create(pgp_pub_field='test')
        instance = self.model.objects.get()
        with self.assertNumQueries(0):
            instance.pgp_pub_field

    def test_value_pgp_pub(self):
        """Assert we can get back the decrypted value."""
        EncryptedModelFactory.create(pgp_pub_field='test')
        instance = self.model.objects.get()
        self.assertEqual(instance.pgp_pub_field, 'test')

    def test_value_pgp_date_pub(self):
        """Assert we can get back the decrypted value."""
        EncryptedModelFactory.create(pgp_pub_date_field=datetime.date.today())
        instance = self.model.objects.get()
        self.assertEqual(instance.pgp_pub_date_field, datetime.date.today())

    def test_value_pgp_date_pub_null(self):
        """Assert we can get back the decrypted value."""
        EncryptedModelFactory.create(pgp_pub_date_field=None)
        instance = self.model.objects.get()
        self.assertIsNone(instance.pgp_pub_date_field)

    def test_value_pgp_null_boolean_pub(self):
        """Assert we can get back the decrypted values."""
        EncryptedModelFactory.create(pgp_pub_null_boolean_field=None)
        instance = self.model.objects.last()
        self.assertIsNone(instance.pgp_pub_null_boolean_field)

        EncryptedModelFactory.create(pgp_pub_null_boolean_field=True)
        instance = self.model.objects.last()
        self.assertTrue(instance.pgp_pub_null_boolean_field)

        EncryptedModelFactory.create(pgp_pub_null_boolean_field=False)
        instance = self.model.objects.last()
        self.assertFalse(instance.pgp_pub_null_boolean_field)

    def test_value_pgp_pub_multipe(self):
        """Assert we get back the correct value when the table contains data."""
        EncryptedModelFactory.create(pgp_pub_field='test')
        created = EncryptedModelFactory.create(pgp_pub_field='test2')
        instance = self.model.objects.get(pk=created.pk)
        self.assertEqual(instance.pgp_pub_field, 'test2')

    def test_instance_not_saved(self):
        """Assert not saved instance return the value to be encrypted."""
        instance = EncryptedModelFactory.build(pgp_pub_field='test')
        self.assertEqual(instance.pgp_pub_field, 'test')
        self.assertEqual(instance.pgp_pub_field, 'test')

    def test_update_attribute_pgp_pub_field(self):
        """Assert pgp field can be updated through its attribute on the model."""
        instance = EncryptedModelFactory.create()
        instance.pgp_pub_field = 'testing'
        instance.save()
        updated_instance = self.model.objects.get()
        self.assertEqual(updated_instance.pgp_pub_field, 'testing')

    def test_update_one_attribute(self):
        """Assert value are not overriden when updating one attribute."""
        expected = 'initial value'
        new_value = 'new_value'
        instance = EncryptedModelFactory.create(
            pgp_pub_field=expected,
        )
        instance.pgp_sym_field = new_value
        instance.save()
        updated_instance = self.model.objects.get()
        self.assertEqual(updated_instance.pgp_pub_field, expected)

    def test_pgp_int_public_key_negative_number(self):
        """Assert negative value is saved with an `IntegerPGPPublicKeyField` field."""
        instance = EncryptedModelFactory.create(integer_pgp_pub_field=-1)
        self.assertEqual(instance.integer_pgp_pub_field, -1)

    def test_pgp_int_public_key_null_number(self):
        """Assert negative value is saved with an `IntegerPGPPublicKeyField` field."""
        instance = EncryptedModelFactory.create(integer_pgp_pub_field=None)
        self.assertEqual(instance.integer_pgp_pub_field, None)

    def test_null(self):
        """Assert `NULL` values are saved."""
        instance = EncryptedModel.objects.create()
        fields = self.model._meta.get_all_field_names()
        fields.remove('id')
        for field in fields:
            self.assertEqual(getattr(instance, field), None)

    def test_unexpected_decrypted_value(self):
        EncryptedModelWithoutManager.objects.create(pgp_pub_field='test')
        obj = EncryptedModelWithoutManager.objects.get()
        with self.assertRaisesMessage(ValueError, 'Unexpected encrypted field "pgp_pub_field"!'):
            obj.pgp_pub_field
