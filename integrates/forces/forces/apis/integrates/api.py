"""Fluid Forces integrates api module."""

from collections.abc import (
    Callable,
    Mapping,
)
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
    KindEnum,
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
    cast,
    TypeVar,
)

# Constants
# pylint: disable=invalid-name
TFun = TypeVar("TFun", bound=Callable[..., object])
SHIELD: Callable[[TFun], TFun] = shield(
    retries=8 if guess_environment() == "production" else 1,
    sleep_between_retries=5,
)


@SHIELD
async def get_findings(
    group: str, **kwargs: str
) -> tuple[dict[str, Any], ...]:
    """Returns the findings of a group.

    Args:
        `group (str)`: Group name

    Returns:
        `tuple[dict[str, Any]]`: A tuple with the findings of a group
    """
    query = """
        query ForcesDoGetGroupFindings($group_name: String!) {
            group(groupName: $group_name) {
                findings {
                    id
                    currentState
                    title
                    status
                    severity {
                        exploitability
                    }
                    severityScore
                }
            }
        }
        """

    result: dict[str, dict[str, list[Any]]] = await execute(
        query=query,
        operation_name="ForcesDoGetGroupFindings",
        variables=dict(group_name=group),
        default={},
        **kwargs,
    )

    return tuple(result["group"]["findings"])


@SHIELD
async def get_vulnerabilities(
    config: ForcesConfig, **kwargs: str
) -> tuple[dict[str, Any], ...]:
    """
    Returns the vulnerabilities of a group.

    :param `config`: Forces config.
    """
    vulnerabilities: list[dict[str, Any]] = []
    query = """
        query ForcesDoGetVulnerabilities(
            $group_name: String!
            $after: String
            $first: Int
            $brk_severity: String
            $state: String
            $vuln_type: String
        ) {
            group(groupName: $group_name) {
                vulnerabilities(
                    after: $after
                    first: $first
                    minSeverity: $brk_severity
                    stateStatus: $state
                    type: $vuln_type
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
    query_parameters = dict(
        brk_severity=str(int(config.breaking_severity))
        if config.verbose_level == 1
        else None,
        first=200,
        group_name=config.group,
        state="VULNERABLE" if config.verbose_level <= 2 else None,
        vuln_type="lines" if config.kind == KindEnum.STATIC else None,
    )
    response: dict = await execute(
        query=query,
        operation_name="ForcesDoGetVulnerabilities",
        variables=query_parameters,
        default={},
        **kwargs,
    )
    while True:
        has_next_page: bool = False
        if response:
            vulnerabilities_connection = response["group"]["vulnerabilities"]
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
            operation_name="ForcesDoGetVulnerabilities",
            variables=dict(**query_parameters, after=end_cursor),
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

    return tuple(vulnerabilities)


@SHIELD
async def upload_report(  # pylint: disable=too-many-arguments
    config: ForcesConfig,
    execution_id: str,
    git_metadata: Mapping[str, str],
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
) -> tuple[dict[str, Any], ...]:
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
            return tuple()
        raise Exception from exc
    return tuple(
        group
        for organization in response["me"]["organizations"]
        for group in cast(list[dict[str, Any]], organization["groups"])
    )


async def get_git_remotes(
    group: str, **kwargs: object
) -> list[dict[str, str]]:
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
    **kwargs: object,
) -> tuple[str | None, str | None, float | None, int | None]:
    groups = await get_groups_access(**kwargs)
    for group in groups:
        if group["userRole"] == "service_forces":
            return (
                group["organization"],
                group["name"],
                group["minBreakingSeverity"],
                group["vulnerabilityGracePeriod"],
            )
    return (None, None, None, None)
