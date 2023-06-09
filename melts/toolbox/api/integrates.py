import aiogqlc
import aiogqlc.utils
import aiohttp
import aiohttp.client_exceptions
import asyncio
import contextlib
from frozendict import (
    frozendict,
)
import functools
import json
import os
import time
from toolbox.api.limits import (
    DEFAULT as DEFAULT_RATE_LIMIT,
)
from toolbox.logger import (
    LOGGER,
)
from toolbox.utils.function import (
    rate_limited,
)
from typing import (
    Any,
    Dict,
    List,
    NamedTuple,
    Optional,
    Tuple,
    Union,
)

# Containers
Response = NamedTuple(
    "Response",
    [
        ("ok", bool),
        ("status_code", int),
        ("data", Any),
        ("errors", Tuple[Any, ...]),
    ],
)

# Debugging
DEBUGGING: bool = False

# Constants
INTEGRATES_API_URL = "https://app.fluidattacks.com/api"
CACHE_SIZE: int = 4**8
RETRY_MAX_ATTEMPTS: int = 3 if DEBUGGING else 12
RETRY_RELAX_SECONDS: float = 3.0
PROXY = "http://127.0.0.1:8080" if DEBUGGING else None


def _format_vulnerability(node: Dict[str, str]) -> Dict[str, str]:
    formatted_node: Dict[str, str] = {**node}
    if "state" in node:
        formatted_node["currentState"] = (
            {
                "SAFE": "closed",
                "VULNERABLE": "open",
            }
            .get(
                str(node["state"]),
                str(node["state"]),
            )
            .lower()
        )

    if "treatmentStatus" in node:
        formatted_node["treatment"] = (
            {
                "UNTREATED": "NEW",
            }
            .get(
                str(node["treatmentStatus"]),
                str(node["treatmentStatus"]),
            )
            .upper()
        )

    return formatted_node


def get_paginated_fields(
    api_token: str,
    paginated_field: str,
    parent_field: str,
    params: Dict[str, Union[str, bool]],
    query: str,
) -> List[Dict[str, str]]:
    """
    Returns all instances of a paginated field in a query as long as the
    paginated field is a direct child of the parent field

    :param ``api_token``: Integrates API token
    :param ``paginated_field``: Name of the field to be retrieved
    :param ``parent_field``: Name of the parent field
    :param ``params``: Query parameters
    :param ``query``: Base query
    """
    result: List[Dict[str, str]] = []
    response: Response = request(
        api_token=api_token,
        body=query,
        params=params,
    )
    while True:
        has_next_page = False
        if response.data:
            field_connection = response.data[parent_field][paginated_field]
            field_page_info = field_connection["pageInfo"]
            field_edges = field_connection["edges"]
            has_next_page = field_page_info["hasNextPage"]
            end_cursor = field_page_info["endCursor"]
            result.extend(
                [
                    _format_vulnerability(vuln_edge["node"])
                    for vuln_edge in field_edges
                ]
            )

        if not has_next_page:
            break

        response = request(
            api_token=api_token,
            body=query,
            params=dict(after=end_cursor, **params),
        )

    return result


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
        connector = aiohttp.TCPConnector()
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
                headers[aiohttp.hdrs.CONTENT_TYPE] = "application/json"
                data = json.dumps(
                    self.prepare_json_data(query, variables, operation)
                )

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
    headers = {"Authorization": f"Bearer {api_token}"}
    client = CustomGraphQLClient(INTEGRATES_API_URL, headers=headers)
    executor = rate_limited(rpm=DEFAULT_RATE_LIMIT)(client.execute)
    response = await executor(payload, variables=variables, **kwargs)
    content = await response.json()
    data: Any = content.get("data")
    errors: Any = content.get("errors")

    # Guarantee data immutability
    if isinstance(data, dict):
        LOGGER.debug("response data is a dict")
        data = frozendict(data)
    elif isinstance(data, list):
        LOGGER.debug("response data is a non-empty tuple")
        data = tuple(data)
    else:
        LOGGER.debug("response data is an empty tuple")
        data = tuple()

    # Guarantee errors immutability
    if errors:
        LOGGER.debug("response errors is a non-empty tuple")
        errors = tuple(errors)
    else:
        LOGGER.debug("response errors is an empty tuple")
        errors = tuple()

    return Response(
        ok=200 <= response.status < 400 and not errors,
        status_code=response.status,
        data=data,
        errors=errors,
    )


def request(
    api_token: str,
    body: str,
    params: Optional[Dict[str, Any]] = None,
    expected_types: tuple = (frozendict,),
    **kwargs: Any,
) -> Response:
    """Make a generic query to a GraphQL instance."""
    assert isinstance(body, str)
    if params is not None:
        assert isinstance(params, dict)

    for _ in range(RETRY_MAX_ATTEMPTS):
        with contextlib.suppress(*CustomGraphQLClient.errors_to_retry):
            if params and "fileHandle" in params:
                if params["fileHandle"].closed:
                    # Reopen it again
                    params[
                        "fileHandle"
                    ] = open(  # pylint: disable=consider-using-with
                        params["fileHandle"].name,
                        params["fileHandle"].mode,
                        encoding="utf8",
                    )
                else:
                    # Reset the file pointer to BOF
                    params["fileHandle"].seek(0)

            awaitable = gql_request(api_token, body, params, **kwargs)
            response = asyncio.run(awaitable, debug=DEBUGGING)

            if response.errors or isinstance(response.data, expected_types):
                # It's ok, return
                LOGGER.debug("response: %s", response)
                return response

        time.sleep(RETRY_RELAX_SECONDS)

    return Response(
        ok=False,
        status_code=0,
        data=None,
        errors=("Unable to get data, even after retrying",),
    )


class Queries:
    """Namespace for Integrates's GraphQL Queries."""

    @staticmethod
    @functools.lru_cache(maxsize=CACHE_SIZE, typed=True)
    def me(api_token: str) -> Response:  # pylint: disable=invalid-name
        """Get an API token from your session token."""
        LOGGER.debug("Query.me()")
        body: str = """
            query MeltsGetMe {
                me {
                    accessToken
                    role
                }
            }
            """
        return request(api_token, body, operation="MeltsGetMe")

    @staticmethod
    @functools.lru_cache(maxsize=CACHE_SIZE, typed=True)
    def group(
        api_token: str,
        group_name: str,
        with_drafts: bool = False,
        with_findings: bool = False,
    ) -> Response:
        """Get a group."""
        LOGGER.debug(
            "Query.group(group_name=%s, with_drafts=%s, with_findings=%s)",
            group_name,
            with_drafts,
            with_findings,
        )
        body: str = """
            query MeltsGetGroup($groupName: String!, $withDrafts: Boolean!,
                             $withFindings: Boolean!) {
                group(groupName: $groupName) {
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
            "groupName": group_name,
            "withDrafts": with_drafts,
            "withFindings": with_findings,
        }
        return request(api_token, body, params, operation="MeltsGetGroup")

    @staticmethod
    @functools.lru_cache(maxsize=CACHE_SIZE, typed=True)
    def finding(
        api_token: str, identifier: str, with_vulns: bool = False
    ) -> Response:
        """Helper to get a finding."""
        LOGGER.debug(
            "Query.finding(identifier=%s, with_vulns=%s)",
            identifier,
            with_vulns,
        )
        assert isinstance(identifier, str)
        body: str = """
            query MeltsGetFinding($identifier: String!, $withVulns: Boolean!) {
                finding(identifier: $identifier) {
                    attackVectorDescription
                    closedVulnerabilities @include(if: $withVulns)
                    description
                    openVulnerabilities @include(if: $withVulns)
                    groupName
                    recommendation
                    releaseDate
                    severityScore
                    threat
                    title
                }
            }
            """

        vulns_query: str = """
            query MeltsGetVulnerabilities(
                    $identifier: String!, $withVulns: Boolean!
                ) {
                finding(identifier: $identifier) {
                    id
                    vulnerabilitiesConnection @include(if: $withVulns) {
                        edges {
                            node {
                                lastStateDate
                                state
                                hacker
                                source
                                lastTreatmentDate
                                treatmentStatus
                                treatmentUser
                                id
                                vulnerabilityType
                                where
                                specific
                            }
                        }
                        pageInfo {
                            hasNextPage
                            endCursor
                        }
                    }
                }
            }
        """

        params: dict = {
            "identifier": identifier,
            "withVulns": with_vulns,
        }
        response: Response = request(
            api_token, body, params, operation="MeltsGetFinding"
        )

        # Filling vulnerability info
        if with_vulns:
            response.data["finding"]["vulnerabilities"] = get_paginated_fields(
                api_token=api_token,
                paginated_field="vulnerabilitiesConnection",
                parent_field="finding",
                params=params,
                query=vulns_query,
            )

        return response

    @staticmethod
    @functools.lru_cache(maxsize=CACHE_SIZE, typed=True)
    def resources(api_token: str, group_name: str) -> Response:
        """Get the group repositories"""
        LOGGER.debug("Query.finding(group_name=%s", group_name)
        body: str = """
        query MeltsGetResources($groupName: String!) {
            resources (groupName: $groupName) {
                repositories
            }
        }
        """
        params: dict = {"groupName": group_name}
        return request(api_token, body, params, operation="MeltsGetResources")

    @staticmethod
    @functools.lru_cache(maxsize=CACHE_SIZE, typed=True)
    def git_roots(api_token: str, group_name: str) -> Response:
        """Get group git roots"""
        query = """
            query MeltsGetGitRoots($groupName: String!) {
              group(groupName: $groupName){
                roots {
                  ...on GitRoot{
                    id
                    branch
                    lastCloningStatusUpdate
                    nickname
                    url
                    state
                    cloningStatus {
                        commit
                    }
                    __typename
                  }
                }
              }
            }
        """
        params: dict = {"groupName": group_name}
        return request(api_token, query, params, operation="MeltsGetGitRoots")

    @staticmethod
    @functools.lru_cache(maxsize=CACHE_SIZE, typed=True)
    def git_root(api_token: str, group_name: str, root_id: str) -> Response:
        """Get group git root"""
        query = """
            query MeltsGetGitRoot($groupName: String!, $rootId: ID!) {
              root(groupName: $groupName, rootId: $rootId) {
                ... on GitRoot {
                  id
                  branch
                  lastCloningStatusUpdate
                  nickname
                  url
                  state
                  downloadUrl
                  uploadUrl
                  cloningStatus {
                    commit
                  }
                }
              }
            }
        """
        params: dict = {"groupName": group_name, "rootId": root_id}
        return request(api_token, query, params, operation="MeltsGetGitRoot")

    @staticmethod
    @functools.lru_cache(maxsize=CACHE_SIZE, typed=True)
    def git_download_url(
        api_token: str, group_name: str, root_id: str
    ) -> Response:
        """Get group git root download url"""
        query = """
            query MeltsGetGitRootDownloadUrl($groupName: String!, $rootId: ID!)
            {
              root(groupName: $groupName, rootId: $rootId) {
                ... on GitRoot {
                  id
                  nickname
                  downloadUrl
                }
              }
            }
        """
        params: dict = {"groupName": group_name, "rootId": root_id}
        return request(
            api_token, query, params, operation="MeltsGetGitRootDownloadUrl"
        )

    @staticmethod
    @functools.lru_cache(maxsize=CACHE_SIZE, typed=True)
    def git_credentials(
        api_token: str, group_name: str, root_id: str
    ) -> Response:
        """Get group git root download url"""
        query = """
            query MeltsGetGitRootCredentials($groupName: String!, $rootId: ID!)
            {
              root(groupName: $groupName, rootId: $rootId) {
                ... on GitRoot {
                  id
                  nickname
                  credentials {
                    user
                    password
                    key
                    token
                    type
                  }
                }
              }
            }
        """
        params: dict = {"groupName": group_name, "rootId": root_id}
        return request(
            api_token, query, params, operation="MeltsGetGitRootCredentials"
        )

    @staticmethod
    @functools.lru_cache(maxsize=CACHE_SIZE, typed=True)
    def git_upload_url(
        api_token: str, group_name: str, root_id: str
    ) -> Response:
        """Get group git root download url"""
        query = """
            query MeltsGetGitRootUploadUrl($groupName: String!, $rootId: ID!) {
              root(groupName: $groupName, rootId: $rootId) {
                ... on GitRoot {
                  id
                  nickname
                  uploadUrl
                }
              }
            }
        """
        params: dict = {"groupName": group_name, "rootId": root_id}
        return request(
            api_token, query, params, operation="MeltsGetGitRootUploadUrl"
        )

    @staticmethod
    @functools.lru_cache(maxsize=CACHE_SIZE, typed=True)
    def git_roots_filter(api_token: str, group_name: str) -> Response:
        """Get group git roots"""
        query = """
            query MeltsGetGitRootsFilter($groupName: String!) {
              group(groupName: $groupName){
                roots {
                  ...on GitRoot{
                    id
                    nickname
                    url
                    gitignore
                    state
                  }
                }
              }
            }
        """
        params: dict = {"groupName": group_name}
        return request(
            api_token,
            query,
            params,
            operation="MeltsGetGitRootsFilter",
        )

    @staticmethod
    def get_group_info(api_token: str, group_name: str) -> Response:
        query = """
            query MeltsGetGroupLanguage($groupName: String!) {
              group(groupName: $groupName){
                hasForces
                language
                hasSquad
              }
            }
        """
        params: dict = {"groupName": group_name}
        return request(
            api_token,
            query,
            params,
            operation="MeltsGetGroupLanguage",
        )

    @staticmethod
    def get_group_permissions(api_token: str, group_name: str) -> Response:
        query = """
            query MeltsGetGroupPermissions($groupName: String!) {
              group(groupName: $groupName){
                permissions
              }
            }
        """
        params: dict = {"groupName": group_name}
        return request(
            api_token,
            query,
            params,
            operation="MeltsGetGroupPermissions",
        )

    @staticmethod
    def get_groups_with_forces(api_token: str) -> Response:
        query = """
            query MeltsListGroupsWithForces{
              groupsWithForces
            }
        """
        return request(
            api_token,
            query,
            operation="MeltsListGroupsWithForces",
        )

    @staticmethod
    def get_forces_token(api_token: str, group_name: str) -> Response:
        query = """
            query MeltsGetForcesToken($groupName: String!) {
              group(groupName: $groupName){
                forcesToken
              }
            }
        """
        params: dict = {"groupName": group_name}
        return request(
            api_token,
            query,
            params,
            operation="MeltsGetForcesToken",
        )


class Mutations:
    """Namespace for Integrates's GraphQL Mutations."""

    @staticmethod
    def refresh_toe_lines(
        api_token: str,
        group_name: str,
    ) -> Response:
        query = """
            mutation MeltsRefreshToeLines(
                $groupName: String!
            ) {
              refreshToeLines(
                groupName: $groupName
              ) {
                success
              }
            }
        """
        params = {
            "groupName": group_name,
        }
        return request(
            api_token,
            query,
            params,
            operation="MeltsRefreshToeLines",
        )

    @staticmethod
    def update_evidence(
        api_token: str,
        finding_id: str,
        evidence_id: str,
        file_path: str,
    ) -> Response:
        """UpdateEvidence."""
        LOGGER.debug(
            "Mutations.update_evidence(finding_id=%s, "
            "evidence_id=%s, file_path=%s, )",
            finding_id,
            evidence_id,
            file_path,
        )
        assert isinstance(finding_id, str)
        assert isinstance(evidence_id, str) and evidence_id in ("EXPLOIT",)
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

        with open(file_path, "rb") as file_handle:
            params: dict = {
                "findingId": finding_id,
                "evidenceId": evidence_id,
                "fileHandle": file_handle,
            }

            return request(
                api_token, body, params, operation="MeltsUpdateEvidence"
            )

    @staticmethod
    def upload_file(
        api_token: str, identifier: str, file_path: str
    ) -> Response:
        """UploadFile."""
        LOGGER.debug(
            "Mutations.upload_file(identifier=%s, file_path=%s)",
            identifier,
            file_path,
        )
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

        with open(file_path, "rb") as file_handle:
            params: dict = {
                "identifier": identifier,
                "fileHandle": file_handle,
            }

            return request(
                api_token, body, params, operation="MeltsUploadFile"
            )

    @staticmethod
    def update_cloning_status(  # pylint: disable=too-many-arguments
        api_token: str,
        group_name: str,
        root_id: str,
        status: str,
        message: str,
        commit: Optional[str] = None,
    ) -> Response:
        query = """
            mutation MeltsUpdateRootCloningStatus(
                $groupName: String!
                $rootId: ID!
                $status: CloningStatus!
                $message: String!
                $commit: String
            ) {
              updateRootCloningStatus(
                groupName: $groupName
                id: $rootId
                status: $status
                message: $message
                commit: $commit
              ) {
                success
              }
            }
        """
        params = {
            "groupName": group_name,
            "rootId": root_id,
            "status": status,
            "message": message,
            "commit": commit,
        }
        return request(
            api_token,
            query,
            params,
            operation="MeltsUpdateRootCloningStatus",
        )


# Metadata
__all__: List[str] = ["request", "request", "Queries", "Mutations"]


def clear_cache() -> None:
    Queries.me.cache_clear()
    Queries.group.cache_clear()
    Queries.finding.cache_clear()
    Queries.resources.cache_clear()
