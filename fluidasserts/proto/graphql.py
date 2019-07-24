"""This module allows to check GraphQL-specific vulnerabilities."""

# standard imports
import json
import textwrap

# 3rd party imports

# local imports
from fluidasserts import Unit, Result, MEDIUM, OPEN, CLOSED, UNKNOWN
from fluidasserts.helper import http
from fluidasserts.utils.decorators import api, track

INTROSPECTION_QUERY: str = textwrap.dedent("""
    query {
        __schema {
            queryType {
                name
            }
            mutationType {
                name
            }
            subscriptionType {
                name
            }
            types {
                ...FullType
            }
            directives {
                name
                description
                locations
                args {
                    ...InputValue
                }
            }
        }
    }

    fragment FullType on __Type {
        kind
        name
        description
        fields(includeDeprecated: true) {
            name
            description
            args {
                ...InputValue
            }
            type {
                ...TypeRef
            }
            isDeprecated
            deprecationReason
        }
        inputFields {
            ...InputValue
        }
        interfaces {
            ...TypeRef
        }
        enumValues(includeDeprecated: true) {
            name
            description
            isDeprecated
            deprecationReason
        }
        possibleTypes {
            ...TypeRef
        }
    }

    fragment InputValue on __InputValue {
        name
        description
        type {
            ...TypeRef
        }
        defaultValue
    }

    fragment TypeRef on __Type {
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
                        }
                    }
                }
            }
        }
    }""")


@track
@api(risk=MEDIUM)
def accepts_introspection(url: str, *args, **kwargs) -> Result:
    r"""
    Check if GraphQL is inplemented in a way that allows for introspection.

    Do pass cookies or special headers if needed using kwargs.
    Do not use json, data, or files parameter, they'll be added accordingly.

    :param url: GraphQL endpoint to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    kwargs['files'] = {'query': (None, INTROSPECTION_QUERY)}

    try:
        obj = http.HTTPSession(url, *args, **kwargs)
    except http.ConnError as exc:
        return UNKNOWN, f'Connection Error: {exc}'
    except http.ParameterError as exc:
        return UNKNOWN, f'Invalid Parameter: {exc}'
    else:
        fingerprint = obj.get_fingerprint()

    units: Unit = [Unit(where=url,
                        attribute='GraphQL/Implementation',
                        specific=['GraphQL/Query/Introspection'],
                        fingerprint=fingerprint)]

    try:
        obj_json = json.loads(obj.response.text)
    except json.JSONDecodeError as exc:
        return UNKNOWN, f'Invalid JSON in GraphQL response: {exc}'

    if obj_json.get('errors'):
        res = CLOSED
        msg = 'GraphQL implementation does not accept introspection queries'
        vulns, safes = [], units
    else:
        res = OPEN
        msg = 'GraphQL implementation accepts introspection queries'
        vulns, safes = units, []

    return res, msg, vulns, safes
