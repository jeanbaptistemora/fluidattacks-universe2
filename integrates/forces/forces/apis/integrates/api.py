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
    ForcesConfig,
    ForcesData,
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
    TypeVar,
)

# Constants
# pylint: disable=invalid-name
TFun = TypeVar("TFun", bound=Callable[..., Any])
SHIELD: Callable[[TFun], TFun] = shield(
    retries=8 if guess_environment() == "production" else 1,
    sleep_between_retries=5,
)


@SHIELD
async def get_findings(group: str, **kwargs: str) -> set[str]:
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

    result: dict[str, dict[str, list[Any]]] = (
        await execute(
            query=query,
            operation_name="ForcesDoGetGroupFindings",
            variables=dict(group_name=group),
            default={},
            **kwargs,
        )
        or {}
    )

    findings: set[str] = set(
        finding["id"]
        for finding in (result.get("group", {}) or {}).get("findings", [])
        if finding["currentState"] == "APPROVED"
    )

    return findings


@SHIELD
async def get_vulnerabilities(
    finding_id: str, **kwargs: str
) -> list[dict[str, str | list[dict[str, dict[str, Any]]]]]:
    """
    Returns the vulnerabilities of a finding.

    :param `finding_id`: Finding identifier.
    """
    vulnerabilities: list[dict[str, Any]] = []
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
                            state
                            treatmentStatus
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
        treatment = vulnerabilities[index].get("treatmentStatus")
        zero_risk = vulnerabilities[index].get("zeroRisk")
        if treatment and "ACCEPTED" in str(treatment):
            vulnerabilities[index]["state"] = "ACCEPTED"
        if zero_risk and str(zero_risk).upper() in {
            "REQUESTED",
            "CONFIRMED",
        }:
            vulnerabilities[index]["state"] = "ACCEPTED"

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
            status
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
    group_name: str, **kwargs: str
) -> AsyncGenerator[dict[str, str | list[dict[str, dict[str, Any]]]], None]:
    """
    Returns a generator with all the vulnerabilities of a group.

    :param `group`: Group Name.
    """
    findings: set[str] = await get_findings(group_name, **kwargs)
    vulns_futures = [get_vulnerabilities(fin, **kwargs) for fin in findings]
    for vulnerabilities in asyncio.as_completed(vulns_futures):
        for vuln in await vulnerabilities:
            # Exception: WF(AsyncGenerator is subtype of iterator)
            yield vuln  # NOSONAR


@SHIELD
async def upload_report(  # pylint: disable=too-many-arguments
    config: ForcesConfig,
    execution_id: str,
    git_metadata: dict[str, str],
    log_file: str,
    report: ForcesData,
    exit_code: str,
) -> bool:
    """
    Upload report execution to Integrates.

    :param `config`: Current Forces config
    :param `execution_id`: ID of forces execution.
    :param `git_metadata`: Repository metadata.
    :param `log`: Forces execution log.
    :param `report`: Forces execution report.
    :param `exit_code`: Exit code.
    """
    mutation = """
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
    vulnerable_vulns: list[dict[str, float | str]] = []
    safe_vulns: list[dict[str, float | str]] = []
    accepted_vulns: list[dict[str, float | str]] = []
    for vuln in [
        vuln for find in report.findings for vuln in find.vulnerabilities
    ]:
        vuln_state: dict[str, float | str] = {
            "kind": vuln.type.value,
            "who": vuln.specific,
            "where": vuln.where,
            "state": {"safe": "closed", "vulnerable": "open"}
            .get(vuln.state.value, vuln.state.value)
            .upper(),
            "exploitability": vuln.exploitability,
        }
        if vuln.state == VulnerabilityState.VULNERABLE:
            vulnerable_vulns.append(vuln_state)
        elif vuln.state == VulnerabilityState.SAFE:
            safe_vulns.append(vuln_state)
        elif vuln.state == VulnerabilityState.ACCEPTED:
            accepted_vulns.append(vuln_state)

    with open(log_file, "rb") as forces_log:
        params: dict[str, Any] = {
            "group_name": config.group,
            "execution_id": execution_id,
            "date": datetime.utcnow().isoformat(),
            "exit_code": exit_code,
            "git_branch": git_metadata["git_branch"],
            "git_commit": git_metadata["git_commit"],
            "git_origin": git_metadata["git_origin"],
            "git_repo": git_metadata["git_repo"],
            "open": vulnerable_vulns,
            "accepted": accepted_vulns,
            "closed": safe_vulns,
            "log": forces_log,
            "strictness": "strict" if config.strict else "lax",
            "grace_period": config.grace_period,
            "severity_threshold": float(config.breaking_severity),
            "kind": config.kind.value,
        }

        response: dict[str, dict[str, bool]] = await execute(
            query=mutation,
            operation_name="ForcesDoUploadReport",
            variables=params,
            default={},
        )
    return response.get("addForcesExecution", {}).get("success", False)


@SHIELD
async def get_groups_access(
    **kwargs: Any,
) -> list[tuple[dict[str, str], float, int]]:
    query = """
        query ForcesGetMeGroups {
          me {
            organizations {
              groups {
                name
                minBreakingSeverity
                vulnerabilityGracePeriod
                organization
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
                list[dict[str, list[dict[str, str]] | int | float]],
            ],
        ] = await execute(
            query,
            operation_name="ForcesGetMeGroups",
            **kwargs,
        )
    except ApiError as exc:
        if (
            "Login required" in exc.messages
            or "Token format unrecognized" in exc.messages
        ):
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
        for group in cast(list[dict[str, str]], organization["groups"])
    )


async def get_git_remotes(group: str, **kwargs: Any) -> list[dict[str, str]]:
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
    response: dict[str, dict[str, list[dict[str, str]]]] = await execute(
        query,
        operation_name="ForcesGetGitRoots",
        variables={"group": group},
        **kwargs,
    )

    return response["group"]["roots"]


async def get_forces_user_and_org_data(
    **kwargs: Any,
) -> tuple[str | None, str | None, float | None, int | None]:
    groups = await get_groups_access(**kwargs)
    for group, global_brk_severity, vuln_grace_period in groups:
        if group["userRole"] == "service_forces":
            return (
                group["organization"],
                group["name"],
                global_brk_severity,
                vuln_grace_period,
            )
    return (None, None, None, None)
