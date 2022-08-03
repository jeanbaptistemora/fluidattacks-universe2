# Starlette templates renders


from custom_types import (
    GraphicParameters,
)
from db_model.group_access.types import (
    GroupAccess,
)
from db_model.organization_access.types import (
    OrganizationAccess,
)
import json
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
from typing import (
    Any,
    Union,
)

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
    return TEMPLATING_ENGINE.TemplateResponse(
        name="graphics-for-entity.html",
        context=dict(
            request=request,
            debug=DEBUG,
            entity=entity_title,
            js_runtime=f"{STATIC_URL}/dashboard/runtime-bundle.min.js",
            js_vendors=f"{STATIC_URL}/dashboard/vendors-bundle.min.js",
            css_vendors=f"{STATIC_URL}/dashboard/vendors-style.min.css",
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


def invalid_invitation(
    request: Request, error: str, entity_name: str = ""
) -> HTMLResponse:
    return TEMPLATING_ENGINE.TemplateResponse(
        name="invalid_invitation.html",
        context={
            "error": error,
            "entity_name": entity_name,
            "request": request,
        },
    )


def login(request: Request) -> HTMLResponse:
    return TEMPLATING_ENGINE.TemplateResponse(
        name="login.html",
        context={
            "request": request,
            "debug": DEBUG,
            "js_runtime": f"{STATIC_URL}/dashboard/runtime-bundle.min.js",
            "js_vendors": f"{STATIC_URL}/dashboard/vendors-bundle.min.js",
            "css_vendors": f"{STATIC_URL}/dashboard/vendors-style.min.css",
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
            "js_runtime": f"{STATIC_URL}/dashboard/runtime-bundle.min.js",
            "js_vendors": f"{STATIC_URL}/dashboard/vendors-bundle.min.js",
            "css_vendors": f"{STATIC_URL}/dashboard/vendors-style.min.css",
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


async def valid_invitation(request: Request, entity_name: str) -> HTMLResponse:
    return TEMPLATING_ENGINE.TemplateResponse(
        name="valid_invitation.html",
        context={
            "entity_name": entity_name,
            "request": request,
        },
    )


async def confirm_deletion(*, request: Request) -> HTMLResponse:

    return TEMPLATING_ENGINE.TemplateResponse(
        name="valid_delete_confirmation.html",
        context={
            "request": request,
        },
    )


def invalid_confirm_deletion(
    *,
    request: Request,
    error: str,
) -> HTMLResponse:

    return TEMPLATING_ENGINE.TemplateResponse(
        name="invalid_delete_confirmation.html",
        context={
            "error": error,
            "request": request,
        },
    )


async def reject_invitation_typed(
    request: Request, access: Union[OrganizationAccess, GroupAccess]
) -> HTMLResponse:
    if isinstance(access, OrganizationAccess):
        entity_name = access.organization_id
        return TEMPLATING_ENGINE.TemplateResponse(
            name="reject_invitation.html",
            context={
                "group_name": entity_name,
                "request": request,
            },
        )
    entity_name = access.group_name
    return TEMPLATING_ENGINE.TemplateResponse(
        name="reject_invitation.html",
        context={
            "group_name": entity_name,
            "request": request,
        },
    )


async def reject_invitation(
    request: Request, group_access: dict[str, Any]
) -> HTMLResponse:
    group_name = (
        get_key_or_fallback(group_access, fallback="") if group_access else ""
    )
    return TEMPLATING_ENGINE.TemplateResponse(
        name="reject_invitation.html",
        context={
            "group_name": group_name,
            "request": request,
        },
    )
