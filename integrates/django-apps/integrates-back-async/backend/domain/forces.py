# Standard library
from datetime import (
    datetime,
)
from functools import (
    reduce,
)
from typing import (
    Any,
    cast,
    Dict,
    List,
    Union,
)
import tempfile
import json
import os

# Third party libraries
from django.core.files.uploadedfile import InMemoryUploadedFile

# Local libraries
from backend.dal import (
    forces as forces_dal,
)
from backend.typing import (
    ExecutionVulnerabilities,
    ForcesExecution as ForcesExecutionType,
)


def match_fields(my_dict: Dict[str, Any]) -> ForcesExecutionType:
    """Replace fields from response according to schema."""
    replace_tuple = (
        ('mocked_exploits',
         'integrates_exploits'),
        ('vulnerability_count_mocked_exploits',
         'num_of_vulnerabilities_in_integrates_exploits'),
        ('vulnerability_count_integrates_exploits',
         'num_of_vulnerabilities_in_integrates_exploits'),
        ('vulnerability_count_exploits',
         'num_of_vulnerabilities_in_exploits'),
        ('vulnerability_count_accepted_exploits',
         'num_of_vulnerabilities_in_accepted_exploits')
    )
    new = {}
    for key, val in my_dict.items():
        if isinstance(val, dict):
            val = match_fields(val)
        new[reduce(lambda a, kv: a.replace(*kv), replace_tuple, key)] = val
    return new


def format_execution(execution: Any) -> ForcesExecutionType:
    for _, vulnerabilities in execution.get('vulnerabilities', {}).items():
        if not isinstance(vulnerabilities, list):
            continue

        for vuln in vulnerabilities:
            explot = {
                '0.91': 'Unproven',
                '0.94': 'Proof of concept',
                '0.97': 'Functional',
                '1.0': 'High',
                '1': 'High',
            }.get(str(vuln.get('exploitability', 0)), '-')
            vuln['exploitability'] = explot

    return cast(ForcesExecutionType, execution)


async def get_executions(
    *,
    from_date: datetime,
    group_name: str,
    to_date: datetime,
) -> List[ForcesExecutionType]:
    return [
        match_fields(execution)
        async for execution in forces_dal.yield_executions(
            project_name=group_name, from_date=from_date, to_date=to_date)
    ]


async def get_executions_new(
    *,
    from_date: datetime,
    group_name: str,
    to_date: datetime,
) -> List[ForcesExecutionType]:
    result = []
    async for execution in forces_dal.yield_executions_new(
            project_name=group_name,
            from_date=from_date,
            to_date=to_date,
    ):
        result.append(format_execution(execution))

    return result


async def get_execution(
    *,
    group_name: str,
    execution_id: str,
) -> ForcesExecutionType:
    execution = await forces_dal.get_execution(
        group_name,
        execution_id,
    )

    return format_execution(execution)


async def add_forces_execution(*,
                               project_name: str,
                               log: Union[InMemoryUploadedFile, None] = None,
                               **execution_attributes: Any) -> bool:
    success = False
    vulnerabilities = execution_attributes.pop('vulnerabilities')

    execution_attributes['vulnerabilities'] = dict()
    execution_attributes['vulnerabilities'][
        'num_of_open_vulnerabilities'] = len(vulnerabilities['open'])
    execution_attributes['vulnerabilities'][
        'num_of_closed_vulnerabilities'] = len(vulnerabilities['closed'])
    execution_attributes['vulnerabilities'][
        'num_of_accepted_vulnerabilities'] = len(vulnerabilities['accepted'])

    log_name = f'{project_name}/{execution_attributes["execution_id"]}.log'
    vulns_name = f'{project_name}/{execution_attributes["execution_id"]}.json'
    # Create a file for vulnerabilities
    with tempfile.NamedTemporaryFile() as vulns_file:
        vulns_file.write(json.dumps(vulnerabilities).encode('utf-8'))
        vulns_file.seek(os.SEEK_SET)

        if await forces_dal.save_log_execution(
                log, log_name) and await forces_dal.save_log_execution(
                    vulns_file, vulns_name):
            success = await forces_dal.create_execution(
                project_name=project_name, **execution_attributes)
    return success


async def get_vulns_execution(
    group_name: str,
    execution_id: str
) -> ExecutionVulnerabilities:
    return cast(
        ExecutionVulnerabilities,
        await forces_dal.get_vulns_execution(group_name, execution_id)
    )


async def get_log_execution(group_name: str, execution_id: str) -> str:
    return await forces_dal.get_log_execution(group_name, execution_id)
