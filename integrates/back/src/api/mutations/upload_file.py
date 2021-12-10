from api import (
    APP_EXCEPTIONS,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    ErrorUploadingFileS3,
    InvalidFileType,
)
from custom_types import (
    SimplePayload,
)
from db_model.findings.types import (
    Finding,
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
        success = False
        finding_id = kwargs["finding_id"]
        file_input = kwargs["file"]
        finding_loader = info.context.loaders.finding
        finding: Finding = await finding_loader.load(finding_id)
        allowed_mime_type = await files_utils.assert_uploaded_file_mime(
            file_input, ["text/x-yaml", "text/plain", "text/html"]
        )
        group = await info.context.loaders.group.load(finding.group_name)
        organization = await info.context.loaders.organization.load(
            group["organization"]
        )
        finding_policy = await policies_domain.get_finding_policy_by_name(
            org_name=organization["name"],
            finding_name=finding.title.lower(),
        )
        if file_input and allowed_mime_type:
            success = await vuln_files_domain.upload_file(
                info,
                file_input,
                finding_id,
                finding_policy,
                finding.group_name,
            )
        else:
            raise InvalidFileType()
        if success:
            await redis_del_by_deps(
                "upload_file",
                finding_id=finding_id,
                group_name=finding.group_name,
            )
            await update_unreliable_indicators_by_deps(
                EntityDependency.upload_file,
                finding_id=finding_id,
            )
            logs_utils.cloudwatch_log(
                info.context,
                f"Security: Uploaded file in {finding.group_name} group "
                "successfully",
            )
        else:
            logs_utils.cloudwatch_log(
                info.context,
                f"Security: Attempted to upload file in {finding.group_name}"
                " group",
            )
            raise ErrorUploadingFileS3()
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to upload file in {finding.group_name} "
            "group",
        )
        raise

    return SimplePayload(success=success)
