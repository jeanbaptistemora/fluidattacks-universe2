# Standard library
import asyncio
import contextlib
import os
import time
import json
import textwrap
import functools
from typing import Any, List, NamedTuple, Tuple

# Third parties libraries
import aiohttp
import aiohttp.client_exceptions
import aiogqlc
import aiogqlc.utils
from frozendict import frozendict

# Local imports
from toolbox import logger

# Containers
Response = NamedTuple('Response', [('ok', bool),
                                   ('status_code', int),
                                   ('data', Any),
                                   ('errors', Tuple[Any, ...])])

# Debugging
DEBUGGING: bool = False

# Constants
INTEGRATES_API_URL = 'https://fluidattacks.com/integrates/api'
CACHE_SIZE: int = 4**8
RETRY_MAX_ATTEMPTS: int = 8 if not DEBUGGING else 1
RETRY_RELAX_SECONDS: float = 2.0
PROXIES = None if not DEBUGGING else {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080",
}


class CustomGraphQLClient(aiogqlc.GraphQLClient):
    errors_to_retry: tuple = (
        asyncio.TimeoutError,
        aiohttp.client_exceptions.ClientError,
    )

    async def execute(self, query: str, variables: dict = None,
                      operation: str = None) -> aiohttp.ClientResponse:
        connector = aiohttp.TCPConnector(verify_ssl=False)
        timeout = aiohttp.ClientTimeout(
            total=None,
            connect=None,
            sock_connect=None,
            sock_read=None,
        )

        async with aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
        ) as session:
            headers = self.prepare_headers()

            if variables and aiogqlc.utils.contains_file_variable(variables):
                data = self.prepare_multipart(query, variables, operation)
            else:
                headers[aiohttp.hdrs.CONTENT_TYPE] = 'application/json'
                data = json.dumps(
                    self.prepare_json_data(query, variables, operation))

            async with session.post(
                self.endpoint,
                data=data,
                headers=headers,
            ) as response:
                await response.read()
                return response


async def gql_request(api_token, payload, variables):
    """Async GraphQL request."""
    headers = {
        'Authorization': f'Bearer {api_token}'
    }
    client = CustomGraphQLClient(INTEGRATES_API_URL, headers=headers)
    response = await client.execute(payload, variables=variables)
    content = await response.json()
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

    return Response(ok=200 <= response.status < 400 and not errors,
                    status_code=response.status,
                    data=data,
                    errors=errors)


def request(api_token: str,
            body: str,
            params: dict = None,
            expected_types: tuple = tuple()) -> Response:
    """Make a generic query to a GraphQL instance."""
    assert isinstance(body, str)
    if params is not None:
        assert isinstance(params, dict)

    payload = textwrap.dedent(body % params if params else body)

    for _ in range(RETRY_MAX_ATTEMPTS):
        with contextlib.suppress(*CustomGraphQLClient.errors_to_retry):
            awaitable = gql_request(api_token, payload, params)
            response = asyncio.run(awaitable, debug=DEBUGGING)

            if response.errors or isinstance(response.data, expected_types):
                # It's ok, return
                logger.debug('response', response)
                return response

        time.sleep(RETRY_RELAX_SECONDS)

    return Response(ok=False,
                    status_code=0,
                    data=None,
                    errors=(
                        'Unable to get data, even after retrying',
                    ))


class Queries:
    """Namespace for Integrates's GraphQL Queries."""

    @staticmethod
    @functools.lru_cache(maxsize=CACHE_SIZE, typed=True)
    def me(api_token: str) -> Response:  # pylint: disable=invalid-name
        """Get an API token from your session token."""
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
                with_drafts: bool = False,
                with_findings: bool = False) -> Response:
        """Get a project."""
        logger.debug(f'Query.project('
                     f'project_name={project_name}, '
                     f'with_drafts={with_drafts}, '
                     f'with_findings={with_findings})')
        body: str = """
            query GetProject($projectName: String!, $withDrafts: Boolean!,
                             $withFindings: Boolean!) {
                project(projectName: $projectName) {
                    drafts @include(if: $withDrafts) {
                        id @include(if: $withDrafts)
                        title @include(if: $withDrafts)
                        verified @include(if: $withDrafts)
                    }
                    findings @include(if: $withFindings) {
                        id @include(if: $withFindings)
                        title @include(if: $withFindings)
                        verified @include(if: $withFindings)
                    }
                }
            }
            """
        params: dict = {
            'projectName': project_name,
            'withDrafts': with_drafts,
            'withFindings': with_findings,
        }
        return request(api_token, body, params, expected_types=(frozendict,))

    @staticmethod
    @functools.lru_cache(maxsize=CACHE_SIZE, typed=True)
    def wheres(api_token: str,
               project_name: str) -> Response:
        """Get all the open, code wheres from a project."""
        logger.debug(f'Query.project('
                     f'project_name={project_name})')
        body: str = """
            query GetWheres($projectName: String!) {
                project(projectName: $projectName) {
                    findings {
                        id
                        vulnerabilities(vulnType: "lines", state: "open") {
                            where
                        }
                    }
                }
            }
            """
        params: dict = {
            'projectName': project_name,
        }
        return request(api_token, body, params,
                       expected_types=(frozendict,))

    @staticmethod
    @functools.lru_cache(maxsize=CACHE_SIZE, typed=True)
    def finding(api_token: str,
                identifier: str,
                with_vulns: bool = False) -> Response:
        """Helper to get a finding."""
        logger.debug(f'Query.finding('
                     f'identifier={identifier}, '
                     f'with_vulns={with_vulns})')
        assert isinstance(identifier, str)
        body: str = """
            query GetFinding($identifier: String!, $withVulns: Boolean!) {
                finding(identifier: $identifier) {
                    attackVectorDesc
                    closedVulnerabilities @include(if: $withVulns)
                    description
                    historicTreatment
                    openVulnerabilities @include(if: $withVulns)
                    projectName
                    recommendation
                    releaseDate
                    severityScore
                    threat
                    title
                    vulnerabilities @include(if: $withVulns) {
                        historicState @include(if: $withVulns)
                        id @include(if: $withVulns)
                        vulnType @include(if: $withVulns)
                        where @include(if: $withVulns)
                    }
                }
            }
            """
        params: dict = {
            'identifier': identifier,
            'withVulns': with_vulns,
        }
        return request(api_token, body, params, expected_types=(frozendict,))

    @staticmethod
    @functools.lru_cache(maxsize=CACHE_SIZE, typed=True)
    def resources(api_token: str,
                  project_name: str) -> Response:
        """Get the project repositories"""
        logger.debug(f'Query.finding('
                     f'project_name={project_name} ')
        body: str = """query GetResources($projectName: String!) {
            resources (projectName: $projectName) {
                repositories
            }
        }"""
        params: dict = {
            'projectName': project_name
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
            mutation UpdateAccessToken ($expirationTime: Int!) {
                updateAccessToken(expirationTime: $expirationTime) {
                    sessionJwt
                    success
                }
            }
            """
        params: dict = {
            'expirationTime': expiration_time,
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
            mutation UploadFile($identifier: String!, $file: Upload!) {
                uploadFile(findingId: $identifier,
                           file: $file,
                           origin: "toolbox") {
                    success
                }
            }
            """
        file_path_handle = open(file_path, 'rb')
        params: dict = {
            'identifier': identifier,
            'file': file_path_handle
        }
        return request(
            api_token, body, params, expected_types=(frozendict,))

    @staticmethod
    def approve_vulns(api_token: str,
                      finding_id: str,
                      uuid: str = '',
                      approval_status: bool = False) -> Response:
        """ApproveVulnMutation."""
        logger.debug(f'Mutations.approve_vulns('
                     f'uuid={uuid}, '
                     f'finding_id={finding_id}, '
                     f'approval_status={approval_status})')
        assert isinstance(uuid, str)
        assert isinstance(finding_id, str)
        body: str = """
            mutation ApproveVulnerability($uuid: String!, $findingId: String!,
                                          $approvalStatus: Boolean!) {
                approveVulnerability(uuid: $uuid,
                                     findingId: $findingId,
                                     approvalStatus: $approvalStatus) {
                    success
                }
            }
            """
        params: dict = {
            'uuid': uuid,
            'findingId': finding_id,
            'approvalStatus': approval_status,
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
