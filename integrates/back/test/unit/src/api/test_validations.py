from api.schema import (
    SCHEMA,
)
from app.app import (
    API_VALIDATIONS,
)
from graphql import (
    get_introspection_query,
    parse,
    validate,
)
import pytest

pytestmark = [
    pytest.mark.asyncio,
]


def test_should_allow_introspection() -> None:
    query = get_introspection_query()
    errors = validate(SCHEMA, parse(query), API_VALIDATIONS)
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
    errors = validate(SCHEMA, parse(query), API_VALIDATIONS)
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
    errors = validate(SCHEMA, parse(query), API_VALIDATIONS)
    assert errors
    assert errors[0].message == "Exception - Max query breadth exceeded"
