"""This module allows to check GraphQL-specific vulnerabilities."""

# standard imports
import json
import asyncio
import textwrap
from typing import List

# 3rd party imports
import aiohttp

# local imports
from fluidasserts import Unit, Result
from fluidasserts import MEDIUM, HIGH
from fluidasserts import OPEN, CLOSED, UNKNOWN
from fluidasserts import DAST
from fluidasserts.helper import http
from fluidasserts.helper import asynchronous
from fluidasserts.utils.generic import get_sha256
from fluidasserts.utils.decorators import api


#
# Constants
#


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


#
# Helpers
#


def query(url: str, query: str, *args, **kwargs) -> None:
    """Make a generic query to a GraphQL instance."""
    kwargs['files'] = {'query': (None, query)}
    return http.HTTPSession(url, *args, **kwargs)


async def query_async(url: str, query: str, *args, **kwargs) -> None:
    """Make a generic query to a GraphQL instance."""
    with aiohttp.MultipartWriter('form-data') as writer_query:
        writer_query.append(
            query, headers={'Content-Disposition': 'form-data; name="query"'})

    kwargs['data'] = writer_query
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.post(url, *args, **kwargs) as response:
            return await response.read()


#
# Methods
#


@api(risk=MEDIUM, kind=DAST)
def accepts_introspection(url: str, *args, **kwargs) -> Result:
    r"""
    Check if GraphQL is implemented in a way that allows for introspection.

    Do pass cookies or special headers if needed using kwargs.
    Do not use json, data, or files parameter, they'll be added accordingly.

    :param url: GraphQL endpoint to test.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    try:
        obj = query(url, INTROSPECTION_QUERY, *args, **kwargs)
    except http.ConnError as exc:
        return UNKNOWN, f'Connection Error: {exc}'
    except http.ParameterError as exc:
        return UNKNOWN, f'Invalid Parameter: {exc}'
    else:
        fingerprint = obj.get_fingerprint()

    units: List[Unit] = [Unit(where=url,
                              source='GraphQL/Configuration',
                              specific=['Introspection query'],
                              fingerprint=fingerprint)]

    try:
        obj_json = json.loads(obj.response.text)
    except json.JSONDecodeError as exc:
        return UNKNOWN, f'Invalid JSON in GraphQL response: {exc}'

    if obj_json.get('errors'):
        res = CLOSED
        msg = 'GraphQL does not accept introspection queries'
        vulns, safes = [], units
    else:
        res = OPEN
        msg = 'GraphQL accepts introspection queries'
        vulns, safes = units, []

    return res, msg, vulns, safes


@api(risk=HIGH, kind=DAST)
def has_dos(url: str, query: str,
            num: int, timeout: float, *args, **kwargs) -> Result:
    r"""
    Check if GraphQL is implemented in a way that allows for a DoS.

    The method will perform `num` asynchronous requests and consider a DoS
    if any of the requests exceed the timeout.

    Consider using an expensive query, (one that takes the server some
    processing time to respond).

    Consider going from one request, to two, then three and so on until you
    find the server starts taking time to respond. Avoid launching one million
    requests at once or you could really be damaging the server.

    Do pass cookies or special headers if needed using kwargs.
    Do not use json, data, or files param, the request body
    will be added accordingly from your `query`.

    :param url: GraphQL endpoint to test.
    :param query: A GraphQL query (see the tests for examples).
    :param num: Number of simultaneous requests to made.
    :param timeout: Max number of seconds to wait for a response.
    :param \*args: Optional arguments for :class:`.HTTPSession`.
    :param \*\*kwargs: Optional arguments for :class:`.HTTPSession`.
    """
    kwargs['timeout'] = aiohttp.ClientTimeout(total=timeout)

    async def run_dos(url: str, query: str, num: int, args, kwargs):
        """Function to run multiple queries and return the errors."""
        tasks = (
            asyncio.ensure_future(
                query_async(url, query, *args, **kwargs)) for _ in range(num))

        responses = await asyncio.gather(*tasks, return_exceptions=True)

        return \
            tuple(filter(asynchronous.is_timeout_error, responses)), \
            tuple(filter(asynchronous.is_parameter_error, responses)), \
            tuple(filter(asynchronous.is_connection_error, responses))

    timeouts, param_errors, conn_errors = asynchronous.run_func(
        func=run_dos, args=(((url, query, num, args, kwargs), {}),))[0]

    if param_errors:
        return UNKNOWN, f'Some parameter errors ocurred: {param_errors}'
    if conn_errors:
        return UNKNOWN, f'Some connection errors ocurred: {conn_errors}'

    units: List[Unit] = [Unit(where=url,
                              source='GraphQL/Architecture',
                              specific=['Response time'],
                              fingerprint=get_sha256(query))]

    if timeouts:
        return OPEN, 'GraphQL is vulnerable to a DoS', units
    else:
        return CLOSED, 'GraphQL is vulnerable to a DoS', [], units
