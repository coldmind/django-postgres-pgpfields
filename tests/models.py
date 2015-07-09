from django.db import models

from django_postgres_pgpfields import fields
from django_postgres_pgpfields.managers import PGPEncryptedManager


class EncryptedModel(models.Model):
    """Dummy model used for tests to check the fields."""
    email_pgp_pub_field = fields.EmailPGPPublicKeyField(blank=True, null=True)
    integer_pgp_pub_field = fields.IntegerPGPPublicKeyField(blank=True, null=True)
    pgp_pub_field = fields.TextPGPPublicKeyField(blank=True, null=True)
    pgp_pub_date_field = fields.DatePGPPublicKeyField(blank=True, null=True)
    pgp_pub_null_boolean_field = fields.NullBooleanPGPPublicKeyField()

    objects = PGPEncryptedManager()


class EncryptedModelWithoutManager(models.Model):
    """
    Should rise ValueError() when accesing encrypted fields without defining
    encrypted manager.
    """
    pgp_pub_field = fields.TextPGPPublicKeyField(blank=True, null=True)
