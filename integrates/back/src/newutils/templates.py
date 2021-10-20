# Starlette templates renders


from custom_types import (
    GraphicParameters,
    GroupAccess as GroupAccessType,
)
import json
import newrelic.agent
from newutils.utils import (
    get_key_or_fallback,
)
from settings import (
    DEBUG,
    STATIC_URL,
    TEMPLATES_DIR,
)
from starlette.requests import (
    Request,
)
from starlette.responses import (
    HTMLResponse,
)
from starlette.templating import (
    Jinja2Templates,
)
import traceback

TEMPLATING_ENGINE = Jinja2Templates(directory=TEMPLATES_DIR)


def error401(request: Request) -> HTMLResponse:
    return TEMPLATING_ENGINE.TemplateResponse(
        name="HTTP401.html", context={"request": request}
    )


def error500(request: Request) -> HTMLResponse:
    return TEMPLATING_ENGINE.TemplateResponse(
        name="HTTP500.html", context={"request": request}
    )


def graphic_error(request: Request) -> HTMLResponse:
    return TEMPLATING_ENGINE.TemplateResponse(
        name="graphic-error.html",
        context=dict(
            request=request,
            debug=DEBUG,
            traceback=traceback.format_exc(),
        ),
    )


def graphics_for_entity_view(request: Request, entity: str) -> HTMLResponse:
    entity_title = entity.title()
    newrelic.agent.disable_browser_autorum()
    return TEMPLATING_ENGINE.TemplateResponse(
        name="graphics-for-entity.html",
        context=dict(
            request=request,
            debug=DEBUG,
            entity=entity_title,
            js=(
                f"{STATIC_URL}/dashboard/"
                f"graphicsFor{entity_title}-bundle.min.js"
            ),
            css=(
                f"{STATIC_URL}/dashboard/"
                f"graphicsFor{entity_title}-style.min.css"
            ),
        ),
    )


def graphic_view(
    request: Request, document: object, params: GraphicParameters
) -> HTMLResponse:
    newrelic.agent.disable_browser_autorum()
    return TEMPLATING_ENGINE.TemplateResponse(
        name="graphic.html",
        context=dict(
            request=request,
            args=dict(
                data=json.dumps(document),
                height=params.height,
                width=params.width,
            ),
            generator_src=(
                f"graphics/"
                f"generators/"
                f"{params.generator_type}/"
                f"{params.generator_name}.js"
            ),
            c3js=f"{STATIC_URL}/external/C3/c3.js",
            c3css=(f"{STATIC_URL}/external/C3/c3.css"),
        ),
    )


def invalid_invitation(
    request: Request,
    error: str,
    group_access: GroupAccessType = None,
) -> HTMLResponse:
    group_name = (
        get_key_or_fallback(group_access, fallback="") if group_access else ""
    )
    return TEMPLATING_ENGINE.TemplateResponse(
        name="invalid_invitation.html",
        context={
            "error": error,
            "group_name": group_name,
            "request": request,
        },
    )


def login(request: Request) -> HTMLResponse:
    return TEMPLATING_ENGINE.TemplateResponse(
        name="login.html",
        context={
            "request": request,
            "debug": DEBUG,
            "js": f"{STATIC_URL}/dashboard/app-bundle.min.js",
            "css": f"{STATIC_URL}/dashboard/app-style.min.css",
        },
    )


def main_app(request: Request) -> HTMLResponse:
    return TEMPLATING_ENGINE.TemplateResponse(
        name="app.html",
        context={
            "request": request,
            "debug": DEBUG,
            "js": f"{STATIC_URL}/dashboard/app-bundle.min.js",
            "css": f"{STATIC_URL}/dashboard/app-style.min.css",
        },
    )


def unauthorized(request: Request) -> HTMLResponse:
    return TEMPLATING_ENGINE.TemplateResponse(
        name="unauthorized.html",
        context={
            "request": request,
            "debug": DEBUG,
        },
    )


async def valid_invitation(
    request: Request, group_access: GroupAccessType
) -> HTMLResponse:
    group_name = get_key_or_fallback(group_access)
    return TEMPLATING_ENGINE.TemplateResponse(
        name="valid_invitation.html",
        context={
            "group_name": group_name,
            "request": request,
        },
    )
