from api import (
    Operation,
)
from api.schema import (
    SCHEMA,
)
from app.app import (
    get_validation_rules,
)
from graphql import (
    get_introspection_query,
    parse,
    validate,
)
import pytest
from typing import (
    NamedTuple,
)

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


class ContextValue(NamedTuple):
    operation: Operation


_context_value = ContextValue(
    operation=Operation(name="", query="", variables="")
)


def test_should_allow_introspection() -> None:
    query = get_introspection_query()
    errors = validate(
        SCHEMA,
        parse(query),
        get_validation_rules(_context_value, parse(query), None),
    )
    assert not errors


def test_should_trigger_depth_validation() -> None:
    query = """
        query MaliciousQuery {
            __schema {
                queryType {
                    name
                    kind
                    ofType {
                        kind
                        name
                        ofType {
                            kind
                            name
                            ofType {
                                kind
                                name
                                ofType {
                                    kind
                                    name
                                    ofType {
                                        kind
                                        name
                                        ofType {
                                            kind
                                            name
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    """
    errors = validate(
        SCHEMA,
        parse(query),
        get_validation_rules(_context_value, parse(query), None),
    )
    assert errors
    assert errors[0].message == "Exception - Max query depth exceeded"


def test_should_trigger_breadth_validation() -> None:
    query = """
        query MaliciousQuery {
            alias1: __schema {
                queryType {
                    name
                    kind
                }
            }
            alias2: __schema {
                queryType {
                    name
                    kind
                }
            }
            alias3: __schema {
                queryType {
                    name
                    kind
                }
            }
            alias4: __schema {
                queryType {
                    name
                    kind
                }
            }
        }
    """
    errors = validate(
        SCHEMA,
        parse(query),
        get_validation_rules(_context_value, parse(query), None),
    )
    assert errors
    assert errors[0].message == "Exception - Max query breadth exceeded"


def test_should_variable_validation() -> None:
    query = """
        mutation ExtraVariables (
            $test: String!,
            $name: String!,
        ) {
            mutationName(
                test: $test
                name: $name
            ) {
                success
            }
        }
    """

    class Context(NamedTuple):
        operation: Operation

    errors = validate(
        SCHEMA,
        parse(query),
        get_validation_rules(
            Context(
                operation=Operation(
                    name="",
                    query="",
                    variables={
                        "test": "value",
                        "name": "value",
                        "extra_variable": "value",
                    },
                )
            ),
            parse(query),
            None,
        ),
    )
    assert errors
    assert errors[0].message == "Exception - Extra variables in operation"
