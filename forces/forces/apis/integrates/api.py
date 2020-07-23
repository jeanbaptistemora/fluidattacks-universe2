"""Fluid Forces integrates api module."""
# Standar Imports
import asyncio
from typing import (
    Any,
    AsyncGenerator,
    Dict,
    List,
    Union
)
# 3dr Imports
from gql import (
    gql,
)

# Local Library
from forces.apis.integrates.client import (
    session,
)


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
        result: Dict[str, Dict[str, Any]] = await client.execute(
            query, variable_values=params)
        findings: List[str] = [
            group['id'] for group in result['project']['findings']
        ]
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
            }
          }
        }
        """)
    async with session(**kwargs) as client:
        params = {'finding_id': finding}
        result = await client.execute(query, variable_values=params)
        return result['finding']['vulnerabilities']  # type: ignore


async def get_finding(finding: str, **kwargs: str) -> Dict[str, str]:
    """
    Returns a finding.

    :param finding: Finding identifier.
    """
    query = gql("""
        query GetFinding($finding_id: String!) {
          finding(identifier: $finding_id) {
            id
            title
            state
          }
        }
        """)
    async with session(**kwargs) as client:
        params = {'finding_id': finding}
        result = await client.execute(query, variable_values=params)
        return result['finding']  # type: ignore


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
