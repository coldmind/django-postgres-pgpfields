import datetime

import factory

from .models import EncryptedModel


class EncryptedModelFactory(factory.DjangoModelFactory):
    """Factory to generate hashed and encrypted data."""

    class Meta:
        model = EncryptedModel

    email_pgp_pub_field = factory.Sequence('email{}@test.com'.format)

    integer_pgp_pub_field = 42

    pgp_pub_field = factory.Sequence('Text with public key {}'.format)
    pgp_pub_date_field = datetime.date(year=2000, month=1, day=1)
    pgp_pub_null_boolean_field = True
