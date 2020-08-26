"""
exceptions_close.py.

This is a test module to check exceptions.
"""
try:
    print('Hello world')
except FileNotFoundError:
    print('Managed')
try:
    print('Hello world')
except IndexError:
    print('Managed')
