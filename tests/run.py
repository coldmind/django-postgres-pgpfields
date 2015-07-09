#! /usr/bin/env python
import os
import sys

import django
from django.conf import settings
from django.test.runner import DiscoverRunner

import dj_database_url
from colour_runner.django_runner import ColourRunnerMixin


BASEDIR = os.path.dirname(os.path.dirname(__file__))
PGPFIELDS_PUBLIC_KEY = os.path.abspath(
    os.path.join(BASEDIR, 'tests/test_keys/public.key')
)
PGPFIELDS_PRIVATE_KEY = os.path.abspath(
    os.path.join(BASEDIR, 'tests/test_keys/private.key')
)


settings.configure(
    DATABASES={
        'default': dj_database_url.config(
            default='postgres://localhost/pgcrypto_fields'
        ),
    },
    INSTALLED_APPS=(
        'django_postgres_pgpfields',
        'tests',
    ),
    MIDDLEWARE_CLASSES=(),
    PGPFIELDS_PUBLIC_KEY=open(PGPFIELDS_PUBLIC_KEY, 'r').read(),
    PGPFIELDS_PRIVATE_KEY=open(PGPFIELDS_PRIVATE_KEY, 'r').read(),
)


if django.VERSION >= (1, 7):
    django.setup()


class TestRunner(ColourRunnerMixin, DiscoverRunner):
    """Enable colorised output."""


test_runner = TestRunner(verbosity=1)
failures = test_runner.run_tests(['tests'])
if failures:
    sys.exit(1)
