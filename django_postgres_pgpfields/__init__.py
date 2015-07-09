from django.conf import settings


CAST_TO_TEXT = "nullif(%s, NULL)::text"

INTEGER_PGP_PUB_ENCRYPT_SQL = "pgp_pub_encrypt({}, dearmor('{}'))".format(
    CAST_TO_TEXT,
    settings.PGPFIELDS_PUBLIC_KEY,
)

PGP_PUB_ENCRYPT_SQL = "pgp_pub_encrypt(%s, dearmor('{}'))".format(
    settings.PGPFIELDS_PUBLIC_KEY,
)
