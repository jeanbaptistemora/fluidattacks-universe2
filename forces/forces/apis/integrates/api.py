# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

"""Fluid Forces integrates api module."""

import asyncio
from datetime import (
    datetime,
)
from forces.apis.integrates.client import (
    ApiError,
    execute,
)
from forces.model import (
    VulnerabilityState,
)
from forces.utils.env import (
    guess_environment,
)
from forces.utils.function import (
    shield,
)
from forces.utils.logs import (
    log,
)
from typing import (
    Any,
    AsyncGenerator,
    Callable,
    cast,
    List,
    Set,
    Tuple,
    TypeVar,
)

# Constants
TFun = TypeVar("TFun", bound=Callable[..., Any])
SHIELD: Callable[[TFun], TFun] = shield(
    retries=8 if guess_environment() == "production" else 1,
    sleep_between_retries=5,
)


@SHIELD
async def get_findings(group: str, **kwargs: str) -> Set[str]:
    """
    Returns the findings of a group.

    :param client: gql Client.
    :param group: Group name.
    """
    query = """
        query ForcesDoGetGroupFindings($group_name: String!) {
          group (groupName: $group_name) {
            findings {
              id
              currentState
            }
          }
        }
        """

    result: dict[str, dict[str, List[Any]]] = (
        await execute(
            query=query,
            operation_name="ForcesDoGetGroupFindings",
            variables=dict(group_name=group),
            default={},
            **kwargs,
        )
        or {}
    )

    findings: Set[str] = set(
        finding["id"]
        for finding in (result.get("group", {}) or {}).get("findings", [])
        if finding["currentState"] == "APPROVED"
    )

    return findings


@SHIELD
async def get_vulnerabilities(
    finding_id: str, **kwargs: str
) -> List[dict[str, str | List[dict[str, dict[str, Any]]]]]:
    """
    Returns the vulnerabilities of a finding.

    :param client: gql Client.
    :param finding: Finding identifier.
    """
    vulnerabilities = []
    query = """
        query ForcesDoGetFindingVulnerabilities(
            $after: String
            $finding_id: String!
            $first: Int
        ) {
            finding(identifier: $finding_id) {
                id
                vulnerabilitiesConnection(
                    after: $after,
                    first: $first,
                ) {
                    edges {
                        node {
                            findingId
                            currentState
                            treatment
                            vulnerabilityType
                            where
                            severity
                            specific
                            reportDate
                            rootNickname
                            zeroRisk
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
    response: dict = await execute(
        query=query,
        operation_name="ForcesDoGetFindingVulnerabilities",
        variables=dict(finding_id=finding_id),
        default={},
        **kwargs,
    )
    while True:
        has_next_page = False
        if response:
            vulnerabilities_connection = response["finding"][
                "vulnerabilitiesConnection"
            ]
            vulnerability_page_info = vulnerabilities_connection["pageInfo"]
            vulnerability_edges = vulnerabilities_connection["edges"]
            has_next_page = vulnerability_page_info["hasNextPage"]
            end_cursor = vulnerability_page_info["endCursor"]
            vulnerabilities.extend(
                [vuln_edge["node"] for vuln_edge in vulnerability_edges]
            )

        if not has_next_page:
            break

        response = await execute(
            query=query,
            operation_name="ForcesDoGetFindingVulnerabilities",
            variables=dict(finding_id=finding_id, after=end_cursor),
            default={},
            **kwargs,
        )

    for index, _ in enumerate(vulnerabilities):
        treatment = vulnerabilities[index].get("treatment")
        zero_risk = vulnerabilities[index].get("zeroRisk")
        if treatment and "ACCEPTED" in treatment.upper():
            vulnerabilities[index]["currentState"] = "accepted"
        if zero_risk and zero_risk.upper() in {
            "REQUESTED",
            "CONFIRMED",
        }:
            vulnerabilities[index]["currentState"] = "accepted"

    return vulnerabilities


@SHIELD
async def get_finding(finding: str, **kwargs: str) -> dict[str, Any]:
    """
    Returns a finding.

    :param finding: Finding identifier.
    """
    query = """
        query ForcesDoGetFinding($finding_id: String!) {
          finding(identifier: $finding_id) {
            title
            id
            state
            severity {
              exploitability
            }
            severityScore
          }
        }
        """
    params = {"finding_id": finding}
    response: dict[str, str] = await execute(
        query=query,
        operation_name="ForcesDoGetFinding",
        variables=params,
        default={},
        **kwargs,
    )
    return response.get("finding", {})  # type: ignore


async def vulns_generator(
    group: str, **kwargs: str
) -> AsyncGenerator[dict[str, str | List[dict[str, dict[str, Any]]]], None]:
    """
    Returns a generator with all the vulnerabilities of a group.

    :param `group`: Group Name.
    """
    findings: Set[str] = await get_findings(group, **kwargs)
    vulns_futures = [get_vulnerabilities(fin, **kwargs) for fin in findings]
    for vulnerabilities in asyncio.as_completed(vulns_futures):
        for vuln in await vulnerabilities:
            # Exception: WF(AsyncGenerator is subtype of iterator)
            yield vuln  # NOSONAR


@SHIELD
async def upload_report(
    group: str,
    report: dict[str, Any],
    log_file: str,
    git_metadata: dict[str, str],
    severity_threshold: float,
    **kwargs: datetime | str | int,
) -> bool:
    """
    Upload report execution to Integrates.

    :param group: Subscription name.
    :param execution_id: ID of forces execution.
    :param exit_code: Exit code.
    :param report: Forces execution report.
    :param log: Forces execution log.
    :param strictness: Strictness execution.
    :param severity_threshold: CVSS score threshold for failure in strict mode
    :param grace_period: Period in days where new open vulns are given a free
    pass in strict mode
    :param git_metadata: Repository metadata.
    :param date: Forces execution date.
    """
    # pylint: disable=consider-using-with
    query = """
        mutation ForcesDoUploadReport(
            $group_name: String!
            $execution_id: String!
            $date: DateTime!
            $exit_code: String!
            $git_branch: String
            $git_commit: String
            $git_origin: String
            $git_repo: String
            $kind: String
            $log: Upload
            $strictness: String!
            $grace_period: Int!
            $severity_threshold: Float!
            $open: [ExploitResultInput!]
            $closed: [ExploitResultInput!]
            $accepted: [ExploitResultInput!]
        ) {
            addForcesExecution(
                groupName: $group_name
                executionId: $execution_id
                date: $date
                exitCode: $exit_code
                gitBranch: $git_branch
                gitCommit: $git_commit
                gitOrigin: $git_origin
                gitRepo: $git_repo
                kind: $kind
                log: $log
                strictness: $strictness
                gracePeriod: $grace_period
                severityThreshold: $severity_threshold
                vulnerabilities: {
                    open: $open,
                    accepted: $accepted,
                    closed: $closed,
                }
            ) {
                success
            }
        }
        """
    open_vulns: List[dict[str, str]] = []
    closed_vulns: List[dict[str, str]] = []
    accepted_vulns: List[dict[str, str]] = []
    for vuln in [
        vuln for find in report["findings"] for vuln in find["vulnerabilities"]
    ]:
        vuln_state = {
            "kind": vuln["type"],
            "who": vuln["specific"],
            "where": vuln["where"],
            "state": str(vuln["state"].value).upper(),
            "exploitability": vuln["exploitability"],
        }
        if vuln["state"] == VulnerabilityState.OPEN:
            open_vulns.append(vuln_state)
        elif vuln["state"] == VulnerabilityState.CLOSED:
            closed_vulns.append(vuln_state)
        elif vuln["state"] == VulnerabilityState.ACCEPTED:
            accepted_vulns.append(vuln_state)

    params: dict[str, Any] = {
        "group_name": group,
        "execution_id": kwargs.pop("execution_id"),
        "date": kwargs.pop(
            "date", datetime.utcnow()
        ).isoformat(),  # type: ignore
        "exit_code": str(kwargs.pop("exit_code")),
        "git_branch": git_metadata["git_branch"],
        "git_commit": git_metadata["git_commit"],
        "git_origin": git_metadata["git_origin"],
        "git_repo": git_metadata["git_repo"],
        "open": open_vulns,
        "accepted": accepted_vulns,
        "closed": closed_vulns,
        "log": open(log_file, "rb"),
        "strictness": kwargs.pop("strictness"),
        "grace_period": kwargs.pop("grace_period"),
        "severity_threshold": severity_threshold,
        "kind": kwargs.pop("kind", "all"),
    }

    response: dict[str, dict[str, bool]] = await execute(
        query=query,
        operation_name="ForcesDoUploadReport",
        variables=params,
        default={},
        **kwargs,
    )
    return response.get("addForcesExecution", {}).get("success", False)


@SHIELD
async def get_groups_access(
    **kwargs: Any,
) -> List[Tuple[dict[str, str], float, int]]:
    query = """
        query ForcesGetMeGroups {
          me {
            organizations {
              groups {
                name
                minBreakingSeverity
                vulnerabilityGracePeriod
                userRole
              }
            }
          }
        }
    """
    try:
        response: dict[
            str,
            dict[
                str,
                List[dict[str, List[dict[str, str]] | int | float]],
            ],
        ] = await execute(
            query,
            operation_name="ForcesGetMeGroups",
            **kwargs,
        )
    except ApiError as exc:
        if "Login required" in exc.messages:
            await log(
                "error",
                "The token has expired or the token has no permissions",
            )
            return []
        raise Exception from exc
    return list(
        (
            group,
            cast(float, group["minBreakingSeverity"]),
            cast(int, group["vulnerabilityGracePeriod"]),
        )
        for organization in response["me"]["organizations"]
        for group in cast(List[dict[str, str]], organization["groups"])
    )


async def get_git_remotes(group: str, **kwargs: Any) -> List[dict[str, str]]:
    query = """
        query ForcesGetGitRoots($group: String!) {
          group(groupName: $group){
            roots {
              ...on GitRoot{
                url
                state
                nickname
              }
            }
          }
        }
    """
    response: dict[str, dict[str, List[dict[str, str]]]] = await execute(
        query,
        operation_name="ForcesGetGitRoots",
        variables={"group": group},
        **kwargs,
    )

    return response["group"]["roots"]


async def get_forces_user_and_org_data(
    **kwargs: Any,
) -> Tuple[str | None, float | None, int | None]:
    groups = await get_groups_access(**kwargs)
    for group, global_brk_severity, vuln_grace_period in groups:
        if group["userRole"] == "service_forces":
            return (group["name"], global_brk_severity, vuln_grace_period)
    return (None, None, None)
