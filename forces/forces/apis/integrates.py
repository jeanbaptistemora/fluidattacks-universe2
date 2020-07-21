# Standar Imports
from typing import Any, Dict, List, Tuple


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
        client: Client, finding: str) -> Tuple[str, List[Dict[str, str]]]:
    """
    Returns the vulnerabilities of a finding.

    :param client: gql Client.
    :param finding: Finding identifier.
    """
    query = gql("""
        query GetFindingVulnerabilities($finding_id: String!){
          finding(identifier: $finding_id) {
            vulnerabilities {
              id,
              historicState
            }
          }
        }
        """)
    params = {'finding_id': finding}
    result = await client.execute(query, variable_values=params)
    return (finding, result['finding']['vulnerabilities'])
