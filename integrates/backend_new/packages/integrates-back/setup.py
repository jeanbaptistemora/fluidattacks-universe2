import time
from setuptools import setup


def _get_version():
    """Return version."""
    cur_time = time.gmtime()
    min_month = (cur_time.tm_mday - 1) * 1440 + cur_time.tm_hour * 60 + \
        cur_time.tm_min
    return time.strftime(f'%y.%m.{min_month}')


setup(
    version=_get_version()
)
