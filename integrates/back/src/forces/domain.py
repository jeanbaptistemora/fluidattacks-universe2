from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    forces as forces_model,
)
from db_model.forces.types import (
    ForcesExecution,
)
from db_model.groups.types import (
    GroupMetadataToUpdate,
)
from group_access import (
    domain as group_access_domain,
)
from groups import (
    domain as groups_domain,
)
import json
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
)


async def save_log_execution(file_object: object, file_name: str) -> None:
    await s3_ops.upload_memory_file(
        file_object,
        f"forces/{file_name}",
    )


async def add_forces_execution(
    *,
    group_name: str,
    log: UploadFile | None = None,
    **execution_attributes: Any,
) -> None:
    orgs_domain.validate_min_breaking_severity(
        execution_attributes["severity_threshold"]
    )
    orgs_domain.validate_vulnerability_grace_period(
        execution_attributes["grace_period"]
    )
    forces_execution = ForcesExecution(
        id=execution_attributes["execution_id"],
        group_name=group_name,
        execution_date=execution_attributes["date"],
        commit=execution_attributes["git_commit"],
        repo=execution_attributes["git_repo"],
        branch=execution_attributes["git_branch"],
        kind=execution_attributes["kind"],
        exit_code=execution_attributes["exit_code"],
        strictness=execution_attributes["strictness"],
        origin=execution_attributes["git_origin"],
        grace_period=int(execution_attributes["grace_period"]),
        severity_threshold=execution_attributes["severity_threshold"],
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
        await forces_model.add(forces_execution=forces_execution)


async def add_forces_stakeholder(
    loaders: Dataloaders,
    group_name: str,
    modified_by: str,
) -> None:
    forces_email = format_forces_email(group_name)
    await groups_domain.invite_to_group(
        loaders=loaders,
        email=forces_email,
        responsibility="Forces service user",
        role="service_forces",
        group_name=group_name,
        modified_by=modified_by,
    )

    # Give permissions directly, no confirmation required
    group_access = await group_access_domain.get_group_access(
        get_new_context(), group_name, forces_email
    )
    await groups_domain.complete_register_for_group_invitation(
        loaders, group_access
    )


def format_forces_email(group_name: str) -> str:
    return f"forces.{group_name}@fluidattacks.com"


async def get_log_execution(group_name: str, execution_id: str) -> str:
    with tempfile.NamedTemporaryFile(mode="w+") as file:
        await s3_ops.download_file(
            f"forces/{group_name}/{execution_id}.log",
            file.name,
        )
        with open(file.name, encoding="utf-8") as reader:
            return reader.read()


async def get_vulns_execution(
    group_name: str, execution_id: str
) -> dict[str, Any]:
    with tempfile.NamedTemporaryFile(mode="w+") as file:
        await s3_ops.download_file(
            f"forces/{group_name}/{execution_id}.json",
            file.name,
        )
        with open(file.name, encoding="utf-8") as reader:
            return json.load(reader)


def is_forces_user(email: str) -> bool:
    """Ensure that is an forces user."""
    pattern = r"forces.(?P<group>\w+)@fluidattacks.com"
    return bool(re.match(pattern, email))


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
