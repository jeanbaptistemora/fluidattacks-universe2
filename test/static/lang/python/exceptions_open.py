"""
exceptions_open.py.

This is a test module to check exceptions.
"""
import pickle

eval('print("a")')
pickle.load('test')

# pylint: disable=bare-except
try:
    print('Hello world')
except:
    print('a')
try:
    print('Hello world')
except:
    pass
try:
    print('Hello world')
except IndexError:
    pass
try:
    print('Hello world')
except (IndexError, AttributeError):
    pass
try:
    print('Hello world')
except IndexError:
    print('a')
try:
    print('Hello world')
except BaseException:
    print('a')
for _ in range(10):
    try:
        print('Hello world')
    except (BaseException, Exception):
        print('a')
    try:
        print('Hello world')
    except (Exception, IndexError) as exc:
        print(exc)
    try:
        print('Hello world')
    except (IndexError, AttributeError):
        pass
