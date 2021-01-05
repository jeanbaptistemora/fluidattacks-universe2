# Third party libraries
import pytest

# Local libraries
from parse_tree_sitter import (
    parse_java,
)


@pytest.mark.skims_test_group('unittesting')
def test_parse_java() -> None:
    data = parse_java(b'package x.x;')

    assert data == {
        "children": [
            {
                "children": [
                    {
                        "children": [],
                        "c": 0,
                        "l": 0,
                        "type": "package"
                    },
                    {
                        "children": [
                            {
                                "children": [],
                                "c": 8,
                                "l": 0,
                                "type": "identifier"
                            },
                            {
                                "children": [],
                                "c": 9,
                                "l": 0,
                                "type": "."
                            },
                            {
                                "children": [],
                                "c": 10,
                                "l": 0,
                                "type": "identifier"
                            }
                        ],
                        "c": 8,
                        "l": 0,
                        "type": "scoped_identifier"
                    },
                    {
                        "children": [],
                        "c": 11,
                        "l": 0,
                        "type": ";"
                    }
                ],
                "c": 0,
                "l": 0,
                "type": "package_declaration"
            }
        ],
        "c": 0,
        "l": 0,
        "type": "program"
    }
