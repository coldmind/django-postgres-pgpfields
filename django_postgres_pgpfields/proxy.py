from __future__ import unicode_literals

import sys

from django.conf import settings
from django.utils import six


class EncryptedProxyField(object):
    """Descriptor for encrypted values.

    Decrypted values will query the database through the field's model.

    When accessing the field name attribute on a model instance we are
    generating N+1 queries.
    """
    def __init__(self, field):
        """
        Create a proxy for a django field.

        `field` is a django field.
        """
        self.field = field
        self.model = field.model

    def __get__(self, instance, owner=None):
        """
        Retrieve the value of the field from the instance.

        If the value has been saved to the database, decrypt it using an aggregate query.
        """
        if not instance:
            return self

        if not instance.pk:
            return instance.__dict__[self.field.name]

        # Value assigned from `__set__`
        value = instance.__dict__[self.field.name]

        if isinstance(value, six.binary_type):
            return value

        # Need to raise error, because it is not a normal
        # situation and need to check what is going on
        # instead of using encrypted buffer.
        # Can be bypassed in some cases.
        if (isinstance(value, six.buffer_types) and
                not self._bypass_non_decrypted_field_exception):
            raise ValueError('Unexpected encrypted field "%s"!' % self.field.name)

        return instance.__dict__[self.field.name]

    def __set__(self, instance, value):
        """
        Store a value in the model instance's __dict__.

        The value will be keyed by the field's name.
        """
        instance.__dict__[self.field.name] = value

    @property
    def _bypass_non_decrypted_field_exception(self):
        """Bypass exception if some field was not decrypted."""
        if getattr(settings, 'PGPFIELDS_BYPASS_NON_DECRYPTED_FIELD_EXCEPTION', False):
            return True
        if getattr(settings, 'PGPFIELDS_BYPASS_FIELD_EXCEPTION_IN_MIGRATIONS', False):
            # Since django versions <1.8 have no support of
            # Manager.use_in_migrations, need to turn raising
            # exception off.
            if {'manage.py', 'migrate'}.issubset(sys.argv):
                return True
        return False
