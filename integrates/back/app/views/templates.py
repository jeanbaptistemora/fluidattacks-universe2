# Starlette templates renders

# Standard library
import json
import traceback

# Third party libraries
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

# Local librariessettings
from custom_types import (
    GraphicParameters,
    ProjectAccess as ProjectAccessType,
)
from settings import (
    DEBUG,
    STATIC_URL,
    TEMPLATES_DIR,
)


TEMPLATING_ENGINE = Jinja2Templates(directory=TEMPLATES_DIR)


def error500(request: Request) -> HTMLResponse:
    return TEMPLATING_ENGINE.TemplateResponse(
        name="HTTP500.html", context={"request": request}
    )


def error401(request: Request) -> HTMLResponse:
    return TEMPLATING_ENGINE.TemplateResponse(
        name="HTTP401.html", context={"request": request}
    )


def invalid_invitation(
    request: Request,
    error: str,
    project_access: ProjectAccessType = None,
) -> HTMLResponse:
    group_name = (
        project_access.get("project_name", "") if project_access else ""
    )
    return TEMPLATING_ENGINE.TemplateResponse(
        name="invalid_invitation.html",
        context={
            "error": error,
            "group_name": group_name,
            "request": request,
        },
    )


async def valid_invitation(
    request: Request, project_access: ProjectAccessType
) -> HTMLResponse:
    group_name = project_access["project_name"]
    return TEMPLATING_ENGINE.TemplateResponse(
        name="valid_invitation.html",
        context={
            "group_name": group_name,
            "request": request,
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
