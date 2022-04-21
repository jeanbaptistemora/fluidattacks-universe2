from api import (
    APP_EXCEPTIONS,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    InvalidFileType,
)
from custom_types import (
    SimplePayload,
)
from dataloaders import (
    Dataloaders,
)
from db_model.findings.types import (
    Finding,
)
from db_model.groups.types import (
    Group,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    files as files_utils,
    logs as logs_utils,
)
from organizations_finding_policies import (
    domain as policies_domain,
)
from redis_cluster.operations import (
    redis_del_by_deps,
)
from typing import (
    Any,
)
from unreliable_indicators.enums import (
    EntityDependency,
)
from unreliable_indicators.operations import (
    update_unreliable_indicators_by_deps,
)
from vulnerability_files import (
    domain as vuln_files_domain,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _parent: None, info: GraphQLResolveInfo, **kwargs: Any
) -> SimplePayload:
    try:
        finding_id = kwargs["finding_id"]
        file_input = kwargs["file"]
        loaders: Dataloaders = info.context.loaders
        finding: Finding = await loaders.finding.load(finding_id)
        allowed_mime_type = await files_utils.assert_uploaded_file_mime(
            file_input, ["text/x-yaml", "text/plain", "text/html"]
        )
        group: Group = await loaders.group_typed.load(finding.group_name)
        finding_policy = await policies_domain.get_finding_policy_by_name(
            org_name=group.organization_name,
            finding_name=finding.title.lower(),
        )
        if file_input and allowed_mime_type:
            processed_vulnerabilities = await vuln_files_domain.upload_file(
                info,
                file_input,
                finding_id,
                finding_policy,
                finding.group_name,
            )
        else:
            raise InvalidFileType()
        await redis_del_by_deps(
            "upload_file",
            finding_id=finding_id,
            group_name=finding.group_name,
        )
        await update_unreliable_indicators_by_deps(
            EntityDependency.upload_file,
            finding_ids=[finding_id],
            vulnerability_ids=list(processed_vulnerabilities),
        )
        if finding_policy:
            await update_unreliable_indicators_by_deps(
                EntityDependency.handle_finding_policy,
                finding_ids=[finding_id],
                vulnerability_ids=list(processed_vulnerabilities),
            )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Uploaded file in {finding.group_name} group "
            "successfully",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to upload file in {finding.group_name} "
            "group",
        )
        raise

    return SimplePayload(success=True)
