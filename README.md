# django-postgres-pgpfields [![Build Status](https://travis-ci.org/coldmind/django-postgres-pgpfields.svg?branch=master)](https://travis-ci.org/coldmind/django-postgres-pgpfields?branch=master)

Inspired by and partially forked https://github.com/incuna/django-pgcrypto-fields.  
Improved to have ability to decrypt at select time instead of  
generating dozens of requests when serializing big amount of data.

`django-postgres-pgpfields` is a `Django` collection of fields,  
which are encrypted by PGP keys using `pgcrypto` extenstion  
of PostgreSQL.

#### Requirements

 - python 2.7 or 3.4
 - postgres with installed `pgcrypto` extension
 - working public and private PGP keys

#### Installation

```
pip install django-postgres-pgpfields
```

or install it directly from github. 

#### Configuration

Define next in `settings.py`:

```python
PGPFIELDS_PUBLIC_KEY = "your public key here"  
PGPFIELDS_PRIVATE_KEY = "your privatekey here"  
# Add 'pgcrypto_fields' to INSTALLED_APPS to create  
# the extension for pgcrypto (it is located in a migration).  
INSTALLED_APPS = (  
    ...  
    'django_postgres_pgpfields',  
    ...  
)  
```

#### Usage

List of available fields.

 - `TextPGPPublicKeyField`
 - `EmailPGPPublicKeyField`
 - `IntegerPGPPublicKeyField`
 - `DatePGPPublicKeyField`
 - `NullBooleanPGPPublicKeyField`

Fields are located at `django_postgres_pgpfields.fields`.  

Your data will be automatically encrypted by using any of  
encrypted fields. To have ability to decrypt data, you **must**  
define the `django_postgres_pgpfields.managers.PGPEncryptedManager`  
manager in your model.  
It is not necessary to override default django manager, but if  
you will try access encrypted field, when data was obtained not by  
`PGPEncryptedManager`, `ValueError` will be raised.
