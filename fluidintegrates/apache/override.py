# pylint: disable=import-error

from fluidintegrates.settings import *  # noqa
from __init__ import FI_DEBUG

DEBUG = FI_DEBUG == 'True'

ALLOWED_HOSTS = [
    'www.fluidattacks.com',
    'fluidattacks.com',
    '.integrates.env.fluidattacks.com',
    'www.fluid.la',
    'fluid.la',
    'localhost',
    '127.0.0.1',
    '192.168.0.11',
    '192.168.56.101'  # development
]
