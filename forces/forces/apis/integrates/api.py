"""Fluid Forces integrates api module."""

import asyncio
from datetime import (
    datetime,
)
from forces.apis.integrates.client import (
    ApiError,
    execute,
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
    Dict,
    List,
    Optional,
    TypeVar,
    Union,
)

# Constants
TFun = TypeVar("TFun", bound=Callable[..., Any])
SHIELD: Callable[[TFun], TFun] = shield(
    retries=8 if guess_environment() == "production" else 1,
    sleep_between_retries=5,
)


@SHIELD
async def get_findings(group: str, **kwargs: str) -> List[str]:
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
            }
          }
        }
        """

    params = {"group_name": group}
    result: Dict[str, Dict[str, List[Any]]] = (
        await execute(
            query=query,
            operation_name="ForcesDoGetGroupFindings",
            variables=params,
            default={},
            **kwargs,
        )
        or {}
    )

    findings: List[str] = [
        group["id"]
        for group in (result.get("group", {}) or {}).get("findings", [])
    ]

    return findings


@SHIELD
async def get_vulnerabilities(
    finding: str, **kwargs: str
) -> List[Dict[str, Union[str, List[Dict[str, Dict[str, Any]]]]]]:
    """
    Returns the vulnerabilities of a finding.

    :param client: gql Client.
    :param finding: Finding identifier.
    """
    query = """
        query ForcesDoGetFindingVulnerabilities($finding_id: String!){
          finding(identifier: $finding_id) {
            vulnerabilities {
              findingId
              currentState
              historicTreatment {
                treatment
              }
              historicZeroRisk{
                status
              }
              vulnerabilityType
              where
              specific
              rootNickname
            }
          }
        }
        """

    params = {"finding_id": finding}
    response: Dict[str, Dict[str, List[Any]]] = await execute(
        query=query,
        operation_name="ForcesDoGetFindingVulnerabilities",
        variables=params,
        default={},
        **kwargs,
    )
    finding_value = response.get("finding", {})
    vulnerabilities = finding_value.get("vulnerabilities", [])
    for index, _ in enumerate(vulnerabilities):
        current_state: Dict[str, str] = (
            vulnerabilities[index].get("historicTreatment", [{}])
        )[-1]
        zero_risk = (vulnerabilities[index].get("historicZeroRisk", [{}]))[-1]
        if "accepted" in current_state.get("treatment", "unknown").lower():
            vulnerabilities[index]["currentState"] = "accepted"
        if zero_risk.get("status") in {"REQUESTED", "CONFIRMED"}:
            vulnerabilities[index]["currentState"] = "accepted"

    return finding_value.get("vulnerabilities", [])


@SHIELD
async def get_finding(finding: str, **kwargs: str) -> Dict[str, Any]:
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
            severity
            severityScore
          }
        }
        """
    params = {"finding_id": finding}
    response: Dict[str, str] = await execute(
        query=query,
        operation_name="ForcesDoGetFinding",
        variables=params,
        default={},
        **kwargs,
    )
    return response.get("finding", {})  # type: ignore


async def vulns_generator(
    group: str, **kwargs: str
) -> AsyncGenerator[
    Dict[str, Union[str, List[Dict[str, Dict[str, Any]]]]], None
]:
    """
    Returns a generator with all the vulnerabilities of a group.

    :param group: Group Name.
    """
    findings = await get_findings(group, **kwargs)
    vulns_futures = [get_vulnerabilities(fin, **kwargs) for fin in findings]
    for vulnerabilities in asyncio.as_completed(vulns_futures):
        for vuln in await vulnerabilities:
            # Exception: WF(AsyncGenerator is subtype of iterator)
            yield vuln  # NOSONAR


@SHIELD
async def upload_report(
    group: str,
    report: Dict[str, Any],
    log_file: str,
    git_metadata: Dict[str, str],
    **kwargs: Union[datetime, str],
) -> bool:
    """
    Upload report execution to Integrates.

    :param group: Subscription name.
    :param execution_id: ID of forces execution.
    :param exit_code: Exit code.
    :param report: Forces execution report.
    :param log: Forces execution log.
    :param strictness: Strictness execution.
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
    open_vulns: List[Dict[str, str]] = []
    closed_vulns: List[Dict[str, str]] = []
    accepted_vulns: List[Dict[str, str]] = []
    for vuln in [
        vuln for find in report["findings"] for vuln in find["vulnerabilities"]
    ]:
        vuln_state = {
            "kind": vuln["type"],
            "who": vuln["specific"],
            "where": vuln["where"],
            "state": vuln["state"].upper(),
            "exploitability": vuln["exploitability"],
        }
        if vuln["state"] == "open":
            open_vulns.append(vuln_state)
        elif vuln["state"] == "closed":
            closed_vulns.append(vuln_state)
        elif vuln["state"] == "accepted":
            accepted_vulns.append(vuln_state)

    params: Dict[str, Any] = {
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
        "kind": kwargs.pop("kind", "all"),
    }

    response: Dict[str, Dict[str, bool]] = await execute(
        query=query,
        operation_name="ForcesDoUploadReport",
        variables=params,
        default={},
        **kwargs,
    )
    return response.get("addForcesExecution", {}).get("success", False)


@SHIELD
async def get_groups_access(**kwargs: Any) -> List[Dict[str, str]]:
    query = """
        query ForcesGetMeGroups {
          me {
            organizations {
              groups {
                name
                userRole
              }
            }
          }
        }
    """
    try:
        response: Dict[
            str, Dict[str, List[Dict[str, List[Dict[str, str]]]]]
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
        group
        for organization in response["me"]["organizations"]
        for group in organization["groups"]
    )


async def get_git_remotes(group: str, **kwargs: Any) -> List[Dict[str, str]]:
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
    response: Dict[str, Dict[str, List[Dict[str, str]]]] = await execute(
        query,
        operation_name="ForcesGetGitRoots",
        variables={"group": group},
        **kwargs,
    )

    return response["group"]["roots"]


async def get_forces_user(**kwargs: Any) -> Optional[str]:
    groups = await get_groups_access(**kwargs)
    for group in groups:
        if group["userRole"] == "service_forces":
            return group["name"]
    return None
