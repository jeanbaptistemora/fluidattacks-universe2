# Standard libraries

# Third-party libraries
from aioextensions import schedule
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from backend import mailer
from backend.dal import project as project_dal
from backend.exceptions import (
    InvalidCommentParent,
    InvalidProjectServicesConfig,
)
from backend.typing import Comment as CommentType
from newutils import comments as comments_utils


async def add_comment(
    info: GraphQLResolveInfo,
    group_name: str,
    email: str,
    comment_data: CommentType
) -> bool:
    """Add comment in a project."""
    parent = str(comment_data['parent'])
    content = str(comment_data['content'])
    await comments_utils.validate_handle_comment_scope(
        content,
        email,
        group_name,
        parent,
        info.context.store
    )
    if parent != '0':
        project_comments = [
            str(comment.get('user_id'))
            for comment in await project_dal.get_comments(group_name)
        ]
        if parent not in project_comments:
            raise InvalidCommentParent()
    return await project_dal.add_comment(group_name, email, comment_data)


def send_comment_mail(
    user_email: str,
    comment_data: CommentType,
    group_name: str
) -> None:
    schedule(
        mailer.send_comment_mail(
            comment_data,
            'project',
            user_email,
            'project',
            group_name
        )
    )


def validate_group_services_config(
    is_continuous_type: bool,
    has_drills: bool,
    has_forces: bool,
    has_integrates: bool,
) -> None:
    if is_continuous_type:
        if has_drills:
            if not has_integrates:
                raise InvalidProjectServicesConfig(
                    'Drills is only available when Integrates is too')

        if has_forces:
            if not has_integrates:
                raise InvalidProjectServicesConfig(
                    'Forces is only available when Integrates is too')
            if not has_drills:
                raise InvalidProjectServicesConfig(
                    'Forces is only available when Drills is too')

    else:
        if has_forces:
            raise InvalidProjectServicesConfig(
                'Forces is only available in projects of type Continuous')
