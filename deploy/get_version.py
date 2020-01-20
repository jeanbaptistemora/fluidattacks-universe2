#! /usr/bin/env python3

import time


def get_version():
    """Return fluidasserts version."""
    cur_time = time.gmtime()
    min_month = (cur_time.tm_mday - 1) * 1440 + cur_time.tm_hour * 60 + \
        cur_time.tm_min
    return time.strftime(f'%y.%m.{min_month}')


if __name__ == '__main__':
    print(get_version())
