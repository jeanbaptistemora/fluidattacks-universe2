# Starlette app init file

from . import (
    utils,
)
from .middleware import (
    CustomRequestMiddleware,
)
from .views import (
    auth,
    charts,
    evidence,
)
from aioextensions import (
    in_thread,
)
from api import (
    IntegratesAPI,
)
from api.extensions.opentelemetry import (
    OpenTelemetryExtension,
)
from api.schema import (
    SCHEMA,
)
from api.validations.characters import (
    validate_characters,
)
from api.validations.query_breadth import (
    QueryBreadthValidation,
)
from api.validations.query_depth import (
    QueryDepthValidation,
)
from api.validations.variables_validation import (
    variables_check,
)
from billing.domain import (
    webhook,
)
import bugsnag
from bugsnag.asgi import (
    BugsnagMiddleware,
)
from context import (
    FI_ENVIRONMENT,
    FI_STARLETTE_SESSION_KEY,
)
from custom_exceptions import (
    ExpiredToken,
    InvalidAuthorization,
    SecureAccessException,
    StakeholderNotInGroup,
    StakeholderNotInOrganization,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.organization_access.types import (
    OrganizationAccess,
)
from decorators import (
    authenticate_session,
)
from dynamodb.resource import (
    dynamo_shutdown,
    dynamo_startup,
)
from graphql import (
    DocumentNode,
    ValidationRule,
)
from group_access import (
    domain as group_access_domain,
)
from groups import (
    domain as groups_domain,
)
import logging
import logging.config
from newutils import (
    analytics,
    templates,
)
from organizations import (
    domain as orgs_domain,
)
from redis_cluster.operations import (
    redis_del_by_deps_soon,
    redis_del_entity_attr,
)
from remove_stakeholder import (
    domain as remove_stakeholder_domain,
)
from search.client import (
    search_shutdown,
    search_startup,
)
from sessions import (
    dal as sessions_dal,
)
from settings import (
    DEBUG,
    JWT_COOKIE_NAME,
    LOGGING,
    TEMPLATES_DIR,
)
from stakeholders import (
    domain as stakeholders_domain,
)
from starlette.applications import (
    Starlette,
)
from starlette.middleware import (
    Middleware,
)
from starlette.middleware.sessions import (
    SessionMiddleware,
)
from starlette.requests import (
    Request,
)
from starlette.responses import (
    HTMLResponse,
    RedirectResponse,
)
from starlette.routing import (
    Mount,
    Route,
)
from starlette.staticfiles import (
    StaticFiles,
)
from telemetry.instrumentation import (
    instrument,
)
from typing import (
    Any,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)


@authenticate_session
async def app(request: Request) -> HTMLResponse:
    """View for authenticated users"""
    email = request.session.get("username")
    try:
        if email:
            if FI_ENVIRONMENT == "production":
                await stakeholders_domain.check_session_web_validity(request)
            response = templates.main_app(request)
            jwt_token = await utils.create_session_token(request.session)
            utils.set_token_in_response(response, jwt_token)
        else:
            response = templates.unauthorized(request)
            response.delete_cookie(key=JWT_COOKIE_NAME)
    except (ExpiredToken, SecureAccessException):
        response = await logout(request)
    return response


async def confirm_access(request: Request) -> HTMLResponse:
    url_token = request.path_params.get("url_token")
    loaders: Dataloaders = get_new_context()
    if url_token:
        try:
            group_access = await group_access_domain.get_access_by_url_token(
                loaders, url_token
            )
            success = (
                await groups_domain.complete_register_for_group_invitation(
                    loaders, group_access
                )
            )
            if success:
                response = await templates.valid_invitation_typed(
                    request, group_access
                )
            else:
                response = templates.invalid_invitation(
                    request,
                    "Invalid or Expired",
                    group_access,
                )
        except StakeholderNotInGroup:
            await in_thread(
                bugsnag.notify, Exception("Invalid token"), severity="warning"
            )
            response = templates.invalid_invitation(
                request, "Invalid or Expired"
            )
    else:
        response = templates.invalid_invitation(request, "Invalid or Expired")
    return response


async def confirm_deletion(request: Request) -> HTMLResponse:
    url_token = request.path_params.get("url_token")
    loaders: Dataloaders = get_new_context()
    if url_token:
        try:
            user_email: str = (
                await remove_stakeholder_domain.get_email_from_url_token(
                    loaders=loaders, url_token=url_token
                )
            )
            if user_email:
                await remove_stakeholder_domain.complete_deletion(
                    loaders=loaders, email=user_email
                )
                response = await templates.confirm_deletion(request=request)
            else:
                await in_thread(
                    bugsnag.notify,
                    Exception("Invalid token"),
                    severity="error",
                )
                response = templates.invalid_confirm_deletion(
                    request=request, error="Invalid or Expired"
                )
        except InvalidAuthorization:
            response = templates.invalid_confirm_deletion(
                request=request, error="Invalid or Expired"
            )
    else:
        response = templates.invalid_confirm_deletion(
            request=request, error="Invalid or Expired"
        )

    return response


async def confirm_access_organization(request: Request) -> HTMLResponse:
    url_token = request.path_params.get("url_token")
    loaders: Dataloaders = get_new_context()
    if url_token:
        try:
            organization_access: OrganizationAccess = (
                await orgs_domain.get_access_by_url_token(loaders, url_token)
            )

            success = await (
                orgs_domain.complete_register_for_organization_invitation(
                    loaders, organization_access
                )
            )
            if success:
                response = await templates.valid_invitation_typed(
                    request, organization_access
                )
            else:
                response = templates.invalid_invitation(
                    request,
                    "Invalid or Expired",
                    access=organization_access,
                )
        except StakeholderNotInOrganization:
            await in_thread(
                bugsnag.notify, Exception("Invalid token"), severity="warning"
            )
            response = templates.invalid_invitation(
                request, "Invalid or Expired"
            )
    else:
        response = templates.invalid_invitation(request, "Invalid or Expired")
    return response


async def reject_access(request: Request) -> HTMLResponse:
    url_token = request.path_params.get("url_token")
    loaders: Dataloaders = get_new_context()
    if url_token:
        try:
            group_access = await group_access_domain.get_access_by_url_token(
                loaders, url_token
            )
            invitation = group_access.invitation
            if invitation and invitation.is_used:
                return templates.invalid_invitation(
                    request,
                    "Invalid or Expired",
                    group_access,
                )
            success = await groups_domain.reject_register_for_group_invitation(
                loaders, group_access
            )
            if success:
                group_name = group_access.group_name
                redis_del_by_deps_soon(
                    "reject_access",
                    group_name=group_name,
                )
                response = await templates.reject_invitation_typed(
                    request, group_access
                )
            else:
                response = templates.invalid_invitation(
                    request,
                    "Invalid or Expired",
                    group_access,
                )
        except StakeholderNotInGroup:
            await in_thread(
                bugsnag.notify, Exception("Invalid token"), severity="warning"
            )
            response = templates.invalid_invitation(
                request, "Invalid or Expired"
            )
    else:
        response = templates.invalid_invitation(request, "Invalid or Expired")
    return response


async def reject_access_organization(request: Request) -> HTMLResponse:
    url_token = request.path_params.get("url_token")
    loaders: Dataloaders = get_new_context()
    if url_token:
        try:
            organization_access: OrganizationAccess = (
                await orgs_domain.get_access_by_url_token(loaders, url_token)
            )

            success = await (
                orgs_domain.reject_register_for_organization_invitation(
                    loaders, organization_access
                )
            )
            if success:
                organization_id: str = organization_access.organization_id
                redis_del_by_deps_soon(
                    "reject_access_organization",
                    organization_id=organization_id,
                )
                response = await templates.reject_invitation_typed(
                    request, organization_access
                )
            else:
                response = templates.invalid_invitation(
                    request, "Invalid or Expired", organization_access
                )
        except StakeholderNotInOrganization:
            await in_thread(
                bugsnag.notify, Exception("Invalid token"), severity="warning"
            )
            response = templates.invalid_invitation(
                request, "Invalid or Expired"
            )
    else:
        response = templates.invalid_invitation(request, "Invalid or Expired")
    return response


async def logout(request: Request) -> HTMLResponse:
    """Close a user's active session"""
    if "username" in request.session:
        user_email = request.session["username"]
        await sessions_dal.remove_session_key(user_email, "web")
        await sessions_dal.remove_session_key(user_email, "jwt")
        await redis_del_entity_attr(
            entity="session", attr="jti", email=user_email
        )
        await analytics.mixpanel_track(user_email, "Logout")

    request.session.clear()
    response = RedirectResponse("/")
    response.delete_cookie(key=JWT_COOKIE_NAME)
    response.headers["Clear-Site-Data"] = '"executionContexts", "cache"'
    return response


async def not_found(request: Request, ex: Exception) -> HTMLResponse:
    LOGGER.exception(ex, extra=dict(extra=locals()))
    return templates.error401(request)


async def server_error(request: Request, ex: Exception) -> HTMLResponse:
    LOGGER.exception(ex, extra=dict(extra=locals()))
    return templates.error500(request)


exception_handlers = {404: not_found, 500: server_error}

API_EXTENSIONS = (OpenTelemetryExtension,)


def get_validation_rules(
    context_value: Any, _document: DocumentNode, _data: dict[str, Any]
) -> tuple[ValidationRule, ...]:
    return (
        QueryBreadthValidation,
        QueryDepthValidation,
        validate_characters(context_value),
        variables_check(context_value),
    )


STARLETTE_APP = Starlette(
    debug=DEBUG,
    on_startup=[dynamo_startup, search_startup],
    on_shutdown=[dynamo_shutdown, search_shutdown],
    routes=[
        Route("/", templates.login),
        Route(
            "/api",
            IntegratesAPI(
                SCHEMA,
                debug=DEBUG,
                extensions=API_EXTENSIONS,
                validation_rules=get_validation_rules,
            ),
        ),
        Route("/authz_azure", auth.authz_azure),
        Route("/authz_bitbucket", auth.authz_bitbucket),
        Route("/authz_google", auth.authz_google),
        Route("/confirm_access/{url_token:path}", confirm_access),
        Route(
            "/confirm_access_organization/{url_token:path}",
            confirm_access_organization,
        ),
        Route(
            "/confirm_deletion/{url_token:path}",
            confirm_deletion,
        ),
        Route("/dglogin", auth.do_google_login),
        Route("/dalogin", auth.do_azure_login),
        Route("/dblogin", auth.do_bitbucket_login),
        Route("/error401", templates.error401),
        Route("/error500", templates.error500),
        Route("/graphic", charts.graphic),
        Route("/graphics-for-group", charts.graphics_for_group),
        Route("/graphics-for-organization", charts.graphics_for_organization),
        Route("/graphics-for-portfolio", charts.graphics_for_portfolio),
        Route("/graphics-report", charts.graphics_report),
        Route("/invalid_invitation", templates.invalid_invitation),
        Route("/logout", logout),
        Route(
            "/orgs/{org_name:str}/groups/"
            "{group_name:str}/{evidence_type:str}/"
            "{finding_id:str}/{_:str}/{file_id:str}",
            evidence.get_evidence,
        ),
        Route("/reject_access/{url_token:path}", reject_access),
        Route(
            "/reject_access_organization/{url_token:path}",
            reject_access_organization,
        ),
        Mount(
            "/static",
            StaticFiles(directory=f"{TEMPLATES_DIR}/static"),
            name="static",
        ),
        Route("/billing", webhook, methods=["POST"]),
        Route("/{full_path:path}", app),
    ],
    middleware=[
        Middleware(SessionMiddleware, secret_key=FI_STARLETTE_SESSION_KEY),
        Middleware(CustomRequestMiddleware),
    ],
    exception_handlers=exception_handlers,
)

# ASGI wrappers
instrument(STARLETTE_APP)
BUGSNAG_WRAPPER = BugsnagMiddleware(STARLETTE_APP)

APP = BUGSNAG_WRAPPER
