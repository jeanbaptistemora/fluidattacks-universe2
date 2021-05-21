"""Fluid Forces integrates api module."""
# Standar Imports
import asyncio
from datetime import (
    datetime,
)
from typing import (
    Any,
    AsyncGenerator,
    Callable,
    Dict,
    List,
    Union,
    TypeVar,
    Optional,
)

# 3dr Imports

# Local Library
from forces.apis.integrates.client import execute
from forces.utils.function import shield
from forces.utils.env import guess_environment

# Constants
TFun = TypeVar("TFun", bound=Callable[..., Any])
SHIELD: Callable[[TFun], TFun] = shield(
    retries=8 if guess_environment() == "production" else 1,
    sleep_between_retries=5,
)


@SHIELD
async def get_findings(project: str, **kwargs: str) -> List[str]:
    """
    Returns the findings of a group.

    :param client: gql Client.
    :param project: Project name.
    """
    query = """
        query ForcesDoGetProjectFindings($project_name: String!) {
          project (projectName: $project_name) {
            findings {
              id
            }
          }
        }
        """

    params = {"project_name": project}
    result: Dict[str, Dict[str, List[Any]]] = (
        await execute(
            query=query,
            operation_name="ForcesDoGetProjectFindings",
            variables=params,
            default=dict(),
            **kwargs,
        )
        or dict()
    )

    findings: List[str] = [
        group["id"]
        for group in (result.get("project", dict()) or {}).get("findings", [])
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
              vulnType
              where
              specific
            }
          }
        }
        """

    params = {"finding_id": finding}
    response: Dict[str, Dict[str, List[Any]]] = await execute(
        query=query,
        operation_name="ForcesDoGetFindingVulnerabilities",
        variables=params,
        default=dict(),
        **kwargs,
    )
    finding_value = response.get("finding", dict())
    vulnerabilities = finding_value.get("vulnerabilities", list())
    for index, _ in enumerate(vulnerabilities):
        current_state: Dict[str, str] = (
            vulnerabilities[index].get("historicTreatment", [{}])
        )[-1]
        zero_risk = (vulnerabilities[index].get("historicZeroRisk", [{}]))[-1]
        if "accepted" in current_state.get("treatment", "unknown").lower():
            vulnerabilities[index]["currentState"] = "accepted"
        if zero_risk.get("status") in {"REQUESTED", "CONFIRMED"}:
            vulnerabilities[index]["currentState"] = "accepted"

    return finding_value.get("vulnerabilities", list())


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
          }
        }
        """
    params = {"finding_id": finding}
    response: Dict[str, str] = await execute(
        query=query,
        operation_name="ForcesDoGetFinding",
        variables=params,
        default=dict(),
        **kwargs,
    )
    return response.get("finding", dict())  # type: ignore


async def vulns_generator(
    project: str, **kwargs: str
) -> AsyncGenerator[
    Dict[str, Union[str, List[Dict[str, Dict[str, Any]]]]], None
]:
    """
    Returns a generator with all the vulnerabilities of a project.

    :param project: Project Name.
    """
    findings = await get_findings(project, **kwargs)
    vulns_futures = [get_vulnerabilities(fin, **kwargs) for fin in findings]
    for vulnerabilities in asyncio.as_completed(vulns_futures):
        for vuln in await vulnerabilities:
            yield vuln


@SHIELD
async def upload_report(
    project: str,
    report: Dict[str, Any],
    log_file: str,
    git_metadata: Dict[str, str],
    **kwargs: Union[datetime, str],
) -> bool:
    """
    Upload report execution to Integrates.

    :param project: Subscription name.
    :param execution_id: ID of forces execution.
    :param exit_code: Exit code.
    :param report: Forces execution report.
    :param log: Forces execution log.
    :param strictness: Strictness execution.
    :param git_metadata: Repository metadata.
    :param date: Forces execution date.
    """
    query = """
        mutation ForcesDoUploadReport(
            $project_name: String!
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
                projectName: $project_name
                execution_id: $execution_id
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
        "project_name": project,
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
    return response.get("addForcesExecution", dict()).get("success", False)


@SHIELD
async def get_projects_access(**kwargs: Any) -> List[Dict[str, str]]:
    query = """
        query ForcesGetMeProjects {
          me {
            organizations {
              projects {
                name
                userRole
              }
            }
          }
        }
    """
    response: Dict[
        str, Dict[str, List[Dict[str, List[Dict[str, str]]]]]
    ] = await execute(
        query,
        operation_name="ForcesGetMeProjects",
        **kwargs,
    )
    return list(
        group
        for organization in response["me"]["organizations"]
        for group in organization["projects"]
    )


async def get_git_remotes(group: str, **kwargs: Any) -> List[Dict[str, str]]:
    query = """
        query ForcesGetGitRoots($group: String!) {
          project(projectName: $group){
            roots {
              ...on GitRoot{
                url
                state
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

    return response["project"]["roots"]


async def get_forces_user(**kwargs: Any) -> Optional[str]:
    projects = await get_projects_access(**kwargs)
    for group in projects:
        if group["userRole"] == "service_forces":
            return group["name"]
    return None
