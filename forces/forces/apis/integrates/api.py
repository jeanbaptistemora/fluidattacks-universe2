"""Fluid Forces integrates api module."""
# Standar Imports
import asyncio
from datetime import datetime
from typing import (
    Any,
    AsyncGenerator,
    Dict,
    List,
    Union,
)
import sys
# 3dr Imports
from gql import (
    gql,
)
from gql.transport.exceptions import (
    TransportQueryError,
)
from aiohttp.client_exceptions import (
    ClientConnectorError,
)

# Local Library
from forces.apis.integrates.client import (
    session,
)
from forces.utils.logs import log as logger


async def get_findings(project: str, **kwargs: str) -> List[str]:
    """
    Returns the findings of a group.

    :param client: gql Client.
    :param project: Project name.
    """
    query = gql("""
        query GetProjectFindings($project_name: String!) {
          project (projectName: $project_name) {
            findings {
              id
            }
          }
        }
        """)
    async with session(**kwargs) as client:
        params = {'project_name': project}
        findings: List[str] = []
        try:
            result: Dict[str, Dict[str, Any]] = await client.execute(
                query, variable_values=params)
            findings = [group['id'] for group in result['project']['findings']]
        except ClientConnectorError as exc:
            await logger('error', str(exc))
            sys.exit(1)
        except TransportQueryError as exc:
            await logger('warning', f"{project}'s findings cannot be obtained")
            await logger('warning', ('The token may be invalid or does '
                                     'not have the required permissions'))
            await logger('error', exc.errors[0]['message'])
        return findings


async def get_vulnerabilities(
        finding: str, **kwargs: str
) -> List[Dict[str, Union[str, List[Dict[str, Dict[str, Any]]]]]]:
    """
    Returns the vulnerabilities of a finding.

    :param client: gql Client.
    :param finding: Finding identifier.
    """
    query = gql("""
        query GetFindingVulnerabilities($finding_id: String!){
          finding(identifier: $finding_id) {
            vulnerabilities {
              findingId,
              currentState
              vulnType
              where
              specific
            }
          }
        }
        """)
    async with session(**kwargs) as client:
        params = {'finding_id': finding}
        result = []
        try:
            response = await client.execute(query, variable_values=params)
            result = response['finding']['vulnerabilities']
        except ClientConnectorError as exc:
            await logger('error', str(exc))
            sys.exit(1)
        except TransportQueryError as exc:
            await logger('warning', (f'the vulnerability of finding {finding}'
                                     ' cannot be obtained'))
            await logger('warning', ('The token may be invalid or does not'
                                     ' have the required permissions'))
            await logger('error', exc.errors[0]['message'])
        return result


async def get_finding(finding: str, **kwargs: str) -> Dict[str, str]:
    """
    Returns a finding.

    :param finding: Finding identifier.
    """
    query = gql("""
        query GetFinding($finding_id: String!) {
          finding(identifier: $finding_id) {
            title
            id
            state
          }
        }
        """)
    async with session(**kwargs) as client:
        params = {'finding_id': finding}
        result: Dict[str, str] = {}
        try:
            response = await client.execute(query, variable_values=params)
            result = response['finding']
        except ClientConnectorError as exc:
            await logger('error', str(exc))
            sys.exit(1)
        except TransportQueryError as exc:
            await logger('warning', f'cannot find finding {finding}')
            await logger('warning', ('The token may be invalid or does not'
                                     ' have the required permissions'))
            await logger('error', exc.errors[0]['message'])
        return result


async def vulns_generator(project: str, **kwargs: str) -> AsyncGenerator[Dict[
        str, Union[str, List[Dict[str, Dict[str, Any]]]]], None]:
    """
    Returns a generator with all the vulnerabilities of a project.

    :param project: Project Name.
    """
    findings = await get_findings(project, **kwargs)
    vulns_futures = [get_vulnerabilities(fin, **kwargs) for fin in findings]
    for vulnerabilities in asyncio.as_completed(vulns_futures):
        for vuln in await vulnerabilities:
            yield vuln


async def upload_report(project: str,
                        report: Dict[str, Any],
                        log: str,
                        git_metadata: Dict[str, str],
                        **kwargs: Union[datetime, str]) -> bool:
    """
    Upload report execution to Integrates.

    :param project:
    :param execution_id:
    :param exit_code:
    :param report:
    :param log:
    :param strictness:
    :param git_metadata:
    :param date:
    """
    query = gql("""
        mutation UploadReport(
            $project_name: String!
            $execution_id: String!
            $date: DateTime!
            $exit_code: String!
            $git_branch: String
            $git_commit: String
            $git_origin: String
            $git_repo: String
            $kind: String
            $log: String
            $strictness: String!
            $exploits: [ExploitResultInput!]
            $accepted: [ExploitResultInput!]
            $num_accepted: Int
            $num_exploits: Int
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
                    exploits: $exploits,
                    acceptedExploits: $accepted,
                    numOfVulnerabilitiesInAcceptedExploits: $num_accepted,
                    numOfVulnerabilitiesInExploits: $num_exploits,
                    numOfVulnerabilitiesInIntegratesExploits: 0
                }
            ) {
                success
            }
        }
        """)
    exploits: List[Dict[str, str]] = []
    accepted: List[Dict[str, str]] = []
    for vuln in [
            vuln
            for find in report['findings'] for vuln in find['vulnerabilities']
    ]:
        (accepted if vuln['state'] == 'accepted' else exploits).append({
            'kind':
            vuln['type'],
            'who':
            vuln['specific'],
            'where':
            vuln['where']
        })
    params: Dict[str, Any] = {
        'project_name': project,
        'execution_id': kwargs.pop('execution_id'),
        'date': kwargs.pop('date', datetime.now()).isoformat(),  # type: ignore
        'exit_code': str(kwargs.pop('exit_code')),
        'git_branch': git_metadata['git_branch'],
        'git_commit': git_metadata['git_commit'],
        'git_origin': git_metadata['git_origin'],
        'git_repo': git_metadata['git_repo'],
        'exploits': exploits,
        'accepted': accepted,
        'log': log,
        'strictness': kwargs.pop('strictness'),
        'kind': 'other',
        'num_accepted': report['summary']['accepted'],
        'num_exploits': report['summary']['open'] + report['summary']['open']
    }

    async with session(**kwargs) as client:
        result = False
        try:
            response = await client.execute(query, variable_values=params)
            result = response['addForcesExecution']['success']
        except ClientConnectorError as exc:
            await logger('error', str(exc))
            sys.exit(1)
        except TransportQueryError as exc:
            await logger('warning', 'Cannot upload report')
            await logger('warning', ('The token may be invalid or does not'
                                     ' have the required permissions'))
            await logger('error', exc.errors[0]['message'])
        return result
