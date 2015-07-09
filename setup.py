from setuptools import find_packages, setup

version = '0.0.1'

setup(
    name='django-postgres-pgpfields',
    packages=find_packages(),
    include_package_data=True,
    version=version,
    license='MIT',
    description='PGP encrypted fields, which are encrypted by the pgcrypto postgres extension.',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Database',
        'Topic :: Security :: Cryptography',
    ],
    author='coldmind',
    author_email='me@asokolovskiy.com',
    url='https://github.com/coldmind/django-postgres-pgpfields',
    keywords=['pgcrypto', 'pgp', 'encryption', 'django', 'fields'],
)
