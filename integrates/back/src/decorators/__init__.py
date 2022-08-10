from aioextensions import (
    collect,
    schedule,
)
import asyncio
from asyncio import (
    sleep,
)
import authz
import contextlib
from custom_exceptions import (
    FindingNotFound,
    InvalidAuthorization,
    InvalidPositiveArgument,
    OnlyCorporateEmails,
    StakeholderNotInOrganization,
)
from db_model.events.types import (
    Event,
)
from db_model.findings.types import (
    Finding,
)
from db_model.groups.types import (
    Group,
)
from db_model.organizations.types import (
    Organization,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from decorators.utils import (
    is_personal_email,
)
import functools
from graphql import (
    GraphQLError,
)
import inspect
import logging
import logging.config
from newutils import (
    function,
    logs as logs_utils,
    organizations as orgs_utils,
    templates as templates_utils,
    token as token_utils,
    validations,
)
from newutils.utils import (
    get_key_or_fallback,
)
from organizations import (
    domain as orgs_domain,
)
from settings import (
    DEBUG,
    LOGGING,
)
from stakeholders import (
    domain as stakeholders_domain,
)
import time
from typing import (
    Any,
    Callable,
    cast,
    Dict,
    Set,
    Tuple,
    Type,
    TypeVar,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
UNAUTHORIZED_ROLE_MSG = (
    "Security: Unauthorized role attempted to perform operation"
)
UNAUTHORIZED_OWNER_MSG = (
    "Security: Unauthorized owner attempted to perform operation"
)
UNAVAILABLE_FINDING_MSG = (
    "Security: The user attempted to operate on an unavailable finding"
)

# Typing
TVar = TypeVar("TVar")
TFun = TypeVar("TFun", bound=Callable[..., Any])


async def _resolve_from_event_id(context: Any, identifier: str) -> str:
    event_loader = context.loaders.event
    data: Event = await event_loader.load(identifier)
    group_name = data.group_name
    return group_name


async def _resolve_from_finding_id(context: Any, identifier: str) -> str:
    validations.validate_finding_id(identifier)
    finding_loader = context.loaders.finding
    finding: Finding = await finding_loader.load(identifier)
    return finding.group_name


async def _resolve_from_vuln_id(context: Any, identifier: str) -> str:
    loaders = context.loaders
    vulnerability: Vulnerability = await loaders.vulnerability.load(identifier)
    group_name = await _resolve_from_finding_id(
        context, vulnerability.finding_id
    )
    return group_name


def authenticate_session(func: TFun) -> TFun:
    @functools.wraps(func)
    async def authenticate_and_call(*args: Any, **kwargs: Any) -> Any:
        request = args[0]
        if (
            "username" not in request.session
            or request.session["username"] is None
        ):
            return templates_utils.unauthorized(request)
        return await func(*args, **kwargs)

    return cast(TFun, authenticate_and_call)


def concurrent_decorators(
    *decorators: Callable[[Any], Any],
) -> Callable[[TFun], TFun]:
    """Decorator to fusion many decorators which will be executed concurrently.

    Either:
    - All decorators succeed and the decorated function is called,
    - Any decorator fail and the error is propagated to the caller.

    In the second case the propagated error is guaranteed to come from the
    first task to raise.
    """
    if len(decorators) <= 1:
        raise ValueError("Expected at least 2 decorators as arguments")

    def decorator(func: TFun) -> TFun:
        @functools.wraps(func)
        async def dummy(*_: Any, **__: Any) -> bool:
            """Dummy function to mimic `func`."""
            return True

        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            success = []
            tasks = iter(
                list(
                    map(
                        schedule,
                        [dec(dummy)(*args, **kwargs) for dec in decorators],
                    )
                )
            )

            try:
                for task in tasks:
                    task_result = await task
                    success.append(task_result.result())  # may rise
            finally:
                # If two or more decorators raised exceptions let's propagate
                # only the first to arrive and cancel the remaining ones
                # to avoid an ugly traceback, also because if one failed
                # there is no purpose in letting the remaining ones run
                for task in tasks:
                    task.cancel()

            # If everything succeed let's call the decorated function
            if success and all(success):
                return await func(*args, **kwargs)

            # May never happen as decorators raise something on errors
            # But it's nice to have a default value here
            raise RuntimeError("Decorators did not success")

        return cast(TFun, wrapper)

    return decorator


def delete_kwargs(attributes: Set[str]) -> Callable[[TVar], TVar]:
    """Decorator to delete function's kwargs.
    Useful to perform api migration.
    """

    def wrapped(func: TVar) -> TVar:
        _func = cast(Callable[..., Any], func)

        @functools.wraps(_func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            kwargs = {
                key: val
                for key, val in kwargs.items()
                if key not in attributes
            }
            return _func(*args, **kwargs)

        return cast(TVar, decorated)

    return wrapped


def enforce_group_level_auth_async(func: TVar) -> TVar:
    """Enforce authorization using the group-level role."""
    _func = cast(Callable[..., Any], func)

    @functools.wraps(_func)
    async def verify_and_call(*args: Any, **kwargs: Any) -> Any:
        if hasattr(args[0], "context") and not isinstance(args[0], Group):
            context = args[0].context
        elif hasattr(args[1], "context") and not isinstance(args[1], Group):
            context = args[1].context
        else:
            GraphQLError("Could not get context from request.")  # NOSONAR

        if isinstance(context, dict):
            context = context.get("request", {})
        store = token_utils.get_request_store(context)
        user_data = await token_utils.get_jwt_content(context)
        subject = user_data["user_email"]
        object_ = await resolve_group_name(context, args, kwargs)
        action = f"{_func.__module__}.{_func.__qualname__}".replace(".", "_")

        if not object_:
            LOGGER.error(
                "Unable to identify group name",
                extra={
                    "extra": {
                        "action": action,
                        "subject": subject,
                    }
                },
            )

        enforcer = await authz.get_group_level_enforcer(subject, store)
        if not enforcer(object_, action):
            logs_utils.cloudwatch_log(context, UNAUTHORIZED_ROLE_MSG)
            raise GraphQLError("Access denied")  # NOSONAR

        if asyncio.iscoroutinefunction(_func):
            return await _func(*args, **kwargs)

        return _func(*args, **kwargs)

    return cast(TVar, verify_and_call)


def enforce_organization_level_auth_async(func: TVar) -> TVar:
    """Enforce authorization using the organization-level role."""
    _func = cast(Callable[..., Any], func)

    @functools.wraps(_func)
    async def verify_and_call(*args: Any, **kwargs: Any) -> Any:
        if hasattr(args[0], "context"):
            context = args[0].context
        elif hasattr(args[1], "context"):
            context = args[1].context
        else:
            GraphQLError("Could not get context from request.")

        organization_identifier = str(
            kwargs.get("identifier")
            or kwargs.get("organization_id")
            or kwargs.get("organization_name")
            or (getattr(args[0], "organization_id", None) if args else None)
            or orgs_utils.add_org_id_prefix(args[0].id)
        )
        loaders = context.loaders
        organization: Organization = await loaders.organization.load(
            organization_identifier
        )
        organization_id = organization.id
        user_data = await token_utils.get_jwt_content(context)
        subject = user_data["user_email"]
        object_ = organization_id.lower()
        action = f"{_func.__module__}.{_func.__qualname__}".replace(".", "_")

        if not object_:
            LOGGER.error(
                "Unable to identify organization to check permissions",
                extra={
                    "action": action,
                    "subject": subject,
                },
            )
        enforcer = await authz.get_organization_level_enforcer(subject)
        if not enforcer(object_, action):
            logs_utils.cloudwatch_log(context, UNAUTHORIZED_ROLE_MSG)
            raise GraphQLError("Access denied")
        if asyncio.iscoroutinefunction(_func):
            return await _func(*args, **kwargs)

        return _func(*args, **kwargs)

    return cast(TVar, verify_and_call)


def enforce_user_level_auth_async(func: TVar) -> TVar:
    """Enforce authorization using the user-level role."""
    _func = cast(Callable[..., Any], func)

    @functools.wraps(_func)
    async def verify_and_call(*args: Any, **kwargs: Any) -> Any:
        if hasattr(args[0], "context"):
            context = args[0].context
        elif hasattr(args[1], "context"):
            context = args[1].context
        else:
            GraphQLError("Could not get context from request.")

        user_data = await token_utils.get_jwt_content(context)
        subject = user_data["user_email"]
        object_ = "self"
        action = f"{_func.__module__}.{_func.__qualname__}".replace(".", "_")

        enforcer = await authz.get_user_level_enforcer(subject)
        if not enforcer(object_, action):
            logs_utils.cloudwatch_log(context, UNAUTHORIZED_ROLE_MSG)
            raise GraphQLError("Access denied")
        return await _func(*args, **kwargs)

    return cast(TVar, verify_and_call)


def enforce_owner(func: TVar) -> TVar:
    """Enforce authorization using the owner attribute."""
    _func = cast(Callable[..., Any], func)

    @functools.wraps(_func)
    async def verify_and_call(*args: Any, **kwargs: Any) -> Any:
        if hasattr(args[0], "context"):
            context = args[0].context
        elif hasattr(args[1], "context"):
            context = args[1].context
        else:
            GraphQLError("Could not get context from request.")

        loaders = context.loaders
        owner = str((getattr(args[0], "owner", None) if args else None))

        user_data = await token_utils.get_jwt_content(context)
        subject = user_data["user_email"]
        if owner != subject:
            stakeholder_level_role = await authz.get_user_level_role(
                loaders=loaders, email=subject
            )
            if stakeholder_level_role != "admin":
                logs_utils.cloudwatch_log(context, UNAUTHORIZED_OWNER_MSG)
                raise GraphQLError("Access denied")

        if asyncio.iscoroutinefunction(_func):
            return await _func(*args, **kwargs)

        return _func(*args, **kwargs)

    return cast(TVar, verify_and_call)


def rename_kwargs(mapping: Dict[str, str]) -> Callable[[TVar], TVar]:
    """Decorator to rename function's kwargs.
    Useful to perform breaking changes,
    with backwards compatibility.
    """

    def wrapped(func: TVar) -> TVar:
        _func = cast(Callable[..., Any], func)

        def rename(kwargs: Dict[str, Any]) -> Dict[str, Any]:
            return {mapping.get(key, key): val for key, val in kwargs.items()}

        if asyncio.iscoroutinefunction(_func):

            @functools.wraps(_func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return await _func(*args, **rename(kwargs))

            return cast(TVar, async_wrapper)

        @functools.wraps(_func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return _func(*args, **rename(kwargs))

        return cast(TVar, wrapper)

    return wrapped


def require_attribute(attribute: str) -> Callable[[TVar], TVar]:
    def wrapper(func: TVar) -> TVar:
        _func = cast(Callable[..., Any], func)

        @functools.wraps(_func)
        async def resolve_and_call(*args: Any, **kwargs: Any) -> Any:
            if hasattr(args[0], "context") and not isinstance(args[0], Group):
                context = args[0].context
            elif hasattr(args[1], "context") and not isinstance(
                args[1], Group
            ):
                context = args[1].context
            else:
                GraphQLError("Could not get context from request.")

            if isinstance(context, dict):
                context = context.get("request", {})
            store = token_utils.get_request_store(context)
            group_name = await resolve_group_name(context, args, kwargs)
            loaders = context.loaders
            group: Group = await loaders.group.load(group_name)

            # Unique ID for this decorator function
            context_store_key: str = function.get_id(
                require_attribute,
                attribute,
                group_name,
            )

            # Within the context of one request we only need to check this once
            # Future calls to this decorator will be passed through
            if not store[context_store_key]:
                enforcer = await authz.get_group_service_attributes_enforcer(
                    group,
                )
                if not enforcer(attribute):
                    raise GraphQLError("Access denied")
            store[context_store_key] = True
            return await _func(*args, **kwargs)

        return cast(TVar, resolve_and_call)

    return wrapper


# Factory functions
REQUIRE_CONTINUOUS = require_attribute("is_continuous")
REQUIRE_SQUAD = require_attribute("has_squad")
REQUIRE_ASM = require_attribute("has_asm")
REQUIRE_SERVICE_BLACK = require_attribute("has_service_black")
REQUIRE_SERVICE_WHITE = require_attribute("has_service_white")
REQUIRE_REPORT_VULNERABILITIES = require_attribute(
    "can_report_vulnerabilities"
)


def require_continuous(func: TVar) -> TVar:
    return REQUIRE_CONTINUOUS(func)


def require_service_black(func: TVar) -> TVar:
    return REQUIRE_SERVICE_BLACK(func)


def require_service_white(func: TVar) -> TVar:
    return REQUIRE_SERVICE_WHITE(func)


def require_finding_access(func: TVar) -> TVar:
    """
    Require_finding_access decorator.
    Verifies that the current user has access to a given finding
    """
    _func = cast(Callable[..., Any], func)

    @functools.wraps(_func)
    async def verify_and_call(*args: Any, **kwargs: Any) -> Any:
        context = args[1].context
        if "finding_id" in kwargs:
            finding_id = kwargs["finding_id"]
        elif "draft_id" in kwargs:
            finding_id = kwargs["draft_id"]
        elif "identifier" in kwargs:
            finding_id = kwargs["identifier"]
        else:
            vulnerability: Vulnerability = (
                await context.loaders.vulnerability.load(kwargs["vuln_uuid"])
            )
            finding_id = vulnerability.finding_id

        validations.validate_finding_id(finding_id)
        finding_loader = context.loaders.finding
        try:
            await finding_loader.load(finding_id)
        except FindingNotFound:
            logs_utils.cloudwatch_log(context, UNAVAILABLE_FINDING_MSG)
            raise

        return await _func(*args, **kwargs)

    return cast(TVar, verify_and_call)


def require_asm(func: TVar) -> TVar:
    return REQUIRE_ASM(func)


def require_squad(func: TVar) -> TVar:
    return REQUIRE_SQUAD(func)


def require_report_vulnerabilities(func: TVar) -> TVar:
    return REQUIRE_REPORT_VULNERABILITIES(func)


def require_corporate_email(func: Callable[..., Any]) -> TVar:
    """
    Verifies the domain on the email address does not belong to a free email
    service
    """

    @functools.wraps(func)
    async def verify_and_call(*args: Any, **kwargs: Any) -> Any:
        context = args[1].context
        user_data = await token_utils.get_jwt_content(context)

        if await is_personal_email(user_data["user_email"]):
            raise OnlyCorporateEmails()

        return await func(*args, **kwargs)

    return cast(TVar, verify_and_call)


def require_login(func: TVar) -> TVar:
    """
    Require_login decorator
    Verifies that the user is logged in with a valid JWT
    """
    _func = cast(Callable[..., Any], func)

    # Unique ID for this decorator function
    context_store_key: str = function.get_id(require_login)

    @functools.wraps(_func)
    async def verify_and_call(*args: Any, **kwargs: Any) -> Any:
        # The underlying request object being served
        context = args[1].context if len(args) > 1 else args[0]
        if isinstance(context, dict):
            context = context.get("request", {})
        store = token_utils.get_request_store(context)

        # Within the context of one request we only need to check this once
        # Future calls to this decorator will be passed trough
        if store[context_store_key]:
            return await _func(*args, **kwargs)

        try:
            user_data: Any = await token_utils.get_jwt_content(context)
            if token_utils.is_api_token(user_data):
                await verify_jti(
                    context.loaders,
                    user_data["user_email"],
                    context.headers.get("Authorization"),
                    user_data["jti"],
                )
        except InvalidAuthorization:
            raise GraphQLError("Login required") from None
        else:
            store[context_store_key] = True
            return await _func(*args, **kwargs)

    return cast(TVar, verify_and_call)


def require_organization_access(func: TVar) -> TVar:
    """
    Decorator
    Verifies that the user trying to fetch information belongs to the
    organization
    """
    _func = cast(Callable[..., Any], func)

    @functools.wraps(_func)
    async def verify_and_call(*args: Any, **kwargs: Any) -> Any:
        if hasattr(args[0], "context"):
            context = args[0].context
        elif hasattr(args[1], "context"):
            context = args[1].context
        organization_identifier = str(
            kwargs.get("identifier")
            or kwargs.get("organization_id")
            or kwargs.get("organization_name")
            or (getattr(args[0], "organization_id", None) if args else None)
        )

        user_data = await token_utils.get_jwt_content(context)
        user_email = user_data["user_email"]
        loaders = context.loaders
        organization: Organization = await loaders.organization.load(
            organization_identifier
        )
        organization_id = organization.id
        role, has_access = await collect(
            [
                authz.get_organization_level_role(user_email, organization_id),
                orgs_domain.has_access(loaders, organization_id, user_email),
            ]
        )

        if role != "admin" and not has_access:
            logs_utils.cloudwatch_log(
                context,
                f"Security: User {user_email} attempted to access "
                f"organization {organization_identifier} without permission",
            )
            raise StakeholderNotInOrganization()
        return await _func(*args, **kwargs)

    return cast(TVar, verify_and_call)


async def resolve_group_name(  # noqa: MC0001
    context: Any,
    args: Any,
    kwargs: Any,
) -> str:
    """Get group name based on args passed."""
    if args and args[0] and isinstance(args[0], Vulnerability):
        vuln: Vulnerability = args[0]
        name = vuln.group_name
    elif args and args[0] and isinstance(args[0], Group):
        group: Group = args[0]
        name = group.name
    elif args and args[0] and hasattr(args[0], "group_name"):
        name = getattr(args[0], "group_name")
    elif args and args[0] and isinstance(args[0], dict) and "name" in args[0]:
        name = args[0]["name"]
    elif (
        args
        and args[0]
        and isinstance(args[0], dict)
        and "project_name" in args[0]
    ):
        name = args[0]["project_name"]
    elif (
        args
        and args[0]
        and isinstance(args[0], dict)
        and "finding_id" in args[0]
    ):
        name = await _resolve_from_finding_id(context, args[0]["finding_id"])
    elif "group_name" in kwargs or "project_name" in kwargs:
        name = get_key_or_fallback(kwargs)
    elif "finding_id" in kwargs:
        name = await _resolve_from_finding_id(context, kwargs["finding_id"])
    elif "draft_id" in kwargs:
        name = await _resolve_from_finding_id(context, kwargs["draft_id"])
    elif "event_id" in kwargs:
        name = await _resolve_from_event_id(context, kwargs["event_id"])
    elif "vuln_id" in kwargs:
        name = await _resolve_from_vuln_id(context, kwargs["vuln_id"])
    elif "vulnerability_id" in kwargs:
        name = await _resolve_from_vuln_id(context, kwargs["vulnerability_id"])
    elif "vuln_uuid" in kwargs:
        name = await _resolve_from_vuln_id(context, kwargs["vuln_uuid"])
    elif "vulnerability_uuid" in kwargs:
        name = await _resolve_from_vuln_id(
            context, kwargs["vulnerability_uuid"]
        )
    elif DEBUG:
        raise Exception("Unable to identify group")
    else:
        name = ""

    if isinstance(name, str):
        name = name.lower()
    return name


def retry_on_exceptions(
    *,
    exceptions: Tuple[Type[Exception], ...],
    max_attempts: int = 5,
    sleep_seconds: float = 0,
) -> Callable[[TVar], TVar]:
    def decorator(func: TVar) -> TVar:
        _func = cast(Callable[..., Any], func)
        if asyncio.iscoroutinefunction(_func):

            @functools.wraps(_func)
            async def wrapper(*args: Any, **kwargs: Any) -> Any:
                for _ in range(max_attempts - 1):
                    with contextlib.suppress(*exceptions):
                        return await _func(*args, **kwargs)

                    await sleep(sleep_seconds)

                return await _func(*args, **kwargs)

        else:

            @functools.wraps(_func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                for _ in range(max_attempts - 1):
                    with contextlib.suppress(*exceptions):
                        return _func(*args, **kwargs)

                    time.sleep(sleep_seconds)

                return _func(*args, **kwargs)

        return cast(TVar, wrapper)

    return decorator


def turn_args_into_kwargs(func: TVar) -> TVar:
    """Turn function's positional-arguments into keyword-arguments.

    Very useful when you want to keep an strongly typed signature in your
    function while using another decorators from this module that work on
    keyword arguments only for backwards compatibility reasons.

    This avoids functions with a typeless **parameters, and then 50 lines
    unpacking the arguments and casting them to the expected types.
    """
    _func = cast(Callable[..., Any], func)

    @functools.wraps(_func)
    async def newfunc(*args: Any, **kwargs: Any) -> Any:
        # The first two arguments are django's self, and info references
        #   They can be safely left intact
        args_as_kwargs = dict(
            zip(inspect.getfullargspec(_func).args[2:], args[2:])
        )
        return await _func(*args[0:2], **args_as_kwargs, **kwargs)

    return cast(TVar, newfunc)


def validate_connection(func: TVar) -> TVar:
    """Decorator to verify the connections"""
    _func = cast(Callable[..., Any], func)

    @functools.wraps(_func)
    async def verify_and_call(*args: Any, **kwargs: Any) -> Any:
        first = kwargs.get("first")
        if first is not None and first < 1:
            raise InvalidPositiveArgument(arg="first")
        return await _func(*args, **kwargs)

    return cast(TVar, verify_and_call)


async def verify_jti(
    loaders: Any, email: str, context: Dict[str, str], jti: str
) -> None:
    if not await stakeholders_domain.has_valid_access_token(
        loaders, email, context, jti
    ):
        raise InvalidAuthorization()
