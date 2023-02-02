from .boundary import (
    get_group_level_roles_with_tag,
)
from .enforcer import (
    get_group_level_enforcer,
    get_group_service_attributes_enforcer,
)
from custom_exceptions import (
    InvalidCommentParent,
    InvalidUserProvided,
    PermissionDenied,
    UnexpectedUserRole,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
)
import functools
from newutils.validations import (
    get_attr_value,
)
from typing import (
    Any,
    Callable,
)

# Constants
FLUIDATTACKS_EMAIL_SUFFIX = "@fluidattacks.com"


def validate_fluidattacks_staff_on_group(
    group: Group, email: str, role: str
) -> bool:
    """Makes sure that Fluid Attacks groups have only Fluid attacks staff."""
    enforcer = get_group_service_attributes_enforcer(group)

    is_user_at_fluidattacks: bool = email.endswith(FLUIDATTACKS_EMAIL_SUFFIX)
    user_has_hacker_role: bool = role in get_group_level_roles_with_tag(
        "drills", email
    )

    group_must_only_have_fluidattacks_hackers: bool = enforcer(
        "must_only_have_fluidattacks_hackers"
    )

    if (
        group_must_only_have_fluidattacks_hackers
        and user_has_hacker_role
        and not is_user_at_fluidattacks
    ):
        raise UnexpectedUserRole(
            "Groups with any active Fluid Attacks service can "
            "only have Hackers provided by Fluid Attacks"
        )
    return True


def validate_fluidattacks_staff_on_group_deco(
    group_field: str, email_field: str, role_field: str
) -> Callable:
    """Makes sure that Fluid Attacks groups have only Fluid attacks staff."""

    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            group = get_attr_value(
                field=group_field, kwargs=kwargs, obj_type=Group
            )
            email = get_attr_value(
                field=email_field, kwargs=kwargs, obj_type=str
            )
            role = get_attr_value(
                field=role_field, kwargs=kwargs, obj_type=str
            )
            enforcer = get_group_service_attributes_enforcer(group)
            is_user_at_fluidattacks: bool = email.endswith(
                FLUIDATTACKS_EMAIL_SUFFIX
            )
            user_has_hacker_role: bool = (
                role in get_group_level_roles_with_tag("drills", email)
            )

            group_must_only_have_fluidattacks_hackers: bool = enforcer(
                "must_only_have_fluidattacks_hackers"
            )
            if (
                group_must_only_have_fluidattacks_hackers
                and user_has_hacker_role
                and not is_user_at_fluidattacks
            ):
                raise UnexpectedUserRole(
                    "Groups with any active Fluid Attacks service can "
                    "only have Hackers provided by Fluid Attacks"
                )
            res = func(*args, **kwargs)
            return res

        return decorated

    return wrapper


async def validate_handle_comment_scope(
    loaders: Dataloaders,
    content: str,
    user_email: str,
    group_name: str,
    parent_comment: str,
) -> None:
    enforcer = await get_group_level_enforcer(loaders, user_email)
    if content.strip() in {"#external", "#internal"}:
        if not enforcer(group_name, "handle_comment_scope"):
            raise PermissionDenied()
        if parent_comment == "0":
            raise InvalidCommentParent()


def validate_handle_comment_scope_deco(
    loaders_field: str,
    content_field: str,
    user_mail: str,
    group_name_field: str,
    parent_comment_field: str,
) -> Callable:
    """Makes sure that Fluid Attacks groups have only Fluid attacks staff."""

    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def decorated(*args: Any, **kwargs: Any) -> Any:
            loaders: Dataloaders = get_attr_value(
                field=loaders_field, kwargs=kwargs, obj_type=Dataloaders
            )
            content: str = get_attr_value(
                field=content_field, kwargs=kwargs, obj_type=str
            )
            user_email: str = get_attr_value(
                field=user_mail, kwargs=kwargs, obj_type=str
            )
            group_name: str = get_attr_value(
                field=group_name_field, kwargs=kwargs, obj_type=str
            )
            parent_comment: str = get_attr_value(
                field=parent_comment_field, kwargs=kwargs, obj_type=str
            )
            enforcer = await get_group_level_enforcer(loaders, user_email)
            if content.strip() in {"#external", "#internal"}:
                if not enforcer(group_name, "handle_comment_scope"):
                    raise PermissionDenied()
                if parent_comment == "0":
                    raise InvalidCommentParent()
            return func(*args, **kwargs)

        return decorated

    return wrapper


def validate_role_fluid_reqs(email: str, role: str) -> bool:
    """Validates that new users belong to Fluid Attacks before granting them
    a restricted role"""
    restricted_roles = {"customer_manager"}
    if role not in restricted_roles or (
        role in restricted_roles and email.endswith(FLUIDATTACKS_EMAIL_SUFFIX)
    ):
        return True
    raise InvalidUserProvided()


def validate_role_fluid_reqs_deco(
    email_field: str, role_field: str
) -> Callable:
    """Makes sure that Fluid Attacks groups have only Fluid attacks staff."""

    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            email = str(kwargs.get(email_field))
            role = str(kwargs.get(role_field))

            restricted_roles = {"customer_manager"}
            if role not in restricted_roles or (
                role in restricted_roles
                and email.endswith(FLUIDATTACKS_EMAIL_SUFFIX)
            ):
                res = func(*args, **kwargs)
                return res
            raise InvalidUserProvided()

        return decorated

    return wrapper
