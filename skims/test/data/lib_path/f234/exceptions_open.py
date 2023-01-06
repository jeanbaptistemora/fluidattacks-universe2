# pylint: skip-file
"""
exceptions_open.py.

This is a test module to check exceptions.
"""
try:
    print("Hello world")
except:  # noqa
    print("a")
try:
    print("Hello world")
except:  # noqa
    print("a")
try:
    print("Hello world")
except:  # noqa
    pass
try:
    print("Hello world")
except IndexError:
    pass
try:
    print("Hello world")
except (IndexError, AttributeError):
    pass
try:
    print("Hello world")
except IndexError:
    print("a")
try:
    print("Hello world")
except BaseException:  # noqa
    print("a")
try:
    list(range(10**10))
except (IOError, MemoryError) as exc:
    print(exc)
try:
    # We cannot replicate syntax errors
    # because we parse it with AST in another check
    pass
except (StopAsyncIteration, SyntaxError) as exc:
    print(exc)
for _ in range(10):
    try:
        print("Hello world")
    except (BaseException, Exception):  # noqa
        print("a")
    try:
        print("Hello world")
    except (Exception, IndexError) as exc:  # noqa
        print(exc)
    try:
        print("Hello world")
    except (IndexError, AttributeError):
        pass
