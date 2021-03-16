# Third party libraries
from aioextensions import (
    run_decorator,
)
import pytest

# Local libraries
from parse_babel import (
    parse,
)
from utils.fs import (
    get_file_raw_content,
)


@run_decorator
@pytest.mark.skims_test_group('unittesting')
async def test_parse_success() -> None:
    path = 'skims/test/data/lib_path/f034/javascript.js'
    data = await parse(
        content=await get_file_raw_content(path),
        path=path,
    )

    assert data == {
        "comments": [],
        "end": 20,
        "errors": [],
        "loc": {
            "end": {
                "column": 0,
                "line": 3
            },
            "start": {
                "column": 0,
                "line": 1
            }
        },
        "program": {
            "body": [
                {
                    "end": 19,
                    "expression": {
                        "arguments": [],
                        "callee": {
                            "computed": False,
                            "end": 16,
                            "loc": {
                                "end": {
                                    "column": 15,
                                    "line": 2
                                },
                                "start": {
                                    "column": 4,
                                    "line": 2
                                }
                            },
                            "object": {
                                "end": 9,
                                "loc": {
                                    "end": {
                                        "column": 8,
                                        "line": 2
                                    },
                                    "identifierName": "Math",
                                    "start": {
                                        "column": 4,
                                        "line": 2
                                    }
                                },
                                "name": "Math",
                                "start": 5,
                                "type": "Identifier"
                            },
                            "optional": False,
                            "property": {
                                "end": 16,
                                "loc": {
                                    "end": {
                                        "column": 15,
                                        "line": 2
                                    },
                                    "identifierName": "random",
                                    "start": {
                                        "column": 9,
                                        "line": 2
                                    }
                                },
                                "name": "random",
                                "start": 10,
                                "type": "Identifier"
                            },
                            "start": 5,
                            "type": "MemberExpression"
                        },
                        "end": 18,
                        "loc": {
                            "end": {
                                "column": 17,
                                "line": 2
                            },
                            "start": {
                                "column": 4,
                                "line": 2
                            }
                        },
                        "optional": False,
                        "start": 5,
                        "type": "CallExpression"
                    },
                    "loc": {
                        "end": {
                            "column": 18,
                            "line": 2
                        },
                        "start": {
                            "column": 4,
                            "line": 2
                        }
                    },
                    "start": 5,
                    "type": "ExpressionStatement"
                }
            ],
            "end": 20,
            "interpreter": None,
            "loc": {
                "end": {
                    "column": 0,
                    "line": 3
                },
                "start": {
                    "column": 0,
                    "line": 1
                }
            },
            "sourceType": "module",
            "start": 0,
            "type": "Program"
        },
        "start": 0,
        "type": "File"
    }


@run_decorator
@pytest.mark.skims_test_group('unittesting')
async def test_parse_fail() -> None:
    path = 'skims/test/data/lib_path/f011/yarn.lock'
    data = await parse(
        content=await get_file_raw_content(path),
        path=path,
    )

    assert data == {}
