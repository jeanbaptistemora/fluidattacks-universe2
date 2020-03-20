# Standard library
import os
import time
import json
import textwrap
import functools
from typing import Any, List, NamedTuple, Tuple, Optional

# Third parties libraries
import requests
import simplejson
from requests.packages.urllib3.exceptions import (  # noqa: import-error
    InsecureRequestWarning
)
from frozendict import frozendict

# Local imports
from toolbox import logger

# On call
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Containers
File = NamedTuple('File', [('name', str),
                           ('filename', Optional[str]),
                           ('buffer', Optional[bytes]),
                           ('content_type', Optional[str])])
Response = NamedTuple('Response', [('ok', bool),
                                   ('status_code', int),
                                   ('data', Any),
                                   ('errors', Tuple[Any, ...])])

# Debugging
DEBUGGING: bool = False

# Constants
CACHE_SIZE: int = 4**8
RETRY_MAX_ATTEMPTS: int = 8 if not DEBUGGING else 1
RETRY_RELAX_SECONDS: float = 2.0
PROXIES = None if not DEBUGGING else {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080",
}
ERRORS: tuple = (
    requests.exceptions.ChunkedEncodingError,
    requests.exceptions.ConnectTimeout,
    requests.exceptions.ConnectionError,
    requests.exceptions.ContentDecodingError,
    requests.exceptions.HTTPError,
    requests.exceptions.ProxyError,
    requests.exceptions.ReadTimeout,
    requests.exceptions.RetryError,
    requests.exceptions.SSLError,
    requests.exceptions.StreamConsumedError,
    requests.exceptions.Timeout,
    requests.exceptions.TooManyRedirects,
    requests.exceptions.UnrewindableBodyError,  # type: ignore

    requests.exceptions.URLRequired,
    requests.exceptions.InvalidHeader,  # type: ignore
    requests.exceptions.InvalidProxyURL,  # type: ignore
    requests.exceptions.InvalidSchema,
    requests.exceptions.InvalidURL,
    requests.exceptions.MissingSchema,

    simplejson.JSONDecodeError,
    json.JSONDecodeError)


def _is_bool(string: str) -> bool:
    """Return True if 'string' is a GraphQL boolean."""
    return string in ('false', 'true')


def _request_parse_as_multipart(payload: str, files: List[File]):
    """Process a request as multipart."""
    # https://github.com/jaydenseric/graphql-multipart-request-spec
    num_of_files: int = len(files)
    single_file: bool = num_of_files == 1

    if single_file:
        map_json = {
            files[0].name: ['variables.file']
        }
        operations_json = {
            "query": payload,
            "variables": {
                "file": None,
            },
        }
    else:
        map_json = {
            file.name: [f'variables.files.{file.name}']
            for file in files
        }
        operations_json = {
            "query": payload,
            "variables": {
                "files": [None] * num_of_files,
            },
        }
    files.insert(0, File(
        name='operations',
        filename=None,
        buffer=json.dumps(operations_json, indent=2, sort_keys=True).encode(),
        content_type=None))
    files.insert(1, File(
        name='map',
        filename=None,
        buffer=json.dumps(map_json, indent=2, sort_keys=True).encode(),
        content_type=None))
    request_files = {
        file.name: (
            file.filename,
            file.buffer,
            file.content_type,
        )
        for index, file in enumerate(files)
    }
    return request_files


def _request_parse_as_json(payload: str):
    """Process a request as JSON."""
    request_json = {
        "query": payload
    }
    return request_json


def _request_handler(api_token: str,
                     payload: str,
                     files: List[File],
                     attempt_no: int = 1
                     ) -> Response:
    """Low level generic POST request to a GraphQL instance."""
    assert isinstance(api_token, str)
    assert isinstance(payload, str)
    assert isinstance(files, list)
    assert isinstance(attempt_no, int)
    assert all(isinstance(file, File) for file in files)

    if files:
        # Do multipart
        request_json = None
        request_files = _request_parse_as_multipart(payload, files)
    else:
        # Do JSON
        request_files = None
        request_json = _request_parse_as_json(payload)

    try:
        response = requests.post(
            url='https://fluidattacks.com/integrates/api',
            proxies=PROXIES,
            headers={
                'Authorization': f'Bearer {api_token}',
            },
            json=request_json,
            files=request_files,
            verify=False,
            timeout=None)

        logger.debug('request', request_files)

        content = response.json()
    except ERRORS as error:
        if attempt_no == RETRY_MAX_ATTEMPTS:
            # We've got no option, return the error
            logger.warn('response with error', str(error))
            return Response(ok=False,
                            status_code=(
                                response.status_code
                                if isinstance(error, (
                                    json.JSONDecodeError,
                                    simplejson.JSONDecodeError,
                                ))
                                else 0),
                            data=None,
                            errors=(
                                str(error),
                            ))
        # Retry
        time.sleep(RETRY_RELAX_SECONDS)
        return _request_handler(api_token, payload, files, attempt_no + 1)

    data: Any = content.get('data')
    errors: Any = content.get('errors')

    # Guarantee data immutability
    if isinstance(data, dict):
        logger.debug('response data is a dict')
        data = frozendict(data)
    elif isinstance(data, list):
        logger.debug('response data is a non-empty tuple')
        data = tuple(data)
    else:
        logger.debug('response data is an empty tuple')
        data = tuple()

    # Guarantee errors immutability
    if errors:
        logger.debug('response errors is a non-empty tuple')
        errors = tuple(errors)
    else:
        logger.debug('response errors is an empty tuple')
        errors = tuple()

    return Response(ok=200 <= response.status_code < 400 and not errors,
                    status_code=response.status_code,
                    data=data,
                    errors=errors)


def request(api_token: str,
            body: str,
            params: dict = None,
            files: List[File] = None,
            expected_types: tuple = tuple()) -> Response:
    """Make a generic query to a GraphQL instance."""
    assert isinstance(body, str)
    if params is not None:
        assert isinstance(params, dict)
    if files is not None:
        assert isinstance(files, list)
        assert all(isinstance(file, File) for file in files)
    else:
        files = []

    payload = textwrap.dedent(body % params if params else body)

    for _ in range(RETRY_MAX_ATTEMPTS):
        response = _request_handler(api_token, payload, files)
        if response.errors or isinstance(response.data, expected_types):
            break
        time.sleep(RETRY_RELAX_SECONDS)

    logger.debug('response', response)
    return response


class Queries:
    """Namespace for Integrates's GraphQL Queries."""

    @staticmethod
    @functools.lru_cache(maxsize=CACHE_SIZE, typed=True)
    def me(api_token: str) -> Response:  # pylint: disable=invalid-name
        """Helper to get an API token from you session token."""
        logger.debug('Query.me()')
        body: str = """
            query {
                me {
                    accessToken
                    role
                    projects {
                        name
                    }
                }
            }
            """
        return request(api_token, body, expected_types=(frozendict,))

    @staticmethod
    @functools.lru_cache(maxsize=CACHE_SIZE, typed=True)
    def project(api_token: str,
                project_name: str,
                with_drafts: str = 'false',
                with_findings: str = 'false') -> Response:
        """Helper to get a project."""
        logger.debug(f'Query.project('
                     f'project_name={project_name}, '
                     f'with_drafts={with_drafts}, '
                     f'with_findings={with_findings})')
        body: str = """
            query {
                project(projectName: "%(project_name)s") {
                    drafts @include(if: %(with_drafts)s) {
                        id @include(if: %(with_drafts)s)
                        title @include(if: %(with_drafts)s)
                    }
                    findings @include(if: %(with_findings)s) {
                        id @include(if: %(with_findings)s)
                        title @include(if: %(with_findings)s)
                    }
                }
            }
            """
        params: dict = {
            'project_name': project_name,
            'with_drafts': with_drafts,
            'with_findings': with_findings,
        }
        return request(api_token, body, params, expected_types=(frozendict,))

    @staticmethod
    @functools.lru_cache(maxsize=CACHE_SIZE, typed=True)
    def finding(api_token: str,
                identifier: str,
                with_vulns: str = 'false') -> Response:
        """Helper to get a finding."""
        logger.debug(f'Query.finding('
                     f'identifier={identifier}, '
                     f'with_vulns={with_vulns})')
        assert isinstance(identifier, str)
        assert _is_bool(with_vulns)
        body: str = """
            query {
                finding(identifier: "%(identifier)s") {
                    attackVectorDesc
                    closedVulnerabilities @include(if: %(with_vulns)s)
                    description
                    historicTreatment
                    lastVulnerability @include(if: %(with_vulns)s)
                    openVulnerabilities @include(if: %(with_vulns)s)
                    projectName
                    recommendation
                    releaseDate
                    severityScore
                    threat
                    title
                    vulnerabilities @include(if: %(with_vulns)s) {
                        historicState @include(if: %(with_vulns)s)
                        id @include(if: %(with_vulns)s)
                        vulnType @include(if: %(with_vulns)s)
                        where @include(if: %(with_vulns)s)
                    }
                }
            }
            """
        params: dict = {
            'identifier': identifier,
            'with_vulns': with_vulns,
        }
        return request(api_token, body, params, expected_types=(frozendict,))

    @staticmethod
    @functools.lru_cache(maxsize=CACHE_SIZE, typed=True)
    def resources(api_token: str,
                  project_name: str) -> Response:
        """Helper to get the project repositories"""
        logger.debug(f'Query.finding('
                     f'project_name={project_name} ')
        body: str = """query {
            resources (projectName : "%(project_name)s") {
                repositories
            }
        }"""
        params: dict = {
            'project_name': project_name
        }
        return request(api_token, body, params, expected_types=(frozendict,))


class Mutations:
    """Namespace for Integrates's GraphQL Mutations."""

    @staticmethod
    def update_access_token(api_token: str, expiration_time: int) -> Response:
        """UpdateAccessToken."""
        logger.debug(f'Mutations.update_access_token('
                     f'expiration_time={expiration_time})')
        body: str = """
            mutation {
                updateAccessToken(expirationTime: %(expiration_time)s) {
                    sessionJwt
                    success
                }
            }
            """
        params: dict = {
            'expiration_time': expiration_time,
        }
        return request(api_token, body, params, expected_types=(frozendict,))

    @staticmethod
    def invalidate_access_token(api_token: str) -> Response:
        """InvalidateAccessToken."""
        logger.debug(f'Mutations.invalidate_access_token()')
        body: str = """
            mutation {
                invalidateAccessToken {
                    success
                }
            }
            """
        return request(api_token, body, expected_types=(frozendict,))

    @staticmethod
    def upload_file(api_token: str,
                    identifier: str,
                    file_path: str) -> Response:
        """UploadFile."""
        logger.debug(f'Mutations.upload_file('
                     f'identifier={identifier}, '
                     f'file_path={file_path})')
        assert isinstance(identifier, str)
        assert isinstance(file_path, str) and os.path.exists(file_path)
        body: str = """
            mutation {
                uploadFile(findingId: "%(identifier)s",
                           file: "",
                           origin: "toolbox") {
                    success
                }
            }
            """
        params: dict = {
            'identifier': identifier,
        }
        with open(file_path, 'rb') as file_path_handle:
            extra_files: List[File] = [
                File(name='1',
                     filename=os.path.basename(file_path),
                     buffer=file_path_handle.read(),
                     content_type='application/x-yaml')]
        return request(
            api_token, body, params, extra_files, expected_types=(frozendict,))

    @staticmethod
    def approve_vulns(api_token: str,
                      finding_id: str,
                      uuid: str = '',
                      approval_status: str = 'false') -> Response:
        """ApproveVulnMutation."""
        logger.debug(f'Mutations.approve_vulns('
                     f'uuid={uuid}, '
                     f'finding_id={finding_id}, '
                     f'approval_status={approval_status})')
        assert isinstance(uuid, str)
        assert isinstance(finding_id, str)
        assert _is_bool(approval_status)
        body: str = """
            mutation {
                approveVulnerability(uuid: "%(uuid)s",
                                     findingId: "%(finding_id)s",
                                     approvalStatus: %(approval_status)s) {
                    success
                }
            }
            """
        params: dict = {
            'uuid': uuid,
            'finding_id': finding_id,
            'approval_status': approval_status,
        }
        return request(api_token, body, params, expected_types=(frozendict,))


# Metadata
__all__: List[str] = [
    'request',
    'request',
    'Queries',
    'Mutations'
]


def clear_cache():
    Queries.me.cache_clear()
    Queries.project.cache_clear()
    Queries.finding.cache_clear()
