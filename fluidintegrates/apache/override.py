# pylint: disable=E0401
from fluidintegrates.settings import * # noqa

DEBUG = True

ALLOWED_HOSTS = [
    'www.fluid.la',
    'fluid.la',
    'localhost',
    '127.0.0.1',
    '192.168.0.11',
    '192.168.56.101' #development
]
