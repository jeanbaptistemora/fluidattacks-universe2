# Standard
from typing import Any

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login
)
from backend.domain import vulnerability as vuln_domain
from backend.exceptions import ErrorUploadingFileS3, InvalidFileType
from backend.typing import SimplePayload


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    **kwargs: Any
) -> SimplePayload:
    success = False
    finding_id = kwargs['finding_id']
    file_input = kwargs['file']
    finding_loader = info.context.loaders['finding']
    finding_data = await finding_loader.load(finding_id)
    group_name = finding_data['project_name']
    allowed_mime_type = await util.assert_uploaded_file_mime(
        file_input,
        ['text/x-yaml', 'text/plain', 'text/html']
    )
    if file_input and allowed_mime_type:
        success = await vuln_domain.upload_file(
            file_input,
            finding_data,
            info
        )
        await vuln_domain.update_last_vuln_date(finding_id)
    else:
        raise InvalidFileType()
    if success:
        util.queue_cache_invalidation(
            f'remediated*{finding_id}',
            f'state*{finding_id}',
            f'tracking*{finding_id}',
            f'verified*{finding_id}',
            f'vuln*{finding_id}',
            f'vuln*{group_name}'
        )
        util.cloudwatch_log(
            info.context,
            f'Security: Uploaded file in {group_name} group successfully'
        )
    else:
        util.cloudwatch_log(
            info.context,
            f'Security: Attempted to delete file from {group_name} group'
        )
        raise ErrorUploadingFileS3()
    return SimplePayload(success=success)
