# -*- coding: utf-8 -*-

"""Installation script.

This module defines the minimum requirements to generate an standard
setup script of fluidasserts.
"""

import io
import time
from setuptools import setup


def _get_readme():
    """Return fluidasserts readme."""
    readme_path = 'conf/README.rst'
    with io.open(readme_path, 'rt', encoding='utf8') as readme_f:
        return readme_f.read()


def _get_version():
    """Return fluidasserts version."""
    cur_time = time.gmtime()
    min_month = (cur_time.tm_mday - 1) * 1440 + cur_time.tm_hour * 60 + \
        cur_time.tm_min
    return time.strftime(f'%y.%m.{min_month}')


setup(
    name='fluidasserts',
    description='Assertion Library for Security Assumptions',
    long_description=_get_readme(),
    version=_get_version(),
    url='https://fluidattacks.com/web/products/asserts',
    project_urls={'Documentation': 'https://fluidattacks.gitlab.io/asserts/'},
    package_data={'': ['conf/conf.cfg', 'conf/conf.spec']},
    author='Fluid Attacks Engineering Team',
    author_email='engineering@fluidattacks.com',
    packages=[
        'fluidasserts',
        'fluidasserts.cloud',
        'fluidasserts.cloud.aws',
        'fluidasserts.cloud.aws.cloudformation',
        'fluidasserts.db',
        'fluidasserts.format',
        'fluidasserts.helper',
        'fluidasserts.iot',
        'fluidasserts.lang',
        'fluidasserts.ot',
        'fluidasserts.proto',
        'fluidasserts.sca',
        'fluidasserts.syst',
        'fluidasserts.utils',
    ],
    package_dir={
        'fluidasserts': 'fluidasserts',
    },
    classifiers=[
        'Environment :: Console',
        'Topic :: Security',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Quality Assurance',
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: Other/Proprietary License',
    ],
    install_requires=[
        'aiohttp==3.6.2',              # fluidasserts
        'androguard==3.3.5',           # fluidasserts.format.apk
        'azure==4.0.0',                # fluidasserts.cloud.azure
        'azure-identity==1.1.0',       # fluidasserts.cloud.azure.key_vaults
        'azure-keyvault-keys==4.0.0',  # fluidasserts.cloud.azure.key_vaults
        'azure-keyvault-secrets==4.0.0',  # fluidasserts.cloud.azure.key_vaults
        'bandit==1.6.2',               # fluidasserts.lang.python
        'bcrypt==3.1.7',               # fluidasserts.proto.ssl
        'beautifulsoup4==4.8.1',       # fluidasserts.helper.http_helper
        'boto3==1.10.17',              # fluidasserts.cloud.aws
        'certifi==2019.9.11',          # fluidasserts.proto.ssl
        'cffi==1.13.2',                # fluidasserts.proto.ssl
        'colorama==0.4.1',             # logging
        'configobj==5.0.6',            # fluidasserts
        'cfn_flip==1.2.2',             # fluidasserts.helper.cloudformation
        'cryptography==2.8',           # fluidasserts.proto.ssl
        'cython==0.29.14',             # fluidasserts.db.mssql
        'defusedxml==0.6.0',           # fluidasserts.sca
        'dnspython==1.16.0',           # fluidasserts.proto.dns
        'gitpython==3.0.4',            # fluidasserts.proto.git
        'google-api-python-client==1.7.11',     # fluidasserts.cloud.gcp
        'google-auth-httplib2==0.0.3',    # fluidasserts.cloud.gcp
        'kubernetes==10.0.1',          # fluidasserts.cloud.kubernetes
        'ldap3==2.6.1',                  # fluidasserts.proto.ldap
        'mixpanel==4.5.0',             # fluidasserts.utils.decorators
        'mysql-connector==2.2.9',      # fluidasserts.db.mysql_db
        'names==0.3.0',                # fluidasserts.helper.http
        'ntplib==0.3.3',               # fluidasserts.proto.http
        'oyaml==0.9',                  # fluidasserts
        'paramiko==2.6.0',             # fluidasserts.helper.ssh_helper
        'pillow==6.2.1',               # fluidasserts.format.captcha
        'psycopg2==2.8.4',             # fluidasserts.db.postgresql
        'pyopenssl==19.0.0',           # fluidasserts.proto.ssl
        'pycrypto==2.6.1; platform_system == "Linux"',
        'pygments==2.4.2',             # fluidasserts
        'pyjks==19.0.0',               # fluidasserts.format.jks
        'pyjwt==1.7.1',                # fluidasserts.format.jwt
        'pymssql==2.1.4',              # fluidasserts.db.mssql
        'pynacl==1.3.0',               # fluidasserts.proto.ssl
        'pyparsing==2.4.5',            # fluidasserts.lang
        'pypdf2==1.26.0',              # fluidasserts.format.pdf
        'pysmb==1.1.27',               # fluidasserts.proto.smb
        'pytesseract==0.3.0',          # fluidasserts.format.captcha
        'python-dateutil==2.8.1',      # fluidasserts.cloud.aws
        'python-magic==0.4.15',        # fluidasserts.format.file
        'pytz==2019.3',                # fluidasserts.proto.http
        'pywinrm==0.4.1',              # fluidasserts.helper.winrm_helper
        'requests==2.22.0',            # fluidasserts.proto.http
        'requirements-detector==0.6',  # fluidasserts.sca
        'selenium==3.141.0',           # fluidasserts.helper.http
        'tlslite-ng==0.8.0-alpha29',   # fluidasserts.proto.ssl
        'typed-ast==1.4.0',            # fluidasserts
        'viewstate==0.4.3',            # fluidasserts.proto.http
    ],
    include_package_data=True,         # files to include in MANIFEST.in
    entry_points={
        'console_scripts': [
            'asserts=fluidasserts.utils.cli:main',
        ],
    },
)
