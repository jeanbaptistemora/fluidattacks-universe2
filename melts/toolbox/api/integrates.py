# Standard library
import asyncio
import contextlib
import os
import time
import json
import functools
from typing import (
    Any,
    Dict,
    List,
    NamedTuple,
    Optional,
    Tuple,
)

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
INTEGRATES_API_URL = 'https://integrates.fluidattacks.com/api'
CACHE_SIZE: int = 4**8
RETRY_MAX_ATTEMPTS: int = 3 if DEBUGGING else 12
RETRY_RELAX_SECONDS: float = 3.0
PROXY = 'http://127.0.0.1:8080' if DEBUGGING else None


class CustomGraphQLClient(aiogqlc.GraphQLClient):
    errors_to_retry: tuple = (
        asyncio.TimeoutError,
        aiohttp.client_exceptions.ClientError,
        ValueError,
    )

    async def execute(
        self,
        query: str,
        variables: Optional[Dict[str, Any]] = None,
        operation: Optional[str] = None,
    ) -> aiohttp.ClientResponse:
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
                proxy=PROXY,
            ) as response:
                await response.read()
                return response


async def gql_request(
    api_token: str,
    payload: str,
    variables: Optional[Dict[str, Any]],
    **kwargs: Any,
) -> Response:
    """Async GraphQL request."""
    headers = {
        'Authorization': f'Bearer {api_token}'
    }
    client = CustomGraphQLClient(INTEGRATES_API_URL, headers=headers)
    response = await client.execute(payload, variables=variables, **kwargs)
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
            params: Optional[Dict[str, Any]] = None,
            expected_types: tuple = (frozendict,),
            **kwargs: Any) -> Response:
    """Make a generic query to a GraphQL instance."""
    assert isinstance(body, str)
    if params is not None:
        assert isinstance(params, dict)

    for _ in range(RETRY_MAX_ATTEMPTS):
        with contextlib.suppress(*CustomGraphQLClient.errors_to_retry):
            if params and 'fileHandle' in params:
                if params['fileHandle'].closed:
                    # Reopen it again
                    params['fileHandle'] = open(
                        params['fileHandle'].name,
                        params['fileHandle'].mode)
                else:
                    # Reset the file pointer to BOF
                    params['fileHandle'].seek(0)

            awaitable = gql_request(api_token, body, params, **kwargs)
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
            query MeltsGetMe {
                me {
                    accessToken
                    role (entity: USER)
                    projects {
                        name
                    }
                }
            }
            """
        return request(api_token, body, operation='MeltsGetMe')

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
            query MeltsGetProject($projectName: String!, $withDrafts: Boolean!,
                             $withFindings: Boolean!) {
                project(projectName: $projectName) {
                    drafts @include(if: $withDrafts) {
                        id @include(if: $withDrafts)
                        title @include(if: $withDrafts)
                    }
                    findings @include(if: $withFindings) {
                        id @include(if: $withFindings)
                        title @include(if: $withFindings)
                    }
                }
            }
            """
        params: dict = {
            'projectName': project_name,
            'withDrafts': with_drafts,
            'withFindings': with_findings,
        }
        return request(api_token, body, params, operation='MeltsGetProject')

    @staticmethod
    @functools.lru_cache(maxsize=CACHE_SIZE, typed=True)
    def wheres(api_token: str,
               project_name: str) -> Response:
        """Get all the open, code wheres from a project."""
        logger.debug(f'Query.project('
                     f'project_name={project_name})')
        body: str = """
            query MeltsGetWheres($projectName: String!) {
                project(projectName: $projectName) {
                    findings {
                        id
                        vulnerabilities(state: "open") {
                            vulnType
                            where
                        }
                    }
                }
            }
            """
        params: dict = {
            'projectName': project_name,
        }
        return request(api_token, body, params, operation='MeltsGetWheres')

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
            query MeltsGetFinding($identifier: String!, $withVulns: Boolean!) {
                finding(identifier: $identifier) {
                    attackVectorDesc
                    closedVulnerabilities @include(if: $withVulns)
                    description
                    openVulnerabilities @include(if: $withVulns)
                    projectName
                    recommendation
                    releaseDate
                    severityScore
                    threat
                    title
                    vulnerabilities @include(if: $withVulns) {
                        historicState @include(if: $withVulns)
                        historicTreatment {
                            date
                            treatment
                            user
                        }
                        id @include(if: $withVulns)
                        vulnType @include(if: $withVulns)
                        where @include(if: $withVulns)
                        specific @include(if: $withVulns)
                    }
                }
            }
            """
        params: dict = {
            'identifier': identifier,
            'withVulns': with_vulns,
        }
        return request(api_token, body, params, operation='MeltsGetFinding')

    @staticmethod
    @functools.lru_cache(maxsize=CACHE_SIZE, typed=True)
    def resources(api_token: str,
                  project_name: str) -> Response:
        """Get the project repositories"""
        logger.debug(f'Query.finding('
                     f'project_name={project_name} ')
        body: str = """
        query MeltsGetResources($projectName: String!) {
            resources (projectName: $projectName) {
                repositories
            }
        }
        """
        params: dict = {
            'projectName': project_name
        }
        return request(api_token, body, params, operation='MeltsGetResources')

    @staticmethod
    @functools.lru_cache(maxsize=CACHE_SIZE, typed=True)
    def git_roots(api_token: str, project_name: str) -> Response:
        """Get project git roots"""
        query = """
            query MeltsGetGitRoots($projectName: String!) {
              project(projectName: $projectName){
                roots {
                  ...on GitRoot{
                    id
                    branch
                    url
                    state
                  }
                }
              }
            }
        """
        params: dict = {
            'projectName': project_name
        }
        return request(api_token, query, params, operation='MeltsGetGitRoots')

    @staticmethod
    @functools.lru_cache(maxsize=CACHE_SIZE, typed=True)
    def git_roots_filter(api_token: str, project_name: str) -> Response:
        """Get project git roots"""
        query = """
            query MeltsGetGitRootsFilter($projectName: String!) {
              project(projectName: $projectName){
                roots {
                  ...on GitRoot{
                    id
                    url
                    filter{
                      include
                      exclude
                    }
                  }
                }
              }
            }
        """
        params: dict = {
            'projectName': project_name
        }
        return request(
            api_token,
            query,
            params,
            operation='MeltsGetGitRootsFilter',
        )

    @staticmethod
    @functools.lru_cache(maxsize=CACHE_SIZE, typed=True)
    def get_group_info(api_token: str, project_name: str) -> Response:
        query = """
            query MeltsGetGroupLanguage($projectName: String!) {
              project(projectName: $projectName){
                hasForces
                language
                hasDrills
              }
            }
        """
        params: dict = {
            'projectName': project_name
        }
        return request(
            api_token,
            query,
            params,
            operation='MeltsGetGroupLanguage',
        )


class Mutations:
    """Namespace for Integrates's GraphQL Mutations."""

    @staticmethod
    def update_evidence(
        api_token: str,
        finding_id: str,
        evidence_id: str,
        file_path: str,
    ) -> Response:
        """UpdateEvidence."""
        logger.debug(f'Mutations.update_evidence('
                     f'finding_id={finding_id}, '
                     f'evidence_id={evidence_id}, '
                     f'file_path={file_path}, '
                     f')')
        assert isinstance(finding_id, str)
        assert isinstance(evidence_id, str) and evidence_id in (
            'EXPLOIT',
        )
        assert isinstance(file_path, str) and os.path.exists(file_path)
        body: str = """
            mutation MeltsUpdateEvidence(
                $evidenceId: EvidenceType!,
                $fileHandle: Upload!,
                $findingId: String!,
            ) {
                updateEvidence(
                    evidenceId: $evidenceId,
                    file: $fileHandle,
                    findingId: $findingId,
                ) {
                    success
                }
            }
            """

        with open(file_path, 'rb') as file_handle:
            params: dict = {
                'findingId': finding_id,
                'evidenceId': evidence_id,
                'fileHandle': file_handle,
            }

            return request(api_token,
                           body,
                           params,
                           operation='MeltsUpdateEvidence')

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
            mutation MeltsUploadFile(
                $identifier: String!,
                $fileHandle: Upload!)
            {
                uploadFile(findingId: $identifier,
                           file: $fileHandle) {
                    success
                }
            }
            """

        with open(file_path, 'rb') as file_handle:
            params: dict = {
                'identifier': identifier,
                'fileHandle': file_handle,
            }

            return request(api_token,
                           body,
                           params,
                           operation='MeltsUploadFile')

    @staticmethod
    def update_cloning_status(
        api_token: str,
        root_id: str,
        status: str,
        message: str,
    ) -> Response:
        query = """
            mutation MeltsUpdateRootCloningStatus(
                $rootId: ID!
                $status: CloningStatus!
                $message: String!
            ) {
              updateRootCloningStatus(
                id: $rootId
                status: $status
                message: $message
              ) {
                success
              }
            }
        """
        params = {
            'rootId': root_id,
            'status': status,
            'message': message,
        }
        return request(
            api_token,
            query,
            params,
            operation='MeltsUpdateRootCloningStatus',
        )


# Metadata
__all__: List[str] = [
    'request',
    'request',
    'Queries',
    'Mutations'
]


def clear_cache() -> None:
    Queries.me.cache_clear()
    Queries.project.cache_clear()
    Queries.finding.cache_clear()
    Queries.resources.cache_clear()
    Queries.wheres.cache_clear()
