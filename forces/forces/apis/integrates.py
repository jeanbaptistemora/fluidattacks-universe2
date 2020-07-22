# Standar Imports
"""Fluid Forces integrates api module."""
from typing import Any, Dict, List, Union

# 3dr Imports
from gql import gql, Client


async def get_findings(client: Client, project: str) -> List[str]:
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
    params = {'project_name': project}
    result: Dict[str, Dict[str, Any]] = await client.execute(
        query, variable_values=params)
    findings: List[str] = [
        group['id'] for group in result['project']['findings']
    ]
    return findings


async def get_vulnerabilities(
        client: Client, finding: str
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
    params = {'finding_id': finding}
    result = await client.execute(query, variable_values=params)
    return result['finding']['vulnerabilities']  # type: ignore


async def get_finding(client: Client, finding: str) -> Dict[str, str]:
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
    params = {'finding_id': finding}
    result = await client.execute(query, variable_values=params)
    return result['finding']  # type: ignore
