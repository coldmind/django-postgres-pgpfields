from __future__ import unicode_literals

from django.conf import settings
from django.db import models

from django_postgres_pgpfields.mixins import PGPMixin


class PGPEncryptedManager(models.Manager):
    """Custom manager to decrypt values at query time."""

    use_for_related_fields = True

    def get_decrypt_sql(self, field):
        """If field needs an explicit cast, use it."""
        if hasattr(field, 'cast_sql'):
            return field.cast_sql % """pgp_pub_decrypt("{0}"."{1}", dearmor('{2}'))"""
        else:
            return """pgp_pub_decrypt("{0}"."{1}", dearmor('{2}'))"""

    def get_queryset(self, *args, **kwargs):
        """Django queryset.extra() is used here to add decryption sql to query."""
        select_sql = {}
        encrypted_fields = []
        for f in self.model._meta.get_fields_with_model():
            field = f[0]
            if isinstance(field, PGPMixin):
                select_sql[field.name] = self.get_decrypt_sql(field).format(
                    field.model._meta.db_table,
                    field.name,
                    settings.PGPFIELDS_PRIVATE_KEY,
                )
                encrypted_fields.append(field.name)
        return super(PGPEncryptedManager, self).get_queryset(
            *args, **kwargs).defer(*encrypted_fields).extra(select=select_sql)
