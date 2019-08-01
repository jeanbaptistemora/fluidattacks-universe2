# -*- coding: utf-8 -*-

"""Archivo estandar para generacion de instalador.

Este modulo define los parametros minimos requeridos para generar
un instalador estandar de fluidasserts.
"""
import time
import io
from setuptools import setup


def _get_readme():
    """Returns fluidasserts readme."""
    readme_path = 'conf/README.rst'
    with io.open(readme_path, 'rt', encoding='utf8') as readme_f:
        return readme_f.read()


def _get_version():
    """Returns fluidasserts version."""
    cur_time = time.localtime()
    min_month = (cur_time.tm_mday - 1) * 1440 + cur_time.tm_hour * 60 + \
        cur_time.tm_min
    return time.strftime('%y.%m.{}').format(min_month)


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
        'fluidasserts.format',
        'fluidasserts.helper',
        'fluidasserts.syst',
        'fluidasserts.proto',
        'fluidasserts.lang',
        'fluidasserts.utils',
        'fluidasserts.sca',
        'fluidasserts.cloud',
        'fluidasserts.cloud.aws',
        'fluidasserts.db',
    ],
    data_files=[
        ('', ['conf/conf.cfg', 'conf/conf.spec']),
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
        'configobj==5.0.6',          # fluidasserts
        'typed-ast==1.4.0',          # fluidasserts
        'PyPDF2==1.26.0',            # fluidasserts.format.pdf
        'requests==2.22.0',          # fluidasserts.proto.http
        'certifi==2019.6.16',         # fluidasserts.proto.ssl
        'ldap3==2.6',                # fluidasserts.proto.ldap
        'paramiko==2.6.0',           # fluidasserts.helper.ssh_helper
        'pywinrm==0.3.0',            # fluidasserts.helper.winrm_helper
        'beautifulsoup4==4.8.0',     # fluidasserts.helper.http_helper
        'dnspython==1.15.0',         # fluidasserts.proto.dns
        'tlslite-ng==0.8.0-alpha26',         # fluidasserts.proto.ssl
        'pyOpenSSL==19.0.0',         # fluidasserts.proto.ssl
        'cffi==1.12.3',              # fluidasserts.proto.ssl
        'cryptography==2.7',         # fluidasserts.proto.ssl
        'bcrypt==3.1.7',             # fluidasserts.proto.ssl
        'pynacl==1.3.0',             # fluidasserts.proto.ssl
        'colorama==0.4.1',           # logging
        'pysmb==1.1.27',             # fluidasserts.proto.smb
        'mixpanel==4.4.0',           # fluidasserts.utils.decorators
        'pytesseract==0.2.7',        # fluidasserts.format.captcha
        'pillow==6.1.0',             # fluidasserts.format.captcha
        'pyparsing==2.4.0',          # fluidasserts.lang
        'bandit==1.6.2',             # fluidasserts.lang.python
        'oyaml==0.9',                # fluidasserts
        'pygments==2.4.2',           # fluidasserts
        'viewstate==0.4.3',          # fluidasserts.proto.http
        'ntplib==0.3.3',             # fluidasserts.proto.http
        'pytz==2019.1',              # fluidasserts.proto.http
        'requirements-detector==0.6',  # fluidasserts.sca
        'defusedxml==0.6.0',         # fluidasserts.sca
        'boto3==1.9.193',            # fluidasserts.cloud.aws
        'python-dateutil==2.8.0',    # fluidasserts.cloud.aws
        'mysql-connector==2.2.9',    # fluidasserts.db.mysql_db
        'pycrypto==2.6.1; platform_system == "Linux"',
        'pyjwt==1.7.1',              # fluidasserts.format.jwt
        'pyjks==19.0.0',             # fluidasserts.format.jks
        'gitpython==2.1.12',         # fluidasserts.proto.git
        'aiohttp==3.5.4',            # fluidasserts
        'androguard==3.3.5',         # fluidasserts.format.apk
    ],
    include_package_data=True,      # archivos a incluir en MANIFEST.in
    entry_points={
            'console_scripts': ['asserts=fluidasserts.utils.cli:main'],
        },
)
