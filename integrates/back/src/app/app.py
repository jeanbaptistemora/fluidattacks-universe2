# Starlette app init file

"""
IMPORTANT
Unlike standard Python functionality, the import order matters:
the agent package must be imported first.
"""
# flake8: noqa
import newrelic.agent
from newutils.utils import (
    get_key_or_fallback,
)
from settings import (
    DEBUG,
    JWT_COOKIE_NAME,
    LOGGING,
    NEW_RELIC_CONF_FILE,
    queue,
    TEMPLATES_DIR,
)

newrelic.agent.initialize(NEW_RELIC_CONF_FILE)
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
    schedule,
)
from api import (
    IntegratesAPI,
)
from api.extensions.new_relic import (
    NewRelicTracingExtension,
)
from api.schema import (
    SCHEMA,
)
from api.validations.query_breadth import (
    QueryBreadthValidation,
)
from api.validations.query_depth import (
    QueryDepthValidation,
)
import asyncio
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
    SecureAccessException,
)
from dataloaders import (
    get_new_context,
)
from decorators import (
    authenticate_session,
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
from sessions import (
    dal as sessions_dal,
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
from users import (
    domain as users_domain,
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
                await users_domain.check_session_web_validity(request)

            if not await orgs_domain.get_user_organizations(email):
                response = templates.unauthorized(request)
            else:
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
    if url_token:
        group_access = await group_access_domain.get_access_by_url_token(
            url_token
        )
        if group_access:
            success = (
                await groups_domain.complete_register_for_group_invitation(
                    group_access
                )
            )
            if success:
                response = await templates.valid_invitation(
                    request, group_access
                )
                schedule(
                    groups_domain.after_complete_register(
                        get_new_context(), group_access
                    )
                )
            else:
                response = templates.invalid_invitation(
                    request,
                    "Invalid or Expired",
                    group_access=group_access,
                )
        else:
            await in_thread(
                bugsnag.notify, Exception("Invalid token"), severity="warning"
            )
            response = templates.invalid_invitation(
                request, "Invalid or Expired"
            )
    else:
        response = templates.invalid_invitation(request, "Invalid or Expired")
    return response


async def confirm_access_organization(request: Request) -> HTMLResponse:
    url_token = request.path_params.get("url_token")
    if url_token:
        organization_access = await orgs_domain.get_access_by_url_token(
            url_token
        )
        if organization_access:
            success = await (
                groups_domain.complete_register_for_organization_invitation(
                    organization_access
                )
            )
            if success:
                response = await templates.valid_invitation(
                    request, organization_access
                )
            else:
                response = templates.invalid_invitation(
                    request,
                    "Invalid or Expired",
                    group_access=organization_access,
                )
        else:
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
    if url_token:
        group_access = await group_access_domain.get_access_by_url_token(
            url_token
        )
        if group_access:
            success = await groups_domain.reject_register_for_group_invitation(
                get_new_context(), group_access
            )
            if success:
                group_name: str = str(get_key_or_fallback(group_access))
                redis_del_by_deps_soon(
                    "reject_access",
                    group_name=group_name,
                )
                response = await templates.reject_invitation(
                    request, group_access
                )
            else:
                response = templates.invalid_invitation(
                    request,
                    "Invalid or Expired",
                    group_access=group_access,
                )
        else:
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
    if url_token:
        organization_access = await orgs_domain.get_access_by_url_token(
            url_token
        )
        if organization_access:
            success = await (
                orgs_domain.reject_register_for_organization_invitation(
                    get_new_context(), organization_access
                )
            )
            if success:
                response = await templates.reject_invitation(
                    request, organization_access
                )
            else:
                response = templates.invalid_invitation(
                    request,
                    "Invalid or Expired",
                    organization_access=organization_access,
                )
        else:
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


async def queue_daemon() -> None:
    queue.init_queue()
    while True:
        func = await queue.get_task()
        if asyncio.iscoroutinefunction(func):
            await func()
        else:
            await in_thread(func)


def start_queue_daemon() -> None:
    asyncio.create_task(queue_daemon())


async def not_found(request: Request, ex: Exception) -> HTMLResponse:
    LOGGER.exception(ex, extra=dict(extra=locals()))
    return templates.error401(request)


async def server_error(request: Request, ex: Exception) -> HTMLResponse:
    LOGGER.exception(ex, extra=dict(extra=locals()))
    return templates.error500(request)


exception_handlers = {404: not_found, 500: server_error}

API_EXTENSIONS = [
    NewRelicTracingExtension,
]

API_VALIDATIONS = [
    QueryBreadthValidation,
    QueryDepthValidation,
]

STARLETTE_APP = Starlette(
    debug=DEBUG,
    routes=[
        Route("/", templates.login),
        Route(
            "/api",
            IntegratesAPI(
                SCHEMA,
                debug=DEBUG,
                extensions=API_EXTENSIONS,
                validation_rules=API_VALIDATIONS,
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
        Route("/crashtest-0b9079cc.html", templates.crashtest),
        Route("/{full_path:path}", app),
    ],
    middleware=[
        Middleware(SessionMiddleware, secret_key=FI_STARLETTE_SESSION_KEY),
        Middleware(CustomRequestMiddleware),
    ],
    on_startup=[start_queue_daemon],
    exception_handlers=exception_handlers,
)

# ASGI wrappers
NEWRELIC_WRAPPER = newrelic.agent.ASGIApplicationWrapper(STARLETTE_APP)
BUGSNAG_WRAPPER = BugsnagMiddleware(NEWRELIC_WRAPPER)

APP = BUGSNAG_WRAPPER
