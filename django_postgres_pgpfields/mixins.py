from __future__ import unicode_literals

from django.core.validators import MaxLengthValidator

from django_postgres_pgpfields.proxy import EncryptedProxyField


def remove_validators(validators, validator_class):
    """Exclude `validator_class` instances from `validators` list."""
    return [v for v in validators if not isinstance(v, validator_class)]


class PGPMixin(object):
    """PGP encryption for field's value.

    `PGPMixin` uses 'pgcrypto' to encrypt data in a postgres database.
    """
    descriptor_class = EncryptedProxyField

    def __init__(self, *args, **kwargs):
        """`max_length` should be set to None as encrypted text size is variable."""
        kwargs['max_length'] = None
        super(PGPMixin, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name, **kwargs):
        """
        Add a decrypted field proxy to the model.

        Add to the field model an `EncryptedProxyField` to get the decrypted
        values of the field.

        The decrypted value can be accessed using the field's name attribute on
        the model instance.
        """
        super(PGPMixin, self).contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, self.descriptor_class(field=self))

    def db_type(self, connection=None):
        """Value stored in the database is hexadecimal."""
        return 'bytea'

    def get_placeholder(self, value=None, compiler=None, connection=None):
        """
        Tell postgres to encrypt this field using PGP.

        `value`, `compiler`, and `connection` are ignored here as we don't need
        custom operators.
        """
        return self.encrypt_sql

    def _check_max_length_attribute(self, **kwargs):
        """Override `_check_max_length_attribute` to remove check on max_length."""
        return []


class RemoveMaxLengthValidatorMixin(object):
    """Exclude `MaxLengthValidator` from field validators."""
    def __init__(self, *args, **kwargs):
        """Remove `MaxLengthValidator` in parent's `.__init__`."""
        super(RemoveMaxLengthValidatorMixin, self).__init__(*args, **kwargs)
        self.validators = remove_validators(self.validators, MaxLengthValidator)


class EmailPGPPublicKeyFieldMixin(PGPMixin, RemoveMaxLengthValidatorMixin):
    """Email mixin for PGP public key fields."""
