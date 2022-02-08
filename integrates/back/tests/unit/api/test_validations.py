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
            }
        }
    """
    errors = validate(SCHEMA, parse(query), API_VALIDATIONS)
    assert errors
    assert errors[0].message == "Exception - Max query depth exceeded"
