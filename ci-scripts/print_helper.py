import sys
from termcolor import colored

def print_info(msg, color='', *args, **kwargs):
    if color == '':
        sys.stdout.write(msg)
    else:
        sys.stdout.write(colored(msg, color, *args, **kwargs))

def print_error(msg, color='', *args, **kwargs):
    if color == '':
        sys.stderr.write(msg)
    else:
        sys.stderr.write(colored(msg, color, *args, **kwargs))

def print_success(msg, color='green', *args, **kwargs):
    print_info(msg, color, *args, **kwargs)

def print_failure(msg, color='red', *args, **kwargs):
    print_info(msg, color, *args, **kwargs)

def print_warning(msg, color='yellow', *args, **kwargs):
    print_info(msg, color, *args, **kwargs)

def print_unknown(msg, color='', *args, **kwargs):
    print_info(msg, color, *args, **kwargs)
