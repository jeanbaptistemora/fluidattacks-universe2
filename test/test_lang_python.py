# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.code.python."""

# standard imports
# None

# 3rd party imports
import pytest
pytestmark = pytest.mark.asserts_module('lang_python')

# local imports
from fluidasserts.lang import python

# Constants

CODE_DIR = 'test/static/lang/python/'
SECURE_CODE = CODE_DIR + 'exceptions_close.py'
INSECURE_CODE = CODE_DIR + 'exceptions_open.py'
NON_EXISTANT_CODE = CODE_DIR + 'not_exists.py'
LINES_FORMAT = 'lines: '


#
# Helpers
#


def test_is_primitive():
    """Check if an object is of primitive type."""
    assert python.is_primitive(12)
    assert python.is_primitive('asserts')
    assert python.is_primitive({'key': 'value'})
    assert not python.is_primitive(lambda x: x)


def test_object_to_dict():
    class Car():
        def __init__(self, color: str, model: str):
            self.color = color
            self.model = model
    assert python.object_to_dict(Car('red', '2018')) == {
        'class_name': 'Car', 'color': 'red', 'model': '2018'}


def test_iterate_dict_nodes():
    instances = {
        'reservations': [{
            'type': 'small',
            'state': {
                'name': 'runing'
            },
            'tags': [[{
                'key': 'name',
                'value': 'web'
            }]]
        }]
    }

    result = [('reservations', [{
        'type': 'small',
        'state': {
            'name': 'runing'
        },
        'tags': [[{
            'key': 'name',
            'value': 'web'
        }]]
    }]), ('type', 'small'), ('state', {
        'name': 'runing'
    }), ('name', 'runing'), ('tags', [[{
        'key': 'name',
        'value': 'web'
    }]]), ('key', 'name'), ('value', 'web')]

    assert list(python.iterate_dict_nodes(instances)) == result


#
# Open tests
#


def test_has_generic_exceptions_open():
    """Code uses generic exceptions."""
    assert python.has_generic_exceptions(CODE_DIR).is_open()
    results = python.has_generic_exceptions(INSECURE_CODE)
    assert results.is_open()
    assert len(results.vulns[0].specific) == 5


def test_swallows_exceptions_open():
    """Code swallows exceptions."""
    assert python.swallows_exceptions(CODE_DIR).is_open()
    results = python.swallows_exceptions(INSECURE_CODE)
    assert results.is_open()
    assert len(results.vulns[0].specific) == 4


def test_insecure_functions_open():
    """Search for insecure functions."""
    assert python.uses_insecure_functions(CODE_DIR).is_open()
    assert python.uses_insecure_functions(INSECURE_CODE).is_open()


def test_uses_catch_for_memory_error_open():
    """Search for MemoryError catches."""
    assert python.uses_catch_for_memory_error(CODE_DIR).is_open()
    assert python.uses_catch_for_memory_error(INSECURE_CODE).is_open()


def test_uses_catch_for_syntax_errors_open():
    """Search for MemoryError catches."""
    assert python.uses_catch_for_syntax_errors(CODE_DIR).is_open()
    assert python.uses_catch_for_syntax_errors(INSECURE_CODE).is_open()


#
# Closing tests
#


def test_has_generic_exceptions_close():
    """Code uses generic exceptions."""
    assert python.has_generic_exceptions(SECURE_CODE).is_closed()
    assert python.has_generic_exceptions(
        CODE_DIR, exclude=['test']).is_closed()


def test_swallows_exceptions_close():
    """Code swallows exceptions."""
    assert python.swallows_exceptions(SECURE_CODE).is_closed()
    assert python.swallows_exceptions(CODE_DIR, exclude=['test']).is_closed()


def test_insecure_functions_close():
    """Search for insecure functions."""
    assert python.uses_insecure_functions(SECURE_CODE).is_closed()
    assert python.uses_insecure_functions(
        CODE_DIR, exclude=['exceptions_open']).is_closed()


def test_uses_catch_for_memory_error_closed():
    """Search for MemoryError catches."""
    assert python.uses_catch_for_memory_error(SECURE_CODE).is_closed()
    assert python.uses_catch_for_memory_error(
        CODE_DIR, exclude=['exceptions_open']).is_closed()


def test_uses_catch_for_syntax_errors_closed():
    """Search for MemoryError catches."""
    assert python.uses_catch_for_syntax_errors(SECURE_CODE).is_closed()
    assert python.uses_catch_for_syntax_errors(
        CODE_DIR, exclude=['exceptions_open']).is_closed()


#
# Unknown tests
#


def test_has_generic_exceptions_unknown():
    """Code uses generic exceptions."""
    assert python.has_generic_exceptions(NON_EXISTANT_CODE).is_unknown()


def test_swallows_exceptions_unknown():
    """Code swallows exceptions."""
    assert python.swallows_exceptions(NON_EXISTANT_CODE).is_unknown()


def test_insecure_functions_unknown():
    """Search for insecure functions."""
    assert python.uses_insecure_functions(NON_EXISTANT_CODE).is_unknown()


def test_uses_catch_for_memory_error_unknown():
    """Search for MemoryError catches."""
    assert python.uses_catch_for_memory_error(NON_EXISTANT_CODE).is_unknown()


def test_uses_catch_for_syntax_errors_unknown():
    """Search for MemoryError catches."""
    assert python.uses_catch_for_syntax_errors(NON_EXISTANT_CODE).is_unknown()
