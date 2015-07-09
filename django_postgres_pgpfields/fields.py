from __future__ import unicode_literals

from django.db import models

from django_postgres_pgpfields import (
    INTEGER_PGP_PUB_ENCRYPT_SQL, PGP_PUB_ENCRYPT_SQL,
)
from django_postgres_pgpfields.mixins import (
    EmailPGPPublicKeyFieldMixin, PGPMixin,
)


class EmailPGPPublicKeyField(EmailPGPPublicKeyFieldMixin, models.EmailField):
    """Email PGP public key encrypted field."""

    encrypt_sql = PGP_PUB_ENCRYPT_SQL


class IntegerPGPPublicKeyField(PGPMixin, models.IntegerField):
    """Integer PGP public key encrypted field."""

    encrypt_sql = INTEGER_PGP_PUB_ENCRYPT_SQL
    cast_sql = "CAST(nullif(%s, '') AS integer)"


class TextPGPPublicKeyField(PGPMixin, models.TextField):
    """Text PGP public key encrypted field."""

    encrypt_sql = PGP_PUB_ENCRYPT_SQL


class DatePGPPublicKeyField(PGPMixin, models.DateField):
    """Date PGP public key encrypted field."""

    encrypt_sql = PGP_PUB_ENCRYPT_SQL
    cast_sql = "to_date(%s, 'YYYY-MM-DD')"

    def get_prep_value(self, value):
        """Need explicit string cast to avoid quotes."""
        if value is None:
            return None
        return "%s" % super(DatePGPPublicKeyField, self).get_prep_value(value)


class NullBooleanPGPPublicKeyField(PGPMixin, models.NullBooleanField):
    """NullBoolean PGP public key encrypted field."""

    encrypt_sql = PGP_PUB_ENCRYPT_SQL
    cast_sql = "CASE %s WHEN 'True' THEN TRUE WHEN 'False' THEN FALSE ELSE NULL END"

    def get_prep_value(self, value):
        """Before encryption, need to prepare values."""
        value = super(NullBooleanPGPPublicKeyField, self).get_prep_value(value)
        if value is None:
            return None
        return "%s" % bool(value)
