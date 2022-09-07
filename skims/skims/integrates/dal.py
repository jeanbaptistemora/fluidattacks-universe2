# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aiogqlc import (
    GraphQLClient,
)
import aiohttp
from aiohttp.client_reqrep import (
    ClientResponse,
)
import asyncio
from contextlib import (
    suppress,
)
from integrates.graphql import (
    client as graphql_client,
)
from model import (
    core_model,
)
from typing import (
    Any,
    Callable,
    Dict,
    List,
    NamedTuple,
    Optional,
    Tuple,
    TypeVar,
    Union,
)
from utils.function import (
    SkimsCanNotOperate,
    StopRetrying,
)
from utils.logs import (
    log,
    log_to_remote,
)

# Constants
TFun = TypeVar("TFun", bound=Callable[..., Any])


class ErrorMapping(NamedTuple):
    exception: Exception
    messages: Tuple[str, ...]


async def raise_errors(
    errors: Optional[Tuple[Dict[str, Any], ...]],
    error_mappings: Tuple[ErrorMapping, ...],
    query: str,
    variables: Dict[str, Any],
) -> None:
    for error in errors or ():
        for error_mapping in error_mappings:
            if error.get("message") in error_mapping.messages:
                raise error_mapping.exception

    if errors:
        for error in errors:
            await log("debug", "query: %s", query)
            await log("debug", "variables: %s", variables)
            await log("error", "%s", error)
    else:
        # no errors happened
        pass


async def _request(
    *,
    query: str,
    operation: str,
    variables: Dict[str, Any],
    client: Optional[GraphQLClient] = None,
) -> ClientResponse:
    if client and not client.session.closed:
        response: aiohttp.ClientResponse = await client.execute(
            query=query,
            operation=operation,
            variables=variables,
        )
    else:
        async with graphql_client() as client:
            response = await client.execute(
                query=query,
                operation=operation,
                variables=variables,
            )
    return response


# @rate_limited(rpm=DEFAULT_RATE_LIMIT)
async def _execute(
    *,
    query: str,
    operation: str,
    variables: Dict[str, Any],
    client: Optional[GraphQLClient] = None,
) -> Dict[str, Any]:
    retries: int = 0
    while True:
        response = await _request(
            query=query,
            operation=operation,
            variables=variables,
            client=client,
        )

        if response.status >= 500:
            retries += 1
            if retries == 3:
                break
            await asyncio.sleep(retries)

        if response.status == 429 and (
            seconds := response.headers.get("retry-after")
        ):
            await asyncio.sleep(int(seconds) + 1)
        else:
            break

    if response.status >= 400:
        await log("debug", "query: %s", query)
        await log("debug", "variables: %s", variables)
        await log("debug", "response status: %s", response.status)
        await log_to_remote(
            msg=aiohttp.ClientResponseError,
            severity="error",
            query=query,
            variables=f"{variables}",
            response_status=response.status,
            response=response.content,
        )
        raise aiohttp.ClientResponseError(
            response.request_info,
            (response,),
            status=response.status,
            headers=response.headers,
            message=f"query: {query}\nvariables: {variables}",
        )

    result: Dict[str, Any] = (await response.json()) or {}

    await raise_errors(
        errors=result.get("errors"),
        error_mappings=(
            ErrorMapping(
                exception=StopRetrying("Invalid API token"),
                messages=("Login required",),
            ),
            ErrorMapping(
                exception=SkimsCanNotOperate(),
                messages=("Exception - Machine cannot operate at this time",),
            ),
        ),
        query=query,
        variables=variables,
    )

    return result


async def get_group_language(
    group: str,
    client: Optional[GraphQLClient] = None,
) -> Optional[core_model.LocalesEnum]:
    result = await _execute(
        query="""
            query SkimsGetGroupLanguage($group: String!) {
                group(groupName: $group) {
                    language
                }
            }
        """,
        operation="SkimsGetGroupLanguage",
        variables=dict(group=group),
        client=client,
    )

    with suppress(AttributeError, KeyError, TypeError):
        return core_model.LocalesEnum(result["data"]["group"]["language"])

    return None


class ResultGetGroupRoots(NamedTuple):
    id: str
    environment_urls: List[str]
    git_environment_urls: List[Dict[str, List[Dict[str, str]]]]
    nickname: str
    gitignore: List[str]
    download_url: Optional[str] = None


async def get_group_roots(
    *,
    group: str,
    client: Optional[GraphQLClient] = None,
) -> Tuple[ResultGetGroupRoots, ...]:
    result = await _execute(
        query="""
            query SkimsGetGroupRoots(
                $group: String!
            ) {
                group(groupName: $group) {
                    roots {
                        ... on GitRoot {
                            environmentUrls
                            gitEnvironmentUrls {
                              url
                              id
                              secrets {
                                value
                                key
                              }
                              urlType
                            }
                            nickname
                            url
                            id
                            gitignore
                        }
                    }
                }
            }
        """,
        operation="SkimsGetGroupRoots",
        variables=dict(
            group=group,
        ),
        client=client,
    )

    try:
        return tuple(
            ResultGetGroupRoots(
                environment_urls=root["environmentUrls"],
                nickname=root["nickname"],
                gitignore=root["gitignore"],
                id=root["id"],
                git_environment_urls=root["gitEnvironmentUrls"],
            )
            for root in result["data"]["group"]["roots"]
        )
    except (AttributeError, KeyError, TypeError):
        return tuple()


async def get_group_root_download_url(
    *,
    group: str,
    root_id: str,
    client: Optional[GraphQLClient] = None,
) -> Tuple[str, Optional[str]]:
    result = await _execute(
        query="""
            query SkimsGetGroupRootDownloadUrl(
                $groupName: String!, $rootId: ID!
            ) {
              root(groupName: $groupName, rootId: $rootId) {
                ... on GitRoot {
                  downloadUrl
                }
              }
            }
        """,
        operation="SkimsGetGroupRootDownloadUrl",
        variables={"groupName": group, "rootId": root_id},
        client=client,
    )

    try:
        return (root_id, result["data"]["root"]["downloadUrl"])

    except (AttributeError, KeyError, TypeError):
        return (root_id, None)


async def do_start_execution(
    *,
    root: str,
    group_name: str,
    job_id: str,
    start_date: str,
    commit_hash: str,
    client: Optional[GraphQLClient] = None,
) -> bool:
    result = await _execute(
        query="""
            mutation SkimsDoStartMachineExecution(
                $root: String!
                $group_name: String!
                $job_id: ID!
                $start_date: DateTime!
                $commit_hash: String!
            ) {
                startMachineExecution(
                    rootNickname: $root,
                    groupName: $group_name,
                    jobId: $job_id,
                    startedAt: $start_date,
                    gitCommit: $commit_hash
                ) {
                    success
                }
            }
        """,
        operation="SkimsDoStartMachineExecution",
        variables=dict(
            root=root,
            group_name=group_name,
            job_id=job_id,
            start_date=start_date,
            commit_hash=commit_hash,
        ),
        client=client,
    )

    with suppress(AttributeError, KeyError, TypeError):
        return result["data"]["addMachineExecution"]["success"]

    return False


async def do_finish_execution(
    *,
    root: str,
    group_name: str,
    job_id: str,
    end_date: str,
    findings_executed: Tuple[Dict[str, Union[int, str]], ...],
    client: Optional[GraphQLClient] = None,
) -> bool:
    result = await _execute(
        query="""
            mutation SkimsDoFinishMachineExecution(
                $root: String!
                $group_name: String!
                $job_id: ID!
                $end_date: DateTime!
                $findings_executed: [MachineFindingResultInput]
            ) {
                finishMachineExecution(
                    rootNickname: $root,
                    groupName: $group_name,
                    jobId: $job_id,
                    stoppedAt: $end_date,
                    findingsExecuted: $findings_executed
                ) {
                    success
                }
            }
        """,
        operation="SkimsDoFinishMachineExecution",
        variables=dict(
            root=root,
            group_name=group_name,
            job_id=job_id,
            end_date=end_date,
            findings_executed=findings_executed,
        ),
        client=client,
    )

    with suppress(AttributeError, KeyError, TypeError):
        return result["data"]["addMachineExecution"]["success"]

    return False
