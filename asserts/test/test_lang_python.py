# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.code.python."""


# None


import pytest

pytestmark = pytest.mark.asserts_module("lang_python")


from fluidasserts.lang import (
    python,
)

# Constants

CODE_DIR = "test/static/lang/python/"
SECURE_CODE = CODE_DIR + "exceptions_close.py"
INSECURE_CODE = CODE_DIR + "exceptions_open.py"
NON_EXISTANT_CODE = CODE_DIR + "not_exists.py"
LINES_FORMAT = "lines: "


#
# Helpers
#


def test_is_primitive():
    """Check if an object is of primitive type."""
    assert python.is_primitive(12)
    assert python.is_primitive("asserts")
    assert python.is_primitive({"key": "value"})
    assert not python.is_primitive(lambda x: x)


def test_object_to_dict():
    class Car:
        def __init__(self, color: str, model: str):
            self.color = color
            self.model = model

    assert python.object_to_dict(Car("red", "2018")) == {
        "class_name": "Car",
        "color": "red",
        "model": "2018",
    }


def test_iterate_dict_nodes():
    instances = {
        "reservations": [
            {
                "type": "small",
                "state": {"name": "runing"},
                "tags": [[{"key": "name", "value": "web"}]],
            }
        ]
    }

    result = [
        {
            "reservations": [
                {
                    "type": "small",
                    "state": {"name": "runing"},
                    "tags": [[{"key": "name", "value": "web"}]],
                }
            ]
        },
        [
            {
                "type": "small",
                "state": {"name": "runing"},
                "tags": [[{"key": "name", "value": "web"}]],
            }
        ],
        {
            "type": "small",
            "state": {"name": "runing"},
            "tags": [[{"key": "name", "value": "web"}]],
        },
        "small",
        {"name": "runing"},
        "runing",
        [[{"key": "name", "value": "web"}]],
        [{"key": "name", "value": "web"}],
        {"key": "name", "value": "web"},
        "name",
        "web",
    ]

    assert list(python.iterate_dict_nodes(instances)) == result


def test_flatten():
    list_ = [1, 2, 3, [4, 5, [6, 7, 8, 9], 10, 11], 12]
    result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    assert python._flatten(list_) == result


def test_execute_query():
    people = {
        "people": [
            {"age": 20, "other": "foo", "name": "Bob"},
            {"age": 25, "other": "bar", "name": "Fred"},
            {"age": 30, "other": "baz", "name": "George"},
        ]
    }

    checks = [
        {
            "query": "people[?age > `20`].[name, age]",
            "expected": [["Fred", 25], ["George", 30]],
        },
        {
            "query": "people[?age > `20`].{name: name, age: age}",
            "expected": [
                {"name": "Fred", "age": 25},
                {"name": "George", "age": 30},
            ],
        },
        {
            "query": "people[?name == `Fred`].{name: name, age: age}[0]",
            "expected": {"name": "Fred", "age": 25},
        },
    ]
    for check in checks:
        assert (
            python.execute_query(check["query"], people)[0]
            == check["expected"]
        )


#
# Open tests
#


def test_insecure_functions_open():
    """Search for insecure functions."""
    assert python.uses_insecure_functions(CODE_DIR).is_open()
    assert python.uses_insecure_functions(INSECURE_CODE).is_open()


#
# Closing tests
#


def test_insecure_functions_close():
    """Search for insecure functions."""
    assert python.uses_insecure_functions(SECURE_CODE).is_closed()
    assert python.uses_insecure_functions(
        CODE_DIR, exclude=["exceptions_open"]
    ).is_closed()


#
# Unknown tests
#


def test_insecure_functions_unknown():
    """Search for insecure functions."""
    assert python.uses_insecure_functions(NON_EXISTANT_CODE).is_unknown()
