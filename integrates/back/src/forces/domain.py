from context import (
    FI_AWS_S3_FORCES_BUCKET,
)
from db_model.forces.types import (
    ForcesExecution,
)
from db_model.group_access.types import (
    GroupAccess,
)
from db_model.groups.types import (
    GroupMetadataToUpdate,
)
from forces import (
    dal as forces_dal,
)
from functools import (
    reduce,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from groups import (
    domain as groups_domain,
)
import json
from newutils import (
    token as token_utils,
)
from newutils.forces import (
    format_forces_vulnerabilities_to_add,
)
from organizations import (
    domain as orgs_domain,
)
import os
import re
from s3 import (
    operations as s3_ops,
)
from starlette.datastructures import (
    UploadFile,
)
import tempfile
from typing import (
    Any,
    AsyncIterable,
    Dict,
    Union,
)


async def save_log_execution(file_object: object, file_name: str) -> None:
    await s3_ops.upload_memory_file(
        FI_AWS_S3_FORCES_BUCKET,
        file_object,
        file_name,
    )


async def add_forces_execution(
    *,
    group_name: str,
    log: Union[UploadFile, None] = None,
    **execution_attributes: Any,
) -> None:
    if "severity_threshold" in execution_attributes:
        orgs_domain.validate_min_breaking_severity(
            execution_attributes["severity_threshold"]
        )
    if "grace_period" in execution_attributes:
        orgs_domain.validate_vulnerability_grace_period(
            execution_attributes["grace_period"]
        )

    force_execution = ForcesExecution(
        id=execution_attributes["execution_id"],
        group_name=group_name,
        date=execution_attributes["date"],
        commit=execution_attributes["git_commit"],
        repo=execution_attributes["git_repo"],
        branch=execution_attributes["git_branch"],
        kind=execution_attributes["kind"],
        exit_code=execution_attributes["exit_code"],
        strictness=execution_attributes["strictness"],
        origin=execution_attributes["git_origin"],
        grace_period=int(execution_attributes["grace_period"]),
        severity_threshold=int(execution_attributes["severity_threshold"]),
        vulnerabilities=format_forces_vulnerabilities_to_add(
            execution_attributes["vulnerabilities"]
        ),
    )

    vulnerabilities = execution_attributes.pop("vulnerabilities")
    log_name = f'{group_name}/{execution_attributes["execution_id"]}.log'
    vulns_name = f'{group_name}/{execution_attributes["execution_id"]}.json'

    # Create a file for vulnerabilities
    with tempfile.NamedTemporaryFile() as vulns_file:
        vulns_file.write(json.dumps(vulnerabilities).encode("utf-8"))
        vulns_file.seek(os.SEEK_SET)
        await save_log_execution(log, log_name)
        await save_log_execution(vulns_file, vulns_name)
        await forces_dal.add_execution_typed(force_execution=force_execution)


async def add_forces_user(info: GraphQLResolveInfo, group_name: str) -> None:
    user_email = format_forces_user_email(group_name)
    user_data = await token_utils.get_jwt_content(info.context)
    modified_by = user_data["user_email"]
    await groups_domain.invite_to_group(
        loaders=info.context.loaders,
        email=user_email,
        responsibility="Forces service user",
        role="service_forces",
        group_name=group_name,
        modified_by=modified_by,
    )
    loaders = info.context.loaders

    # Give permissions directly, no confirmation required
    group_access: GroupAccess = await loaders.group_access.load(
        (group_name, user_email)
    )
    await groups_domain.complete_register_for_group_invitation(
        loaders=info.context.loaders,
        group_access=group_access,
    )


def format_execution(execution: Any) -> Dict[str, Any]:
    for _, vulnerabilities in execution.get("vulnerabilities", {}).items():
        if not isinstance(vulnerabilities, list):
            continue

        for vuln in vulnerabilities:
            explot = {
                "0.91": "Unproven",
                "0.94": "Proof of concept",
                "0.97": "Functional",
                "1.0": "High",
                "1": "High",
            }.get(str(vuln.get("exploitability", 0)), "-")
            vuln["exploitability"] = explot
    return execution


def format_forces_user_email(group_name: str) -> str:
    return f"forces.{group_name}@fluidattacks.com"


async def get_execution(
    *,
    group_name: str,
    execution_id: str,
) -> Dict[str, Any]:
    execution = await forces_dal.get_execution(group_name, execution_id)
    return format_execution(execution)


async def get_executions(
    *,
    group_name: str,
    group_name_key: str,
) -> AsyncIterable[Dict[str, Any]]:
    async for execution in forces_dal.yield_executions(
        group_name=group_name,
        group_name_key=group_name_key,
    ):
        yield format_execution(execution)


async def get_log_execution(group_name: str, execution_id: str) -> str:
    with tempfile.NamedTemporaryFile(mode="w+") as file:
        await s3_ops.download_file(
            FI_AWS_S3_FORCES_BUCKET,
            f"{group_name}/{execution_id}.log",
            file.name,
        )
        with open(file.name, encoding="utf-8") as reader:
            return reader.read()


async def get_vulns_execution(
    group_name: str, execution_id: str
) -> Dict[str, Any]:
    with tempfile.NamedTemporaryFile(mode="w+") as file:
        await s3_ops.download_file(
            FI_AWS_S3_FORCES_BUCKET,
            f"{group_name}/{execution_id}.json",
            file.name,
        )
        with open(file.name, encoding="utf-8") as reader:
            return json.load(reader)


def is_forces_user(email: str) -> bool:
    """Ensure that is an forces user."""
    pattern = r"forces.(?P<group>\w+)@fluidattacks.com"
    return bool(re.match(pattern, email))


def match_fields(my_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Replace fields from response according to schema."""
    replace_tuple = (
        ("mocked_exploits", "integrates_exploits"),
        (
            "vulnerability_count_mocked_exploits",
            "num_of_vulnerabilities_in_integrates_exploits",
        ),
        (
            "vulnerability_count_integrates_exploits",
            "num_of_vulnerabilities_in_integrates_exploits",
        ),
        ("vulnerability_count_exploits", "num_of_vulnerabilities_in_exploits"),
        (
            "vulnerability_count_accepted_exploits",
            "num_of_vulnerabilities_in_accepted_exploits",
        ),
    )
    new = {}
    for key, val in my_dict.items():
        if isinstance(val, dict):
            val = match_fields(val)
        new[reduce(lambda a, kv: a.replace(*kv), replace_tuple, key)] = val
    return new


async def update_token(
    group_name: str,
    organization_id: str,
    token: str,
) -> None:
    return await groups_domain.update_metadata(
        group_name=group_name,
        metadata=GroupMetadataToUpdate(
            agent_token=token,
        ),
        organization_id=organization_id,
    )
