# Starlette templates renders

import json
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
    return TEMPLATING_ENGINE.TemplateResponse(  # type: ignore
        name="HTTP401.html", context={"request": request}
    )


def error500(request: Request) -> HTMLResponse:
    return TEMPLATING_ENGINE.TemplateResponse(  # type: ignore
        name="HTTP500.html", context={"request": request}
    )


def graphic_error(request: Request) -> HTMLResponse:
    return TEMPLATING_ENGINE.TemplateResponse(  # type: ignore
        name="graphic-error.html",
        context=dict(
            request=request,
            debug=DEBUG,
            traceback=traceback.format_exc(),
        ),
    )


def graphics_for_entity_view(request: Request, entity: str) -> HTMLResponse:
    entity_title = entity.title()
    return TEMPLATING_ENGINE.TemplateResponse(  # type: ignore
        name="graphics-for-entity.html",
        context=dict(
            request=request,
            debug=DEBUG,
            entity=entity_title,
            js_runtime=f"{STATIC_URL}/dashboard/runtime-bundle.min.js",
            js_vendors=f"{STATIC_URL}/dashboard/vendors-bundle.min.js",
            css_vendors=f"{STATIC_URL}/dashboard/vendors-style.min.css",
            entity_graphic_css=f"{STATIC_URL}/styles/generic_graphic.css",
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


def graphic_view(  # pylint: disable=too-many-arguments
    request: Request,
    document: object,
    height: int,
    width: int,
    generator_type: str,
    generator_name: str,
) -> HTMLResponse:
    return TEMPLATING_ENGINE.TemplateResponse(  # type: ignore
        name="graphic.html",
        context=dict(
            request=request,
            debug=DEBUG,
            args=dict(
                data=json.dumps(document),
                height=height,
                width=width,
            ),
            generator_src=(
                f"graphics/"
                f"generators/"
                f"{generator_type}/"
                f"{generator_name}.js"
            ),
            generator_js=(
                f"{STATIC_URL}/"
                "graphics/"
                "generators/"
                f"{generator_type}/"
                f"{generator_name}.js"
            ),
            graphic_css=f"{STATIC_URL}/styles/graphic.css",
        ),
    )


def invalid_invitation(
    request: Request, error: str, entity_name: str = ""
) -> HTMLResponse:
    return TEMPLATING_ENGINE.TemplateResponse(  # type: ignore
        name="invalid_invitation.html",
        context={
            "error": error,
            "entity_name": entity_name,
            "request": request,
        },
    )


def login(request: Request) -> HTMLResponse:
    return TEMPLATING_ENGINE.TemplateResponse(  # type: ignore
        name="login.html",
        context={
            "request": request,
            "debug": DEBUG,
            "js_runtime": f"{STATIC_URL}/dashboard/runtime-bundle.min.js",
            "js_vendors": f"{STATIC_URL}/dashboard/vendors-bundle.min.js",
            "css_vendors": f"{STATIC_URL}/dashboard/vendors-style.min.css",
            "js": f"{STATIC_URL}/dashboard/app-bundle.min.js",
        },
    )


def main_app(request: Request) -> HTMLResponse:
    return TEMPLATING_ENGINE.TemplateResponse(  # type: ignore
        name="app.html",
        context={
            "request": request,
            "debug": DEBUG,
            "js_runtime": f"{STATIC_URL}/dashboard/runtime-bundle.min.js",
            "js_vendors": f"{STATIC_URL}/dashboard/vendors-bundle.min.js",
            "css_vendors": f"{STATIC_URL}/dashboard/vendors-style.min.css",
            "js": f"{STATIC_URL}/dashboard/app-bundle.min.js",
        },
    )


def unauthorized(request: Request) -> HTMLResponse:
    return TEMPLATING_ENGINE.TemplateResponse(  # type: ignore
        name="unauthorized.html",
        context={
            "request": request,
            "debug": DEBUG,
        },
    )


def valid_invitation(request: Request, entity_name: str) -> HTMLResponse:
    return TEMPLATING_ENGINE.TemplateResponse(  # type: ignore
        name="valid_invitation.html",
        context={
            "entity_name": entity_name,
            "request": request,
        },
    )


def confirm_deletion(*, request: Request) -> HTMLResponse:
    return TEMPLATING_ENGINE.TemplateResponse(  # type: ignore
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
    return TEMPLATING_ENGINE.TemplateResponse(  # type: ignore
        name="invalid_delete_confirmation.html",
        context={
            "error": error,
            "request": request,
        },
    )


def reject_invitation(request: Request, entity_name: str) -> HTMLResponse:
    return TEMPLATING_ENGINE.TemplateResponse(  # type: ignore
        name="reject_invitation.html",
        context={
            "entity_name": entity_name,
            "request": request,
        },
    )
