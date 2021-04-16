# Standard library
import os
import json
import logging
import re
import tempfile
from datetime import datetime
from functools import reduce
from typing import (
    Any,
    cast,
    Dict,
    List,
    Optional,
    Union,
)

# Third party libraries
from graphql.type.definition import GraphQLResolveInfo
from starlette.datastructures import UploadFile

# Local libraries
from back.settings import LOGGING
from backend.typing import (
    ExecutionVulnerabilities,
    ForcesExecution as ForcesExecutionType,
)
from forces import dal as forces_dal
from group_access import domain as group_access_domain
from groups import domain as groups_domain
from users import domain as users_domain


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def add_forces_execution(
    *,
    project_name: str,
    log: Union[UploadFile, None] = None,
    **execution_attributes: Any
) -> bool:
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
        if (
            await forces_dal.save_log_execution(log, log_name) and
            await forces_dal.save_log_execution(vulns_file, vulns_name)
        ):
            success = await forces_dal.create_execution(
                project_name=project_name, **execution_attributes
            )
    return success


async def create_forces_user(
    info: GraphQLResolveInfo,
    group_name: str
) -> bool:
    user_email = format_forces_user_email(group_name)
    success = await groups_domain.invite_to_group(
        email=user_email,
        responsibility='Forces service user',
        role='service_forces',
        phone_number='',
        group_name=group_name
    )

    # Give permissions directly, no confirmation required
    group_access = await group_access_domain.get_user_access(
        user_email,
        group_name
    )
    success = (
        success and
        await users_domain.complete_register_for_group_invitation(group_access)
    )
    if not success:
        LOGGER.error(
            'Couldn\'t grant access to project',
            extra={
                'extra': info.context,
                'username': group_name
            },
        )
    return success


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


def format_forces_user_email(project_name: str) -> str:
    return f'forces.{project_name}@fluidattacks.com'


async def get_execution(
    *,
    group_name: str,
    execution_id: str,
) -> ForcesExecutionType:
    execution = await forces_dal.get_execution(group_name, execution_id)
    return format_execution(execution)


async def get_executions(
    *,
    from_date: datetime,
    group_name: str,
    to_date: datetime,
) -> List[ForcesExecutionType]:
    result = []
    async for execution in forces_dal.yield_executions(
            project_name=group_name,
            from_date=from_date,
            to_date=to_date,
    ):
        result.append(format_execution(execution))
    return result


async def get_log_execution(group_name: str, execution_id: str) -> str:
    return await forces_dal.get_log_execution(group_name, execution_id)


async def get_token(project_name: str) -> Optional[str]:
    return await forces_dal.get_secret_token(project_name)


async def get_vulns_execution(
    group_name: str,
    execution_id: str
) -> ExecutionVulnerabilities:
    return cast(
        ExecutionVulnerabilities,
        await forces_dal.get_vulns_execution(group_name, execution_id)
    )


def is_forces_user(email: str) -> bool:
    """Ensure that is an forces user."""
    pattern = r'forces.(?P<group>\w+)@fluidattacks.com'
    return bool(re.match(pattern, email))


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


async def update_token(project_name: str, token: str) -> bool:
    return await forces_dal.update_secret_token(project_name, token)
