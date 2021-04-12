# Standard libraries
import secrets

# Third-party libraries
from aioextensions import schedule
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from backend import mailer
from backend.dal import project as group_dal
from backend.domain import project as group_domain
from backend.exceptions import (
    InvalidCommentParent,
    InvalidProjectServicesConfig,
)
from backend.typing import (
    Comment as CommentType,
    MailContent as MailContentType,
)
from group_access import domain as group_access_domain
from newutils import (
    comments as comments_utils,
    datetime as datetime_utils,
)
from newutils.validations import (
    validate_alphanumeric_field,
    validate_email_address,
    validate_field_length,
    validate_fluidattacks_staff_on_group,
    validate_phone_field,
)
from __init__ import BASE_URL


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
            for comment in await group_dal.get_comments(group_name)
        ]
        if parent not in project_comments:
            raise InvalidCommentParent()
    return await group_dal.add_comment(group_name, email, comment_data)


async def invite_to_group(
    email: str,
    responsibility: str,
    role: str,
    phone_number: str,
    group_name: str,
) -> bool:
    success = False
    if (
        validate_field_length(responsibility, 50) and
        validate_alphanumeric_field(responsibility) and
        validate_phone_field(phone_number) and
        validate_email_address(email) and
        await validate_fluidattacks_staff_on_group(group_name, email, role)
    ):
        expiration_time = datetime_utils.get_as_epoch(
            datetime_utils.get_now_plus_delta(weeks=1)
        )
        url_token = secrets.token_urlsafe(64)
        success = await group_access_domain.update(
            email,
            group_name,
            {
                'expiration_time': expiration_time,
                'has_access': False,
                'invitation': {
                    'is_used': False,
                    'phone_number': phone_number,
                    'responsibility': responsibility,
                    'role': role,
                    'url_token': url_token,
                },

            }
        )
        description = await group_domain.get_description(group_name.lower())
        project_url = f'{BASE_URL}/confirm_access/{url_token}'
        mail_to = [email]
        email_context: MailContentType = {
            'admin': email,
            'project': group_name,
            'project_description': description,
            'project_url': project_url,
        }
        schedule(mailer.send_mail_access_granted(mail_to, email_context))
    return success


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
